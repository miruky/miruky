#!/usr/bin/env python3
"""ヒーロー（assets/header.svg）・ロールカルーセル（assets/roles.svg）・フッター（assets/footer.svg）を生成する。
方針: 全て自作 SVG / camo 安全（SMIL のみ、CSS アニメ・foreignObject 不可）。
静的レンダラでも破綻しないよう、アニメ対象は「基準値=完成形」にして values で 0 から動かす。"""
import os, base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

BG="#0D1117"; TEXT="#E6EDF3"; MUTED="#7D8590"
ACCENT="#5CD1F0"; ACCENT2="#A8ECFF"; DEEP="#3AA0E0"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic','Noto Sans JP','Meiryo',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"

def b64(name):
    with open(os.path.join(ASSETS, name), "rb") as f:
        return base64.b64encode(f.read()).decode()

# ============================================================ HEADER
def build_header():
    mascot = b64("mascot-lg.png")

    # イコライザーバー（マスコット左・呼吸＋一部は高さパルス）
    heights=[46,84,60,112,72,132,92,56,104,66]
    bars=""
    for i,h in enumerate(heights):
        x=766+i*18; y=224-h
        dur=2.6+(i%3)*0.5; beg=i*0.22
        pulse=""
        if i%3==1:
            h2=int(h*1.3); y2=224-h2; pd=2.8+0.3*i
            pulse=(f'<animate attributeName="height" values="{h};{h2};{h}" dur="{pd}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>'
                   f'<animate attributeName="y" values="{y};{y2};{y}" dur="{pd}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>')
        bars+=(f'<rect x="{x}" y="{y}" width="8" height="{h}" rx="3" fill="{ACCENT}" opacity="0.13">'
               f'<animate attributeName="opacity" values="0.08;0.24;0.08" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>{pulse}</rect>')

    # 浮遊パーティクル（下から上へ・非同期）
    parts=[(160,0,11,2.0),(340,2,13,1.6),(520,4,10,1.8),(640,1,14,2.2),(730,3,12,1.5),(905,5.5,15,2.0),(245,6.5,12,1.4)]
    particles=""
    for x,beg,dur,r in parts:
        particles+=(f'<circle cx="{x}" cy="200" r="{r}" fill="{ACCENT2}" opacity="0">'
                    f'<animate attributeName="cy" values="272;46" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="0;0.4;0" keyTimes="0;0.35;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></circle>')

    # コーヒーの湯気（マスコットのカップ上）
    steam=""
    for (sx,sy,dur,beg) in [(1036,188,3.8,0.4),(1047,182,4.4,1.5),(1057,189,5.0,2.6)]:
        steam+=(f'<g transform="translate({sx},{sy})">'
                f'<path d="M0 0 C-4 -7 4 -12 0 -20" fill="none" stroke="#D7EDF7" stroke-width="1.6" stroke-linecap="round" opacity="0.15">'
                f'<animate attributeName="opacity" values="0;0.5;0" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -16" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                f'</path></g>')

    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300" role="img" aria-label="miruky - AWS Cloud Engineer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0A0D12"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.8" cy="0.32" r="0.6">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.15"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aurA" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.11"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aurB" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{DEEP}" stop-opacity="0.10"/><stop offset="1" stop-color="{DEEP}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT2}"/>
    </linearGradient>
    <linearGradient id="glint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="mglow" cx="0.5" cy="0.46" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.28"/><stop offset="0.6" stop-color="{ACCENT}" stop-opacity="0.08"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <filter id="msoft" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="asoft" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="24"/></filter>
    <filter id="hgrain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.36  0 0 0 0 0.82  0 0 0 0 0.94  0 0 0 0.05 0"/>
    </filter>
    <clipPath id="kclip">
      <rect x="90" y="74" width="380" height="30">
        <animate attributeName="width" values="0;380" dur="0.9s" begin="0.15s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/>
      </rect>
    </clipPath>
  </defs>

  <rect width="1200" height="300" fill="url(#bg)"/>
  <!-- aurora drift -->
  <ellipse cx="300" cy="80" rx="270" ry="95" fill="url(#aurA)" filter="url(#asoft)">
    <animateTransform attributeName="transform" type="translate" values="0 0;60 14;0 0" dur="16s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </ellipse>
  <ellipse cx="640" cy="215" rx="300" ry="100" fill="url(#aurB)" filter="url(#asoft)">
    <animateTransform attributeName="transform" type="translate" values="0 0;-70 -12;0 0" dur="21s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </ellipse>
  <rect width="1200" height="300" fill="url(#glow)"/>
  <rect width="1200" height="300" fill="#000" opacity="0.7" filter="url(#hgrain)"/>

  {particles}
  <g>{bars}</g>

  <!-- kicker (wipe-in) -->
  <text x="92" y="96" font-family="{MONO}" font-size="15" letter-spacing="6" fill="{MUTED}" clip-path="url(#kclip)">AWS &#183; SERVERLESS &#183; GENAI</text>

  <!-- wordmark -->
  <text x="86" y="184" font-family="{SANS}" font-size="94" font-weight="800" letter-spacing="1" fill="#F0F6FC">miruky</text>
  <!-- diagonal glint（柔らかいグラデ帯が素早く通過 → 静止） -->
  <rect x="-340" y="-40" width="240" height="380" fill="url(#glint)" transform="skewX(-18)">
    <animate attributeName="x" values="-340;1560;1560" keyTimes="0;0.11;1" dur="12s" begin="1.5s" repeatCount="indefinite"/>
  </rect>

  <rect x="92" y="203" width="382" height="4" rx="2" fill="url(#rule)">
    <animate attributeName="width" values="0;382" dur="1.1s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/>
  </rect>
  <text x="94" y="244" font-family="{JP}" font-size="22" letter-spacing="1" fill="{MUTED}">クラウドエンジニア <tspan fill="#30363D">/</tspan> Qiita ライター</text>

  <!-- status pill -->
  <g transform="translate(92,258)">
    <rect width="452" height="32" rx="16" fill="#12161D" fill-opacity="0.85" stroke="{ACCENT}" stroke-opacity="0.28"/>
    <rect x="1" y="1" width="450" height="14" rx="13" fill="#FFFFFF" opacity="0.05"/>
    <circle cx="18" cy="16" r="4" fill="{ACCENT}">
      <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="r" values="4;5.2;4" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="34" y="21" font-family="{JP}" font-size="13" fill="#9FB6C8">いま構築中 : Terraform × Amazon Bedrock の生成AI基盤</text>
  </g>

  <!-- mascot: orbit ring + glow + bob + steam -->
  <g>
    <circle cx="1058" cy="160" r="96" fill="none" stroke="{ACCENT}" stroke-opacity="0.16" stroke-width="1.2" stroke-dasharray="2 9">
      <animateTransform attributeName="transform" type="rotate" from="0 1058 160" to="360 1058 160" dur="70s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1058" cy="160" r="98" fill="url(#mglow)" filter="url(#msoft)"/>
    <image x="972" y="74" width="172" height="172" href="data:image/png;base64,{mascot}" preserveAspectRatio="xMidYMid meet">
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="4.4s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
    </image>
    {steam}
  </g>
</svg>'''
    with open(os.path.join(ASSETS,"header.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("header.svg", os.path.getsize(os.path.join(ASSETS,"header.svg")), "B")

# ============================================================ ROLES (typing-svg の置き換え)
def build_roles():
    lines=["AWS Cloud Engineer","Qiita Writer / 80+ Articles","AWS All Certifications","IaC / Serverless / GenAI"]
    n=len(lines); per=4.0; total=per*n
    items=""
    for i,s in enumerate(lines):
        base = 1 if i==0 else 0
        items+=(f'<text x="34" y="29" font-family="{MONO}" font-size="18" letter-spacing="1" fill="#B6C9D6" opacity="{base}">{s}'
                f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.04;0.22;0.26;1" dur="{total}s" begin="{i*per}s" repeatCount="indefinite"/></text>')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 44" width="560" height="44" role="img" aria-label="roles">
  <text x="8" y="29" font-family="{MONO}" font-size="18" fill="{ACCENT}">&gt;</text>
  <rect x="22" y="13" width="3" height="20" fill="{ACCENT}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
  {items}
</svg>'''
    with open(os.path.join(ASSETS,"roles.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("roles.svg", os.path.getsize(os.path.join(ASSETS,"roles.svg")), "B")

# ============================================================ FOOTER
def build_footer():
    mascot = b64("mascot.png")
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 116" width="1200" height="116" role="img" aria-label="footer">
  <defs>
    <linearGradient id="fd" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="0.5" stop-color="{ACCENT}" stop-opacity="0.5"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fs" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{ACCENT2}" stop-opacity="0"/><stop offset="0.5" stop-color="{ACCENT2}" stop-opacity="0.9"/><stop offset="1" stop-color="{ACCENT2}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="10" width="1200" height="1.4" fill="url(#fd)"/>
  <rect x="-260" y="9.4" width="260" height="2.6" rx="1.3" fill="url(#fs)">
    <animate attributeName="x" values="-260;1200;1200" keyTimes="0;0.35;1" dur="8s" begin="5s" repeatCount="indefinite"/>
  </rect>
  <image x="578" y="22" width="44" height="44" href="data:image/png;base64,{mascot}" preserveAspectRatio="xMidYMid meet">
    <animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="3.8s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </image>
  <text x="600" y="90" text-anchor="middle" font-family="{JP}" font-size="14" fill="{MUTED}">このプロフィールのビジュアルは、すべて自作の SVG でできています</text>
  <text x="1188" y="108" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="2" fill="#57606A">DESIGNED &amp; BUILT BY MIRUKY</text>
</svg>'''
    with open(os.path.join(ASSETS,"footer.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("footer.svg", os.path.getsize(os.path.join(ASSETS,"footer.svg")), "B")

if __name__=="__main__":
    build_header(); build_roles(); build_footer()
