#!/usr/bin/env python3
"""ヒーロー（assets/header.svg）・ロールカルーセル（assets/roles.svg）・フッター（assets/footer.svg）を生成する。
方針: 全て自作 SVG / camo 安全（SMIL のみ、CSS アニメ・foreignObject 不可）。
静的レンダラでも破綻しないよう、アニメ対象は「基準値=完成形」にして values で 0 から動かす。"""
import os, re, base64

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

# ============================================================ HEADER
def build_header():
    mascot = b64("mascot-lg.png")
    # ブログ・カプセル（既存アセット）をキャンバスに埋め込む（外側の svg タグだけ剥がす）
    with open(os.path.join(ASSETS, "blog-badge.svg"), encoding="utf-8") as f:
        badge_inner = re.sub(r'^<svg[^>]*>', '', f.read(), count=1).rsplit('</svg>', 1)[0]

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

    # 宇宙要素: 小さな星々（静的）＋非同期きらめき＋たまの流れ星
    star_pts=[(140,26,0.35,0.9),(300,18,0.25,0.7),(470,34,0.4,1.0),(560,52,0.3,0.8),(650,24,0.45,1.1),
              (700,58,0.25,0.7),(745,36,0.35,0.9),(905,26,0.3,0.8),(1005,20,0.4,1.0),(1170,40,0.35,0.9),
              (620,140,0.22,0.7),(730,150,0.2,0.8)]
    stars="".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STAR}" opacity="{op}"/>' for x,y,op,r in star_pts)
    for x,y,c,dur,beg in [(520,30,ACCENT2,4.2,0.5),(830,48,"#FFFFFF",5.1,1.3),(1178,64,VIO_LT,3.6,2.1)]:
        stars+=(f'<g transform="translate({x},{y})">'
                f'<path d="M0 -3 L0.7 -0.7 L3 0 L0.7 0.7 L0 3 L-0.7 0.7 L-3 0 L-0.7 -0.7 Z" fill="{c}" opacity="0.5">'
                f'<animate attributeName="opacity" values="0.2;1;0.4;0.2" keyTimes="0;0.2;0.5;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                f'</path></g>')
    stars+=(f'<line x1="628" y1="16" x2="668" y2="32" stroke="url(#hshoot)" stroke-width="1.2" stroke-linecap="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;0.9;0" keyTimes="0;0.02;0.06;0.12" dur="14s" begin="6s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="-30 -12;70 28;70 28" keyTimes="0;0.12;1" dur="14s" begin="6s" repeatCount="indefinite"/>'
            f'</line>')

    # コーヒーの湯気（マスコットのカップ上）
    steam=""
    for (sx,sy,dur,beg) in [(1036,188,3.8,0.4),(1047,182,4.4,1.5),(1057,189,5.0,2.6)]:
        steam+=(f'<g transform="translate({sx},{sy})">'
                f'<path d="M0 0 C-4 -7 4 -12 0 -20" fill="none" stroke="#D7EDF7" stroke-width="1.6" stroke-linecap="round" opacity="0.15">'
                f'<animate attributeName="opacity" values="0;0.5;0" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -16" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                f'</path></g>')

    # ===== 下段（キャンバス y300-476）: ロール / ソーシャルピル / ブログカプセル =====
    lines=["AWS Cloud Engineer","Qiita Writer / 80+ Articles","AWS All Certifications","IaC / Serverless / GenAI"]
    per=4.0; total=per*len(lines)
    roles_txt=""
    for i,s in enumerate(lines):
        base=1 if i==0 else 0
        roles_txt+=(f'<text x="356" y="332" font-family="{MONO}" font-size="17" letter-spacing="1" fill="#B6C9D6" opacity="{base}">{s}'
                    f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.04;0.22;0.26;1" dur="{total}s" begin="{i*per}s" repeatCount="indefinite"/></text>')
    lower=(f'<text x="330" y="332" font-family="{MONO}" font-size="17" fill="{ACCENT}">&gt;</text>'
           f'<rect x="344" y="317" width="3" height="18" fill="{ACCENT}">'
           f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
           + roles_txt)
    # ソーシャルピル（リンクは README 側で 左右50%の <a> により付与）
    lower+=(f'<g transform="translate(430,358)">'
            f'<rect width="150" height="36" rx="18" fill="#55C500" fill-opacity="0.13" stroke="#55C500" stroke-opacity="0.4" stroke-width="1.1"/>'
            f'<rect x="1.5" y="1.5" width="147" height="14" rx="12" fill="#FFFFFF" opacity="0.06"/>'
            f'<circle cx="24" cy="18" r="4.2" fill="#55C500"><animate attributeName="opacity" values="1;0.4;1" dur="2.4s" repeatCount="indefinite"/></circle>'
            f'<text x="40" y="24" font-family="{SANS}" font-size="15" font-weight="700" fill="#C2F0C2">Qiita</text>'
            f'<g fill="none" stroke="#9FE86B" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" transform="translate(114,12)">'
            f'<path d="M0 12 L11 1"/><path d="M4 1 H11 V8"/></g></g>')
    lower+=(f'<g transform="translate(620,358)">'
            f'<rect width="190" height="36" rx="18" fill="{ACCENT}" fill-opacity="0.10" stroke="{ACCENT}" stroke-opacity="0.35" stroke-width="1.1"/>'
            f'<rect x="1.5" y="1.5" width="187" height="14" rx="12" fill="#FFFFFF" opacity="0.06"/>'
            f'<g stroke="#D5E9F2" stroke-width="2" stroke-linecap="round" transform="translate(20,12)">'
            f'<path d="M0 0 L11 12"/><path d="M11 0 L0 12"/></g>'
            f'<text x="42" y="23" font-family="{MONO}" font-size="12.5" fill="#D5E9F2">@miruky_tech</text></g>')
    # ブログ・カプセル（既存アセットをそのまま埋め込み・中央配置）
    lower+=f'<g transform="translate(455,398) scale(0.85)">{badge_inner}</g>'
    # 下段の星（背景の連続感）
    for x,y,op,r in [(200,330,0.3,0.8),(1000,326,0.35,0.9),(150,432,0.3,0.8),(1056,442,0.35,1.0),
                     (90,382,0.25,0.7),(1130,392,0.3,0.8),(320,452,0.22,0.7),(880,455,0.25,0.8)]:
        lower+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STAR}" opacity="{op}"/>'

    content=f'''
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
    <radialGradient id="aurV" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{VIO}" stop-opacity="0.26"/><stop offset="0.6" stop-color="{VIO}" stop-opacity="0.12"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aurV2" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#A78BFA" stop-opacity="0.16"/><stop offset="1" stop-color="#A78BFA" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vglow" cx="0.32" cy="1.0" r="0.75">
      <stop offset="0" stop-color="{VIO}" stop-opacity="0.16"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="hshoot" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{VIO_LT}"/>
    </linearGradient>
    <linearGradient id="glint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="hmglow" cx="0.5" cy="0.46" r="0.5">
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

  <rect width="1200" height="476" fill="url(#bg)"/>
  <!-- aurora drift -->
  <ellipse cx="300" cy="80" rx="270" ry="95" fill="url(#aurA)" filter="url(#asoft)">
    <animateTransform attributeName="transform" type="translate" values="0 0;60 14;0 0" dur="16s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </ellipse>
  <ellipse cx="640" cy="215" rx="300" ry="100" fill="url(#aurB)" filter="url(#asoft)">
    <animateTransform attributeName="transform" type="translate" values="0 0;-70 -12;0 0" dur="21s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </ellipse>
  <ellipse cx="920" cy="70" rx="320" ry="105" fill="url(#aurV)" filter="url(#asoft)">
    <animateTransform attributeName="transform" type="translate" values="0 0;-40 16;0 0" dur="24s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </ellipse>
  <ellipse cx="560" cy="120" rx="230" ry="62" fill="url(#aurV2)" filter="url(#asoft)" transform="rotate(-9 560 120)">
    <animateTransform attributeName="transform" type="translate" values="0 0;55 -12;0 0" additive="sum" dur="19s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
  </ellipse>
  <rect width="1200" height="300" fill="url(#glow)"/>
  <rect width="1200" height="476" fill="url(#vglow)"/>
  <rect width="1200" height="476" fill="#000" opacity="0.7" filter="url(#hgrain)"/>

  {stars}
  {particles}
  <g>{bars}</g>

  <!-- kicker (wipe-in) -->
  <text x="92" y="96" font-family="{MONO}" font-size="15" letter-spacing="6" fill="{MUTED}" clip-path="url(#kclip)">AWS &#183; SERVERLESS &#183; GENAI</text>

  <!-- wordmark -->
  <text x="86" y="184" font-family="{SANS}" font-size="94" font-weight="800" letter-spacing="1" fill="#F0F6FC">miruky</text>
  <!-- diagonal glint（柔らかいグラデ帯が素早く通過 → 静止） -->
  <rect x="-340" y="-40" width="240" height="560" fill="url(#glint)" transform="skewX(-18)">
    <animate attributeName="x" values="-340;1720;1720" keyTimes="0;0.11;1" dur="12s" begin="1.5s" repeatCount="indefinite"/>
  </rect>

  <rect x="92" y="203" width="382" height="4" rx="2" fill="url(#rule)">
    <animate attributeName="width" values="0;382" dur="1.1s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/>
  </rect>
  <text x="94" y="244" font-family="{JP}" font-size="22" letter-spacing="1" fill="{MUTED}">クラウドエンジニア <tspan fill="#30363D">/</tspan> Qiita ライター</text>

  <!-- status pill -->
  <g transform="translate(92,258)">
    <rect width="524" height="32" rx="16" fill="#12161D" fill-opacity="0.85" stroke="{ACCENT}" stroke-opacity="0.28"/>
    <rect x="1" y="1" width="522" height="14" rx="13" fill="#FFFFFF" opacity="0.05"/>
    <circle cx="18" cy="16" r="4" fill="{ACCENT}">
      <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="r" values="4;5.2;4" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="34" y="21" font-family="{JP}" font-size="13" fill="#9FB6C8">いま構築中 : CloudFormation × AWS Code シリーズの CI/CD パイプライン</text>
  </g>

  <!-- mascot: orbit ring + glow + bob + steam -->
  <g>
    <circle cx="1058" cy="160" r="96" fill="none" stroke="{ACCENT}" stroke-opacity="0.16" stroke-width="1.2" stroke-dasharray="2 9">
      <animateTransform attributeName="transform" type="rotate" from="0 1058 160" to="360 1058 160" dur="70s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1058" cy="160" r="98" fill="url(#hmglow)" filter="url(#msoft)"/>
    <image x="972" y="74" width="172" height="172" href="data:image/png;base64,{mascot}" preserveAspectRatio="xMidYMid meet">
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="4.4s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
    </image>
    {steam}
  </g>

  <!-- ===== 下段: 同一キャンバスから帯として切り出す ===== -->
  {lower}
'''
    # 1枚のキャンバス(1200x476)を viewBox で帯に切り出す（背景が帯間で完全に連続する）
    strips=[("header.svg",0,0,1200,300),("strip-roles.svg",0,300,1200,52),
            ("strip-social-l.svg",0,352,600,46),("strip-social-r.svg",600,352,600,46),
            ("strip-blog.svg",0,398,1200,78)]
    for fn,vx,vy,vw,vh in strips:
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx} {vy} {vw} {vh}" '
             f'width="{vw}" height="{vh}" role="img" aria-label="miruky">'+content+'</svg>')
        with open(os.path.join(ASSETS,fn),"w",encoding="utf-8") as f: f.write(svg)
        print(fn, os.path.getsize(os.path.join(ASSETS,fn)), "B")

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

# ============================================================ SECTIONS（ランナー型見出し）
# 「浮いた箱」をやめ、ゴースト番号 + タイトル + 右へ溶けていく罫線 + 端の小星座で構成する。
SECTIONS=[("01","自己紹介","section-about.svg"),("02","Qiita","section-qiita.svg"),
          ("03","保有資格","section-certifications.svg"),("04","技術スタック","section-stack.svg"),
          ("05","GitHub","section-github.svg"),("06","リンク","section-links.svg")]

def build_sections():
    for i,(num,title,fname) in enumerate(SECTIONS):
        title_w = sum(30 if ord(c)>0x2E7F else 17 for c in title)
        lx = 92 + title_w + 26          # 罫線の開始位置
        lw = 1160 - lx                  # 罫線の長さ
        gb = 2.5 + i*1.8                # glint の時差発火
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 76" width="1200" height="76" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="sline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.55"/>
      <stop offset="0.55" stop-color="{VIO}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{VIO}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sglint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT2}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{ACCENT2}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{ACCENT2}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="sclip"><rect x="{lx}" y="41" width="{lw}" height="6"/></clipPath>
  </defs>
  <text x="24" y="58" font-family="{MONO}" font-size="50" font-weight="700" letter-spacing="2" fill="{ACCENT}" opacity="0.17">{num}</text>
  <text x="92" y="52" font-family="{JP}" font-size="26" font-weight="700" letter-spacing="4" fill="{TEXT}">{title}</text>
  <rect x="{lx}" y="43" width="{lw}" height="1.3" fill="url(#sline)">
    <animate attributeName="width" values="0;{lw}" dur="0.9s" begin="0.15s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/>
  </rect>
  <g clip-path="url(#sclip)">
    <rect x="{lx-140}" y="42.4" width="140" height="2.6" fill="url(#sglint)">
      <animate attributeName="x" values="{lx-140};1180;1180" keyTimes="0;0.14;1" dur="12s" begin="{gb}s" repeatCount="indefinite"/>
    </rect>
  </g>
  <g transform="translate({lx-14},43.5)">
    <path d="M0 -4 L0.9 -0.9 L4 0 L0.9 0.9 L0 4 L-0.9 0.9 L-4 0 L-0.9 -0.9 Z" fill="{ACCENT2}" opacity="0.8">
      <animate attributeName="opacity" values="0.5;1;0.5" dur="3.4s" begin="{0.4+i*0.5:.1f}s" repeatCount="indefinite"/>
    </path>
  </g>
  <g opacity="0.65">
    <line x1="1120" y1="30" x2="1148" y2="44" stroke="{STAR}" stroke-opacity="0.25" stroke-width="0.7"/>
    <line x1="1148" y1="44" x2="1170" y2="26" stroke="{STAR}" stroke-opacity="0.25" stroke-width="0.7"/>
    <circle cx="1120" cy="30" r="1.2" fill="{STAR}" opacity="0.5"/>
    <circle cx="1148" cy="44" r="1.6" fill="{ACCENT2}" opacity="0.7">
      <animate attributeName="opacity" values="0.4;0.9;0.4" dur="{3.2+i*0.4:.1f}s" begin="{i*0.7:.1f}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1170" cy="26" r="1.1" fill="{VIO_LT}" opacity="0.55"/>
  </g>
</svg>'''
        with open(os.path.join(ASSETS,fname),"w",encoding="utf-8") as f: f.write(svg)
    print("sections:", len(SECTIONS), "runner headers")

if __name__=="__main__":
    build_header(); build_roles(); build_footer(); build_sections()
