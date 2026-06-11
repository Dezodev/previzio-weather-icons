import math, os, json

os.makedirs("icons", exist_ok=True)

DEFS = '''<defs>
<radialGradient id="sun" cx="38%" cy="34%" r="70%"><stop offset="0%" stop-color="#FFF3B0"/><stop offset="45%" stop-color="#FFD23F"/><stop offset="100%" stop-color="#F39C12"/></radialGradient>
<radialGradient id="sunGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFE066" stop-opacity="0.55"/><stop offset="100%" stop-color="#FFE066" stop-opacity="0"/></radialGradient>
<radialGradient id="moon" cx="38%" cy="34%" r="72%"><stop offset="0%" stop-color="#FDFCF4"/><stop offset="60%" stop-color="#E6E9D8"/><stop offset="100%" stop-color="#C2C6B0"/></radialGradient>
<radialGradient id="moonGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#DCE6FF" stop-opacity="0.45"/><stop offset="100%" stop-color="#DCE6FF" stop-opacity="0"/></radialGradient>
<linearGradient id="cloudLight" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#DCE4EE"/></linearGradient>
<linearGradient id="cloudMid" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#E3EAF3"/><stop offset="100%" stop-color="#B4C1D2"/></linearGradient>
<linearGradient id="cloudDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#9FAFC1"/><stop offset="100%" stop-color="#6E7E92"/></linearGradient>
<linearGradient id="cloudStorm" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#6C7585"/><stop offset="100%" stop-color="#454C59"/></linearGradient>
<linearGradient id="cloudNightLight" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#C7D0E2"/><stop offset="100%" stop-color="#97A2BC"/></linearGradient>
<linearGradient id="cloudNightMid" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#9AA5C0"/><stop offset="100%" stop-color="#6E7A98"/></linearGradient>
<linearGradient id="cloudNightDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#6E7A98"/><stop offset="100%" stop-color="#4A5470"/></linearGradient>
<linearGradient id="rainDrop" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7FB8E8"/><stop offset="100%" stop-color="#2E73C4"/></linearGradient>
<linearGradient id="rainDeep" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#4A8FD4"/><stop offset="100%" stop-color="#14529A"/></linearGradient>
<linearGradient id="bolt" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFE680"/><stop offset="100%" stop-color="#F5A623"/></linearGradient>
<radialGradient id="hail" cx="38%" cy="34%" r="70%"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#C3D4E4"/></radialGradient>
</defs>'''

def cloud(grad,x,y,s):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<ellipse cx="0" cy="2" rx="20" ry="11" fill="url(#{grad})"/>'
            f'<circle cx="-11" cy="-1" r="9" fill="url(#{grad})"/>'
            f'<circle cx="3" cy="-7" r="11" fill="url(#{grad})"/>'
            f'<circle cx="13" cy="-2" r="8" fill="url(#{grad})"/></g>')

def drop(x,y1,y2,w,grad):
    return f'<line x1="{x}" y1="{y1}" x2="{x-2}" y2="{y2}" stroke="url(#{grad})" stroke-width="{w}" stroke-linecap="round"/>'

def flake(x,y,sz,col):
    p=''
    for a in range(6):
        r=a*math.pi/3
        p+=f'<line x1="{x}" y1="{y}" x2="{x+math.cos(r)*sz:.2f}" y2="{y+math.sin(r)*sz:.2f}" stroke="{col}" stroke-width="1.4" stroke-linecap="round"/>'
    return p

def sun_rays(cx,cy,r,length,col):
    p=''
    for a in range(8):
        ang=a*math.pi/4
        x1=cx+math.cos(ang)*(r+3); y1=cy+math.sin(ang)*(r+3)
        x2=cx+math.cos(ang)*(r+3+length); y2=cy+math.sin(ang)*(r+3+length)
        p+=f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>'
    return p

def sun(cx,cy,r,length):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r+length+7}" fill="url(#sunGlow)"/>'
            + sun_rays(cx,cy,r,length,"#FBB938")
            + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sun)"/>')

def moon(cx,cy,r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r+8}" fill="url(#moonGlow)"/>'
            f'<path d="M {cx+r*0.45:.2f} {cy-r*0.9:.2f} A {r} {r} 0 1 0 {cx+r*0.45:.2f} {cy+r*0.9:.2f} '
            f'A {r*0.78:.2f} {r*0.78:.2f} 0 1 1 {cx+r*0.45:.2f} {cy-r*0.9:.2f} Z" fill="url(#moon)"/>'
            f'<circle cx="{cx-r*0.15:.2f}" cy="{cy-r*0.25:.2f}" r="{r*0.16:.2f}" fill="#B9BEA6" opacity="0.6"/>'
            f'<circle cx="{cx-r*0.35:.2f}" cy="{cy+r*0.3:.2f}" r="{r*0.11:.2f}" fill="#B9BEA6" opacity="0.5"/>')

def stars(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF0FF"/>' for x,y,r in pts)

def wrap(inner):
    return (f'<svg viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg">{DEFS}{inner}</svg>')

BOLT95='<polygon points="30,33 21,46 27,46 23,55 38,40 30,40 35,33" fill="url(#bolt)" stroke="#E8902A" stroke-width="0.5"/>'
BOLT96='<polygon points="26,32 18,43 24,43 20,52 33,38 26,38 31,32" fill="url(#bolt)" stroke="#E8902A" stroke-width="0.5"/>'
BOLT99='<polygon points="27,32 18,44 24,44 20,54 35,39 27,39 32,32" fill="url(#bolt)" stroke="#E8902A" stroke-width="0.5"/>'
HAIL96='<circle cx="39" cy="40" r="3.4" fill="url(#hail)" stroke="#9FB3C6" stroke-width="0.8"/><circle cx="40" cy="49" r="3.4" fill="url(#hail)" stroke="#9FB3C6" stroke-width="0.8"/>'
HAIL99='<circle cx="40" cy="39" r="3.8" fill="url(#hail)" stroke="#9FB3C6" stroke-width="0.8"/><circle cx="41" cy="49" r="3.8" fill="url(#hail)" stroke="#9FB3C6" stroke-width="0.8"/>'

def fog(dark=False):
    s1,s2 = ("#7C8AA4","#94A1BC") if dark else ("#AEB9C6","#C2CCD8")
    return (f'<line x1="12" y1="36" x2="44" y2="36" stroke="{s1}" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="16" y1="42" x2="40" y2="42" stroke="{s2}" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="12" y1="48" x2="44" y2="48" stroke="{s1}" stroke-width="3" stroke-linecap="round"/>')

def fog_ice(dark=False):
    s1,s2 = ("#7C8AA4","#94A1BC") if dark else ("#AEB9C6","#C2CCD8")
    return (f'<line x1="12" y1="33" x2="44" y2="33" stroke="{s1}" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="16" y1="39" x2="40" y2="39" stroke="{s2}" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="12" y1="45" x2="44" y2="45" stroke="{s1}" stroke-width="3" stroke-linecap="round"/>'
            + flake(18,51,3,"#7EC8E3")+flake(28,51,3,"#7EC8E3")+flake(38,51,3,"#7EC8E3"))

GRAINS='<circle cx="20" cy="42" r="3" fill="#EAF4FA" stroke="#6FBEDE" stroke-width="1.4"/><circle cx="30" cy="47" r="3" fill="#EAF4FA" stroke="#6FBEDE" stroke-width="1.4"/><circle cx="40" cy="42" r="3" fill="#EAF4FA" stroke="#6FBEDE" stroke-width="1.4"/>'

ST1=[(13,12,1.1),(42,14,1.2),(10,30,0.9)]
ST2=[(12,13,1.1),(40,12,1.1),(44,30,0.9)]
ST0=[(12,14,1.3),(44,18,1.1),(16,42,1),(43,40,1.4),(33,11,0.9)]
STsm=[(12,11,1.1),(44,13,1.0)]

ICONS = {
 0:dict(cat="Dégagé",label="Ciel dégagé",
        day=sun(28,28,12,6),
        night=stars(ST0)+moon(29,27,13)),
 1:dict(cat="Nuageux",label="Principalement dégagé",
        day=sun(22,20,9,5)+cloud('cloudLight',30,34,0.92),
        night=stars(ST1)+moon(22,19,10)+cloud('cloudNightLight',30,34,0.92)),
 2:dict(cat="Nuageux",label="Partiellement nuageux",
        day=sun(19,19,8,5)+cloud('cloudMid',29,33,1.05),
        night=stars(ST2)+moon(19,18,9)+cloud('cloudNightMid',29,33,1.05)),
 3:dict(cat="Nuageux",label="Couvert",
        day=cloud('cloudMid',20,22,0.85)+cloud('cloudDark',30,32,1.1),
        night=cloud('cloudNightMid',20,22,0.85)+cloud('cloudNightDark',30,32,1.1)),
 45:dict(cat="Brouillard",label="Brouillard",
        day=cloud('cloudLight',28,20,0.95)+fog(False),
        night=cloud('cloudNightLight',28,20,0.95)+fog(True)),
 48:dict(cat="Brouillard",label="Brouillard givrant",
        day=cloud('cloudLight',28,18,0.92)+fog_ice(False),
        night=cloud('cloudNightLight',28,18,0.92)+fog_ice(True)),
 51:dict(cat="Bruine",label="Bruine légère",
        day=cloud('cloudMid',28,20,1.05)+drop(22,36,42,2,"rainDrop")+drop(33,36,42,2,"rainDrop")),
 53:dict(cat="Bruine",label="Bruine modérée",
        day=cloud('cloudMid',28,20,1.05)+drop(19,36,43,2,"rainDrop")+drop(28,36,43,2,"rainDrop")+drop(37,36,43,2,"rainDrop")),
 55:dict(cat="Bruine",label="Bruine dense",
        day=cloud('cloudDark',28,20,1.05)+drop(17,36,44,2.2,"rainDrop")+drop(25,36,44,2.2,"rainDrop")+drop(33,36,44,2.2,"rainDrop")+drop(41,36,44,2.2,"rainDrop")),
 56:dict(cat="Bruine",label="Bruine verglaçante légère",
        day=cloud('cloudMid',28,20,1.05)+drop(22,36,42,2,"rainDrop")+flake(33,42,3.5,"#7EC8E3")),
 57:dict(cat="Bruine",label="Bruine verglaçante dense",
        day=cloud('cloudDark',28,20,1.05)+drop(20,36,43,2.2,"rainDrop")+flake(30,42,3.5,"#7EC8E3")+flake(40,46,3.5,"#7EC8E3")),
 61:dict(cat="Pluie",label="Pluie légère",
        day=cloud('cloudMid',28,19,1.05)+drop(22,35,45,2.4,"rainDrop")+drop(33,35,45,2.4,"rainDrop")),
 63:dict(cat="Pluie",label="Pluie modérée",
        day=cloud('cloudDark',28,19,1.05)+drop(19,35,46,2.6,"rainDrop")+drop(28,35,46,2.6,"rainDrop")+drop(37,35,46,2.6,"rainDrop")),
 65:dict(cat="Pluie",label="Pluie forte",
        day=cloud('cloudDark',28,19,1.1)+drop(16,35,48,3,"rainDeep")+drop(24,35,48,3,"rainDeep")+drop(32,35,48,3,"rainDeep")+drop(40,35,48,3,"rainDeep")),
 66:dict(cat="Pluie",label="Pluie verglaçante légère",
        day=cloud('cloudMid',28,19,1.05)+drop(22,35,44,2.4,"rainDrop")+flake(34,44,3.5,"#7EC8E3")),
 67:dict(cat="Pluie",label="Pluie verglaçante forte",
        day=cloud('cloudDark',28,19,1.05)+drop(19,35,45,2.6,"rainDeep")+drop(28,35,45,2.6,"rainDeep")+flake(38,46,3.5,"#7EC8E3")),
 71:dict(cat="Neige",label="Neige légère",
        day=cloud('cloudLight',28,19,1.05)+flake(21,42,4,"#9CD3EA")+flake(34,44,4,"#9CD3EA")),
 73:dict(cat="Neige",label="Neige modérée",
        day=cloud('cloudMid',28,19,1.05)+flake(18,42,4,"#6FBEDE")+flake(28,46,3.6,"#6FBEDE")+flake(38,42,4,"#6FBEDE")),
 75:dict(cat="Neige",label="Neige forte",
        day=cloud('cloudDark',28,19,1.05)+flake(16,42,3.8,"#4AA8D0")+flake(25,47,3.8,"#4AA8D0")+flake(34,42,3.8,"#4AA8D0")+flake(42,47,3.8,"#4AA8D0")),
 77:dict(cat="Neige",label="Grains de neige",
        day=cloud('cloudMid',28,19,1.05)+GRAINS),
 80:dict(cat="Averses",label="Averses légères",
        day=sun(17,16,7,4)+cloud('cloudDark',31,26,0.95)+drop(25,42,49,2.4,"rainDrop")+drop(35,42,49,2.4,"rainDrop"),
        night=stars(STsm)+moon(17,15,8)+cloud('cloudNightDark',31,26,0.95)+drop(25,42,49,2.4,"rainDrop")+drop(35,42,49,2.4,"rainDrop")),
 81:dict(cat="Averses",label="Averses modérées",
        day=cloud('cloudDark',28,19,1.05)+drop(19,35,46,2.6,"rainDrop")+drop(28,35,46,2.6,"rainDrop")+drop(37,35,46,2.6,"rainDrop"),
        night=cloud('cloudNightDark',28,19,1.05)+drop(19,35,46,2.6,"rainDrop")+drop(28,35,46,2.6,"rainDrop")+drop(37,35,46,2.6,"rainDrop")),
 82:dict(cat="Averses",label="Averses violentes",
        day=cloud('cloudStorm',28,19,1.1)+drop(16,35,49,3.2,"rainDeep")+drop(24,35,49,3.2,"rainDeep")+drop(32,35,49,3.2,"rainDeep")+drop(40,35,49,3.2,"rainDeep"),
        night=cloud('cloudStorm',28,19,1.1)+drop(16,35,49,3.2,"rainDeep")+drop(24,35,49,3.2,"rainDeep")+drop(32,35,49,3.2,"rainDeep")+drop(40,35,49,3.2,"rainDeep")),
 85:dict(cat="Averses neige",label="Averses de neige légères",
        day=sun(17,16,7,4)+cloud('cloudMid',31,26,0.95)+flake(26,44,3.8,"#6FBEDE")+flake(37,46,3.8,"#6FBEDE"),
        night=stars(STsm)+moon(17,15,8)+cloud('cloudNightMid',31,26,0.95)+flake(26,44,3.8,"#6FBEDE")+flake(37,46,3.8,"#6FBEDE")),
 86:dict(cat="Averses neige",label="Averses de neige fortes",
        day=cloud('cloudDark',28,19,1.05)+flake(17,42,3.6,"#4AA8D0")+flake(26,47,3.6,"#4AA8D0")+flake(35,42,3.6,"#4AA8D0")+flake(43,47,3.6,"#4AA8D0"),
        night=cloud('cloudNightDark',28,19,1.05)+flake(17,42,3.6,"#4AA8D0")+flake(26,47,3.6,"#4AA8D0")+flake(35,42,3.6,"#4AA8D0")+flake(43,47,3.6,"#4AA8D0")),
 95:dict(cat="Orage",label="Orage",
        day=cloud('cloudStorm',28,19,1.12)+BOLT95),
 96:dict(cat="Orage",label="Orage avec grêle",
        day=cloud('cloudStorm',28,18,1.12)+BOLT96+HAIL96),
 99:dict(cat="Orage",label="Orage fort avec grêle",
        day=cloud('cloudStorm',28,18,1.15)+BOLT99+HAIL99),
}

DAY_NIGHT = {0,1,2,3,45,48,80,81,82,85,86}

index = {"name":"previzio-weather-icons","version":"1.1.0","viewBox":"0 0 56 56","icons":{}}

for code,d in ICONS.items():
    day_svg = wrap(d["day"])
    fn_day = f"icons/{code:02d}-day.svg"
    with open(fn_day,"w") as f: f.write(day_svg)
    entry = {"label":d["label"],"category":d["cat"],"day":os.path.basename(fn_day),"hasNightVariant":code in DAY_NIGHT}
    if code in DAY_NIGHT:
        night_svg = wrap(d["night"])
        fn_night = f"icons/{code:02d}-night.svg"
        with open(fn_night,"w") as f: f.write(night_svg)
        entry["night"]=os.path.basename(fn_night)
    else:
        entry["night"]=os.path.basename(fn_day)
    index["icons"][str(code)]=entry

with open("index.json","w") as f:
    json.dump(index,f,ensure_ascii=False,indent=2)

print("SVG files:", len(os.listdir("icons")))
print("Codes:", len(ICONS), "| with night variant:", len(DAY_NIGHT))
