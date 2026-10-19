import io, os, re, sys, tempfile
os.environ["DENIK_DATA"] = tempfile.mkdtemp()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import app as A

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 50


def tok(c, url="/login"):
    return re.search(r'name="csrf" value="(\w+)"', c.get(url).get_data(as_text=True)).group(1)


def post(c, url, data=None, page=None, **kw):
    d = dict(data or {})
    d["csrf"] = tok(c, page or url)
    return c.post(url, data=d, follow_redirects=True, **kw)


def test_flow():
    c = A.app.test_client()
    assert c.get("/").status_code == 302                      # redirect to setup
    r = post(c, "/setup", {"name": "Marek", "email": "a@b.cz", "password": "heslo12345"})
    assert "přihlaste" in r.get_data(as_text=True)
    post(c, "/login", {"email": "a@b.cz", "password": "heslo12345"})
    assert c.get("/").status_code == 200
    post(c, "/customers/new", {"name": "Müller GmbH", "country": "DE"}, page="/customers/new")
    post(c, "/items", {"name": "Trubka", "unit": "m", "buy_eur": "1", "sell_eur": "3", "buy_czk": "20", "sell_czk": "60"}, page="/items")
    post(c, "/jobs/new", {"customer_id": 1, "name": "Heizung", "currency": "EUR", "budget": "1000"}, page="/jobs/new")
    r = post(c, "/jobs/1/diary/new", {"date": "2026-10-19", "work_done": "Montáž", "item_id": ["1"], "item_qty": ["12,5"],
             "photos": (io.BytesIO(PNG), "x.png")}, page="/jobs/1/diary/new", content_type="multipart/form-data")
    assert "Montáž" in r.get_data(as_text=True)
    assert len(os.listdir(A.UPLOADS)) == 1
    bad = post(c, "/jobs/1/gallery", {"photos": (io.BytesIO(b"<?php"), "x.png")}, page="/jobs/1/gallery", content_type="multipart/form-data")
    assert "není podporovaný" in bad.get_data(as_text=True)
    fn = os.listdir(A.UPLOADS)[0]
    assert c.get(f"/uploads/{fn}").status_code == 200
    post(c, "/jobs/1/stages", {"act": "add", "name": "Rozvody", "weight": "1"}, page="/jobs/1/stages")
    post(c, "/jobs/1/stages", {"act": "set", "sid": 1, "percent": "50"}, page="/jobs/1/stages")
    assert "50 %" in c.get("/jobs/1").get_data(as_text=True)
    post(c, "/jobs/1/docs/new", {"kind": "quote"}, page="/jobs/1")
    post(c, "/docs/1", {"act": "add", "item_id": "1", "qty": "100"}, page="/docs/1")
    html = c.get("/docs/1").get_data(as_text=True)
    assert "357,00 €" in html, html      # 100*3=300 + 19 % MwSt
    post(c, "/docs/1/to_invoice", page="/docs/1")
    p = c.get("/docs/2/print").get_data(as_text=True)
    assert "Rechnung" in p and "357,00 €" in p
    # worker role cannot see prices / documents
    post(c, "/users", {"act": "add", "name": "M", "email": "m@b.cz", "password": "montér1234", "role": "worker"}, page="/users")
    w = A.app.test_client()
    post(w, "/login", {"email": "m@b.cz", "password": "montér1234"})
    assert w.get("/docs/1").status_code == 403 and w.get("/items").status_code == 403
    assert "Doklady" not in w.get("/jobs/1").get_data(as_text=True)
    # CSRF
    assert w.post("/jobs/1/stages", data={"act": "set"}).status_code == 400
    # open redirect
    z = A.app.test_client()
    t = tok(z)
    r = z.post("/login?next=//evil.com", data={"email": "a@b.cz", "password": "heslo12345", "csrf": t})
    assert r.headers["Location"] == "/"
