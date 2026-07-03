#!/usr/bin/env python3
"""ヒーロー（assets/header.svg）・ロールカルーセル（roles.svg）・フッター（footer.svg）・セクション見出しを生成。
方針: 全て自作 SVG / camo 安全（SMIL のみ）。ワードマークは Futura Bold の字形パス（wordmark.py）。
登場シーケンス（begin=0 + keyTimes 保持→移動）で静的レンダラでも破綻しない（基準値=完成形）。"""
import os, re, base64, random, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wordmark import LETTERS, WORDMARK_X0, WORDMARK_BASE, WORDMARK_W

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

BG="#0D1117"; TEXT="#E6EDF3"; MUTED="#7D8590"
ACCENT="#5CD1F0"; ACCENT2="#A8ECFF"; DEEP="#3AA0E0"
VIO="#8A7DD8"; VIO_LT="#C9BEF5"; STAR="#DDE8FF"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic','Noto Sans JP','Meiryo',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"

def b64(name):
    with open(os.path.join(ASSETS, name), "rb") as f:
        return base64.b64encode(f.read()).decode()

# ロード時の登場（不透明度＋下から）。begin=0 で keyTimes 保持→移動、基準=完成形。
def _rise(delay, dy, dur=1.6, span=0.15):
    d0, d1 = delay, min(0.999, delay+span)
    return (f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{d0:.3f};{d1:.3f}" dur="{dur}s" begin="0s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 {dy};0 0" keyTimes="0;{d0:.3f};{d1:.3f}" '
            f'dur="{dur}s" begin="0s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;0.16 1 0.3 1"/>')

def _stars(seed, n, rmin, rmax, omin, omax, avoid=None):
    rnd = random.Random(seed); out = []
    for _ in range(n):
        x = rnd.uniform(16, 1184); y = rnd.uniform(12, 288)
        if avoid and avoid[0] < x < avoid[1] and avoid[2] < y < avoid[3]:
            continue
        out.append((x, y, rnd.uniform(rmin, rmax), rnd.uniform(omin, omax)))
    return out

def _starc(x, y, r, o, tw=False, dur=4.0, beg=0.0):
    base = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{STAR}" opacity="{o:.2f}"'
    if tw:
        return base + (f'><animate attributeName="opacity" values="{o:.2f};{min(1,o*2.3):.2f};{o*0.55:.2f};{o:.2f}" '
                       f'keyTimes="0;0.2;0.5;1" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/></circle>')
    return base + '/>'

def _cluster(seed, cx, cy, spread, n):
    # 星団: 中心に淡いグロー + ガウス分布で密集した小星群
    rnd = random.Random(seed)
    out = f'<circle cx="{cx}" cy="{cy}" r="{spread*2.3:.0f}" fill="url(#clglow)" filter="url(#asoft)"/>'
    for i in range(n):
        a = rnd.uniform(0, 6.283); rr = abs(rnd.gauss(0, spread*0.55))
        x = cx + rr*math.cos(a); y = cy + rr*math.sin(a)*0.68
        out += _starc(x, y, rnd.uniform(0.4, 1.15), rnd.uniform(0.25, 0.72),
                      tw=(i % 5 == 0), dur=3+(i % 3)*0.7, beg=(i % 4)*0.6)
    return out

def _flare(x, y, size, col, beg=1.0):
    # 光条星（回折スパイク付きの明るい星）
    return (f'<g transform="translate({x},{y})">'
            f'<path d="M0 {-size} L0 {size} M{-size} 0 L{size} 0 M{-size*0.5:.1f} {-size*0.5:.1f} L{size*0.5:.1f} {size*0.5:.1f} M{-size*0.5:.1f} {size*0.5:.1f} L{size*0.5:.1f} {-size*0.5:.1f}" '
            f'stroke="{col}" stroke-width="0.6" stroke-linecap="round" opacity="0.4"/>'
            f'<circle r="1.7" fill="{col}" filter="url(#nodeglow)"/>'
            f'<animate attributeName="opacity" values="0.55;1;0.55" dur="4.5s" begin="{beg}s" repeatCount="indefinite"/></g>')

# ============================================================ HEADER
def build_header():
    mascot = b64("mascot-lg.png")

    # --- 3層パララックス星空 ---
    far = _stars(11, 80, 0.4, 0.8, 0.12, 0.30)
    mid = _stars(23, 40, 0.7, 1.05, 0.26, 0.48)
    near = _stars(31, 18, 1.0, 1.6, 0.38, 0.66, avoid=(58, 486, 62, 214))
    far_svg = "".join(_starc(*s) for s in far)
    mid_svg = "".join(_starc(*s, tw=(i % 4 == 0), dur=3.2+(i % 3)*0.6, beg=(i % 5)*0.7) for i, s in enumerate(mid))
    near_svg = "".join(_starc(*s, tw=(i % 3 == 0), dur=3.6+(i % 3)*0.5, beg=(i % 4)*0.6) for i, s in enumerate(near))
    spk = ""
    for x, y, c, dur, beg in [(516,30,ACCENT2,4.2,0.5),(834,50,"#FFFFFF",5.1,1.3),(1122,58,VIO_LT,3.6,2.1),(706,252,ACCENT2,4.6,2.8)]:
        spk += (f'<g transform="translate({x},{y})"><path d="M0 -3.4 L0.8 -0.8 L3.4 0 L0.8 0.8 L0 3.4 L-0.8 0.8 L-3.4 0 L-0.8 -0.8 Z" '
                f'fill="{c}" opacity="0.5"><animate attributeName="opacity" values="0.2;1;0.4;0.2" keyTimes="0;0.2;0.5;1" '
                f'dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></path></g>')
    def _drift(inner, amp_x, amp_y, dur):
        return (f'<g>{inner}<animateTransform attributeName="transform" type="translate" values="0 0;{amp_x} {amp_y};0 0" '
                f'dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></g>')
    far_layer = f'<g filter="url(#sblur)">{_drift(far_svg, 5, 3, 46)}</g>'
    mid_layer = _drift(mid_svg, -9, 4, 31)
    near_layer = _drift(near_svg + spk, 13, -6, 22)

    # --- 星団（クラスター）＋ 光条星 ---
    clusters = _cluster(41, 716, 50, 26, 22) + _cluster(42, 322, 250, 30, 26) + _cluster(43, 604, 234, 22, 15)
    flares = _flare(876, 112, 7, ACCENT2, 1.0) + _flare(506, 74, 6, VIO_LT, 2.4) + _flare(690, 210, 5, ACCENT2, 3.1)

    shoot = ('<line x1="628" y1="16" x2="668" y2="32" stroke="url(#hshoot)" stroke-width="1.2" stroke-linecap="round" opacity="0">'
             '<animate attributeName="opacity" values="0;0;0.9;0" keyTimes="0;0.02;0.06;0.12" dur="15s" begin="7s" repeatCount="indefinite"/>'
             '<animateTransform attributeName="transform" type="translate" values="-30 -12;70 28;70 28" keyTimes="0;0.12;1" dur="15s" begin="7s" repeatCount="indefinite"/></line>')

    # --- 星座線（ワードマークとマスコットの間の空白を結ぶ） ---
    cp = [(492,196),(600,150),(720,176),(852,120),(958,152)]
    cline = "M" + " L".join(f"{x} {y}" for x, y in cp)
    constellation = (f'<path d="{cline}" fill="none" stroke="{ACCENT}" stroke-opacity="0.16" stroke-width="1" stroke-dasharray="1.5 6" '
                     f'pathLength="100" stroke-dashoffset="0"><animate attributeName="stroke-dashoffset" values="100;0" dur="1.6s" begin="0.5s" fill="freeze"/></path>')
    for i, (x, y) in enumerate(cp):
        rr = 1.9 if i in (0, 4) else 1.3
        constellation += (f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{ACCENT2 if i%2 else STAR}" opacity="0.55">'
                          f'<animate attributeName="opacity" values="0.35;0.85;0.35" dur="{3+i*0.4:.1f}s" begin="{i*0.5:.1f}s" repeatCount="indefinite"/></circle>')

    # --- 環付き惑星（マスコット手前上） ---
    planet = ('<g transform="translate(902,58)" opacity="0.9">'
              '<ellipse rx="18" ry="6" fill="none" stroke="#8FA0D8" stroke-opacity="0.3" stroke-width="1" transform="rotate(-16)"/>'
              '<circle r="11" fill="url(#planet)"/>'
              '<circle cx="-3.4" cy="-3.6" r="3" fill="#FFFFFF" opacity="0.3" filter="url(#psoft)"/>'
              '<ellipse rx="18" ry="6" fill="none" stroke="#BFCBF7" stroke-opacity="0.5" stroke-width="1.1" transform="rotate(-16)"/></g>')

    # --- ワードマーク（Futura Bold 字形・1文字ずつ登場） ---
    wm = ""
    for i, (ch, d, lx) in enumerate(LETTERS):
        wm += (f'<g>{_rise(0.10+i*0.035, 24)}<path d="{d}" fill="url(#wmgrad)"/></g>')

    # --- シグナル下線（描画 → 光ノードが走る → 端で点滅） ---
    uw = WORDMARK_W - 6; ux = 92; ue = ux + uw
    underline = (f'<rect x="{ux}" y="203" width="{uw:.0f}" height="4" rx="2" fill="url(#rule)">'
                 f'<animate attributeName="width" values="0;{uw:.0f}" dur="1.0s" begin="0.34s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/></rect>'
                 f'<circle cy="205" r="3.4" fill="#EAFBFF" filter="url(#nodeglow)">'
                 f'<animate attributeName="cx" values="{ux};{ue:.0f}" dur="2.4s" begin="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 1 0.3 1" keyTimes="0;1"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="2.4s" begin="0.4s" fill="freeze"/></circle>'
                 f'<circle cx="{ue:.0f}" cy="205" r="3" fill="{ACCENT2}"><animate attributeName="r" values="2;5;2" dur="2.8s" begin="2.8s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.9;0.25;0.9" dur="2.8s" begin="2.8s" repeatCount="indefinite"/></circle>')

    # --- マスコット・シーン（イコライザー廃止 → 軌道＋衛星） ---
    def orbit(rx, ry, rot, dash, sat_c, sat_r, dur, rev=False):
        ell = f"M {rx} 0 A {rx} {ry} 0 1 1 {-rx} 0 A {rx} {ry} 0 1 1 {rx} 0 Z"
        kp = "1;0" if rev else "0;1"
        return (f'<g transform="rotate({rot})">'
                f'<ellipse rx="{rx}" ry="{ry}" fill="none" stroke="{ACCENT}" stroke-opacity="0.13" stroke-width="1.1" stroke-dasharray="{dash}"/>'
                f'<circle r="{sat_r}" fill="{sat_c}" filter="url(#nodeglow)">'
                f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{ell}" keyPoints="{kp}" keyTimes="0;1" calcMode="linear"/></circle></g>')
    orbits = ('<g transform="translate(1058,158)">'
              + orbit(104, 104, 0, "2 9", ACCENT2, 2.6, 16)
              + orbit(128, 66, -22, "2 8", ACCENT, 2.3, 22, rev=True)
              + orbit(74, 116, 26, "1.5 8", VIO_LT, 2.2, 19)
              + '</g>')
    steam = ""
    for sx, sy, dur, beg in [(1036,192,3.8,0.4),(1047,186,4.4,1.5),(1057,193,5.0,2.6)]:
        steam += (f'<g transform="translate({sx},{sy})"><path d="M0 0 C-4 -7 4 -12 0 -20" fill="none" stroke="#D7EDF7" stroke-width="1.6" '
                  f'stroke-linecap="round" opacity="0.15"><animate attributeName="opacity" values="0;0.5;0" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                  f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -16" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></path></g>')
    mascot_img = (f'<image x="972" y="76" width="172" height="172" href="data:image/png;base64,{mascot}" preserveAspectRatio="xMidYMid meet">'
                  f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="4.4s" begin="0s" repeatCount="indefinite" '
                  f'calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></image>')
    mascot_scene = (f'<g><animate attributeName="opacity" values="0;0;1" keyTimes="0;0.10;0.34" dur="1.6s" begin="0s" fill="freeze"/>'
                    f'<circle cx="1058" cy="158" r="98" fill="url(#hmglow)" filter="url(#msoft)"/>'
                    f'{orbits}{mascot_img}{steam}</g>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300" role="img" aria-label="miruky - AWS Cloud Engineer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0A0D12"/></linearGradient>
    <radialGradient id="glow" cx="0.8" cy="0.32" r="0.6"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.15"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
    <radialGradient id="aurA" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.11"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
    <radialGradient id="aurB" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{DEEP}" stop-opacity="0.10"/><stop offset="1" stop-color="{DEEP}" stop-opacity="0"/></radialGradient>
    <radialGradient id="aurV" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{VIO}" stop-opacity="0.26"/><stop offset="0.6" stop-color="{VIO}" stop-opacity="0.12"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/></radialGradient>
    <radialGradient id="aurV2" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#A78BFA" stop-opacity="0.16"/><stop offset="1" stop-color="#A78BFA" stop-opacity="0"/></radialGradient>
    <radialGradient id="vglow" cx="0.32" cy="1.0" r="0.75"><stop offset="0" stop-color="{VIO}" stop-opacity="0.16"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/></radialGradient>
    <radialGradient id="vig" cx="0.34" cy="0.5" r="0.85"><stop offset="0" stop-color="#04060A" stop-opacity="0"/><stop offset="0.55" stop-color="#04060A" stop-opacity="0"/><stop offset="1" stop-color="#04060A" stop-opacity="0.6"/></radialGradient>
    <radialGradient id="planet" cx="0.36" cy="0.3" r="0.8"><stop offset="0" stop-color="#8B93D8"/><stop offset="0.6" stop-color="#3A3F7A"/><stop offset="1" stop-color="#171B3E"/></radialGradient>
    <linearGradient id="hshoot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.9"/></linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{VIO_LT}"/></linearGradient>
    <linearGradient id="wmgrad" x1="0" y1="0" x2="0.85" y2="1"><stop offset="0" stop-color="#F2F7FF"/><stop offset="0.42" stop-color="#A9D3FF"/><stop offset="0.74" stop-color="#BFB4F3"/><stop offset="1" stop-color="#AE97E8"/></linearGradient>
    <radialGradient id="clglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#A6BEFF" stop-opacity="0.16"/><stop offset="1" stop-color="#A6BEFF" stop-opacity="0"/></radialGradient>
    <linearGradient id="pillglass" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#3E4E72" stop-opacity="0.34"/><stop offset="0.5" stop-color="#1A2236" stop-opacity="0.40"/><stop offset="1" stop-color="#0E1320" stop-opacity="0.52"/></linearGradient>
    <linearGradient id="pillrim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACCENT2}" stop-opacity="0.5"/><stop offset="0.5" stop-color="{ACCENT}" stop-opacity="0.22"/><stop offset="1" stop-color="{VIO}" stop-opacity="0.42"/></linearGradient>
    <clipPath id="pillclip"><rect width="524" height="32" rx="16"/></clipPath>
    <linearGradient id="glint" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.08"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
    <radialGradient id="hmglow" cx="0.5" cy="0.46" r="0.5"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.28"/><stop offset="0.6" stop-color="{ACCENT}" stop-opacity="0.08"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
    <filter id="msoft" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="asoft" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="24"/></filter>
    <filter id="psoft" x="-80%" y="-80%" width="260%" height="260%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="1.4"/></filter>
    <filter id="sblur" x="-40%" y="-40%" width="180%" height="180%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0.6"/></filter>
    <filter id="nodeglow" x="-300%" y="-300%" width="700%" height="700%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="hgrain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0.36  0 0 0 0 0.82  0 0 0 0 0.94  0 0 0 0.05 0"/></filter>
    <clipPath id="kclip"><rect x="90" y="74" width="380" height="30"><animate attributeName="width" values="0;380" dur="0.9s" begin="0.05s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/></rect></clipPath>
  </defs>

  <rect width="1200" height="300" fill="url(#bg)"/>
  <ellipse cx="300" cy="80" rx="270" ry="95" fill="url(#aurA)" filter="url(#asoft)"><animateTransform attributeName="transform" type="translate" values="0 0;60 14;0 0" dur="16s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></ellipse>
  <ellipse cx="640" cy="215" rx="300" ry="100" fill="url(#aurB)" filter="url(#asoft)"><animateTransform attributeName="transform" type="translate" values="0 0;-70 -12;0 0" dur="21s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></ellipse>
  <ellipse cx="920" cy="70" rx="320" ry="105" fill="url(#aurV)" filter="url(#asoft)"><animateTransform attributeName="transform" type="translate" values="0 0;-40 16;0 0" dur="24s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></ellipse>
  <ellipse cx="560" cy="120" rx="230" ry="62" fill="url(#aurV2)" filter="url(#asoft)" transform="rotate(-9 560 120)"><animateTransform attributeName="transform" type="translate" values="0 0;55 -12;0 0" additive="sum" dur="19s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></ellipse>
  <rect width="1200" height="300" fill="url(#glow)"/>
  <rect width="1200" height="300" fill="url(#vglow)"/>

  {far_layer}
  {mid_layer}
  {clusters}
  {planet}
  {constellation}
  {near_layer}
  {flares}
  {shoot}

  <rect width="1200" height="300" fill="url(#vig)"/>
  <rect width="1200" height="300" fill="#000" opacity="0.7" filter="url(#hgrain)"/>

  <line x1="62" y1="78" x2="62" y2="250" stroke="{ACCENT}" stroke-opacity="0.13" stroke-width="1"/>
  <text x="92" y="96" font-family="{MONO}" font-size="15" letter-spacing="6" fill="{MUTED}" clip-path="url(#kclip)">AWS &#183; SERVERLESS &#183; GENAI</text>

  <g>{wm}</g>
  <rect x="-340" y="-40" width="240" height="380" fill="url(#glint)" transform="skewX(-18)"><animate attributeName="x" values="-340;1560;1560" keyTimes="0;0.11;1" dur="12s" begin="1.8s" repeatCount="indefinite"/></rect>

  {underline}

  <g><g>{_rise(0.42, 12)}<text x="94" y="244" font-family="{JP}" font-size="22" letter-spacing="1" fill="{MUTED}">クラウドエンジニア <tspan fill="#30363D">/</tspan> Qiita ライター</text></g></g>

  <g transform="translate(92,258)"><g>{_rise(0.52, 10)}
    <rect width="524" height="32" rx="16" fill="url(#pillglass)"/>
    <g clip-path="url(#pillclip)"><rect x="-150" y="-6" width="95" height="44" fill="#FFFFFF" opacity="0.05" transform="skewX(-18)"><animate attributeName="x" values="-150;640;640" keyTimes="0;0.13;1" dur="9s" begin="2.2s" repeatCount="indefinite"/></rect></g>
    <rect x="1.5" y="1.5" width="521" height="13" rx="12" fill="#FFFFFF" opacity="0.06"/>
    <rect width="524" height="32" rx="16" fill="none" stroke="url(#pillrim)" stroke-width="1"/>
    <circle cx="19" cy="16" r="3.6" fill="{ACCENT2}" filter="url(#nodeglow)"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/><animate attributeName="r" values="3.4;4.7;3.4" dur="2s" repeatCount="indefinite"/></circle>
    <text x="36" y="21" font-family="{JP}" font-size="13" fill="#CDDBE8">いま構築中 <tspan fill="{ACCENT2}" font-family="{MONO}">:</tspan> CloudFormation × AWS Code シリーズの CI/CD パイプライン</text>
  </g></g>

  {mascot_scene}

  <text x="1168" y="286" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}" opacity="0.5">TOKYO &#183; 35.68&#176;N 139.76&#176;E</text>
</svg>'''
    with open(os.path.join(ASSETS,"header.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("header.svg", os.path.getsize(os.path.join(ASSETS,"header.svg")), "B")

# ============================================================ ROLES
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
  <rect x="22" y="13" width="3" height="20" fill="{ACCENT}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
  {items}
</svg>'''
    with open(os.path.join(ASSETS,"roles.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("roles.svg", os.path.getsize(os.path.join(ASSETS,"roles.svg")), "B")

# ============================================================ FOOTER
def build_footer():
    mascot = b64("mascot.png")
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 116" width="1200" height="116" role="img" aria-label="footer">
  <defs>
    <linearGradient id="fd" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="0.5" stop-color="{ACCENT}" stop-opacity="0.5"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>
    <linearGradient id="fs" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{ACCENT2}" stop-opacity="0"/><stop offset="0.5" stop-color="{ACCENT2}" stop-opacity="0.9"/><stop offset="1" stop-color="{ACCENT2}" stop-opacity="0"/></linearGradient>
  </defs>
  <rect x="0" y="10" width="1200" height="1.4" fill="url(#fd)"/>
  <rect x="-260" y="9.4" width="260" height="2.6" rx="1.3" fill="url(#fs)"><animate attributeName="x" values="-260;1200;1200" keyTimes="0;0.35;1" dur="8s" begin="5s" repeatCount="indefinite"/></rect>
  <image x="578" y="22" width="44" height="44" href="data:image/png;base64,{mascot}" preserveAspectRatio="xMidYMid meet"><animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="3.8s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></image>
  <text x="600" y="90" text-anchor="middle" font-family="{JP}" font-size="14" fill="{MUTED}">このプロフィールのビジュアルは、すべて自作の SVG でできています</text>
  <text x="1188" y="108" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="2" fill="#57606A">DESIGNED &amp; BUILT BY MIRUKY</text>
</svg>'''
    with open(os.path.join(ASSETS,"footer.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("footer.svg", os.path.getsize(os.path.join(ASSETS,"footer.svg")), "B")

# ============================================================ SECTIONS（ランナー型見出し）
SECTIONS=[("01","自己紹介","section-about.svg"),("02","Qiita","section-qiita.svg"),
          ("03","保有資格","section-certifications.svg"),("04","技術スタック","section-stack.svg"),
          ("05","GitHub","section-github.svg"),("06","リンク","section-links.svg")]

def build_sections():
    for i,(num,title,fname) in enumerate(SECTIONS):
        title_w = sum(30 if ord(c)>0x2E7F else 17 for c in title)
        lx = 92 + title_w + 26
        lw = 1160 - lx
        gb = 2.5 + i*1.8
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 76" width="1200" height="76" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="sline" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.55"/><stop offset="0.55" stop-color="{VIO}" stop-opacity="0.30"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/></linearGradient>
    <linearGradient id="sglint" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACCENT2}" stop-opacity="0"/><stop offset="0.5" stop-color="{ACCENT2}" stop-opacity="0.9"/><stop offset="1" stop-color="{ACCENT2}" stop-opacity="0"/></linearGradient>
    <clipPath id="sclip"><rect x="{lx}" y="41" width="{lw}" height="6"/></clipPath>
  </defs>
  <text x="24" y="58" font-family="{MONO}" font-size="50" font-weight="700" letter-spacing="2" fill="{ACCENT}" opacity="0.17">{num}</text>
  <text x="92" y="52" font-family="{JP}" font-size="26" font-weight="700" letter-spacing="4" fill="{TEXT}">{title}</text>
  <rect x="{lx}" y="43" width="{lw}" height="1.3" fill="url(#sline)"><animate attributeName="width" values="0;{lw}" dur="0.9s" begin="0.15s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/></rect>
  <g clip-path="url(#sclip)"><rect x="{lx-140}" y="42.4" width="140" height="2.6" fill="url(#sglint)"><animate attributeName="x" values="{lx-140};1180;1180" keyTimes="0;0.14;1" dur="12s" begin="{gb}s" repeatCount="indefinite"/></rect></g>
  <g transform="translate({lx-14},43.5)"><path d="M0 -4 L0.9 -0.9 L4 0 L0.9 0.9 L0 4 L-0.9 0.9 L-4 0 L-0.9 -0.9 Z" fill="{ACCENT2}" opacity="0.8"><animate attributeName="opacity" values="0.5;1;0.5" dur="3.4s" begin="{0.4+i*0.5:.1f}s" repeatCount="indefinite"/></path></g>
  <g opacity="0.65">
    <line x1="1120" y1="30" x2="1148" y2="44" stroke="{STAR}" stroke-opacity="0.25" stroke-width="0.7"/>
    <line x1="1148" y1="44" x2="1170" y2="26" stroke="{STAR}" stroke-opacity="0.25" stroke-width="0.7"/>
    <circle cx="1120" cy="30" r="1.2" fill="{STAR}" opacity="0.5"/>
    <circle cx="1148" cy="44" r="1.6" fill="{ACCENT2}" opacity="0.7"><animate attributeName="opacity" values="0.4;0.9;0.4" dur="{3.2+i*0.4:.1f}s" begin="{i*0.7:.1f}s" repeatCount="indefinite"/></circle>
    <circle cx="1170" cy="26" r="1.1" fill="{VIO_LT}" opacity="0.55"/>
  </g>
</svg>'''
        with open(os.path.join(ASSETS,fname),"w",encoding="utf-8") as f: f.write(svg)
    print("sections:", len(SECTIONS), "runner headers")

if __name__=="__main__":
    build_header(); build_roles(); build_footer(); build_sections()
