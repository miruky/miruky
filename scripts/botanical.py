#!/usr/bin/env python3
"""ボタニカル背景レイヤー（緑テーマのカード用）。
額縁ツタは「くねくね」蛇行（サイン波 + Catmull-Rom スプライン）、葉は中心を向く。
数本だけ中央へ。小さな木々、舞う胞子、新緑グロー、木漏れ日ダップル。
Qiita は左上/右下のコーナーマークを避けて2隅を開ける。camo 安全（SMIL のみ）。
"""
import math

VINE="#4E9E2E"; VEIN="#2E5A18"; SPORE="#A9E86B"

# ---------- 幾何 ----------
def _bez(p0, p1, p2, p3, t):
    mt = 1 - t
    return (mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0],
            mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1])

def _ang(p0, p1, p2, p3, t):
    mt = 1 - t
    dx = 3*mt*mt*(p1[0]-p0[0]) + 6*mt*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*mt*mt*(p1[1]-p0[1]) + 6*mt*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return math.degrees(math.atan2(dy, dx))

def _inward(x, y, a, cx, cy):
    ca = math.cos(math.radians(a+90)); sa = math.sin(math.radians(a+90))
    return 90 if (ca*(cx-x) + sa*(cy-y)) >= 0 else -90

def _cr_segments(W):
    """Catmull-Rom で通過点 W を滑らかな3次ベジェ列に。"""
    n = len(W); segs = []
    for i in range(n-1):
        p0 = W[i-1] if i > 0 else W[i]
        p1 = W[i]; p2 = W[i+1]
        p3 = W[i+2] if i+2 < n else W[i+1]
        b1 = (p1[0]+(p2[0]-p0[0])/6.0, p1[1]+(p2[1]-p0[1])/6.0)
        b2 = (p2[0]-(p3[0]-p1[0])/6.0, p2[1]-(p3[1]-p1[1])/6.0)
        segs.append((p1, b1, b2, p2))
    return segs

def _path(segs):
    d = f"M{segs[0][0][0]:.1f} {segs[0][0][1]:.1f}"
    for (_, b1, b2, p3) in segs:
        d += f" C {b1[0]:.1f} {b1[1]:.1f} {b2[0]:.1f} {b2[1]:.1f} {p3[0]:.1f} {p3[1]:.1f}"
    return d

def _at(segs, t):
    n = len(segs); ft = max(0.0, min(0.999999, t))*n
    i = int(ft); lt = ft - i
    if i >= n: i, lt = n-1, 1.0
    p0, b1, b2, p3 = segs[i]
    return _bez(p0, b1, b2, p3, lt), _ang(p0, b1, b2, p3, lt)

def _wave(axis, a0, a1, base, amp, waves, phase=0.0):
    """辺に沿って蛇行する通過点列を生成。axis='h'|'v'。"""
    n = int(waves*2) + 2; pts = []
    for i in range(n+1):
        f = i/n
        a = a0 + (a1-a0)*f
        off = amp*math.sin(f*waves*math.pi + phase)
        pts.append((a, base+off) if axis == 'h' else (base+off, a))
    return pts

# ---------- 素材 ----------
def _leaf(px, py, ang, L, grad_id, op, i):
    W = L*0.44
    d = f"M0 0 Q {L*0.42:.1f} {-W:.1f} {L:.1f} 0 Q {L*0.42:.1f} {W:.1f} 0 0 Z"
    dur = 4.6 + (i % 4)*0.8; beg = (i % 5)*0.55
    return (f'<g transform="translate({px:.1f},{py:.1f}) rotate({ang:.1f})">'
            f'<g opacity="{op:.2f}">'
            f'<path d="{d}" fill="url(#{grad_id})"/>'
            f'<path d="M1 0 L {L*0.92:.1f} 0" stroke="{VEIN}" stroke-opacity="0.55" stroke-width="0.6"/>'
            f'<animateTransform attributeName="transform" type="rotate" values="-2.6;2.6;-2.6" '
            f'dur="{dur}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" '
            f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/></g></g>')

def _tendril(px, py, ang, s, op):
    d = (f"M0 0 c {s*0.5:.1f} {-s*0.7:.1f} {s*1.4:.1f} {-s*0.5:.1f} {s*1.4:.1f} {s*0.3:.1f} "
         f"c 0 {s*0.7:.1f} {-s*0.9:.1f} {s*0.85:.1f} {-s*1.05:.1f} {s*0.15:.1f} "
         f"c {-s*0.12:.1f} {-s*0.4:.1f} {s*0.4:.1f} {-s*0.5:.1f} {s*0.55:.1f} {-s*0.12:.1f}")
    return (f'<g transform="translate({px:.1f},{py:.1f}) rotate({ang:.1f})">'
            f'<path d="{d}" fill="none" stroke="{VINE}" stroke-opacity="{op:.2f}" '
            f'stroke-width="1.3" stroke-linecap="round"/></g>')

def _vine(W, grad_id, s_op, l_op, sizes, K, grow_beg, k, cx, cy):
    segs = _cr_segments(W)
    out = (f'<path d="{_path(segs)}" fill="none" stroke="{VINE}" stroke-opacity="{s_op:.2f}" '
           f'stroke-width="2" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0">'
           f'<animate attributeName="stroke-dashoffset" values="100;0" dur="1.8s" begin="{grow_beg:.1f}s" '
           f'fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/></path>')
    for m in range(K):
        t = (m+0.5)/K
        (x, y), a = _at(segs, t)
        s = _inward(x, y, a, cx, cy)
        jit = 15 if m % 2 == 0 else -15
        out += _leaf(x, y, a+s+jit, sizes[m % len(sizes)], grad_id, l_op, k*9+m)
    (ex, ey), ea = _at(segs, 0.999)
    out += _tendril(ex, ey, ea, 7, min(0.9, s_op*1.5))
    return out

def _tree(x, by, h, grad_id, op, i):
    ch = h*0.58; cyc = -h*0.6
    blobs = "".join(f'<circle cx="{dx:.1f}" cy="{cyc+dy:.1f}" r="{r:.1f}"/>' for dx, dy, r in
                    [(0,0,ch*0.5),(-ch*0.36,ch*0.14,ch*0.34),(ch*0.36,ch*0.12,ch*0.35),
                     (-ch*0.14,-ch*0.3,ch*0.3),(ch*0.18,-ch*0.26,ch*0.28)])
    trunk = (f'<path d="M-1.4 0 Q-0.7 {cyc*0.5:.1f} -0.9 {cyc*0.82:.1f} '
             f'L0.9 {cyc*0.82:.1f} Q0.7 {cyc*0.5:.1f} 1.4 0 Z" fill="{VEIN}" fill-opacity="0.6"/>')
    dur = 6 + (i % 3)*0.7; beg = (i % 4)*0.5
    return (f'<g transform="translate({x:.1f},{by:.1f})" opacity="{op:.2f}"><g>'
            f'<animateTransform attributeName="transform" type="rotate" values="-1.1;1.1;-1.1" '
            f'dur="{dur}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" '
            f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>'
            f'{trunk}<g fill="url(#{grad_id})">{blobs}</g></g></g>')

# ---------- レイアウト ----------
# frame: (axis, a0, a1, base, amp, waves)  ／ Qiita は左上(20,20)・右下(840,380)を開ける
_LAYOUT = {
    "qiita": dict(
        cx=430, cy=200,
        frame=[('h', 92, 834, 30, 13, 3.0),     # 上辺（左上ティックを避けて x92 から）
               ('v', 50, 300, 833, 12, 2.5),    # 右辺（右下ティック手前 y300 まで）
               ('h', 766, 30, 372, 13, 3.0),    # 下辺（右下を避け x766→左下）
               ('v', 356, 92, 27, 12, 2.5)],    # 左辺（左下→左上ティック手前 y92 まで）
        inner=[[(118,60),(150,102),(205,120),(232,162),(256,196)],
               [(778,332),(712,312),(668,290),(628,262),(596,236)],
               [(430,26),(446,62),(414,88),(440,120),(432,142)]],
        trees=[(72,388,42),(150,390,56),(240,386,34),(556,390,48),(648,392,40),(738,388,52)],
    ),
    "articles": dict(
        cx=430, cy=118,
        frame=[('h', 28, 834, 22, 11, 3.0),
               ('v', 30, 214, 836, 11, 2.5),
               ('h', 834, 28, 220, 11, 3.0),
               ('v', 214, 24, 26, 11, 2.5)],
        inner=[[(74,42),(126,66),(172,74),(212,100)],
               [(802,206),(732,182),(686,168),(646,148)]],
        trees=[(96,226,34),(196,228,46),(636,226,32),(752,228,42)],
    ),
}
_SPORES = {
    "qiita": [(120,11,0.0,1.6),(250,13,1.4,1.2),(360,10,0.7,1.4),(520,14,3.1,1.7),(610,12,2.2,1.3),
              (700,15,0.4,1.1),(780,12,4.0,1.5),(170,12,5.2,1.2),(450,13,2.8,1.4),(830,11,3.6,1.3)],
    "articles": [(140,11,0.4,1.4),(300,13,2.0,1.2),(470,12,1.1,1.4),(600,14,3.2,1.6),(720,12,0.8,1.2),(200,12,4.1,1.3)],
}

def botanical(idp, variant):
    """(defs_inner, layer_svg) を返す。defs は <defs> 内、layer は clip 群の中へ。"""
    lo = _LAYOUT[variant]; h = 400 if variant == "qiita" else 236
    cx, cy = lo["cx"], lo["cy"]
    sizes = [16, 13, 11, 9] if variant == "qiita" else [13, 11, 9, 8]
    s_op, l_op = 0.16, 0.18
    K_frame = 8; K_inner = 4

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

    layer = (f'<circle cx="70" cy="{h-40}" r="150" fill="url(#{idp}fg)" filter="url(#{idp}fs)"/>'
             f'<circle cx="800" cy="30" r="140" fill="url(#{idp}fg2)" filter="url(#{idp}fs)"/>'
             f'<rect x="2" y="2" width="856" height="{h-4}" filter="url(#{idp}dapple)" opacity="0.5"/>')
    # 額縁ツタ（くねくね）
    for k, (ax, a0, a1, base, amp, wv) in enumerate(lo["frame"]):
        W = _wave(ax, a0, a1, base, amp, wv, phase=0.4*k)
        layer += _vine(W, f"{idp}leaf", s_op, l_op, sizes, K_frame, 0.2+k*0.3, k, cx, cy)
    # 中央へ伸びる数本
    for k, W in enumerate(lo["inner"]):
        layer += _vine(W, f"{idp}leaf", s_op*0.9, l_op*0.92, sizes, K_inner, 0.9+k*0.3, 20+k, cx, cy)
    # 木々
    for i, (x, by, th) in enumerate(lo["trees"]):
        layer += _tree(x, by, th, f"{idp}leaf", 0.12, i)
    # 舞う胞子
    for i, (x, dur, beg, r) in enumerate(_SPORES[variant]):
        layer += (f'<circle cx="{x}" cy="{h//2}" r="{r}" fill="{SPORE}" opacity="0">'
                  f'<animate attributeName="cy" values="{h+12};-12" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="0;0.42;0.42;0" keyTimes="0;0.16;0.7;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="cx" values="{x};{x+8};{x-6};{x}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></circle>')
    return defs, layer
