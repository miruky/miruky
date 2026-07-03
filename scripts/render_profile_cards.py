#!/usr/bin/env python3
"""自己紹介カード（assets/about-card.svg）と技術スタックカード（assets/stack-card.svg）を生成する。
素の Markdown テーブルを、他カードと同じ「水色グラス素材」の自作 SVG に置き換えるためのもの。
制約: camo 安全（SMIL のみ）。静的レンダラでも破綻しないよう基準値=完成形。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stack_icons import STACK_ICONS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# 技術スタックカード背景に、AWSサービス公式アイコンを透明度高めで散布する
_SCATTER = [
    ("AWS",770,110,66,-10,0.065),("Lambda",624,112,40,12,0.06),("DynamoDB",726,300,50,-8,0.06),
    ("S3",506,142,36,14,0.055),("EC2",822,206,46,-14,0.06),("RDS",560,300,40,10,0.055),
    ("SQS",470,196,34,-10,0.05),("CloudWatch",644,196,38,16,0.055),("Bedrock",762,250,44,-6,0.06),
    ("SageMaker",690,150,34,-16,0.05),("CodePipeline",504,388,40,8,0.055),("CodeBuild",624,388,36,-12,0.05),
    ("ECS",830,338,44,18,0.06),("Connect",300,392,38,-10,0.05),("CloudFormation",150,396,34,12,0.048),
    ("SAM",402,340,32,-8,0.05),("Comprehend",832,58,30,10,0.05),("Lex",560,244,30,-14,0.05),
    ("CDK",720,390,34,6,0.05),("CodeDeploy",250,300,30,-12,0.045),
]

def stack_scatter(color, clip):
    out = ""
    for name, cx, cy, size, rot, op in _SCATTER:
        vb, inner = STACK_ICONS[name]
        s = size/vb
        op = min(0.10, op*1.45)
        out += (f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s:.3f}) translate({-vb/2:.1f},{-vb/2:.1f})" '
                f'fill="{color}" opacity="{op:.3f}">{inner.replace("white", color)}</g>')
    return f'<g clip-path="url(#{clip})">{out}</g>'

# ---- palette: water-blue glass（システム色） ----
BASE_C="#0D141C"; BASE_E="#0A0E14"
ACC="#5CD1F0"; ACC_LT="#A8ECFF"; DEEP="#3AA0E0"
TEXT="#E6F4FA"; MUTED="#7D93A0"; SUB="#9FC2D3"; SHADOW="#04121C"
SANS="'Segoe UI',-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic','Noto Sans JP',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
JP="'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans JP','Meiryo',sans-serif"

def defs(idp, h, w=860):
    return f'''<defs>
  <radialGradient id="{idp}tray" cx="0.5" cy="0.25" r="0.95">
    <stop offset="0" stop-color="{BASE_C}"/><stop offset="1" stop-color="{BASE_E}"/>
  </radialGradient>
  <linearGradient id="{idp}glass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.10"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.03"/>
  </linearGradient>
  <linearGradient id="{idp}rim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#DDF6FF" stop-opacity="0.45"/><stop offset="0.5" stop-color="{ACC}" stop-opacity="0.16"/><stop offset="1" stop-color="{SHADOW}" stop-opacity="0.10"/>
  </linearGradient>
  <linearGradient id="{idp}sheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.07"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="{idp}orb" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.20"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="{idp}glint" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.09"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <filter id="{idp}soft" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="{idp}grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.36  0 0 0 0 0.82  0 0 0 0 0.94  0 0 0 0.05 0"/>
  </filter>
  <clipPath id="{idp}round"><rect x="2" y="2" width="{w-4}" height="{h-4}" rx="20"/></clipPath>
</defs>'''

def tray(idp, h, w=860, orb='<circle cx="700" cy="40" r="130"/>', sweep_begin=4.5, sweep_dur=11):
    orb_el = orb.replace('/>', f' fill="url(#{idp}orb)" filter="url(#{idp}soft)"/>')
    gx_end = int(w + 0.33*h + 200)
    return f'''<g clip-path="url(#{idp}round)">
  <rect x="2" y="2" width="{w-4}" height="{h-4}" fill="url(#{idp}tray)"/>
  {orb_el}
  <rect x="2" y="2" width="{w-4}" height="{h-4}" fill="url(#{idp}glass)"/>
  <rect x="2" y="2" width="{w-4}" height="60" fill="url(#{idp}sheen)"/>
  <rect x="-300" y="-40" width="240" height="{h+80}" fill="url(#{idp}glint)" transform="skewX(-18)">
    <animate attributeName="x" values="-300;{gx_end};{gx_end}" keyTimes="0;0.11;1" dur="{sweep_dur}s" begin="{sweep_begin}s" repeatCount="indefinite"/>
  </rect>
</g>'''

def frame(idp, h, w=860):
    return (f'<path d="M20 40 L20 20 L40 20" fill="none" stroke="{ACC}" stroke-opacity="0.5" stroke-width="1.5"/>'
            f'<path d="M{w-20} {h-40} L{w-20} {h-20} L{w-40} {h-20}" fill="none" stroke="{ACC}" stroke-opacity="0.5" stroke-width="1.5"/>'
            f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="20" fill="none" stroke="url(#{idp}rim)" stroke-width="1.4"/>'
            f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="20" fill="#000" opacity="0.5" filter="url(#{idp}grain)" clip-path="url(#{idp}round)"/>')

def header(idp, title_en, title_jp, right):
    return (f'<circle cx="38" cy="42" r="5" fill="{ACC}">'
            f'<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
            f'<text x="54" y="48" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">{title_en}</text>'
            f'<text x="{54+len(title_en)*11+16}" y="48" font-family="{JP}" font-size="13" letter-spacing="2" fill="{SUB}">{title_jp}</text>'
            f'<text x="822" y="47" text-anchor="end" font-family="{JP}" font-size="11.5" letter-spacing="1" fill="{MUTED}">{right}</text>'
            f'<line x1="40" y1="64" x2="820" y2="64" stroke="{ACC}" stroke-opacity="0.16" stroke-width="1"/>')

def enter(i, inner):
    # 行のステージ入場（基準=完成形、opacityのみアニメ）
    return (f'<g>{inner}'
            f'<animate attributeName="opacity" values="0;1" dur="0.55s" begin="{0.15+i*0.12:.2f}s" fill="freeze"/></g>')

# ---- 手描き線アイコン（16x16、stroke 1.5） ----
def icon(x, y, body, color=ACC):
    return (f'<g transform="translate({x},{y})" fill="none" stroke="{color}" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{body}</g>')

I_CLOUD='<path d="M4 11 A3 3 0 0 1 4 5 A4.5 4.5 0 0 1 12.5 6 A2.8 2.8 0 0 1 12.5 11 Z"/>'
I_PEN='<path d="M2 14 L2.8 10.8 L11 2.6 L13.4 5 L5.2 13.2 Z"/><path d="M9.8 3.8 L12.2 6.2"/>'
I_SPARK='<path d="M8 1.5 L9.3 6.7 L14.5 8 L9.3 9.3 L8 14.5 L6.7 9.3 L1.5 8 L6.7 6.7 Z" fill="'+ACC+'" fill-opacity="0.18"/>'
I_PIN='<path d="M8 14 C8 14 3 9.5 3 6 A5 5 0 0 1 13 6 C13 9.5 8 14 8 14 Z"/><circle cx="8" cy="6" r="1.8"/>'
I_CHECK=f'<path d="M2 8.5 L6 12 L14 3.5" stroke="{ACC_LT}"/>'
I_SERVER='<rect x="1.5" y="2.5" width="13" height="4.6" rx="1.4"/><rect x="1.5" y="9" width="13" height="4.6" rx="1.4"/><circle cx="4.4" cy="4.8" r="0.9" fill="'+ACC+'" stroke="none"/><circle cx="4.4" cy="11.3" r="0.9" fill="'+ACC+'" stroke="none"/>'
I_DB='<ellipse cx="8" cy="3.6" rx="6" ry="2.3"/><path d="M2 3.6 V12.4 A6 2.3 0 0 0 14 12.4 V3.6"/><path d="M2 8 A6 2.3 0 0 0 14 8"/>'
I_MSG='<path d="M1.8 4 L14.2 4 L14.2 12 L1.8 12 Z"/><path d="M2.2 4.6 L8 9 L13.8 4.6"/>'
I_LAYERS='<path d="M8 1.8 L14.5 5.4 L8 9 L1.5 5.4 Z"/><path d="M2.8 8.2 L8 11.2 L13.2 8.2"/><path d="M4.2 11 L8 13.4 L11.8 11"/>'
I_CYCLE='<path d="M12.8 5 A5.6 5.6 0 0 0 3 5.6"/><path d="M3 2.6 L3 5.8 L6.2 5.8"/><path d="M3.2 11 A5.6 5.6 0 0 0 13 10.4"/><path d="M13 13.4 L13 10.2 L9.8 10.2"/>'
I_CODE='<path d="M5.5 4 L1.8 8 L5.5 12"/><path d="M10.5 4 L14.2 8 L10.5 12"/><path d="M9 2.5 L7 13.5"/>'
I_MEDAL='<circle cx="8" cy="6" r="4"/><path d="M5.6 9.4 L4.4 14 L8 12 L11.6 14 L10.4 9.4"/>'

# ============================================================ ABOUT CARD（コズミック・バイオレット）
VIO="#8A7DD8"; VIO_LT="#C9BEF5"; VIO_DP="#6B5CB7"; STARC="#DDE8FF"
I_CHECK_V='<path d="M2 8.5 L6 12 L14 3.5" stroke="#C9BEF5"/>'

def build_about():
    H=316
    rows=[
        ("業務","WORK",I_CLOUD,ACC,"AWS を用いたクラウドインフラの設計・構築 〜 運用・保守"),
        ("発信","WRITING",I_PEN,ACC,"Qiita で AWS・AI・セキュリティを中心に技術記事を連載"),
        ("関心","FOCUS",I_SPARK,"#B9A8F5","CloudFormation と AWS Code シリーズを使った CI/CD パイプライン構築"),
    ]
    body=""
    for i,(jp,en,ic,col,desc) in enumerate(rows):
        y=108+i*66
        inner=(f'<rect x="32" y="{y-22}" width="36" height="36" rx="10" fill="url(#abibox)" stroke="url(#abiboxr)" stroke-width="1"/>'
               + icon(42, y-12, ic, col) +
               f'<text x="86" y="{y-6}" font-family="{JP}" font-size="15" font-weight="700" fill="{TEXT}">{jp}</text>'
               f'<text x="122" y="{y-7}" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}">{en}</text>'
               f'<text x="86" y="{y+16}" font-family="{JP}" font-size="13.5" fill="{SUB}">{desc}</text>')
        body+=enter(i, inner)
        if i<2:
            body+=f'<line x1="32" y1="{y+32}" x2="540" y2="{y+32}" stroke="{VIO}" stroke-opacity="0.12" stroke-width="1"/>'

    # 右パネル: 要点（バイオレット・グラス）
    facts=[
        (I_PIN, "東京（Tokyo）を拠点に活動"),
        (I_MEDAL, "AWS 認定 全冠"),
        (I_CHECK_V, "IPA : AP ・ NW ・ SC"),
        (I_CHECK_V, "LPIC Level 3"),
    ]
    panel=(f'<rect x="572" y="86" width="260" height="200" rx="14" fill="url(#abpanel)" stroke="url(#abprim)" stroke-width="1"/>'
           f'<rect x="573" y="87" width="258" height="26" rx="13" fill="#FFFFFF" opacity="0.05"/>'
           f'<text x="592" y="116" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{VIO_LT}">PROFILE</text>'
           f'<text x="666" y="116" font-family="{JP}" font-size="11" letter-spacing="2" fill="{MUTED}">要点</text>')
    for j,(ic,txt) in enumerate(facts):
        fy=148+j*34
        panel+=(icon(592, fy-12, ic, VIO_LT) +
                f'<text x="618" y="{fy}" font-family="{JP}" font-size="13" fill="{TEXT}">{txt}</text>')
        if j<3:
            panel+=f'<line x1="592" y1="{fy+16}" x2="812" y2="{fy+16}" stroke="{VIO}" stroke-opacity="0.12" stroke-width="1"/>'
    body+=enter(3, panel)

    # ---- 宇宙レイヤ（星・きらめき・流れ星・環つき惑星） ----
    stars=""
    for x,y,op,r in [(300,26,0.4,0.9),(420,40,0.3,0.7),(500,22,0.45,1.0),(640,34,0.35,0.8),(760,24,0.4,1.0),
                     (240,52,0.25,0.7),(552,120,0.3,0.8),(556,186,0.25,0.7),(550,246,0.3,0.8),
                     (620,300,0.3,0.8),(760,302,0.35,0.9),(200,300,0.25,0.7),(844,150,0.3,0.8),(846,224,0.25,0.7)]:
        stars+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STARC}" opacity="{op}"/>'
    for x,y,c,dur,beg in [(350,40,ACC_LT,4.2,0.5),(700,52,VIO_LT,3.6,1.3),(556,206,"#FFFFFF",5.0,2.1),(250,296,VIO_LT,4.6,2.9)]:
        stars+=(f'<g transform="translate({x},{y})">'
                f'<path d="M0 -3 L0.7 -0.7 L3 0 L0.7 0.7 L0 3 L-0.7 0.7 L-3 0 L-0.7 -0.7 Z" fill="{c}" opacity="0.5">'
                f'<animate attributeName="opacity" values="0.2;1;0.4;0.2" keyTimes="0;0.2;0.5;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                f'</path></g>')
    stars+=(f'<line x1="600" y1="24" x2="644" y2="38" stroke="url(#abshoot)" stroke-width="1.2" stroke-linecap="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;0.9;0" keyTimes="0;0.02;0.06;0.12" dur="16s" begin="7s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="-26 -9;60 22;60 22" keyTimes="0;0.12;1" dur="16s" begin="7s" repeatCount="indefinite"/></line>')
    stars+=(f'<g transform="translate(76,282)">'
            f'<circle r="9" fill="url(#abplanet)"/>'
            f'<circle cx="-3" cy="-3.4" r="2.6" fill="#FFFFFF" opacity="0.35" filter="url(#absoft2)"/>'
            f'<ellipse rx="16.5" ry="5.4" fill="none" stroke="#9FB0E8" stroke-opacity="0.5" stroke-width="1" transform="rotate(-14)"/>'
            f'<g transform="rotate(-14)"><circle cx="16.5" cy="0" r="1.4" fill="#CFE0FF">'
            f'<animateMotion dur="22s" repeatCount="indefinite" path="M0 0 a16.5 5.4 0 1 1 0 0.1 Z"/></circle></g></g>')

    gx=int(860+0.33*H+200)
    tray_c=(f'<g clip-path="url(#abround)">'
            f'<rect x="2" y="2" width="856" height="{H-4}" fill="url(#abtray)"/>'
            f'<circle cx="170" cy="50" r="150" fill="url(#aborbC)" filter="url(#absoft)"/>'
            f'<circle cx="760" cy="70" r="160" fill="url(#aborbV)" filter="url(#absoft)"/>'
            f'<circle cx="430" cy="310" r="150" fill="url(#aborbV2)" filter="url(#absoft)"/>'
            f'<rect x="2" y="2" width="856" height="{H-4}" filter="url(#abdust)" opacity="0.4"/>'
            f'<rect x="2" y="2" width="856" height="{H-4}" fill="url(#abglass)"/>'
            f'<rect x="2" y="2" width="856" height="60" fill="url(#absheen)"/>'
            f'{stars}'
            f'<rect x="-300" y="-40" width="240" height="{H+80}" fill="url(#abglint)" transform="skewX(-18)">'
            f'<animate attributeName="x" values="-300;{gx};{gx}" keyTimes="0;0.11;1" dur="11s" begin="4.5s" repeatCount="indefinite"/></rect>'
            f'</g>')

    defs_c=f'''<defs>
  <radialGradient id="abtray" cx="0.5" cy="0.22" r="1.0">
    <stop offset="0" stop-color="#121631"/><stop offset="1" stop-color="#090C18"/>
  </radialGradient>
  <linearGradient id="abglass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.07"/><stop offset="1" stop-color="{VIO}" stop-opacity="0.05"/>
  </linearGradient>
  <linearGradient id="abrim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#DDF6FF" stop-opacity="0.5"/><stop offset="0.5" stop-color="{VIO}" stop-opacity="0.28"/><stop offset="1" stop-color="#0A0620" stop-opacity="0.12"/>
  </linearGradient>
  <linearGradient id="absheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.07"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="aborbC" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.18"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="aborbV" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{VIO}" stop-opacity="0.24"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="aborbV2" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{VIO_DP}" stop-opacity="0.14"/><stop offset="1" stop-color="{VIO_DP}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="abglint" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.09"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="abibox" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.13"/><stop offset="1" stop-color="{VIO}" stop-opacity="0.12"/>
  </linearGradient>
  <linearGradient id="abiboxr" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.4"/><stop offset="1" stop-color="{VIO}" stop-opacity="0.42"/>
  </linearGradient>
  <linearGradient id="abpanel" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="{VIO}" stop-opacity="0.12"/><stop offset="1" stop-color="{VIO}" stop-opacity="0.04"/>
  </linearGradient>
  <linearGradient id="abprim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{VIO_LT}" stop-opacity="0.45"/><stop offset="0.5" stop-color="{VIO}" stop-opacity="0.2"/><stop offset="1" stop-color="#0A0620" stop-opacity="0.1"/>
  </linearGradient>
  <radialGradient id="abplanet" cx="0.36" cy="0.3" r="0.8">
    <stop offset="0" stop-color="#8B93D8"/><stop offset="0.6" stop-color="#3A3F7A"/><stop offset="1" stop-color="#171B3E"/>
  </radialGradient>
  <linearGradient id="abshoot" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.9"/>
  </linearGradient>
  <filter id="absoft" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="absoft2" x="-80%" y="-80%" width="260%" height="260%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="1.6"/></filter>
  <filter id="abdust" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.75  0 0 0 0 0.82  0 0 0 0 1  0 0 0 0.55 -0.47"/>
  </filter>
  <filter id="abgrain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.6  0 0 0 0 0.95  0 0 0 0.05 0"/>
  </filter>
  <clipPath id="abround"><rect x="2" y="2" width="856" height="{H-4}" rx="20"/></clipPath>
</defs>'''

    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 {H}" width="860" height="{H}" role="img" aria-label="自己紹介">'
         + defs_c + tray_c
         + header("ab","About Me","自己紹介","@miruky ・ he/him")
         + body + frame("ab",H) + '</svg>')
    with open(os.path.join(ASSETS,"about-card.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("about-card.svg", os.path.getsize(os.path.join(ASSETS,"about-card.svg")), "B")

# ============================================================ STACK CARD
def build_stack():
    cats=[
        ("COMPUTE","コンピューティング",I_SERVER,["EC2","Lambda","ECS"]),
        ("STORAGE / DB","ストレージ・DB",I_DB,["S3","DynamoDB","RDS"]),
        ("MESSAGING / OBS","メッセージング・監視",I_MSG,["SQS","CloudWatch"]),
        ("IAC","構成管理",I_LAYERS,["Terraform","CloudFormation","CDK","SAM"]),
        ("AI / ML","生成AI・機械学習",I_SPARK,["Bedrock","SageMaker","Comprehend","Lex","Connect"]),
        ("CI / CD","継続的デリバリー",I_CYCLE,["GitHub Actions","CodePipeline","CodeBuild","CodeDeploy"]),
        ("LANGUAGES","言語",I_CODE,["Python","TypeScript","HCL"]),
    ]
    n_tools=sum(len(c[3]) for c in cats)
    H=64+len(cats)*48+30
    body=""
    pulse_idx=0
    for i,(en,jp,ic,tools) in enumerate(cats):
        y=100+i*48
        row = icon(32, y-13, ic)
        row+=(f'<text x="58" y="{y-3}" font-family="{MONO}" font-size="10.5" letter-spacing="1.5" fill="{TEXT}">{en}</text>'
              f'<text x="58" y="{y+12}" font-family="{JP}" font-size="9.5" fill="{MUTED}">{jp}</text>')
        # chips
        cx=196
        for t in tools:
            w=int(len(t)*7.0+30)
            pulse=""
            if pulse_idx%5==2:  # 一部のドットだけ静かに鼓動（リズム）
                pulse=f'<animate attributeName="opacity" values="1;0.35;1" dur="{3.0+(pulse_idx%3)*0.7:.1f}s" begin="{pulse_idx*0.4:.1f}s" repeatCount="indefinite"/>'
            row+=(f'<rect x="{cx}" y="{y-16}" width="{w}" height="27" rx="13.5" fill="{ACC}" fill-opacity="0.08" stroke="{ACC}" stroke-opacity="0.26" stroke-width="1"/>'
                  f'<rect x="{cx+1}" y="{y-15}" width="{w-2}" height="11" rx="5.5" fill="#FFFFFF" opacity="0.05"/>'
                  f'<circle cx="{cx+14}" cy="{y-2.5}" r="2.6" fill="{ACC}">{pulse}</circle>'
                  f'<text x="{cx+25}" y="{y+1.5}" font-family="{MONO}" font-size="11.5" fill="#D5E9F2">{t}</text>')
            cx+=w+9
            pulse_idx+=1
        body+=enter(i, row)
        if i<len(cats)-1:
            body+=f'<line x1="28" y1="{y+25}" x2="832" y2="{y+25}" stroke="{ACC}" stroke-opacity="0.07" stroke-width="1"/>'

    # スキャンライン（上→下に走る薄い光）
    scan=(f'<rect x="24" y="-40" width="812" height="18" fill="{ACC}" opacity="0.05" clip-path="url(#stround)">'
          f'<animate attributeName="y" values="70;{H-20};70" dur="9s" begin="1.5s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" keyTimes="0;0.5;1"/></rect>')

    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 {H}" width="860" height="{H}" role="img" aria-label="技術スタック">'
         + defs("st",H) + tray("st",H, orb='<circle cx="720" cy="60" r="150"/>', sweep_begin=8, sweep_dur=11)
         + stack_scatter(ACC, "stround")
         + header("st","Tech Stack","技術スタック",f"{n_tools} TOOLS ・ {len(cats)} CATEGORIES")
         + scan + body + frame("st",H) + '</svg>')
    with open(os.path.join(ASSETS,"stack-card.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("stack-card.svg", os.path.getsize(os.path.join(ASSETS,"stack-card.svg")), "B", "| tools:", n_tools, "| H:", H)

if __name__=="__main__":
    build_about(); build_stack()
