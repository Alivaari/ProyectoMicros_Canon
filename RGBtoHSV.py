def rgb_to_hsv(rojo, verde, azul):
    rojo=float(rojo)
    verde=float(verde)
    azul=float(azul)
    r, g, b = rojo/255.0, verde/255.0, azul/255.0
    maximo = max(r, g, b)
    minimo = min(r, g, b)
    rango = maximo-minimo
    if maximo == minimo:
        h = 0
    elif maximo == r:
        h = (60 * ((g-b)/rango) + 180) % 180
    elif maximo == g:
        h = (60 * ((b-r)/rango) + 60) % 180
    elif maximo == b:
        h = (60 * ((r-g)/rango) + 120) % 180
    if maximo == 0:
        s = 0
    else:
        s = (rango/maximo)*255.0
    v = maximo*255.0
    print(str(h),', ',str(s),', ',str(v))
    return [h,s,v]

def lista(t):
    print(str(t[:]))
    return 0
    
rojo=input('Rojo:')
verde=input('Verde:')
azul=input('Azul:')

lista(rgb_to_hsv(rojo, verde, azul))

