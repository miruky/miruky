#!/usr/bin/env python3
"""ボタニカル背景レイヤー（緑テーマのカード用）。
ツタ（ベジェ曲線・ロード時に伸びる）＋葉（そよ風で揺れる）＋巻きひげ＋舞う胞子＋新緑グロー。
Qiita カード / Latest Articles カードのトレイ・クリップ群の中に敷いて、
半透明ガラス越しに透けて見える「木々・ツタが這う」表現にする。camo 安全（SMIL のみ）。
"""
import math

VINE="#4E9E2E"; VEIN="#2E5A18"; SPORE="#A9E86B"

def _bez(p0, p1, p2, p3, t):
    mt = 1 - t
    x = mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0]
    y = mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]
    return x, y

def _ang(p0, p1, p2, p3, t):
    mt = 1 - t
    dx = 3*mt*mt*(p1[0]-p0[0]) + 6*mt*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*mt*mt*(p1[1]-p0[1]) + 6*mt*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return math.degrees(math.atan2(dy, dx))

def _leaf(px, py, ang, L, grad_id, op, i):
    W = L*0.44
    d = f"M0 0 Q {L*0.42:.1f} {-W:.1f} {L:.1f} 0 Q {L*0.42:.1f} {W:.1f} 0 0 Z"
    dur = 4.6 + (i % 4)*0.8
    beg = (i % 5)*0.55
    return (f'<g transform="translate({px:.1f},{py:.1f}) rotate({ang:.1f})">'
            f'<g opacity="{op:.2f}">'
            f'<path d="{d}" fill="url(#{grad_id})"/>'
            f'<path d="M1 0 L {L*0.92:.1f} 0" stroke="{VEIN}" stroke-opacity="0.55" stroke-width="0.6"/>'
            f'<animateTransform attributeName="transform" type="rotate" values="-2.6;2.6;-2.6" '
            f'dur="{dur}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" '
            f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>'
            f'</g></g>')

def _tendril(px, py, ang, s, op):
    d = (f"M0 0 c {s*0.5:.1f} {-s*0.7:.1f} {s*1.4:.1f} {-s*0.5:.1f} {s*1.4:.1f} {s*0.3:.1f} "
         f"c 0 {s*0.7:.1f} {-s*0.9:.1f} {s*0.85:.1f} {-s*1.05:.1f} {s*0.15:.1f} "
         f"c {-s*0.12:.1f} {-s*0.4:.1f} {s*0.4:.1f} {-s*0.5:.1f} {s*0.55:.1f} {-s*0.12:.1f}")
    return (f'<g transform="translate({px:.1f},{py:.1f}) rotate({ang:.1f})">'
            f'<path d="{d}" fill="none" stroke="{VINE}" stroke-opacity="{op:.2f}" '
            f'stroke-width="1.3" stroke-linecap="round"/></g>')

def _vine(pts, grad_id, stroke_op, leaf_op, sizes, ts, grow_beg, k):
    p = f"M{pts[0][0]:.1f} {pts[0][1]:.1f} C {pts[1][0]:.1f} {pts[1][1]:.1f} {pts[2][0]:.1f} {pts[2][1]:.1f} {pts[3][0]:.1f} {pts[3][1]:.1f}"
    out = (f'<path d="{p}" fill="none" stroke="{VINE}" stroke-opacity="{stroke_op:.2f}" '
           f'stroke-width="2" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0">'
           f'<animate attributeName="stroke-dashoffset" values="100;0" dur="1.7s" begin="{grow_beg:.1f}s" '
           f'fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/></path>')
    for j, t in enumerate(ts):
        x, y = _bez(*pts, t)
        a = _ang(*pts, t)
        side = 60 if j % 2 == 0 else -60
        L = sizes[j % len(sizes)]
        out += _leaf(x, y, a + side, L, grad_id, leaf_op, k*7 + j)
        # 対になる小葉（房感を出す）
        out += _leaf(x, y, a - side*0.62, L*0.62, grad_id, leaf_op*0.9, k*7 + j + 50)
    ex, ey = pts[3]
    out += _tendril(ex, ey, _ang(*pts, 1.0), 7, min(0.9, stroke_op*1.5))
    return out

# ---- vine layouts per card ----
_VINES = {
    "qiita": [
        [(-24, 30), (150, 4), (330, 54), (286, 170)],
        [(884, 16), (756, 44), (852, 150), (812, 286)],
        [(-16, 414), (120, 352), (52, 244), (196, 206)],
        [(392, 416), (556, 384), (704, 416), (846, 352)],
        [(602, -16), (602, 42), (556, 92), (602, 158)],
    ],
    "articles": [
        [(-24, 22), (150, 2), (300, 44), (252, 122)],
        [(884, 12), (770, 30), (846, 108), (812, 196)],
        [(120, 246), (330, 214), (560, 246), (820, 206)],
    ],
}
_SPORES = {
    "qiita": [(120, 11, 0.0, 1.6), (250, 13, 1.4, 1.2), (360, 10, 0.7, 1.4), (520, 14, 3.1, 1.7),
              (610, 12, 2.2, 1.3), (700, 15, 0.4, 1.1), (780, 12, 4.0, 1.5), (170, 12, 5.2, 1.2),
              (450, 13, 2.8, 1.4), (830, 11, 3.6, 1.3)],
    "articles": [(140, 11, 0.4, 1.4), (300, 13, 2.0, 1.2), (470, 12, 1.1, 1.4),
                 (600, 14, 3.2, 1.6), (720, 12, 0.8, 1.2), (200, 12, 4.1, 1.3)],
}

def botanical(idp, variant):
    """(defs_inner, layer_svg) を返す。defs は <defs> 内に、layer は clip 群の中に置く。"""
    h = 400 if variant == "qiita" else 236
    sizes = [17, 15, 12, 10, 9] if variant == "qiita" else [13, 11.5, 10, 8.5]
    ts = [0.2, 0.38, 0.56, 0.72, 0.88] if variant == "qiita" else [0.24, 0.46, 0.68, 0.86]
    stroke_op = 0.17
    leaf_op = 0.19

    defs = (f'<linearGradient id="{idp}leaf" x1="0" y1="0" x2="0.2" y2="1">'
            f'<stop offset="0" stop-color="#9CEC63"/><stop offset="0.55" stop-color="#5FA83A"/>'
            f'<stop offset="1" stop-color="#356E1F"/></linearGradient>'
            f'<radialGradient id="{idp}fg" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="#55C500" stop-opacity="0.22"/><stop offset="1" stop-color="#55C500" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{idp}fg2" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="#8FE04D" stop-opacity="0.16"/><stop offset="1" stop-color="#8FE04D" stop-opacity="0"/></radialGradient>'
            f'<filter id="{idp}fs" x="-70%" y="-70%" width="240%" height="240%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="26"/></filter>'
            f'<filter id="{idp}dapple" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="2" seed="11" stitchTiles="stitch" result="n"/>'
            f'<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.33  0 0 0 0 0.66  0 0 0 0 0.15  0 0 0 0.5 -0.34"/></filter>')

    # 新緑グロー（隅）＋ 木漏れ日ダップル
    layer = (f'<circle cx="70" cy="{h-40}" r="150" fill="url(#{idp}fg)" filter="url(#{idp}fs)"/>'
             f'<circle cx="800" cy="30" r="140" fill="url(#{idp}fg2)" filter="url(#{idp}fs)"/>'
             f'<rect x="2" y="2" width="856" height="{h-4}" filter="url(#{idp}dapple)" opacity="0.5"/>')
    # ツタ＋葉＋巻きひげ
    for k, pts in enumerate(_VINES[variant]):
        layer += _vine(pts, f"{idp}leaf", stroke_op, leaf_op, sizes, ts, 0.2 + k*0.35, k)
    # 舞う胞子
    for i, (x, dur, beg, r) in enumerate(_SPORES[variant]):
        layer += (f'<circle cx="{x}" cy="{h//2}" r="{r}" fill="{SPORE}" opacity="0">'
                  f'<animate attributeName="cy" values="{h+12};-12" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="0;0.42;0.42;0" keyTimes="0;0.16;0.7;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="cx" values="{x};{x+8};{x-6};{x}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></circle>')
    return defs, layer
