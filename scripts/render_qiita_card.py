#!/usr/bin/env python3
"""Qiita 実績カード（緑グラスのベント型・非チャート）。
史料: qiita-contibution-count/data/history.json。GitHub Actions から毎日再生成。
設計: 株価折れ線を廃し、閲覧数を主役の 270 度ゲージ + 4種の異なる非チャート微グラフ。
制約: committed SVG / camo安全（SMIL + feTurbulence + feGaussianBlur, no CSS/backdrop-filter）。
※ フォロワーは掲載しない。数値はカンマ区切りの full 桁（省略しない）。"""
import json, os, sys, math, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from botanical import botanical

HIST = "https://raw.githubusercontent.com/miruky/qiita-contibution-count/main/data/history.json"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "qiita-card.svg")

# ---- palette: green glass ----
BASE_C="#0E1511"; BASE_E="#0A0F0B"
NUM="#C2F0C2"; NUM2="#EAF6EA"; HERO="#7FE04A"; ACC="#55C500"; MINT="#8FBF8A"; MINT2="#71D083"
SHADOW="#0C2400"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic','Noto Sans JP',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"

def load():
    try:
        with urllib.request.urlopen(HIST, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print("fetch failed, fallback:", e)
        return {"daily":[{"contribution":6810,"articles":80,"likes":4464,"stocks":4532,"views":1797538}]}

def fmt(n): return f"{int(round(float(n))):,}"

def polar(cx,cy,r,deg):
    a=math.radians(deg); return (cx+r*math.cos(a), cy+r*math.sin(a))

def arc(cx,cy,r,a0,a1):
    x0,y0=polar(cx,cy,r,a0); x1,y1=polar(cx,cy,r,a1)
    large=1 if abs(a1-a0)>180 else 0
    sweep=1 if a1>a0 else 0
    return f"M{x0:.2f} {y0:.2f} A{r} {r} 0 {large} {sweep} {x1:.2f} {y1:.2f}"

TILE_BASE="#0A140C"  # ブロックのダーク基盤（背後のツタを抑えて数値を読みやすく）

def glass_tile(x,y,w,h,rx,grad):
    # ダーク基盤 → 半透明ガラス面 → 上辺リムライト + 影
    return (f'<g filter="url(#drop)">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{TILE_BASE}" fill-opacity="0.62"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{grad})"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="url(#rim)" stroke-width="1.2"/>'
            f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h*0.4:.0f}" rx="{rx-2}" fill="url(#sheen)"/>'
            f'</g>')

def build(data):
    daily=data["daily"]; last=daily[-1]
    contribution=int(round(float(last["contribution"])))
    articles=int(last["articles"]); likes=int(last["likes"]); stocks=int(last["stocks"]); views=int(last["views"])
    i30=max(0,len(daily)-31); delta=int(round(float(last["contribution"])-float(daily[i30]["contribution"]))); span=len(daily)-1-i30

    # ---------- HERO: VIEWS 270deg gauge (2M milestone) ----------
    GOAL=2_000_000
    pct=min(1.0, views/GOAL)
    cx,cy,rr=214,208,104
    track=arc(cx,cy,rr,135,405)                 # full 270deg (gap at bottom)
    dash=f"{pct*100:.1f} 100"
    # icons (1.5px line) small
    def icon(px,py,path):
        return f'<g transform="translate({px},{py})" fill="none" stroke="{MINT2}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{path}</g>'
    eye = '<path d="M0 6 C3 1 11 1 14 6 C11 11 3 11 0 6 Z"/><circle cx="7" cy="6" r="2.2" fill="'+MINT2+'" stroke="none"/>'
    sprout='<path d="M7 13 V6"/><path d="M7 7 C4 7 2 5 2 2 C5 2 7 4 7 7Z" fill="'+MINT2+'" fill-opacity="0.18"/><path d="M7 8 C10 8 12 6 12 3 C9 3 7 5 7 8Z" fill="'+MINT2+'" fill-opacity="0.18"/>'
    pencil='<path d="M2 12 L2 9 L9 2 L12 5 L5 12 Z"/><path d="M8 3 L11 6"/>'
    heart='<path d="M7 12 C1 8 1 3 4 3 C6 3 7 5 7 5 C7 5 8 3 10 3 C13 3 13 8 7 12 Z"/>'
    book ='<path d="M3 2 H11 V13 L7 10 L3 13 Z"/>'

    # articles: unconnected dots grid (articles tile 632,88 内の右上)
    dots=""
    for i in range(12):
        r_=i//6; c_=i%6
        op=0.25+0.06*i
        dots+=f'<circle cx="{732+c_*13}" cy="{110+r_*12}" r="2.1" fill="{HERO}" opacity="{min(0.95,op):.2f}"/>'
    # likes: waffle 10 cells (progress to 5K) — likes tile 416,238 内の右上
    lk_goal=5000; lk_fill=round(10*min(1.0,likes/lk_goal))
    waffle=""
    for i in range(10):
        r_=i//5; c_=i%5
        on = i<lk_fill
        fill = HERO if on else "none"
        op = "1" if on else "0.14"
        waffle+=(f'<rect x="{528+c_*13}" y="{256+r_*13}" width="10" height="10" rx="2.5" '
                 f'fill="{fill}" fill-opacity="{op}" stroke="{ACC}" stroke-opacity="0.25" stroke-width="0.8"/>')
    # stocks: thin progress bar (to 5K) — stocks tile 632,238 内の右上
    st_goal=5000; st_pct=min(1.0,stocks/st_goal)
    bar=(f'<rect x="700" y="264" width="116" height="8" rx="4" fill="{ACC}" fill-opacity="0.14"/>'
         f'<rect x="700" y="264" width="{116*st_pct:.0f}" height="8" rx="4" fill="url(#barg)">'
         f'<animate attributeName="width" values="0;{116*st_pct:.0f}" dur="1.1s" begin="0.5s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1"/></rect>')

    # 直近30日の増分チップ（矢印＋数値＋期間ラベルを一体化して誤読を防ぐ）
    dtxt=f"+{delta:,}"
    jp_txt=f"直近{span}日"
    dw=22+len(dtxt)*6.8+8
    jpw=sum(9.5 if ord(c)>0x2E7F else 5.5 for c in jp_txt)
    chip_w=int(dw+jpw+12)
    chip_x=600-chip_w
    delta_chip=(f'<g transform="translate({chip_x},104)">'
                f'<rect x="0" y="0" width="{chip_w}" height="20" rx="10" fill="{ACC}" fill-opacity="0.14"/>'
                f'<path d="M8 13 l4 -6 l4 6 Z" fill="{HERO}"/>'
                f'<text x="22" y="14" font-family="{MONO}" font-size="11" font-weight="700" fill="{HERO}">{dtxt}</text>'
                f'<text x="{dw:.0f}" y="14" font-family="{JP}" font-size="9.5" fill="{MINT2}">{jp_txt}</text>'
                f'</g>')

    bot_defs, bot_layer = botanical("qb", "qiita")
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 400" width="860" height="400" role="img" aria-label="Qiita 活動記録">
<defs>
  <radialGradient id="tray" cx="0.5" cy="0.28" r="0.9">
    <stop offset="0" stop-color="{BASE_C}"/><stop offset="1" stop-color="{BASE_E}"/>
  </radialGradient>
  <linearGradient id="heroGlass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.18"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.05"/>
  </linearGradient>
  <linearGradient id="tileGlass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.11"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.04"/>
  </linearGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#D8FFC2" stop-opacity="0.5"/><stop offset="0.5" stop-color="{ACC}" stop-opacity="0.18"/><stop offset="1" stop-color="#0C2400" stop-opacity="0.10"/>
  </linearGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="heroNum" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#B9F58C"/><stop offset="1" stop-color="{HERO}"/>
  </linearGradient>
  <linearGradient id="gaugeVal" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="#9AF05A"/>
  </linearGradient>
  <linearGradient id="barg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{HERO}"/>
  </linearGradient>
  <radialGradient id="orb" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.30"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="qglint" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <filter id="drop" x="-20%" y="-20%" width="140%" height="150%" color-interpolation-filters="sRGB">
    <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="{SHADOW}" flood-opacity="0.42"/>
  </filter>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB">
    <feGaussianBlur stdDeviation="6"><animate attributeName="stdDeviation" values="5;8;5" dur="6s" repeatCount="indefinite"/></feGaussianBlur>
  </filter>
  <filter id="soft" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB">
    <feGaussianBlur stdDeviation="14"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" seed="7" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.77  0 0 0 0 0.10  0 0 0 0.05 0"/>
  </filter>
  <clipPath id="round"><rect x="2" y="2" width="856" height="396" rx="22"/></clipPath>
  {bot_defs}
</defs>

<g clip-path="url(#round)">
  <rect x="2" y="2" width="856" height="396" fill="url(#tray)"/>
  <!-- light-leak orbs behind hero -->
  <circle cx="150" cy="170" r="140" fill="url(#orb)" filter="url(#soft)"/>
  <circle cx="300" cy="300" r="110" fill="url(#orb)" filter="url(#soft)" opacity="0.7"/>
  <!-- ボタニカル: ツタ・葉・巻きひげ・胞子（ガラス越しに透ける） -->
  {bot_layer}
  <!-- diagonal glint（素早く通過 → 静止） -->
  <rect x="-300" y="-40" width="240" height="480" fill="url(#qglint)" transform="skewX(-18)">
    <animate attributeName="x" values="-300;1160;1160" keyTimes="0;0.11;1" dur="10s" begin="3s" repeatCount="indefinite"/>
  </rect>
</g>

<!-- header -->
<circle cx="38" cy="46" r="5" fill="{ACC}">
  <animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/>
  <animate attributeName="r" values="5;6.4;5" dur="2.4s" repeatCount="indefinite"/>
</circle>
<text x="54" y="52" font-family="{SANS}" font-size="22" font-weight="700" fill="{NUM}">Qiita</text>
<text x="120" y="52" font-family="{JP}" font-size="14" letter-spacing="2" fill="{MINT2}">活動記録</text>
<text x="822" y="51" text-anchor="end" font-family="{JP}" font-size="13" fill="{MINT2}">@miruky ・ 毎日更新</text>
<line x1="40" y1="72" x2="820" y2="72" stroke="{ACC}" stroke-opacity="0.16" stroke-width="1"/>

<!-- ===== HERO: VIEWS gauge ===== -->
{glass_tile(28,88,372,284,18,'heroGlass')}
<g>
  <path d="{track}" fill="none" stroke="{ACC}" stroke-opacity="0.15" stroke-width="14" stroke-linecap="round"/>
  <path d="{track}" fill="none" stroke="url(#gaugeVal)" stroke-width="14" stroke-linecap="round" pathLength="100"
        stroke-dasharray="{dash}" filter="url(#glow)" opacity="0.55"/>
  <path d="{track}" fill="none" stroke="url(#gaugeVal)" stroke-width="14" stroke-linecap="round" pathLength="100"
        stroke-dasharray="{dash}" stroke-dashoffset="0">
    <animate attributeName="stroke-dashoffset" values="{pct*100:.1f};0" dur="1.3s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1"/>
  </path>
  {icon(cx-8, cy-70, eye)}
  <text x="{cx}" y="{cy-30}" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{MINT}">VIEWS</text>
  <text x="{cx}" y="{cy+12}" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="800" fill="url(#heroNum)">{views:,}</text>
  <text x="{cx}" y="{cy+40}" text-anchor="middle" font-family="{JP}" font-size="14" fill="{MINT}">閲覧数</text>
  <text x="{cx}" y="{cy+96}" text-anchor="middle" font-family="{JP}" font-size="11" fill="{MINT2}">目標 2.0M まで {pct*100:.0f}%</text>
</g>

<!-- ===== support tiles ===== -->
{glass_tile(416,88,200,134,16,'tileGlass')}
{icon(432,106, sprout)}
{delta_chip}
<text x="432" y="180" font-family="{SANS}" font-size="30" font-weight="800" fill="{NUM}">{contribution:,}</text>
<text x="432" y="204" font-family="{MONO}" font-size="10" letter-spacing="1.2" fill="{MINT}">CONTRIBUTION <tspan font-family="{JP}" letter-spacing="0">・ 累計</tspan></text>

{glass_tile(632,88,200,134,16,'tileGlass')}
{icon(648,106, pencil)}
{dots}
<text x="648" y="180" font-family="{SANS}" font-size="30" font-weight="800" fill="{NUM}">{articles}</text>
<text x="648" y="204" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{MINT}">ARTICLES <tspan font-family="{JP}" letter-spacing="0">・ 記事</tspan></text>

{glass_tile(416,238,200,134,16,'tileGlass')}
{icon(432,256, heart)}
{waffle}
<text x="432" y="330" font-family="{SANS}" font-size="30" font-weight="800" fill="{NUM}">{likes:,}</text>
<text x="432" y="354" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{MINT}">LIKES <tspan font-family="{JP}" letter-spacing="0">・ いいね</tspan></text>

{glass_tile(632,238,200,134,16,'tileGlass')}
{icon(648,256, book)}
{bar}
<text x="648" y="330" font-family="{SANS}" font-size="30" font-weight="800" fill="{NUM}">{stocks:,}</text>
<text x="648" y="354" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{MINT}">STOCKS <tspan font-family="{JP}" letter-spacing="0">・ ストック</tspan></text>

<!-- corner ticks + grain + rim -->
<path d="M20 40 L20 20 L40 20" fill="none" stroke="{ACC}" stroke-opacity="0.5" stroke-width="1.5"/>
<path d="M840 360 L840 380 L820 380" fill="none" stroke="{ACC}" stroke-opacity="0.5" stroke-width="1.5"/>
<rect x="2" y="2" width="856" height="396" rx="22" fill="none" stroke="url(#rim)" stroke-width="1.5"/>
<rect x="2" y="2" width="856" height="396" rx="22" fill="#000" opacity="0.5" filter="url(#grain)" clip-path="url(#round)"/>
</svg>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT,"w",encoding="utf-8") as f: f.write(svg)
    print("wrote", OUT, "views", f"{views:,}", "pct", f"{pct*100:.0f}%", "delta", delta,
          "| C",contribution,"A",articles,"L",likes,"S",stocks)

if __name__=="__main__":
    build(load())
