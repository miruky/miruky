#!/usr/bin/env python3
"""自己紹介カード（assets/about-card.svg）と技術スタックカード（assets/stack-card.svg）を生成する。
素の Markdown テーブルを、他カードと同じ「水色グラス素材」の自作 SVG に置き換えるためのもの。
制約: camo 安全（SMIL のみ）。静的レンダラでも破綻しないよう基準値=完成形。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

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

# ============================================================ ABOUT CARD
def build_about():
    H=316
    rows=[
        ("業務","WORK",I_CLOUD,"AWS を用いたクラウドインフラの設計・構築 〜 運用・保守"),
        ("発信","WRITING",I_PEN,"Qiita で AWS・AI・セキュリティを中心に技術記事を連載"),
        ("関心","FOCUS",I_SPARK,"CloudFormation と AWS Code シリーズを使った CI/CD パイプライン構築"),
    ]
    body=""
    for i,(jp,en,ic,desc) in enumerate(rows):
        y=108+i*66
        inner=(f'<rect x="32" y="{y-22}" width="36" height="36" rx="10" fill="{ACC}" fill-opacity="0.10" stroke="{ACC}" stroke-opacity="0.28" stroke-width="1"/>'
               + icon(42, y-12, ic) +
               f'<text x="86" y="{y-6}" font-family="{JP}" font-size="15" font-weight="700" fill="{TEXT}">{jp}</text>'
               f'<text x="122" y="{y-7}" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}">{en}</text>'
               f'<text x="86" y="{y+16}" font-family="{JP}" font-size="13.5" fill="{SUB}">{desc}</text>')
        body+=enter(i, inner)
        if i<2:
            body+=f'<line x1="32" y1="{y+32}" x2="540" y2="{y+32}" stroke="{ACC}" stroke-opacity="0.08" stroke-width="1"/>'

    # 右パネル: 要点
    facts=[
        (I_PIN, "東京（Tokyo）を拠点に活動"),
        (I_MEDAL, "AWS 認定 全冠"),
        (I_CHECK, "IPA : AP ・ NW ・ SC"),
        (I_CHECK, "LPIC Level 3"),
    ]
    panel=(f'<rect x="572" y="86" width="260" height="200" rx="14" fill="{ACC}" fill-opacity="0.07" stroke="{ACC}" stroke-opacity="0.22" stroke-width="1"/>'
           f'<rect x="573" y="87" width="258" height="26" rx="13" fill="#FFFFFF" opacity="0.04"/>'
           f'<text x="592" y="116" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{MUTED}">PROFILE</text>'
           f'<text x="666" y="116" font-family="{JP}" font-size="11" letter-spacing="2" fill="{MUTED}">要点</text>')
    for j,(ic,txt) in enumerate(facts):
        fy=148+j*34
        panel+=(icon(592, fy-12, ic) +
                f'<text x="618" y="{fy}" font-family="{JP}" font-size="13" fill="{TEXT}">{txt}</text>')
        if j<3:
            panel+=f'<line x1="592" y1="{fy+16}" x2="812" y2="{fy+16}" stroke="{ACC}" stroke-opacity="0.08" stroke-width="1"/>'
    body+=enter(3, panel)

    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 {H}" width="860" height="{H}" role="img" aria-label="自己紹介">'
         + defs("ab",H) + tray("ab",H, orb='<circle cx="180" cy="60" r="150"/>', sweep_begin=4.5, sweep_dur=11)
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
         + header("st","Tech Stack","技術スタック",f"{n_tools} TOOLS ・ {len(cats)} CATEGORIES")
         + scan + body + frame("st",H) + '</svg>')
    with open(os.path.join(ASSETS,"stack-card.svg"),"w",encoding="utf-8") as f: f.write(svg)
    print("stack-card.svg", os.path.getsize(os.path.join(ASSETS,"stack-card.svg")), "B", "| tools:", n_tools, "| H:", H)

if __name__=="__main__":
    build_about(); build_stack()
