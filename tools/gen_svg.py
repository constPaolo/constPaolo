#!/usr/bin/env python3
"""Genera dark_mode.svg e light_mode.svg per il profilo di constPaolo."""

WIDTH = 60  # larghezza totale di ogni riga, in caratteri

HEADER = "paolo@meccariello"

# (chiavi, valore, id_dinamico_or_None)
ROWS = [
    (["OS"], "Windows 11, Android 16, macOS", None),
    (["Uptime"], "28 years, 9 months, 9 days", "age_data"),
    (["Host"], "https://www.paolomeccariello.dev/", None),
    (["IDE"], "VSCode 1.129.1", None),
    None,
    (["Languages", "Programming"], "JavaScript, Java, C++", None),
    (["Languages", "Computer"], "HTML, CSS, JSON, LaTeX, YAML", None),
    (["Languages", "Real"], "English, Italian", None),
    None,
    (["Hobbies", "Software"], "Personal Spotify, Personal Netflix", None),
    (["Hobbies", "Android"], "APK Sideloading", None),
    (["Hobbies", "Hardware"], "Home Server", None),
    (["Hobbies", "Other"], "Cooking, Movies", None),
]

CONTACT = [
    (["Email", "Personal"], "paolomeccariello97@gmail.com"),
    (["LinkedIn"], "Paolo Meccariello"),
    (["GitHub"], "constPaolo"),
]


ART_FILES = {"dark": "darkmode.txt", "light": "lightmode.txt"}
MAX_ART_WIDTH = 44  # oltre questa larghezza l'arte invade la colonna di testo


def load_art(theme):
    """Legge l'ASCII art dal .txt del tema e verifica che stia nel layout."""
    with open(ART_FILES[theme], encoding="utf-8") as f:
        lines = f.read().strip("\n").split("\n")
    w = max(len(l.rstrip()) for l in lines)
    if w > MAX_ART_WIDTH:
        raise ValueError(f"{ART_FILES[theme]}: {w} caratteri di larghezza, il massimo e' {MAX_ART_WIDTH}")
    return lines


def keylen(keys):
    """Lunghezza del prefisso '. Key.Key:'"""
    return 2 + len(".".join(keys)) + 1


def dots(keys, value):
    """Puntini di riempimento per arrivare a WIDTH caratteri."""
    n = WIDTH - keylen(keys) - len(value)
    if n < 2:
        raise ValueError(f"riga troppo lunga: {'.'.join(keys)} = {value!r} (servono {2-n} char in meno)")
    return " " + ("." * (n - 2)) + " "


def keyspan(keys):
    return ".".join(f'<tspan class="key">{k}</tspan>' for k in keys)


def row(y, keys, value, dyn):
    d = dots(keys, value)
    if dyn:
        dot_el = f'<tspan class="cc" id="{dyn}_dots">{d}</tspan>'
        val_el = f'<tspan class="value" id="{dyn}">{value}</tspan>'
    else:
        dot_el = f'<tspan class="cc">{d}</tspan>'
        val_el = f'<tspan class="value">{value}</tspan>'
    return f'<tspan x="390" y="{y}" class="cc">. </tspan>{keyspan(keys)}:{dot_el}{val_el}'


def sep(title):
    """Riga separatore tipo '- Contact ---------'."""
    dashes = "—" * (WIDTH - len(title) - 6)
    return f'{title}</tspan> -{dashes}-—-'


def build(theme):
    if theme == "dark":
        bg, fg = "#161b22", "#c9d1d9"
        css = ".key {fill: #ffa657;}\n.value {fill: #a5d6ff;}\n.addColor {fill: #3fb950;}\n.delColor {fill: #f85149;}\n.cc {fill: #616e7f;}"
    else:
        bg, fg = "#f6f8fa", "#24292f"
        css = ".key {fill: #953800;}\n.value {fill: #0a3069;}\n.addColor {fill: #1a7f37;}\n.delColor {fill: #cf222e;}\n.cc {fill: #c2cfde;}"

    out = []
    out.append("<?xml version='1.0' encoding='UTF-8'?>")
    out.append('<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">')
    out.append("<style>")
    out.append("@font-face {\nsrc: local('Consolas'), local('Consolas Bold');\nfont-family: 'ConsolasFallback';\nfont-display: swap;\n-webkit-size-adjust: 109%;\nsize-adjust: 109%;\n}")
    out.append(css)
    out.append("text, tspan {white-space: pre;}")
    out.append("</style>")
    out.append(f'<rect width="985px" height="530px" fill="{bg}" rx="15"/>')

    # colonna sinistra: ASCII art
    art = load_art(theme)
    # il passo verticale si adatta al numero di righe, per restare dentro y=30..510
    step = min(20, 480 // max(1, len(art) - 1))
    out.append(f'<text x="15" y="30" fill="{fg}" class="ascii">')
    for i, line in enumerate(art):
        y = 30 + i * step
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        out.append(f'<tspan x="15" y="{y}">{safe}</tspan>')
    out.append("</text>")

    # colonna destra
    out.append(f'<text x="390" y="30" fill="{fg}">')
    out.append(f'<tspan x="390" y="30">{sep(HEADER)}')

    y = 50
    for r in ROWS:
        if r is None:
            out.append(f'<tspan x="390" y="{y}" class="cc">. </tspan>')
        else:
            out.append(row(y, r[0], r[1], r[2]))
        y += 20

    y += 20
    out.append(f'<tspan x="390" y="{y}">{sep("- Contact")}')
    y += 20
    for keys, value in CONTACT:
        out.append(row(y, keys, value, None))
        y += 20

    y += 20
    out.append(f'<tspan x="390" y="{y}">{sep("- GitHub Stats")}')
    y += 20
    out.append(f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">29</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">29</tspan>}} | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ............. </tspan><tspan class="value" id="star_data">0</tspan>')
    y += 20
    out.append(f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> ................... </tspan><tspan class="value" id="commit_data">416</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ......... </tspan><tspan class="value" id="follower_data">3</tspan>')
    y += 20
    out.append(f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots"></tspan><tspan class="value" id="loc_data">330,624</tspan> ( <tspan class="addColor" id="loc_add">362,358</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">31,734</tspan><tspan class="delColor">--</tspan> )')

    out.append("</text>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


for theme, fn in (("dark", "dark_mode.svg"), ("light", "light_mode.svg")):
    with open(fn, "w", encoding="utf-8") as f:
        f.write(build(theme))
    print(f"scritto {fn}")

# verifica larghezze
print("\nControllo larghezza righe (target 60):")
for keys, value, *_ in [r for r in ROWS if r] + [(k, v, None) for k, v in CONTACT]:
    tot = keylen(keys) + len(dots(keys, value)) + len(value)
    flag = "OK" if tot == WIDTH else f"!! {tot}"
    print(f"  {'.'.join(keys):<24} {flag}")
