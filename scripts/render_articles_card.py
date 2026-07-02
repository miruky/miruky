#!/usr/bin/env python3
"""最新の Qiita 記事カード（緑グラス・Qiitaカードと同素材）。
Qiita API v2 /users/miruky/items から最新3件を取得して assets/articles-card.svg を描画。
GitHub Actions から毎日実行。取得失敗時は既存ファイルを保持したまま正常終了する。"""
import json, os, sys, urllib.request

API = "https://qiita.com/api/v2/users/miruky/items?page=1&per_page=3"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "articles-card.svg")

BASE_C="#0E1511"; BASE_E="#0A0F0B"
NUM="#C2F0C2"; HERO="#7FE04A"; ACC="#55C500"; MINT="#8FBF8A"; MINT2="#71D083"; SHADOW="#0C2400"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic','Noto Sans JP',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"

def esc(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;"))

def strip_emoji(s):
    out=[]
    for ch in s:
        o=ord(ch)
        if 0x1F000<=o<=0x1FAFF or 0x2600<=o<=0x27BF or 0x1F1E6<=o<=0x1F1FF or o in (0xFE0F,0x200D,0x2B50,0x2B55):
            continue
        out.append(ch)
    return "".join(out).strip()

def fetch():
    req = urllib.request.Request(API, headers={"User-Agent":"miruky-profile-card"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def build(items):
    rows=""
    for i,it in enumerate(items[:3]):
        y=96+i*50
        title=strip_emoji(it.get("title",""))
        if len(title)>37: title=title[:36]+"…"
        title=esc(title)
        likes=int(it.get("likes_count",0))
        d=it.get("created_at","")[:10]
        date=f"{d[5:7]}/{d[8:10]}" if len(d)==10 else ""
        rows+=(f'<g opacity="1">'
               f'<animate attributeName="opacity" values="0;1" dur="0.6s" begin="{0.2+i*0.18:.2f}s" fill="freeze"/>'
               f'<text x="44" y="{y}" font-family="{MONO}" font-size="13" fill="{HERO}">0{i+1}</text>'
               f'<text x="80" y="{y}" font-family="{JP}" font-size="15" fill="{NUM}">{title}</text>'
               f'<g transform="translate(724,{y-11})">'
               f'<path d="M6 11 C1 7 1 3 3.5 3 C5 3 6 4.5 6 4.5 C6 4.5 7 3 8.5 3 C11 3 11 7 6 11 Z" fill="{MINT2}"/>'
               f'</g>'
               f'<text x="740" y="{y}" font-family="{MONO}" font-size="12" fill="{MINT2}">{likes}</text>'
               f'<text x="816" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MINT}">{date}</text>'
               f'</g>')
        if i<2:
            rows+=f'<line x1="44" y1="{y+18}" x2="816" y2="{y+18}" stroke="{ACC}" stroke-opacity="0.09" stroke-width="1"/>'

    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 236" width="860" height="236" role="img" aria-label="最新の記事">
<defs>
  <radialGradient id="atray" cx="0.5" cy="0.25" r="0.95">
    <stop offset="0" stop-color="{BASE_C}"/><stop offset="1" stop-color="{BASE_E}"/>
  </radialGradient>
  <linearGradient id="aglass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.10"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.03"/>
  </linearGradient>
  <linearGradient id="arim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#D8FFC2" stop-opacity="0.45"/><stop offset="0.5" stop-color="{ACC}" stop-opacity="0.16"/><stop offset="1" stop-color="{SHADOW}" stop-opacity="0.10"/>
  </linearGradient>
  <radialGradient id="aorb" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.22"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="aglint" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.09"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <filter id="asoft2" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="agrain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.77  0 0 0 0 0.10  0 0 0 0.05 0"/>
  </filter>
  <clipPath id="around"><rect x="2" y="2" width="856" height="232" rx="20"/></clipPath>
</defs>

<g clip-path="url(#around)">
  <rect x="2" y="2" width="856" height="232" fill="url(#atray)"/>
  <circle cx="700" cy="40" r="130" fill="url(#aorb)" filter="url(#asoft2)"/>
  <rect x="2" y="2" width="856" height="232" fill="url(#aglass)"/>
  <rect x="-300" y="-40" width="240" height="320" fill="url(#aglint)" transform="skewX(-18)">
    <animate attributeName="x" values="-300;1100;1100" keyTimes="0;0.11;1" dur="10s" begin="6s" repeatCount="indefinite"/>
  </rect>
</g>

<circle cx="38" cy="42" r="5" fill="{ACC}">
  <animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/>
</circle>
<text x="54" y="48" font-family="{SANS}" font-size="20" font-weight="700" fill="{NUM}">Latest Articles</text>
<text x="208" y="48" font-family="{JP}" font-size="13" letter-spacing="2" fill="{MINT2}">最新の記事</text>
<text x="822" y="47" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MINT}">qiita.com/miruky</text>
<line x1="40" y1="64" x2="820" y2="64" stroke="{ACC}" stroke-opacity="0.16" stroke-width="1"/>

{rows}

<rect x="2" y="2" width="856" height="232" rx="20" fill="none" stroke="url(#arim)" stroke-width="1.4"/>
<rect x="2" y="2" width="856" height="232" rx="20" fill="#000" opacity="0.5" filter="url(#agrain)" clip-path="url(#around)"/>
</svg>'''
    with open(OUT,"w",encoding="utf-8") as f: f.write(svg)
    print("wrote", OUT, "|", [strip_emoji(it["title"])[:24] for it in items[:3]])

if __name__=="__main__":
    try:
        items=fetch()
    except Exception as e:
        print("fetch failed — keep existing card:", e)
        sys.exit(0)
    if not items:
        print("no items — keep existing card"); sys.exit(0)
    build(items)
