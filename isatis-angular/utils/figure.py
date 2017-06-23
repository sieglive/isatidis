import math

ew = 30
eh = 30
dx = 2
l = 5
x = ew/2
y = eh/2 + l / 2 / math.sqrt(3)
h = l / 2 * math.sqrt(3)
delta = dx / math.sqrt(3)
print(h, dx, delta)

plist = []
plist.append((x-l/2, y))
plist.append((x-l/2 - delta, y+dx))
plist.append((x+l/2+delta*5, y+dx))
plist.append((x+delta, y-h-3*dx))
plist.append((x-delta, y-h-3*dx))
plist.append((x+l/2+delta*2, y))
plist.append(plist[0])
a1 = ' '.join([f'L{p[0]} {p[1]}' for p in plist])
a1 = 'M' + a1[1:]

plist = []
plist.append((x-l/2-delta, y+dx))
plist.append((x+l/2+delta*5, y+dx))
plist.append((x+l/2+delta*4, y+dx*2))
plist.append((x-l/2-delta*4, y+dx*2))
plist.append((x-delta, y-h-dx))
plist.append((x, y-h))
plist.append(plist[0])
a2 = ' '.join([f'L{p[0]} {p[1]}' for p in plist])
a2 = 'M' + a2[1:]

plist = []
plist.append((x-l/2-delta*4, y+dx*2))
plist.append((x-l/2-delta*5, y+dx))
plist.append((x-delta, y-h-3*dx))
plist.append((x+l/2+delta*2, y))
plist.append((x+l/2, y))
plist.append((x-delta, y-h-dx))
plist.append(plist[0])
a3 = ' '.join([f'L{p[0]} {p[1]}' for p in plist])
a3 = 'M' + a3[1:]

print(a1)
print(a2)
print(a3)

out = f"""<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
<div style="margin-top:200px;">
    <svg class="site-logo" style="width:{ew}px;height:{eh}px;">
        <defs>
            <filter id="Gaussian_Blur">
                <feGaussianBlur in="SourceGraphic" stdDeviation="1" />
            </filter>
        </defs>
        <circle cx="{ew/2}" cy="{eh/2}" r="{(ew if ew < eh else eh) / 2}" 
        filter="url(#Gaussian_Blur)"/>
        <path class="path-1" d="{a1}" />
        <path class="path-2" d="{a2}" />
        <path class="path-3" d="{a3}" />
        <animateTransform attributeName="transform" begin="0s" dur="2s" 
        type="rotate" from="0 0 0" to="360 0 0" repeatCount="indefinite"/>
    </svg>
</div>
</body>
</html>"""

with open('ttt.html', 'wb') as f:
    f.write(out.encode())
print(out)