import sys, json, re, pymupdf
# texty z vektorového PDF po řádcích; souřadnice v mm při NOMINÁLNÍM měřítku (jen pro párování, ne pro délky)
p = pymupdf.open(sys.argv[1])[0]; H = p.rect.height; K = 25.4/72*float(sys.argv[3])
out=[]
for b in p.get_text("dict")["blocks"]:
    for l in b.get("lines",[]):
        t=re.sub(r"\s+"," ","".join(s["text"] for s in l["spans"])).strip()
        if not t: continue
        x0,y0,x1,y1=l["bbox"]; col="%06X"%l["spans"][0]["color"]
        out.append({"t":t,"x":round(x0*K),"y":round((H-(y0+y1)/2)*K),"layer":"PDF_"+col})
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False); print(len(out),"lines")
