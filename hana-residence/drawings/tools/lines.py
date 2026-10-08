import sys, pymupdf, collections
doc = pymupdf.open(sys.argv[1]); page=doc[int(sys.argv[2])-1]
segs=[]
for p in page.get_drawings():
    for it in p['items']:
        if it[0]=='l':
            a,b=it[1],it[2]; segs.append((a.x,a.y,b.x,b.y,p.get('color'),p.get('width'),p.get('dashes')))
# long axis-parallel lines
H=collections.defaultdict(float); V=collections.defaultdict(float)
for x0,y0,x1,y1,c,w,d in segs:
    if abs(y0-y1)<0.05: H[round(y0,1)]+=abs(x1-x0)
    if abs(x0-x1)<0.05: V[round(x0,1)]+=abs(y1-y0)
print("constant-y lines (len>300):", sorted([(k,round(v)) for k,v in H.items() if v>300]))
print("constant-x lines (len>300):", sorted([(k,round(v)) for k,v in V.items() if v>300]))
print("dash styles", collections.Counter(s[6] for s in segs).most_common(5))
