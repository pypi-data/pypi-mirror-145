import random

def aposta(wnumbers=6,wrange=60):
    wcont = int(wnumbers)
    wlista=[]
    while wcont > 0:
        d1 = random.randrange(1,wrange)
        if not (d1 in wlista):
            wlista.append(d1)
            print(d1)
            wcont = wcont -1
