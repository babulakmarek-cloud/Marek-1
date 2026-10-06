"""Opraví DXF z LibreDWG (dwg2dxf), kde je text MTEXT rozdělený zalomením řádku uvnitř hodnoty.
Použití: python dxf_oprav_zalomeni.py VSTUP.dxf VYSTUP.dxf
"""
import sys
L=open(sys.argv[1],encoding="utf-8",errors="replace",newline="").read().split("\r\n")
out=[];i=0;n=0
while i < len(L)-1:
    code=L[i].strip()
    if not code.lstrip("-").isdigit():
        out[-1]+=L[i]; i+=1; n+=1; continue   # pokračování hodnoty rozdělené zalomením
    out.append(L[i]); out.append(L[i+1]); i+=2
open(sys.argv[2],"w",encoding="utf-8",newline="").write("\r\n".join(out)+"\r\n")
print("spojeno",n)
