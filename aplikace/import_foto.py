"""Založí zakázku (a zákazníka) a naimportuje složku s fotkami.

Použití (u sebe na PC, ve složce aplikace; stejná proměnná DENIK_DATA jako při spuštění app.py):
  python import_foto.py --folder "C:\\cesta\\Foto strecha" --job "Maroldovka VZT" --customer "Maroldovka" \\
      --area "Střecha" --phase pred --currency CZK
Fotky se zkopírují do data/uploads, popisky zůstanou prázdné - doplníte je v aplikaci (Zakázka → Popisky fotek).
Opakované spuštění nenahraje stejný soubor dvakrát. Podporováno: jpg, png, webp, gif (HEIC z iPhonu nejdřív převeďte).
"""
import argparse
import hashlib
import os
import secrets
import shutil
from datetime import date, datetime

import app as A

ap = argparse.ArgumentParser()
ap.add_argument("--folder", required=True)
ap.add_argument("--job", required=True)
ap.add_argument("--customer", required=True)
ap.add_argument("--country", default="CZ", choices=["CZ", "DE"])
ap.add_argument("--currency", default="CZK", choices=["CZK", "EUR"])
ap.add_argument("--area", default="")
ap.add_argument("--phase", default="pred", choices=list(A.PHASES))
a = ap.parse_args()

if not os.path.isdir(a.folder):
    raise SystemExit(f"Složka neexistuje: {a.folder}")

with A.app.app_context():
    cust = A.q1("SELECT id FROM customers WHERE name=?", a.customer)
    cid = cust["id"] if cust else A.ex("INSERT INTO customers(name,country) VALUES(?,?)", a.customer, a.country)
    job = A.q1("SELECT id FROM jobs WHERE name=? AND customer_id=?", a.job, cid)
    if job:
        jid = job["id"]
    else:
        n = A.q1("SELECT COUNT(*) c FROM jobs WHERE number LIKE ?", f"{date.today().year}-%")["c"] + 1
        jid = A.ex("INSERT INTO jobs(customer_id,number,name,status,currency,start_date) VALUES(?,?,?,?,?,?)",
                   cid, f"{date.today().year}-{n:03d}", a.job, "realizace", a.currency, date.today().isoformat())
    added = skipped = 0
    for name in sorted(os.listdir(a.folder)):
        src = os.path.join(a.folder, name)
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if not os.path.isfile(src):
            continue
        with open(src, "rb") as f:
            head = f.read(12)
            f.seek(0)
            digest = hashlib.sha1(f.read()).hexdigest()
        if ext not in A.ALLOWED_EXT or not head.startswith(A.MAGIC):
            print(f"přeskočeno (nepodporovaný formát): {name}")
            skipped += 1
            continue
        if A.q1("SELECT 1 FROM photos WHERE job_id=? AND src_hash=?", jid, digest):
            continue
        fn = f"{secrets.token_hex(16)}.{ext}"
        shutil.copyfile(src, os.path.join(A.UPLOADS, fn))
        taken = datetime.fromtimestamp(os.path.getmtime(src)).date().isoformat()
        A.ex("INSERT INTO photos(job_id,filename,caption,phase,area,taken,src_hash) VALUES(?,?,?,?,?,?,?)",
             jid, fn, "", a.phase, a.area, taken, digest)
        added += 1
    print(f"Zakázka #{jid} '{a.job}': nahráno {added} fotek, přeskočeno {skipped}.")
