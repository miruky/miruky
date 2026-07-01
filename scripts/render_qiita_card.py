#!/usr/bin/env python3
"""Qiita 実績を「透け感のある水色（グラス調）」の自作 SVG カードに描画する。
データは自作パイプライン qiita-contibution-count/data/history.json を参照（Qiita API のレート制限を避ける）。
GitHub Actions から毎日実行して assets/qiita-card.svg を更新する想定。stdlib のみ。"""
import json, os, urllib.request

HIST = "https://raw.githubusercontent.com/miruky/qiita-contibution-count/main/data/history.json"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "qiita-card.svg")

# ---- palette : translucent water-blue / glass ----
BG="#0A0E14"; TEXT="#EAF6FC"; MUTED="#84A7BA"
CY="#5CD1F0"; CY_LT="#A8ECFF"; CY_DP="#3AA0E0"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO="'JetBrains Mono','SF Mono',Menlo,Consolas,monospace"

def load():
    try:
        with urllib.request.urlopen(HIST, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print("fetch failed, using fallback:", e)
        return {"daily":[{"contribution":6809,"likes":4463,"stocks":4489,"views":1796337,"articles":80,"followers":1252}]}

def fmt(n):
    n=int(round(float(n)))
    if n>=1_000_000:
        return (f"{n/1_000_000:.2f}").rstrip('0').rstrip('.')+"M"
    if n>=100_000:
        return (f"{n/1000:.1f}").rstrip('0').rstrip('.')+"K"
    return f"{n:,}"

def build(data):
    daily=data["daily"]; last=daily[-1]
    cells=[("Articles",last["articles"]),("Followers",last["followers"]),("Contribution",last["contribution"]),
           ("Likes",last["likes"]),("Stocks",last["stocks"]),("Views",last["views"])]

    # sparkline (contribution trend)
    pts=[float(d["contribution"]) for d in daily] or [0,1]
    lo,hi=min(pts),max(pts); rng=(hi-lo) or 1
    x0,x1,ytop,ybot=44,796,312,360
    def X(i): return x0+(x1-x0)*(i/max(1,len(pts)-1))
    def Y(v): return ybot-(v-lo)/rng*(ybot-ytop)
    line=" ".join(("M" if i==0 else "L")+f"{X(i):.1f} {Y(v):.1f}" for i,v in enumerate(pts))
    area=f"M{x0} {ybot} "+" ".join(f"L{X(i):.1f} {Y(v):.1f}" for i,v in enumerate(pts))+f" L{x1} {ybot} Z"
    ex,ey=X(len(pts)-1),Y(pts[-1])

    # 3x2 grid cell centres
    cx=[173,420,667]; num_y=[152,232]; lab_y=[176,256]
    grid=""
    for idx,(label,val) in enumerate(cells):
        col=idx%3; row=idx//3
        grid+=(f'<text x="{cx[col]}" y="{num_y[row]}" text-anchor="middle" font-family="{SANS}" '
               f'font-size="42" font-weight="800" fill="url(#num)">{fmt(val)}</text>'
               f'<text x="{cx[col]}" y="{lab_y[row]}" text-anchor="middle" font-family="{MONO}" '
               f'font-size="12" letter-spacing="3" fill="{MUTED}">{label.upper()}</text>')

    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 380" width="840" height="380" role="img" aria-label="Qiita stats">
  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0E1826"/><stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <linearGradient id="num" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CY_LT}"/><stop offset="1" stop-color="{CY}"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CY}" stop-opacity="0.55"/><stop offset="0.5" stop-color="{CY}" stop-opacity="0.12"/><stop offset="1" stop-color="{CY_DP}" stop-opacity="0.45"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0" r="0.9">
      <stop offset="0" stop-color="{CY}" stop-opacity="0.16"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="spark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CY}" stop-opacity="0.35"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CY_LT}" stop-opacity="0"/><stop offset="0.5" stop-color="{CY_LT}" stop-opacity="0.14"/><stop offset="1" stop-color="{CY_LT}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="round"><rect x="2" y="2" width="836" height="376" rx="20"/></clipPath>
  </defs>

  <g clip-path="url(#round)">
    <rect x="2" y="2" width="836" height="376" fill="url(#panel)"/>
    <rect x="2" y="2" width="836" height="376" fill="url(#glow)"/>
    <rect x="2" y="2" width="836" height="140" fill="url(#glass)"/>
    <!-- glassy sweep -->
    <rect x="-360" y="2" width="360" height="376" fill="url(#sweep)">
      <animate attributeName="x" values="-360;840" dur="6s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1" keyTimes="0;1"/>
    </rect>
  </g>

  <!-- header -->
  <circle cx="34" cy="40" r="5" fill="{CY}">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="r" values="5;6.5;5" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="50" y="45" font-family="{MONO}" font-size="14" letter-spacing="5" fill="{CY_LT}">QIITA</text>
  <text x="806" y="45" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">@miruky &#183; updated daily</text>

  {grid}

  <!-- sparkline -->
  <text x="44" y="300" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MUTED}">CONTRIBUTION HISTORY</text>
  <path d="{area}" fill="url(#spark)"/>
  <path d="{line}" fill="none" stroke="url(#num)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
        stroke-dasharray="2600" stroke-dashoffset="0">
    <animate attributeName="stroke-dashoffset" values="2600;0" dur="1.8s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/>
  </path>
  <circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{CY_LT}">
    <animate attributeName="r" values="3.5;6;3.5" dur="2.2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0.4;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>

  <!-- glass border on top -->
  <rect x="2" y="2" width="836" height="376" rx="20" fill="none" stroke="url(#border)" stroke-width="1.5"/>
</svg>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT,"w",encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT, "| latest:", {k:fmt(v) for k,v in cells})

if __name__=="__main__":
    build(load())
