#!/usr/bin/env python3
"""保有資格の自作バッジ 5 種を生成する（同一デザイン・色違いの透け感グラスピル）。
- AWS 全冠: 紺 / 応用情報(AP): 緑 / ネットワークスペシャリスト(NW): 紫 /
  セキュリティスペシャリスト(SC): 濃い青 / LPIC-3: 赤
制約: camo 安全（SMIL のみ）。glint は pass-and-rest で全バッジ時差発火。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

TEXT="#E9F1FA"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"

I_MEDAL='<circle cx="8" cy="6" r="4"/><path d="M5.6 9.4 L4.4 14 L8 12 L11.6 14 L10.4 9.4"/>'

def tw(s, jp_w, lat_w):
    return sum(jp_w if ord(c) > 0x2E7F else lat_w for c in s)

def badge(fname, idp, accent, light, label, tag, tag_is_jp, glint_begin, glint_dur):
    H=44; PAD_L=16; ICON=16; GAP=10; PAD_R=14
    label_w = tw(label, 14, 8.6)
    tag_txt_w = tw(tag, 12, 6.8)
    tag_w = int(tag_txt_w + 20)
    W = int(PAD_L + ICON + GAP + label_w + GAP + tag_w + PAD_R)
    lx = PAD_L + ICON + GAP
    tx = lx + label_w + GAP
    tag_font = JP if tag_is_jp else MONO
    gx_end = W + 80

    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label} {tag}">
<defs>
  <linearGradient id="{idp}g" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="{accent}" stop-opacity="0.22"/><stop offset="1" stop-color="{accent}" stop-opacity="0.06"/>
  </linearGradient>
  <linearGradient id="{idp}r" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{light}" stop-opacity="0.55"/><stop offset="0.5" stop-color="{accent}" stop-opacity="0.20"/><stop offset="1" stop-color="#050A14" stop-opacity="0.12"/>
  </linearGradient>
  <linearGradient id="{idp}gl" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.12"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <filter id="{idp}d" x="-30%" y="-40%" width="160%" height="200%" color-interpolation-filters="sRGB">
    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#050A14" flood-opacity="0.45"/>
  </filter>
  <clipPath id="{idp}c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21"/></clipPath>
</defs>
<g filter="url(#{idp}d)">
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21" fill="url(#{idp}g)"/>
  <rect x="2" y="2" width="{W-4}" height="16" rx="14" fill="#FFFFFF" opacity="0.07"/>
  <g clip-path="url(#{idp}c)">
    <rect x="-120" y="-10" width="90" height="64" fill="url(#{idp}gl)" transform="skewX(-18)">
      <animate attributeName="x" values="-120;{gx_end};{gx_end}" keyTimes="0;0.10;1" dur="{glint_dur}s" begin="{glint_begin}s" repeatCount="indefinite"/>
    </rect>
  </g>
  <g transform="translate({PAD_L},{H//2-8})" fill="none" stroke="{light}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{I_MEDAL}</g>
  <text x="{lx}" y="{H//2+5}" font-family="{JP}" font-size="14" font-weight="600" fill="{TEXT}">{label}</text>
  <rect x="{tx}" y="{H//2-11}" width="{tag_w}" height="22" rx="11" fill="{accent}" fill-opacity="0.24" stroke="{accent}" stroke-opacity="0.4" stroke-width="1"/>
  <text x="{tx+tag_w/2:.0f}" y="{H//2+4}" text-anchor="middle" font-family="{tag_font}" font-size="11" font-weight="600" fill="{light}">{tag}</text>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21" fill="none" stroke="url(#{idp}r)" stroke-width="1.2"/>
</g>
</svg>'''
    path=os.path.join(ASSETS, fname)
    with open(path,"w",encoding="utf-8") as f: f.write(svg)
    print(f"{fname}  {W}x{H}  {os.path.getsize(path)}B")

BADGES=[
    # (file, idp, accent, light, label, tag, tag_is_jp, begin, dur)
    ("cert-aws.svg",  "ca", "#3B5BA5", "#AEC4F0", "AWS 認定",            "全冠",    True,  2.0, 13),
    ("cert-ap.svg",   "cp", "#3CB061", "#A9E8BD", "応用情報技術者",       "AP",     False, 4.6, 13),
    ("cert-nw.svg",   "cn", "#8B5CF6", "#D0BDFB", "ネットワークスペシャリスト", "NW", False, 7.2, 13),
    ("cert-sc.svg",   "cs", "#1D6FD6", "#9AC7F5", "セキュリティスペシャリスト", "SC", False, 9.8, 13),
    ("cert-lpic.svg", "cl", "#D64545", "#F5A7A0", "LPIC",               "Level 3", False, 12.4, 13),
]

if __name__=="__main__":
    for b in BADGES:
        badge(*b)
