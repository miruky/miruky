#!/usr/bin/env python3
"""Qiita 実績を「透け感のある水色（グラス調）」の自作 SVG カードに描画する。
データは自作パイプライン qiita-contibution-count/data/history.json を参照。
GitHub Actions から毎日実行して assets/qiita-card.svg を更新する。stdlib のみ。
※ フォロワー数は API 側の値が不正確なため掲載しない。
※ 数値は省略(M/K)せず full 桁で表示（大きく見せるため）。"""
import json, os, urllib.request

HIST = "https://raw.githubusercontent.com/miruky/qiita-contibution-count/main/data/history.json"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "qiita-card.svg")

# ---- palette : translucent water-blue / glass ----
BG="#0A0E14"; TEXT="#EAF6FC"; MUTED="#84A7BA"
CY="#5CD1F0"; CY_LT="#A8ECFF"; CY_DP="#3AA0E0"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"

def load():
    try:
        with urllib.request.urlopen(HIST, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print("fetch failed, using fallback:", e)
        return {"daily":[{"contribution":6810,"likes":4464,"stocks":4531,"views":1796337,"articles":80}]}

def fmt(n):
    return f"{int(round(float(n))):,}"

def build(data):
    daily=data["daily"]; last=daily[-1]
    contribution=int(round(float(last["contribution"])))
    i30=max(0, len(daily)-31)
    delta=int(round(float(last["contribution"])-float(daily[i30]["contribution"])))
    span=len(daily)-1-i30

    supporting=[("記事数", last["articles"]), ("いいね", last["likes"]),
                ("ストック", last["stocks"]), ("閲覧数", last["views"])]

    # sparkline (contribution trend) — 左カラム
    pts=[float(d["contribution"]) for d in daily] or [0,1]
    lo,hi=min(pts),max(pts); rng=(hi-lo) or 1
    x0,x1,ytop,ybot=48,384,256,360
    def X(i): return x0+(x1-x0)*(i/max(1,len(pts)-1))
    def Y(v): return ybot-(v-lo)/rng*(ybot-ytop)
    line=" ".join(("M" if i==0 else "L")+f"{X(i):.1f} {Y(v):.1f}" for i,v in enumerate(pts))
    area=f"M{x0} {ybot} "+" ".join(f"L{X(i):.1f} {Y(v):.1f}" for i,v in enumerate(pts))+f" L{x1} {ybot} Z"
    ex,ey=X(len(pts)-1),Y(pts[-1])

    # 右カラム：ダッシュボード型リスト（ラベル左 / 数値右揃え）
    rows_y=[152, 216, 280, 344]
    lst=""
    for i,(label,val) in enumerate(supporting):
        y=rows_y[i]
        lst+=(f'<text x="452" y="{y}" font-family="{JP}" font-size="16" fill="{TEXT}">{label}</text>'
              f'<text x="812" y="{y}" text-anchor="end" font-family="{SANS}" font-size="31" font-weight="800" fill="url(#num)">{fmt(val)}</text>')
        if i<3:
            lst+=f'<line x1="450" y1="{y+24}" x2="812" y2="{y+24}" stroke="{CY}" stroke-opacity="0.09" stroke-width="1"/>'

    delta_svg=""
    if delta>0:
        dtxt=f"+{delta:,}"
        delta_svg=(f'<g transform="translate(48,206)">'
                   f'<polygon points="0,10 5,1 10,10" fill="{CY}"/>'
                   f'<text x="16" y="10" font-family="{SANS}" font-size="15" font-weight="700" fill="{CY_LT}">{dtxt}</text>'
                   f'<text x="{16+len(dtxt)*9+10}" y="10" font-family="{JP}" font-size="12" fill="{MUTED}">直近{span}日</text>'
                   f'</g>')

    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 400" width="860" height="400" role="img" aria-label="Qiita 活動記録">
  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0E1826"/><stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <linearGradient id="num" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CY_LT}"/><stop offset="1" stop-color="{CY}"/>
    </linearGradient>
    <linearGradient id="feat" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="{CY_LT}"/><stop offset="1" stop-color="{CY}"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CY}" stop-opacity="0.55"/><stop offset="0.5" stop-color="{CY}" stop-opacity="0.10"/><stop offset="1" stop-color="{CY_DP}" stop-opacity="0.45"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.26" cy="0.08" r="0.85">
      <stop offset="0" stop-color="{CY}" stop-opacity="0.16"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="spark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CY}" stop-opacity="0.32"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CY_LT}" stop-opacity="0"/><stop offset="0.5" stop-color="{CY_LT}" stop-opacity="0.12"/><stop offset="1" stop-color="{CY_LT}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="round"><rect x="2" y="2" width="856" height="396" rx="22"/></clipPath>
  </defs>

  <g clip-path="url(#round)">
    <rect x="2" y="2" width="856" height="396" fill="url(#panel)"/>
    <rect x="2" y="2" width="856" height="396" fill="url(#glow)"/>
    <rect x="2" y="2" width="856" height="150" fill="url(#glass)"/>
    <rect x="-380" y="2" width="380" height="396" fill="url(#sweep)">
      <animate attributeName="x" values="-380;860" dur="6.5s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1" keyTimes="0;1"/>
    </rect>
  </g>

  <!-- header -->
  <circle cx="38" cy="46" r="5" fill="{CY}">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="r" values="5;6.5;5" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="54" y="52" font-family="{SANS}" font-size="22" font-weight="700" fill="{CY_LT}">Qiita</text>
  <text x="120" y="52" font-family="{JP}" font-size="14" letter-spacing="2" fill="{MUTED}">活動記録</text>
  <text x="822" y="51" text-anchor="end" font-family="{JP}" font-size="13" fill="{MUTED}">@miruky ・ 毎日更新</text>
  <line x1="40" y1="72" x2="820" y2="72" stroke="{CY}" stroke-opacity="0.14" stroke-width="1"/>

  <!-- featured: contribution -->
  <text x="48" y="112" font-family="{JP}" font-size="14" letter-spacing="3" fill="{MUTED}">コントリビューション</text>
  <text x="46" y="180" font-family="{SANS}" font-size="62" font-weight="800" fill="url(#feat)">{contribution:,}</text>
  {delta_svg}

  <!-- sparkline -->
  <text x="48" y="238" font-family="{JP}" font-size="11" letter-spacing="1" fill="{MUTED}">コントリビューション推移</text>
  <line x1="{x0}" y1="{ybot}" x2="{x1}" y2="{ybot}" stroke="{CY}" stroke-opacity="0.12" stroke-width="1"/>
  <path d="{area}" fill="url(#spark)"/>
  <path d="{line}" fill="none" stroke="url(#num)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
        stroke-dasharray="2400" stroke-dashoffset="0">
    <animate attributeName="stroke-dashoffset" values="2400;0" dur="1.8s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/>
  </path>
  <circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{CY_LT}">
    <animate attributeName="r" values="3.5;6;3.5" dur="2.2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0.4;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>

  <!-- vertical divider -->
  <line x1="424" y1="96" x2="424" y2="372" stroke="{CY}" stroke-opacity="0.15" stroke-width="1"/>

  <!-- supporting list -->
  {lst}

  <!-- corner ticks -->
  <path d="M20 40 L20 20 L40 20" fill="none" stroke="{CY}" stroke-opacity="0.5" stroke-width="1.5"/>
  <path d="M840 360 L840 380 L820 380" fill="none" stroke="{CY}" stroke-opacity="0.5" stroke-width="1.5"/>

  <rect x="2" y="2" width="856" height="396" rx="22" fill="none" stroke="url(#border)" stroke-width="1.5"/>
</svg>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT,"w",encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT, "| contribution:", f"{contribution:,}", "delta:", delta, "span:", span,
          "| supporting:", {l:fmt(v) for l,v in supporting})

if __name__=="__main__":
    build(load())
