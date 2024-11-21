import datetime

def lyambdaod(x1, y1, p, a): #oblicza nachylenie stycznej λ dla operacji podwajania punktu na eliptycznej krzywej
    l=((3*pow(x1, 2)+a)*(pow((2 * y1), (p-1-1))))%p
    return l

def lyambdaraz(x1, y1, x2, y2, p): #oblicza nachylenie stycznej λ dla operacji dodawania punktów na eliptycznej krzywej
    l=((y2-y1)*pow((x2-x1), (p-1-1)))%p
    return l

def odraz(x1, x2, y1, y2, p, a): #funkcja wyznacza czy trzeba wykonać operacje dodawania punktów czy podwajania
    if x1==x2 and y1==y2:
        l=lyambdaod(x1, y1, p, a)
    else:
        l=lyambdaraz(x1, y1, x2, y2, p)
    return l

def x(l, x1, x2, p): #oblicza współrzędną x3​
    x3=(pow(l, 2)-x1-x2)%p
    return x3

def y(l, x1, x3, y1, p): #oblicza współrzędną y3
    y3=(l*(x1-x3)-y1)%p
    return y3

def numberfrompoint(find_point, G, p, a): #przewraca punkt na eliptycznej krzywej w liczbe
    now_point = G
    n=1
    while now_point!=find_point:
        x1, y1 = now_point
        x2, y2 = G
        l = odraz(x1, x2, y1, y2, p, a)
        x3 = (l**2 - x1 - x2) % p
        y3 = (l * (x1 - x3) - y1) % p
        now_point = (x3, y3)
        n+=1
    return n

def findYa(ka, G, p, a): #obliczenie klucza publicznego uzytkownika A (Ya)
    x1=G[0]
    y1=G[1]
    x2=G[0]
    y2=G[1]
    for i in range(ka-1):
        l=odraz(x1, x2, y1, y2, p, a)
        x3=x(l, x1, x2, p)
        y3=y(l, x1, x3, y1, p)
        x2=x3
        y2=y3
    Ya=(x3, y3)
    return Ya

def findYb(kb, G, p, a): #obliczenie klucza publicznego uzytkownika B (Yb)
    x1=G[0]
    y1=G[1]
    x2=G[0]
    y2=G[1]
    for i in range(kb-1):
        l=odraz(x1, x2, y1, y2, p, a)
        x3=x(l, x1, x2, p)
        y3=y(l, x1, x3, y1, p)
        x2=x3
        y2=y3
    Yb=(x3, y3)
    return Yb

def findrG(G, r, p, a): #obliczenie punktu r * G 
    x1=G[0]
    y1=G[1]
    x2=G[0]
    y2=G[1]
    for i in range(r-1):
        l=odraz(x1, x2, y1, y2, p, a)
        x3=x(l, x1, x2, p)
        y3=y(l, x1, x3, y1, p)
        x2=x3
        y2=y3
    rG=(x3, y3)
    return rG

def findrYb(Yb, r, p, a): #obliczenie punktu Y * b
    x1=Yb[0]
    y1=Yb[1]
    x2=Yb[0]
    y2=Yb[1]
    for i in range(r-1):
        l=odraz(x1, x2, y1, y2, p, a)
        x3=x(l, x1, x2, p)
        y3=y(l, x1, x3, y1, p)
        x2=x3
        y2=y3
    rYb=(x3, y3)
    return rYb

def enc(n, G, p, a, rYb, rG): #funkcja szyfrowania
    x1=G[0]
    y1=G[1]
    x2=G[0]
    y2=G[1]
    #Pm
    for i in range(n-1):
        l=odraz(x1, x2, y1, y2, p, a)
        x3=x(l, x1, x2, p)
        y3=y(l, x1, x3, y1, p)
        x2=x3
        y2=y3
    Pm=(x3, y3) #sumbol w postaci punktu na eliptycznej krzywej
    #R=Pm+rYb
    x1=Pm[0]
    y1=Pm[1]
    x2=rYb[0]
    y2=rYb[1]
    l=odraz(x1, x2, y1, y2, p, a)
    x3=x(l, x1, x2, p)
    y3=y(l, x1, x3, y1, p)
    R=(x3, y3)
    C=(rG, R) #zaszyfrowana wiadomość
    return C, R, Pm

def dec(p, a, rG, kb, R): #funkcja deszyfrowania
    #kb*rG
    x1=rG[0]
    y1=rG[1]
    x2=rG[0]
    y2=rG[1]
    for i in range (kb-1):
        l=odraz(x1, x2, y1, y2, p, a)
        x3=x(l, x1, x2, p)
        y3=y(l, x1, x3, y1, p)
        x2=x3
        y2=y3
    kbrG=(x3, y3)
    #R-kbrG
    x1=R[0]
    y1=R[1]
    x2=kbrG[0]
    y2=-kbrG[1]
    l=odraz(x1, x2, y1, y2, p, a)
    x3=x(l, x1, x2, p)
    y3=y(l, x1, x3, y1, p)
    dec=(x3, y3) #deszyfrowana wiadomość
    return dec

def main():
    p=751
    a=-1
    b=1
    E=(-1, 1)
    G=(0, 1)
    ka=4
    kb=15
    print("Values")
    print("p = ", p)
    print("a = ", a)
    print("b = ", b)
    print("E = ", E)
    #y^2=((x^3)-x+1)mod751
    print("G = ", G)
    print("ka = ", ka)
    print("kb = ", kb)
    print("--------------------")
    
    #Ya:
    Ya=findYa(ka, G, p, a)
    print("Public key of user A: Ya = ", Ya)
    #Yb:
    Yb=findYb(kb, G, p, a)
    print("Public key of user B: Yb = ", Yb)
    print("Encryption")
    time1=datetime.datetime.now()
    while True:
        try:
            r = int(input("Enter a random integer r: "))
            break  # jeśli r jest poprawne, wychodzimy z pętli
        except ValueError:
            print("Error: you need to enter an integer")

    #rG:
    rG=findrG(G, r, p, a)
    print("rG = ", rG)

    #rYb:
    rYb=findrYb(Yb, r, p, a)
    print("rYb = ", rYb)
    
    msg=input("Enter a message:")
    msg = msg.replace(' ', '.') # zamiana spacji na `.`, aby uniknąć problemów z kodowaniem
    MSG=msg.upper() 
    symbols = list(MSG)
    print(symbols)
    decoded_msg = []
    for symbol in MSG: #dzielenie wiadomości na symboly
        n=ord(symbol) #kod symbolu w Unicode
        print("_______")
        print(f"Symbol: {symbol}")
        encrypted, R, Pm = enc(n, G, p, a, rYb, rG) 
        print("Point on an elliptic curve: ", Pm) #punkt na eliptycznej krzywej do szyfrowania
        print("Encrypted message: ", encrypted) #zaszyfrowany punkt

        decrypted=dec(p, a, rG, kb, R)
        print("Decrypted point on an elliptic curve: ", decrypted) #deszyfrowany punkt
        number=numberfrompoint(decrypted, G, p, a) #przewracamy punkt w liczbe
        findletter=chr(number) #przewracanie liczby w symbol w Unicode
        print("Decrypted symbol: ", findletter)
        if findletter == '.':
            findletter = ' '
        decoded_msg.append(findletter)
    mod_word=''.join(decoded_msg) #łączenie deszyfrowanych symboli
    print("\nDecrypted message:", "".join(map(str, decoded_msg))) #deszyfrowana wiadomość
    time2=datetime.datetime.now()
    time=str(time2-time1)
    print()
    print("Time spent on encryption and decryption: ", time) #czas wytracony na szyfrowanie i deszyfrowanie
    print()

main()
