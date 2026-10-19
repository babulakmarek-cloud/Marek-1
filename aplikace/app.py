"""Stavební deník + zakázky + nabídky + faktury (CZK / EUR), více uživatelů."""
import os
import secrets
import sqlite3
from datetime import date, timedelta
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   send_from_directory, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DENIK_DATA", os.path.join(BASE, "data"))
UPLOADS = os.path.join(DATA, "uploads")
os.makedirs(UPLOADS, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024
secret_file = os.path.join(DATA, "secret.key")
if not os.path.exists(secret_file):
    with open(secret_file, "w") as f:
        f.write(secrets.token_hex(32))
    os.chmod(secret_file, 0o600)
app.secret_key = open(secret_file).read()
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

STATUSES = ["poptavka", "nabidka", "realizace", "predano", "fakturovano", "uzavreno"]
STATUS_CZ = {"poptavka": "Poptávka", "nabidka": "Nabídka", "realizace": "Realizace",
             "predano": "Předáno", "fakturovano": "Fakturováno", "uzavreno": "Uzavřeno"}
PHASES = {"pred": "Před", "behem": "Během", "po": "Po", "zavada": "Závada", "predani": "Předání"}
WEATHER = ["", "Slunečno", "Oblačno", "Déšť", "Sníh", "Vítr", "Mráz"]
VAT = {"cz": ("CZ – DPH 21 %", 21.0), "de": ("DE – MwSt 19 %", 19.0),
       "rc": ("Přenesená daň. povinnost / Reverse charge", 0.0)}
KIND_CZ = {"quote": "Nabídka", "invoice": "Faktura", "advance": "Zálohová faktura"}
ALLOWED_EXT = {"jpg", "jpeg", "png", "webp", "gif"}
MAGIC = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"GIF8", b"RIFF")


# ---------------------------------------------------------------- db
def db():
    if "db" not in g:
        g.db = sqlite3.connect(os.path.join(DATA, "denik.db"))
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db


@app.teardown_appcontext
def close_db(_):
    d = g.pop("db", None)
    if d:
        d.close()


def init_db():
    with sqlite3.connect(os.path.join(DATA, "denik.db")) as c:
        c.executescript(open(os.path.join(BASE, "schema.sql"), encoding="utf-8").read())


def q(sql, *a):
    return db().execute(sql, a).fetchall()


def q1(sql, *a):
    return db().execute(sql, a).fetchone()


def ex(sql, *a):
    cur = db().execute(sql, a)
    db().commit()
    return cur.lastrowid


def setting(key, default=""):
    r = q1("SELECT value FROM settings WHERE key=?", key)
    return r["value"] if r else default


# ---------------------------------------------------------------- auth / csrf
def login_required(admin=False):
    def deco(fn):
        @wraps(fn)
        def w(*a, **kw):
            if not q1("SELECT 1 FROM users LIMIT 1"):
                return redirect(url_for("setup"))
            uid = session.get("uid")
            u = q1("SELECT * FROM users WHERE id=? AND active=1", uid) if uid else None
            if not u:
                return redirect(url_for("login", next=request.path))
            if admin and u["role"] != "admin":
                abort(403)
            g.user = u
            return fn(*a, **kw)
        return w
    return deco


@app.before_request
def csrf():
    if request.method == "POST":
        t = session.get("csrf")
        if not t or not secrets.compare_digest(t, request.form.get("csrf", "")):
            abort(400, "Neplatný CSRF token")


@app.context_processor
def inject():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return dict(csrf=session["csrf"], STATUS_CZ=STATUS_CZ, PHASES=PHASES, KIND_CZ=KIND_CZ,
                VAT=VAT, user=getattr(g, "user", None), company=setting("company_name"),
                today=date.today().isoformat())


@app.template_filter("money")
def money(v, cur="CZK"):
    s = f"{v or 0:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} {'Kč' if cur == 'CZK' else '€'}"


@app.template_filter("num")
def num(v):
    return f"{v:g}".replace(".", ",") if v is not None else ""


@app.template_filter("dt")
def dt(s):
    try:
        return date.fromisoformat(s).strftime("%d.%m.%Y")
    except (TypeError, ValueError):
        return s or ""


def f_float(name, default=0.0):
    try:
        return float(request.form.get(name, "").replace(",", ".").replace(" ", "") or default)
    except ValueError:
        return default


@app.route("/setup", methods=["GET", "POST"])
def setup():
    if q1("SELECT 1 FROM users LIMIT 1"):
        return redirect(url_for("login"))
    if request.method == "POST":
        pw = request.form["password"]
        if len(pw) < 8:
            flash("Heslo musí mít alespoň 8 znaků.")
        else:
            ex("INSERT INTO users(name,email,pw_hash,role) VALUES(?,?,?, 'admin')",
               request.form["name"], request.form["email"].lower().strip(), generate_password_hash(pw))
            flash("Administrátor vytvořen, přihlaste se.")
            return redirect(url_for("login"))
    return render_template("auth.html", mode="setup")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = q1("SELECT * FROM users WHERE email=? AND active=1", request.form["email"].lower().strip())
        if u and check_password_hash(u["pw_hash"], request.form["password"]):
            csrf_keep = secrets.token_hex(16)
            session.clear()
            session["uid"], session["csrf"] = u["id"], csrf_keep
            nxt = request.args.get("next", "")
            return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else url_for("index"))
        flash("Špatný e-mail nebo heslo.")
    return render_template("auth.html", mode="login")


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------- helpers
def job_or_404(jid):
    j = q1("SELECT j.*, c.name AS cust FROM jobs j JOIN customers c ON c.id=j.customer_id WHERE j.id=?", jid)
    if not j:
        abort(404)
    return j


def progress(jid):
    r = q1("SELECT SUM(weight*percent) s, SUM(weight) w FROM stages WHERE job_id=?", jid)
    return (r["s"] / r["w"]) if r["w"] else 0.0


def material_rows(jid, cur):
    rows = q("""SELECT i.id, i.name, i.unit, i.buy_czk, i.buy_eur,
                COALESCE(jm.plan_qty,0) plan,
                COALESCE((SELECT SUM(qty) FROM material_use u WHERE u.job_id=? AND u.item_id=i.id),0) used
                FROM items i LEFT JOIN job_material jm ON jm.item_id=i.id AND jm.job_id=?
                WHERE jm.item_id IS NOT NULL OR EXISTS(SELECT 1 FROM material_use u WHERE u.job_id=? AND u.item_id=i.id)
                ORDER BY i.name""", jid, jid, jid)
    out = []
    for r in rows:
        price = r["buy_czk"] if cur == "CZK" else r["buy_eur"]
        out.append(dict(r, cost=r["used"] * price, pct=(r["used"] / r["plan"]) if r["plan"] else None,
                        left=r["plan"] - r["used"]))
    return out


def doc_totals(doc_id):
    lines = q("SELECT * FROM doc_items WHERE doc_id=? ORDER BY id", doc_id)
    base = sum(l["qty"] * l["price"] for l in lines)
    by = {}
    for l in lines:
        by[l["vat_rate"]] = by.get(l["vat_rate"], 0) + l["qty"] * l["price"]
    vat = {r: round(b * r / 100, 2) for r, b in by.items()}
    return lines, round(base, 2), vat, round(base + sum(vat.values()), 2)


def next_number(kind):
    prefix = {"quote": "N", "invoice": "F", "advance": "Z"}[kind]
    y = date.today().year
    n = q1("SELECT COUNT(*) c FROM docs WHERE number LIKE ?", f"{prefix}{y}%")["c"] + 1
    while q1("SELECT 1 FROM docs WHERE number=?", f"{prefix}{y}{n:04d}"):
        n += 1
    return f"{prefix}{y}{n:04d}"


def save_photos(jid, entry_id, phase, area):
    n = 0
    for f in request.files.getlist("photos"):
        if not f or not f.filename:
            continue
        ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
        head = f.stream.read(12)
        f.stream.seek(0)
        if ext not in ALLOWED_EXT or not head.startswith(MAGIC):
            flash(f"Soubor {f.filename} není podporovaný obrázek (jpg, png, webp, gif).")
            continue
        fn = f"{secrets.token_hex(16)}.{ext}"
        f.save(os.path.join(UPLOADS, fn))
        ex("INSERT INTO photos(job_id,entry_id,filename,caption,phase,area,taken) VALUES(?,?,?,?,?,?,?)",
           jid, entry_id, fn, request.form.get("caption", ""), phase, area, date.today().isoformat())
        n += 1
    return n


@app.route("/uploads/<fn>")
@login_required()
def upload(fn):
    if not q1("SELECT 1 FROM photos WHERE filename=?", fn):
        abort(404)
    return send_from_directory(UPLOADS, fn)


# ---------------------------------------------------------------- dashboard / customers
@app.route("/")
@login_required()
def index():
    jobs = q("""SELECT j.*, c.name cust FROM jobs j JOIN customers c ON c.id=j.customer_id
                ORDER BY CASE j.status WHEN 'realizace' THEN 0 ELSE 1 END, j.id DESC""")
    return render_template("index.html", jobs=[dict(j, prog=progress(j["id"])) for j in jobs])


@app.route("/customers")
@login_required()
def customers():
    return render_template("customers.html", rows=q("SELECT * FROM customers ORDER BY name"))


@app.route("/customers/<cid>", methods=["GET", "POST"])
@login_required()
def customer(cid):
    c = None if cid == "new" else q1("SELECT * FROM customers WHERE id=?", cid)
    if cid != "new" and not c:
        abort(404)
    if request.method == "POST":
        v = [request.form.get(k, "").strip() for k in ("name", "country", "ico", "dic", "email", "phone", "address", "note")]
        if not v[0]:
            flash("Jméno je povinné.")
        elif v[1] not in ("CZ", "DE"):
            abort(400)
        else:
            if c:
                ex("UPDATE customers SET name=?,country=?,ico=?,dic=?,email=?,phone=?,address=?,note=? WHERE id=?", *v, cid)
            else:
                cid = ex("INSERT INTO customers(name,country,ico,dic,email,phone,address,note) VALUES(?,?,?,?,?,?,?,?)", *v)
            return redirect(url_for("customer", cid=cid))
    jobs = q("SELECT * FROM jobs WHERE customer_id=? ORDER BY id DESC", cid) if c else []
    return render_template("customer.html", c=c, jobs=jobs)


# ---------------------------------------------------------------- jobs
@app.route("/jobs/new", methods=["GET", "POST"])
@login_required(admin=True)
def job_new():
    if request.method == "POST":
        cust = request.form.get("customer_id")
        if not q1("SELECT 1 FROM customers WHERE id=?", cust):
            abort(400)
        cur = request.form.get("currency", "CZK")
        if cur not in ("CZK", "EUR"):
            abort(400)
        n = q1("SELECT COUNT(*) c FROM jobs WHERE number LIKE ?", f"{date.today().year}-%")["c"] + 1
        jid = ex("""INSERT INTO jobs(customer_id,number,name,site_address,status,currency,start_date,end_plan,budget)
                    VALUES(?,?,?,?,?,?,?,?,?)""", cust, f"{date.today().year}-{n:03d}",
                 request.form["name"], request.form.get("site_address", ""), "realizace", cur,
                 request.form.get("start_date") or None, request.form.get("end_plan") or None, f_float("budget"))
        return redirect(url_for("job", jid=jid))
    cust = request.args.get("customer_id")
    return render_template("job_new.html", customers=q("SELECT * FROM customers ORDER BY name"), sel=cust)


@app.route("/jobs/<int:jid>")
@login_required()
def job(jid):
    j = job_or_404(jid)
    entries = q("""SELECT d.*, u.name author, (SELECT COUNT(*) FROM photos p WHERE p.entry_id=d.id) nphotos
                   FROM diary d LEFT JOIN users u ON u.id=d.user_id WHERE job_id=? ORDER BY date DESC, id DESC""", jid)
    stats = q1("SELECT COALESCE(SUM(hours),0) h, COUNT(*) n FROM diary WHERE job_id=?", jid)
    mat = material_rows(jid, j["currency"])
    docs = q("SELECT * FROM docs WHERE job_id=? ORDER BY id DESC", jid) if g.user["role"] == "admin" else []
    docs = [dict(d, total=doc_totals(d["id"])[3]) for d in docs]
    return render_template("job.html", j=j, entries=entries, stats=stats, prog=progress(jid),
                           mat=mat, mat_cost=sum(m["cost"] for m in mat), docs=docs,
                           stages=q("SELECT * FROM stages WHERE job_id=? ORDER BY id", jid))


@app.route("/jobs/<int:jid>/edit", methods=["POST"])
@login_required(admin=True)
def job_edit(jid):
    job_or_404(jid)
    st = request.form.get("status")
    if st not in STATUSES:
        abort(400)
    ex("UPDATE jobs SET name=?,site_address=?,status=?,start_date=?,end_plan=?,budget=?,note=? WHERE id=?",
       request.form["name"], request.form.get("site_address", ""), st, request.form.get("start_date") or None,
       request.form.get("end_plan") or None, f_float("budget"), request.form.get("note", ""), jid)
    return redirect(url_for("job", jid=jid))


@app.route("/jobs/<int:jid>/diary/new", methods=["GET", "POST"])
@login_required()
def diary_new(jid):
    j = job_or_404(jid)
    items = q("SELECT * FROM items ORDER BY name")
    if request.method == "POST":
        w = request.form.get("weather", "")
        if w not in WEATHER:
            abort(400)
        d = request.form.get("date") or date.today().isoformat()
        eid = ex("INSERT INTO diary(job_id,date,weather,workers,hours,work_done,issues,user_id) VALUES(?,?,?,?,?,?,?,?)",
                 jid, d, w, int(f_float("workers")), f_float("hours"), request.form.get("work_done", ""),
                 request.form.get("issues", ""), g.user["id"])
        phase = request.form.get("phase", "behem")
        save_photos(jid, eid, phase if phase in PHASES else "behem", request.form.get("area", ""))
        for iid, qty in zip(request.form.getlist("item_id"), request.form.getlist("item_qty")):
            try:
                qty = float(qty.replace(",", "."))
            except ValueError:
                continue
            if iid and qty and q1("SELECT 1 FROM items WHERE id=?", iid):
                ex("INSERT INTO material_use(job_id,item_id,entry_id,date,qty) VALUES(?,?,?,?,?)", jid, iid, eid, d, qty)
        return redirect(url_for("job", jid=jid))
    return render_template("diary_new.html", j=j, items=items, WEATHER=WEATHER)


@app.route("/jobs/<int:jid>/entry/<int:eid>")
@login_required()
def entry(jid, eid):
    j = job_or_404(jid)
    e = q1("SELECT d.*, u.name author FROM diary d LEFT JOIN users u ON u.id=d.user_id WHERE d.id=? AND d.job_id=?", eid, jid)
    if not e:
        abort(404)
    use = q("SELECT u.qty, i.name, i.unit FROM material_use u JOIN items i ON i.id=u.item_id WHERE u.entry_id=?", eid)
    return render_template("entry.html", j=j, e=e, use=use, photos=q("SELECT * FROM photos WHERE entry_id=?", eid))


@app.route("/jobs/<int:jid>/gallery", methods=["GET", "POST"])
@login_required()
def gallery(jid):
    j = job_or_404(jid)
    if request.method == "POST":
        phase = request.form.get("phase", "behem")
        if not save_photos(jid, None, phase if phase in PHASES else "behem", request.form.get("area", "")):
            flash("Nebyla nahrána žádná fotka.")
        return redirect(url_for("gallery", jid=jid))
    ph = request.args.get("phase")
    if ph in PHASES:
        rows = q("SELECT * FROM photos WHERE job_id=? AND phase=? ORDER BY taken DESC, id DESC", jid, ph)
    else:
        rows = q("SELECT * FROM photos WHERE job_id=? ORDER BY taken DESC, id DESC", jid)
    return render_template("gallery.html", j=j, photos=rows, ph=ph)


@app.post("/photos/<int:pid>/delete")
@login_required(admin=True)
def photo_delete(pid):
    p = q1("SELECT * FROM photos WHERE id=?", pid)
    if not p:
        abort(404)
    ex("DELETE FROM photos WHERE id=?", pid)
    try:
        os.remove(os.path.join(UPLOADS, p["filename"]))
    except OSError:
        pass
    return redirect(url_for("gallery", jid=p["job_id"]))


@app.post("/jobs/<int:jid>/material")
@login_required()
def material_use(jid):
    job_or_404(jid)
    qty = f_float("qty")
    if request.form.get("item_id") and qty and q1("SELECT 1 FROM items WHERE id=?", request.form["item_id"]):
        ex("INSERT INTO material_use(job_id,item_id,date,qty) VALUES(?,?,?,?)", jid, request.form["item_id"],
           request.form.get("date") or date.today().isoformat(), qty)
    return redirect(url_for("material", jid=jid))


@app.route("/jobs/<int:jid>/material", methods=["GET", "POST"])
@login_required()
def material(jid):
    j = job_or_404(jid)
    if request.method == "POST":
        return material_use(jid)
    mat = material_rows(jid, j["currency"])
    return render_template("material.html", j=j, mat=mat, items=q("SELECT * FROM items ORDER BY name"),
                           log=q("SELECT u.*, i.name, i.unit FROM material_use u JOIN items i ON i.id=u.item_id WHERE job_id=? ORDER BY date DESC, u.id DESC", jid))


@app.post("/jobs/<int:jid>/material/plan")
@login_required(admin=True)
def material_plan(jid):
    job_or_404(jid)
    if q1("SELECT 1 FROM items WHERE id=?", request.form.get("item_id")):
        ex("INSERT INTO job_material(job_id,item_id,plan_qty) VALUES(?,?,?) ON CONFLICT(job_id,item_id) DO UPDATE SET plan_qty=excluded.plan_qty",
           jid, request.form["item_id"], f_float("plan_qty"))
    return redirect(url_for("material", jid=jid))


@app.route("/jobs/<int:jid>/stages", methods=["GET", "POST"])
@login_required()
def stages(jid):
    j = job_or_404(jid)
    if request.method == "POST":
        act = request.form.get("act")
        if act == "add" and g.user["role"] == "admin":
            ex("INSERT INTO stages(job_id,name,weight,plan_from,plan_to) VALUES(?,?,?,?,?)", jid, request.form["name"],
               f_float("weight", 1), request.form.get("plan_from") or None, request.form.get("plan_to") or None)
        elif act == "set":
            p = min(max(f_float("percent"), 0), 100) / 100
            ex("UPDATE stages SET percent=? WHERE id=? AND job_id=?", p, request.form.get("sid"), jid)
        elif act == "del" and g.user["role"] == "admin":
            ex("DELETE FROM stages WHERE id=? AND job_id=?", request.form.get("sid"), jid)
        return redirect(url_for("stages", jid=jid))
    return render_template("stages.html", j=j, rows=q("SELECT * FROM stages WHERE job_id=? ORDER BY id", jid), prog=progress(jid))


@app.route("/jobs/<int:jid>/report")
@login_required()
def report(jid):
    j = job_or_404(jid)
    entries = q("SELECT d.*, u.name author FROM diary d LEFT JOIN users u ON u.id=d.user_id WHERE job_id=? ORDER BY date, d.id", jid)
    data = [dict(e, photos=q("SELECT * FROM photos WHERE entry_id=?", e["id"]),
                 use=q("SELECT u.qty,i.name,i.unit FROM material_use u JOIN items i ON i.id=u.item_id WHERE u.entry_id=?", e["id"]))
            for e in entries]
    return render_template("report.html", j=j, data=data, prog=progress(jid), mat=material_rows(jid, j["currency"]),
                           stages=q("SELECT * FROM stages WHERE job_id=?", jid))


# ---------------------------------------------------------------- items
@app.route("/items", methods=["GET", "POST"])
@login_required(admin=True)
def items():
    if request.method == "POST":
        if request.form.get("act") == "del":
            try:
                ex("DELETE FROM items WHERE id=?", request.form.get("id"))
            except sqlite3.IntegrityError:
                flash("Položka je použitá a nelze ji smazat.")
        elif request.form.get("name", "").strip():
            args = (request.form["name"].strip(), request.form.get("unit", "ks"), f_float("buy_czk"), f_float("buy_eur"),
                    f_float("sell_czk"), f_float("sell_eur"))
            if request.form.get("id"):
                ex("UPDATE items SET name=?,unit=?,buy_czk=?,buy_eur=?,sell_czk=?,sell_eur=? WHERE id=?", *args, request.form["id"])
            else:
                ex("INSERT INTO items(name,unit,buy_czk,buy_eur,sell_czk,sell_eur) VALUES(?,?,?,?,?,?)", *args)
        return redirect(url_for("items"))
    return render_template("items.html", rows=q("SELECT * FROM items ORDER BY name"))


# ---------------------------------------------------------------- documents
@app.route("/jobs/<int:jid>/docs/new", methods=["POST"])
@login_required(admin=True)
def doc_new(jid):
    j = job_or_404(jid)
    kind = request.form.get("kind")
    if kind not in KIND_CZ:
        abort(400)
    cust = q1("SELECT country FROM customers WHERE id=?", j["customer_id"])
    mode = "de" if cust["country"] == "DE" else "cz"
    did = ex("INSERT INTO docs(job_id,kind,number,issued,due,currency,vat_mode) VALUES(?,?,?,?,?,?,?)", jid, kind,
             next_number(kind), date.today().isoformat(),
             (date.today() + timedelta(days=14 if kind != "quote" else 30)).isoformat(), j["currency"], mode)
    return redirect(url_for("doc", did=did))


@app.route("/docs/<int:did>", methods=["GET", "POST"])
@login_required(admin=True)
def doc(did):
    d = q1("SELECT * FROM docs WHERE id=?", did)
    if not d:
        abort(404)
    if request.method == "POST":
        act = request.form.get("act")
        locked = d["status"] in ("odeslano", "zaplaceno") and d["kind"] != "quote"
        if act == "head":
            mode = request.form.get("vat_mode")
            if mode not in VAT:
                abort(400)
            ex("UPDATE docs SET issued=?,due=?,vat_mode=?,status=?,note=? WHERE id=?", request.form["issued"],
               request.form.get("due") or None, mode,
               request.form.get("status") if request.form.get("status") in ("koncept", "odeslano", "zaplaceno", "prijata", "zamitnuta") else d["status"],
               request.form.get("note", ""), did)
        elif act == "add" and not locked:
            rate = VAT[d["vat_mode"]][1]
            item = q1("SELECT * FROM items WHERE id=?", request.form.get("item_id")) if request.form.get("item_id") else None
            if item:
                price = item["sell_czk"] if d["currency"] == "CZK" else item["sell_eur"]
                ex("INSERT INTO doc_items(doc_id,text,unit,qty,price,vat_rate) VALUES(?,?,?,?,?,?)",
                   did, item["name"], item["unit"], f_float("qty", 1), price, rate)
            elif request.form.get("text", "").strip():
                ex("INSERT INTO doc_items(doc_id,text,unit,qty,price,vat_rate) VALUES(?,?,?,?,?,?)", did,
                   request.form["text"].strip(), request.form.get("unit", "ks"), f_float("qty", 1), f_float("price"), rate)
        elif act == "del" and not locked:
            ex("DELETE FROM doc_items WHERE id=? AND doc_id=?", request.form.get("lid"), did)
        elif act == "delete" and d["status"] == "koncept":
            ex("DELETE FROM docs WHERE id=?", did)
            return redirect(url_for("job", jid=d["job_id"]))
        return redirect(url_for("doc", did=did))
    lines, base, vat, total = doc_totals(did)
    return render_template("doc.html", d=d, j=job_or_404(d["job_id"]), lines=lines, base=base, vat=vat, total=total,
                           items=q("SELECT * FROM items ORDER BY name"))


@app.post("/docs/<int:did>/to_invoice")
@login_required(admin=True)
def to_invoice(did):
    d = q1("SELECT * FROM docs WHERE id=? AND kind='quote'", did)
    if not d:
        abort(404)
    nid = ex("INSERT INTO docs(job_id,kind,number,issued,due,currency,vat_mode,note) VALUES(?,?,?,?,?,?,?,?)", d["job_id"], "invoice",
             next_number("invoice"), date.today().isoformat(), (date.today() + timedelta(days=14)).isoformat(),
             d["currency"], d["vat_mode"], d["note"])
    db().execute("INSERT INTO doc_items(doc_id,text,unit,qty,price,vat_rate) SELECT ?,text,unit,qty,price,vat_rate FROM doc_items WHERE doc_id=?", (nid, did))
    db().execute("UPDATE docs SET status='prijata' WHERE id=?", (did,))
    db().commit()
    return redirect(url_for("doc", did=nid))


@app.route("/docs/<int:did>/print")
@login_required(admin=True)
def doc_print(did):
    d = q1("SELECT * FROM docs WHERE id=?", did)
    if not d:
        abort(404)
    j = job_or_404(d["job_id"])
    cust = q1("SELECT * FROM customers WHERE id=?", j["customer_id"])
    lines, base, vat, total = doc_totals(did)
    s = {k: setting(k) for k in ("company_name", "company_address", "company_ico", "company_dic", "company_email",
                                 "company_phone", "iban_czk", "iban_eur", "bic", "footer")}
    return render_template("doc_print.html", d=d, j=j, c=cust, lines=lines, base=base, vat=vat, total=total, s=s)


# ---------------------------------------------------------------- admin
@app.route("/users", methods=["GET", "POST"])
@login_required(admin=True)
def users():
    if request.method == "POST":
        act = request.form.get("act")
        if act == "add":
            pw = request.form.get("password", "")
            role = request.form.get("role")
            if len(pw) < 8 or role not in ("admin", "worker"):
                flash("Heslo musí mít alespoň 8 znaků a role musí být platná.")
            else:
                try:
                    ex("INSERT INTO users(name,email,pw_hash,role) VALUES(?,?,?,?)", request.form["name"],
                       request.form["email"].lower().strip(), generate_password_hash(pw), role)
                except sqlite3.IntegrityError:
                    flash("Tento e-mail už existuje.")
        elif act == "toggle" and int(request.form.get("id", 0)) != g.user["id"]:
            ex("UPDATE users SET active=1-active WHERE id=?", request.form.get("id"))
        elif act == "pw" and len(request.form.get("password", "")) >= 8:
            ex("UPDATE users SET pw_hash=? WHERE id=?", generate_password_hash(request.form["password"]), request.form.get("id"))
        return redirect(url_for("users"))
    return render_template("users.html", rows=q("SELECT * FROM users ORDER BY id"))


@app.route("/settings", methods=["GET", "POST"])
@login_required(admin=True)
def settings():
    keys = ("company_name", "company_address", "company_ico", "company_dic", "company_email", "company_phone",
            "iban_czk", "iban_eur", "bic", "footer")
    if request.method == "POST":
        for k in keys:
            ex("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", k, request.form.get(k, "").strip())
        flash("Uloženo.")
        return redirect(url_for("settings"))
    return render_template("settings.html", s={k: setting(k) for k in keys})


init_db()

if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", 5000)))
