#!/usr/bin/env python3
"""リンクセクション用のクリッカブル・グラスカード 4 枚を生成する。
README 側で各カードを <a> で包む＝カード全体が実リンクになる（真のインタラクティブ）。
カードごとにブランド色（Qiita=緑 / コード=水色 / ブログ=紫+星 / 集計ツール=深青）。
制約: camo 安全（SMIL のみ）。基準値=完成形。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

TEXT="#E9F1FA"; MUTED="#8A9BAB"; STAR="#DDE8FF"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic','Noto Sans JP',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"

I_PEN='<path d="M3 17 L4 13 L14 3 L17 6 L7 16 Z"/><path d="M12.5 4.5 L15.5 7.5"/>'
I_CODE='<path d="M7 5 L2.5 10 L7 15"/><path d="M13 5 L17.5 10 L13 15"/>'
I_PLANET='<circle cx="10" cy="10" r="5.5"/><ellipse cx="10" cy="10" rx="9" ry="3.2" transform="rotate(-16 10 10)"/>'
I_CHART='<path d="M3 17 V10"/><path d="M8 17 V6"/><path d="M13 17 V12"/><path d="M18 17 V3"/>'

CARDS=[
    # (file, idp, accent, light, icon, en, title, desc, glint_begin, extra)
    ("link-qiita.svg",  "lq", "#55C500", "#9FE86B", I_PEN,    "QIITA",   "Qiita",           "AWS・AI・セキュリティ の技術記事 ・ 全10シリーズ", 2.0, ""),
    ("link-code.svg",   "lc", "#5CD1F0", "#A8ECFF", I_CODE,   "GITHUB",  "サンプルコード",     "連載記事のサンプルコード集",                    4.8, ""),
    ("link-blog.svg",   "lb", "#8A7DD8", "#C9BEF5", I_PLANET, "BLOG",    "mirukyのIT備忘録",  "ポートフォリオ・技術ブログ ・ 宇宙の片隅から",      7.6, "stars"),
    ("link-tracker.svg","lt", "#3AA0E0", "#9AD1F5", I_CHART,  "TRACKER", "Qiita 集計ツール",  "自作のコントリビューション可視化ツール",           10.4, ""),
]

def build(file, idp, acc, light, icon, en, title, desc, gb, extra):
    W,H=560,108
    stars=""
    if extra=="stars":
        pts=[(376,26,0.5,1.0),(432,66,0.35,0.8),(468,22,0.45,1.1),(492,78,0.3,0.7),(350,80,0.3,0.8)]
        stars="".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STAR}" opacity="{op}"/>' for x,y,op,r in pts)
        stars+=(f'<g transform="translate(452,42)"><path d="M0 -2.6 L0.6 -0.6 L2.6 0 L0.6 0.6 L0 2.6 L-0.6 0.6 L-2.6 0 L-0.6 -0.6 Z" fill="{light}" opacity="0.6">'
                f'<animate attributeName="opacity" values="0.3;0.9;0.3" dur="4.2s" begin="1.1s" repeatCount="indefinite"/></path></g>')

    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
<defs>
  <radialGradient id="{idp}t" cx="0.5" cy="0.2" r="1.0">
    <stop offset="0" stop-color="#0E141C"/><stop offset="1" stop-color="#0A0E14"/>
  </radialGradient>
  <linearGradient id="{idp}g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{acc}" stop-opacity="0.13"/><stop offset="1" stop-color="{acc}" stop-opacity="0.04"/>
  </linearGradient>
  <linearGradient id="{idp}r" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{light}" stop-opacity="0.5"/><stop offset="0.5" stop-color="{acc}" stop-opacity="0.18"/><stop offset="1" stop-color="#04121C" stop-opacity="0.10"/>
  </linearGradient>
  <linearGradient id="{idp}gl" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.10"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="{idp}o" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{acc}" stop-opacity="0.20"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/>
  </radialGradient>
  <filter id="{idp}s" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="{idp}d" x="-20%" y="-30%" width="140%" height="170%" color-interpolation-filters="sRGB">
    <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#04121C" flood-opacity="0.45"/>
  </filter>
  <filter id="{idp}n" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.36  0 0 0 0 0.82  0 0 0 0 0.94  0 0 0 0.04 0"/>
  </filter>
  <clipPath id="{idp}c"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="17"/></clipPath>
</defs>
<g filter="url(#{idp}d)">
  <g clip-path="url(#{idp}c)">
    <rect x="2" y="2" width="{W-4}" height="{H-4}" fill="url(#{idp}t)"/>
    <circle cx="120" cy="20" r="110" fill="url(#{idp}o)" filter="url(#{idp}s)"/>
    <rect x="2" y="2" width="{W-4}" height="{H-4}" fill="url(#{idp}g)"/>
    <rect x="2" y="2" width="{W-4}" height="40" fill="#FFFFFF" opacity="0.045"/>
    {stars}
    <rect x="-200" y="-20" width="150" height="{H+40}" fill="url(#{idp}gl)" transform="skewX(-18)">
      <animate attributeName="x" values="-200;760;760" keyTimes="0;0.12;1" dur="11s" begin="{gb}s" repeatCount="indefinite"/>
    </rect>
    <rect x="2" y="2" width="{W-4}" height="{H-4}" fill="#000" opacity="0.5" filter="url(#{idp}n)"/>
  </g>
  <!-- icon box -->
  <rect x="24" y="30" width="48" height="48" rx="13" fill="{acc}" fill-opacity="0.12" stroke="{acc}" stroke-opacity="0.32" stroke-width="1"/>
  <g transform="translate(38,44)" fill="none" stroke="{light}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
  <!-- text -->
  <text x="92" y="42" font-family="{MONO}" font-size="9.5" letter-spacing="3" fill="{acc}" opacity="0.9">{en}</text>
  <text x="92" y="63" font-family="{JP}" font-size="17" font-weight="700" fill="{TEXT}">{title}</text>
  <text x="92" y="85" font-family="{JP}" font-size="12" fill="{MUTED}">{desc}</text>
  <!-- arrow（そっと誘うナッジ） -->
  <g>
    <circle cx="512" cy="54" r="17" fill="{acc}" fill-opacity="0.10" stroke="{acc}" stroke-opacity="0.35" stroke-width="1.2"/>
    <g fill="none" stroke="{light}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M505 54 H518"/><path d="M513 48.5 L518.5 54 L513 59.5"/>
    </g>
    <animateTransform attributeName="transform" type="translate" values="0 0;3 0;0 0" dur="2.6s" begin="{gb/3:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </g>
  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="17" fill="none" stroke="url(#{idp}r)" stroke-width="1.3"/>
</g>
</svg>'''
    path=os.path.join(ASSETS,file)
    with open(path,"w",encoding="utf-8") as f: f.write(svg)
    print(f"{file}  {os.path.getsize(path)}B")

if __name__=="__main__":
    for c in CARDS:
        build(*c)
