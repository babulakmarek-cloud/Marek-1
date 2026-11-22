"""Sestaví jeden samostatný soubor dist/Rozvadec.html (bez závislostí, běží offline).
Spuštění: python3 build.py"""
import re, pathlib
root = pathlib.Path(__file__).parent
html = (root / 'index.html').read_text(encoding='utf-8')
css = (root / 'app.css').read_text(encoding='utf-8')
html = html.replace('<link rel="stylesheet" href="app.css">', '<style>\n' + css + '\n</style>')
def inline(m):
    js = (root / m.group(1)).read_text(encoding='utf-8').replace('</script', '<\\/script')
    return '<script>\n' + js + '\n</script>'
html = re.sub(r'<script src="([^"]+)"></script>', inline, html)
out = root / 'dist' / 'Rozvadec.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding='utf-8')
print(out, len(html), 'B')
