def RGB_to_hex(rgb):
    r = hex(rgb[0])[2:]
    g = hex(rgb[1])[2:]
    b = hex(rgb[2])[2:]

    if len(r) < 2: r = f"0{r}"
    if len(g) < 2: g = f"0{g}"
    if len(b) < 2: b = f"0{b}"

    return f"#{r}{g}{b}"