from math import *

def lcm(x, y):
    if x > y:
        z = x
    else:
        z = y
    while(True):
        if((z % x == 0) and (z % y == 0)):
            lcm = z
            break
        z += 1
    return lcm

def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

class Koren:
    def __init__(self, *args):
        if len(args) == 3:
            self.rat = args[0]
            self.irat = args[1]
            self.koren = args[2]
        elif len(args) == 1:
            self.rat = args[0]
            self.irat = 0
            self.koren = 0
    def __str__(self):
        return f'{self.rat}+{self.irat}√{self.koren}'
    def eval(self):
        return self.rat + self.irat * sqrt(self.koren)

def k_sestej(k1, k2):
    rat = k1.rat + k2.rat
    if (k1.koren == k2.koren or k1.irat == 0 or k2.irat == 0):
        irat = k1.irat + k2.irat
        koren = max(k1.koren, k2.koren)
    else:
        raise ValueError("cannot sum two different square roots")
    rez = Koren(rat, irat, koren)
    return rez

def k_neg(k1):
    rez = Koren(-k1.rat, -k1.irat, k1.koren)
    return rez

def k_odstej(k1, k2):
    return k_sestej(k1, k_neg(k2))

def k_zmnozi(k1, k2):
    if not (k1.koren == k2.koren or k1.irat == 0 or k2.irat == 0):
        raise ValueError("cannot multiply two different square roots")
    koren = max(k1.koren, k2.koren)
    rez = Koren(0,0,koren)
    rez.rat = int(k1.rat * k2.rat + k1.irat * k2.irat * koren)
    rez.irat = int(k1.rat * k2.irat + k2.rat * k1.irat)
    return rez

def k_skalar(k1, skal):
    rez = Koren(int(k1.rat*skal), int(k1.irat*skal), k1.koren)
    return rez

def k_gcd(k):
    return gcd(k.rat, k.irat)


class Ulomek:
    def __init__(self, st, im):
        # st je Koren, im je int
        self.st = st
        self.im = im
    def __str__(self):
        return f'{self.st}/{self.im}'
    def eval(self):
        return self.st.eval()/self.im

def sestej(r1, r2):
    im = lcm(r1.im, r2.im)
    st1 = k_skalar(r1.st, im/r1.im)
    st2 = k_skalar(r2.st, im/r2.im)
    st = k_sestej(st1, st2)
    d = gcd(k_gcd(st), im)
    rez = Ulomek(k_skalar(st, 1/d), int(im/d))
    return rez

def odstej(r1, r2):
    minus_r2 = Ulomek(k_neg(r2.st), r2.im)
    return sestej(r1,minus_r2)

def zmnozi(r1, r2):
    st = k_zmnozi(r1.st, r2.st)
    im = r1.im*r2.im
    d = gcd(k_gcd(st), im)
    rez = Ulomek(k_skalar(st, 1/d), int(im/d))
    return rez

def lambda_I(l, n):
    result = [[Ulomek(Koren(0),1) for i in range(n)] for j in range(n)]
    for i in range(n):
        result[i][i] = l
    return result

def m_sestej(A, B):
    result = [[Ulomek(Koren(0),1) for i in range(len(A[0]))] for j in range(len(B))]
    for i in range(len(A)):
        for j in range(len(A[i])):
            result[i][j] = sestej(A[i][j], B[i][j])
    return result

def m_odstej(A, B):
    result = [[Ulomek(Koren(0),1) for i in range(len(A[0]))] for j in range(len(B))]
    for i in range(len(A)):
        for j in range(len(A[i])):
            result[i][j] = odstej(A[i][j], B[i][j])
    return result

def m_zmnozi(A,B):
    result = [[Ulomek(Koren(0),1) for i in range(len(A[0]))] for j in range(len(B))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] = sestej(result[i][j], zmnozi(A[i][k], B[k][j]))
    return result

def print_matrix(P, eval=False):
    print()
    for i in range(len(P)):
        row = ""
        for j in range(len(P[i])):
            if not eval:
                if P[i][j].im == 1 or P[i][j].st == 0:
                    row += "   " + str(P[i][j].st) + "   "
                else:
                    row += "  " + str(P[i][j]) + "  "
            else:
                row += "  " + str(round(P[i][j].eval(), 2)) + "  "
        row += "\n"
        print(row)
    print()

kor1 = Koren(1,3,2)
kor2 = Koren(2,-1,2)
kor3 = Koren(2,-1,3)

a = Ulomek(Koren(1),2)
b = Ulomek(Koren(1),3)
c = Ulomek(Koren(1),4)
d = Ulomek(Koren(1),1)
z = Ulomek(Koren(0),1)

P = [
    [z,b,b,b,z],
    [a,z,a,z,z],
    [c,c,z,c,c],
    [a,z,a,z,z],
    [z,z,d,z,z]
]

l1 = Ulomek(Koren(1),1)
l2 = Ulomek(Koren(-1),2)
l3 = Ulomek(Koren(0), 1)
l4 = Ulomek(Koren(-3,1,33), 12)
l5 = Ulomek(Koren(-3,-1,33), 12)

imenovalec = zmnozi(zmnozi(odstej(l1,l2), odstej(l1,l3)), zmnozi(odstej(l1,l4), odstej(l1,l5)))

Pml2 = m_odstej(P, lambda_I(l2, 5))
Pml3 = m_odstej(P, lambda_I(l3, 5))
Pml4 = m_odstej(P, lambda_I(l4, 5))
Pml5 = m_odstej(P, lambda_I(l5, 5))

Pml23 = m_zmnozi(Pml2, Pml3)
Pml234 = m_zmnozi(Pml23, Pml4)
Pml2345 = m_zmnozi(Pml234, Pml5)