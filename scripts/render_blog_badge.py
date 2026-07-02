#!/usr/bin/env python3
"""ブログ用の自作バッジ（宇宙グラスカプセル + マスコット）。
mirukyのIT備忘録（宇宙テーマの技術ブログ）への小さく薄い光沢グラス・バッジ。
制約: committed SVG / camo安全（SMIL + feTurbulence + feGaussianBlur、CSS/foreignObject不可）。
マスコットPNGは base64 埋め込み（camo越しの外部参照は読めないため）。"""
import os, base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASCOT = os.path.join(ROOT, "assets", "mascot.png")
OUT = os.path.join(ROOT, "assets", "blog-badge.svg")

NAV1="#0D0B1A"; NAV2="#05040B"; STAR="#DDE8FF"; CYAN="#7EE8E3"; VIO="#8A7DD8"
TEXT="#EAF2FF"; SUB="#93A2CE"; GREEN="#55C500"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"

def b64():
    with open(MASCOT, "rb") as f:
        return base64.b64encode(f.read()).decode()

def build():
    data = b64()
    # ---- 手置きの星（決定的） ----
    stars = [(28,20,0.7,1.0),(64,58,0.5,0.8),(120,16,0.9,1.1),(150,64,0.6,0.9),(186,26,0.7,1.0),
             (214,60,0.5,0.8),(250,20,0.8,1.0),(276,52,0.6,0.9),(300,66,0.5,0.8),(196,48,0.5,0.7),
             (108,40,0.5,0.8),(238,42,0.6,0.9)]
    star_svg=""
    for i,(x,y,op,r) in enumerate(stars):
        star_svg+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STAR}" opacity="{op}"/>'
    # twinkle 4つ（非同期）
    tw=[(96,22,CYAN,3.2,'0.3'),(168,58,'#FFFFFF',4.1,'0.7'),(258,30,VIO,5.0,'1.1'),(210,20,CYAN,3.7,'1.9')]
    twinkle=""
    for x,y,c,dur,beg in tw:
        twinkle+=(f'<g transform="translate({x},{y})">'
                  f'<path d="M0 -3 L0.7 -0.7 L3 0 L0.7 0.7 L0 3 L-0.7 0.7 L-3 0 L-0.7 -0.7 Z" fill="{c}">'
                  f'<animate attributeName="opacity" values="0.2;1;0.4;0.2" keyTimes="0;0.2;0.5;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                  f'</path></g>')

    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 90" width="340" height="90" role="img" aria-label="mirukyのIT備忘録 (Blog)">
<defs>
  <radialGradient id="space" cx="0.28" cy="0.35" r="1.0">
    <stop offset="0" stop-color="{NAV1}"/><stop offset="1" stop-color="{NAV2}"/>
  </radialGradient>
  <radialGradient id="neb1" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{VIO}" stop-opacity="0.55"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="neb2" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0.30"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="planet" cx="0.36" cy="0.30" r="0.75">
    <stop offset="0" stop-color="#6E7BC8"/><stop offset="0.6" stop-color="#2A2F63"/><stop offset="1" stop-color="#12142E"/>
  </radialGradient>
  <radialGradient id="mglow" cx="0.5" cy="0.45" r="0.5">
    <stop offset="0" stop-color="{VIO}" stop-opacity="0.6"/><stop offset="0.6" stop-color="{GREEN}" stop-opacity="0.18"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="0.7" y2="1">
    <stop offset="0" stop-color="#CFE0FF" stop-opacity="0.16"/><stop offset="0.5" stop-color="{VIO}" stop-opacity="0.08"/><stop offset="1" stop-color="#0A0620" stop-opacity="0.30"/>
  </linearGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#E4F3FF" stop-opacity="0.55"/><stop offset="0.5" stop-color="{VIO}" stop-opacity="0.15"/><stop offset="1" stop-color="#101a40" stop-opacity="0.10"/>
  </linearGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.16"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="shoot" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.9"/>
  </linearGradient>
  <linearGradient id="bglint" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.12"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <filter id="soft" x="-80%" y="-80%" width="260%" height="260%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="7"/></filter>
  <filter id="soft2" x="-80%" y="-80%" width="260%" height="260%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="drop" x="-30%" y="-30%" width="160%" height="180%" color-interpolation-filters="sRGB">
    <feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="#0A0620" flood-opacity="0.45"/>
  </filter>
  <filter id="dust" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.87  0 0 0 0 0.91  0 0 0 0 1  0 0 0 0.5 -0.42"/>
  </filter>
  <clipPath id="pill"><rect x="2" y="2" width="336" height="86" rx="20"/></clipPath>
  <clipPath id="bubble"><circle cx="47" cy="46" r="27"/></clipPath>
</defs>

<g filter="url(#drop)">
<g clip-path="url(#pill)">
  <rect x="2" y="2" width="336" height="86" fill="url(#space)"/>
  <!-- nebula -->
  <ellipse cx="60" cy="52" rx="70" ry="46" fill="url(#neb1)" filter="url(#soft)"/>
  <ellipse cx="120" cy="30" rx="60" ry="34" fill="url(#neb2)" filter="url(#soft)" opacity="0.8"/>
  <!-- procedural dust -->
  <rect x="2" y="2" width="336" height="86" filter="url(#dust)" opacity="0.5"/>
  <!-- stars -->
  {star_svg}
  {twinkle}
  <!-- planet + orbit + moon (upper right) -->
  <g transform="translate(300,24)">
    <ellipse cx="0" cy="0" rx="20" ry="7" fill="none" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="0.6" stroke-dasharray="1 5" transform="rotate(-18)">
      <animateTransform attributeName="transform" type="rotate" from="-18" to="342" dur="80s" repeatCount="indefinite"/>
    </ellipse>
    <circle r="7.5" fill="url(#planet)"/>
    <ellipse cx="0" cy="0" rx="11" ry="3.4" fill="none" stroke="#9FB0E8" stroke-opacity="0.5" stroke-width="1.1" transform="rotate(-18)"/>
    <circle cx="-2.4" cy="-2.6" r="2" fill="#FFFFFF" opacity="0.5" filter="url(#soft2)"/>
    <g transform="rotate(-18)"><circle cx="20" cy="0" r="1.4" fill="#CFE0FF">
      <animateMotion dur="80s" repeatCount="indefinite" path="M0 0 a20 7 0 1 1 0 0.1 Z"/></circle></g>
  </g>
  <!-- shooting star -->
  <line x1="150" y1="14" x2="182" y2="26" stroke="url(#shoot)" stroke-width="1.3" stroke-linecap="round" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.02;0.06;0.12" dur="9s" begin="3s" repeatCount="indefinite"/>
  </line>

  <!-- glass veil over the scene -->
  <rect x="2" y="2" width="336" height="86" rx="20" fill="url(#glass)"/>
  <rect x="3" y="3" width="334" height="34" rx="18" fill="url(#sheen)"/>
</g>

<!-- mascot bubble (inside the glass) -->
<circle cx="47" cy="46" r="30" fill="url(#mglow)" filter="url(#soft2)"/>
<circle cx="47" cy="46" r="27.5" fill="#0B0A18" fill-opacity="0.5"/>
<image x="17" y="16" width="60" height="60" clip-path="url(#bubble)" href="data:image/png;base64,{data}" preserveAspectRatio="xMidYMid slice">
  <animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" dur="3.6s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
</image>
<circle cx="47" cy="46" r="27.5" fill="none" stroke="url(#rim)" stroke-width="1.2"/>
<path d="M28 34 A27 27 0 0 1 60 26" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1.4" stroke-linecap="round"/>

<!-- text -->
<text x="92" y="42" font-family="{JP}" font-size="14.5" font-weight="600" fill="{TEXT}">mirukyのIT備忘録</text>
<text x="92" y="61" font-family="{MONO}" font-size="9.5" letter-spacing="3" fill="{SUB}">BLOG <tspan font-family="{JP}" letter-spacing="1">・ 宇宙の片隅から</tspan></text>

<!-- rim + one asymmetric glint -->
<rect x="2" y="2" width="336" height="86" rx="20" fill="none" stroke="url(#rim)" stroke-width="1.3"/>
<circle cx="292" cy="74" r="8" fill="#FFFFFF" opacity="0.12" filter="url(#soft2)"/>
<!-- diagonal glint（素早く通過 → 静止） -->
<g clip-path="url(#pill)">
  <rect x="-140" y="-20" width="110" height="130" fill="url(#bglint)" transform="skewX(-18)">
    <animate attributeName="x" values="-140;480;480" keyTimes="0;0.13;1" dur="9s" begin="2.2s" repeatCount="indefinite"/>
  </rect>
</g>
</g>
</svg>'''
    with open(OUT,"w",encoding="utf-8") as f: f.write(svg)
    print("wrote", OUT, "size", os.path.getsize(OUT), "B")

if __name__=="__main__":
    build()
