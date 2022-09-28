import collections


options = [
    # Serie A
    ("black", "blue"),
    ("red", "darkblue"),
    ("grey", "red"),
    ("blue",),
    ("purple",),
    ("yellow", "blue"),
    ("black", "blue"),
    ("white", "black"),
    ("lightblue",),
    ("yellow", "red"),
    ("red", "black"),
    ("red", "white"),
    ("blue",),
    ("yellow", "red"),
    ("maroon",),
    ("blue",),
    ("green", "black"),
    ("white", "black"),
    ("maroon",),
    ("white", "black"),
    # Serie B
    ("white", "black"),
    ("white", "red"),
    ("yellow", "red"),
    ("blue", "white"),
    ("red", "darkblue"),
    ("maroon",),
    ("blue",),
    ("red", "darkblue"),
    ("yellow", "blue"),
    ("red", "darkblue"),
    ("yellow", "blue"),
    ("pink", "black"),
    ("yellow", "blue"),
    ("red", "white"),
    ("black", "blue"),
    ("maroon",),
    ("white", "lightblue"),
    ("white", "red"),
    ("red", "green"),
    ("orange", "green"),
]

summary = collections.defaultdict(lambda: 0)
for colors in options:
    summary[colors] += 1
print(summary)

i = 0
for colors, count in summary.items():
    i += 1
    print('<div style="display: flex">')
    print(f'<div><strong>{i:02d}</strong></div>')
    for color in colors:
        print(f'  <div style="background-color: {color}; border: solid 1px black; color: grey; width: 200px; height: 50px;">{color}</div>')
    print(f'<div><strong>{count}</strong></div>')
    print("</div>")
