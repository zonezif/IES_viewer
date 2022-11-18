import numpy as np
import matplotlib.pyplot as plt
import math

filt = 0.1
angulo = 6
page = './out/'


def abrir(name, nick):

    with open(name, "r") as f:
        reader = f.read()

    x = reader
    x = x.splitlines()

    data = ""
    cabeçalho = []

    for i in range(len(x)):
        if(x[i] == 'TILT=NONE'):
            for j in x[i+1:]:
                data += j
                cabeçalho = x[:i]
            break
    dic = {}

    for i in cabeçalho:
        if(len(i.split()) > 1):
            dic[i.split()[0]] = i.split(']')[1:]

    if(nick == 0):
        data = data[:]
        return data

    if(nick == 1):
        data = data[4:len(data)-1]
        return data

    if(nick == 2):
        return(dic)


def coord(data, angle):

    ex = angle
    defase = ex+int(len(data)/2)

    if(defase > len(data)-1):
        defase = defase-len(data)

    if(ex > len(data)-1):
        ex = ex-len(data)

    vet = data[defase]

    vet = vet[0:len(vet)-1]

    vet2 = data[ex]

    vet2 = vet2[0:len(vet2)-1]

    val = []
    l = len(vet2)

    for i in vet:
        val.append(float(i))

    for i in range(len(vet2)):
        val.append(float(vet2[l-1-i]))
    return val


def rad(vet):
    rads = []

    x = range(len(vet))

    for i in x:
        rads.append(float(i)*np.pi/180-np.pi/2)

    return rads


def grad(vet):
    grads = []

    x = range(int(len(vet)/2), 0, -1)
    for i in x:
        grads.append(i)

    x = range(int(len(vet)/2))

    for i in x:
        grads.append(i)

    return grads


class IES(object):

    def __init__(self, arq):
        self.x = abrir(arq, 0).split(" ")
        self.off = 0

        AngV = [0]
        self.off = int(self.Nang())+11

        for i in self.x[12:self.off]:
            AngV.append(float(i))

        self.angv = AngV

        AngH = []
        for i in self.x[self.off:int(self.Nah())+self.off]:
            AngH.append(float(i))
        self.angh = AngH

        Cd = []

        self.off += int(self.Nah())

        for j in range(int(self.Nah())):
            cd = []
            for i in self.x[self.off:int(self.Nang())+self.off]:
                cd.append(float(i))
            self.off += int(self.Nang())
            Cd.append(cd)
        self.Xd = Cd

        self.dic = abrir(arq, 2)

    def Lm(self):
        return float(self.x[1])  # Fluxo

    def Fat(self):
        return float(self.x[2])  # Fator de multiplicação

    def Nang(self):
        return self.x[3]  # Numeros de angulos da teia

    def Nah(self):
        return self.x[4]  # numero de angulos horizontais

    def Unid(self):
        return self.x[6]  # Unidade 1 para pes 2 para metros

    def AngV(self):
        return self.angv

    def AngH(self):
        return self.angh

    def Cd(self):
        return self.Xd

    def Dic(self):
        return self.dic


ies1 = IES("m1.ies")

Valplt = coord(ies1.Cd(), angulo)  # valor em Cd para cada angulo

maxmd = [0, 0]
maxme = [0, 0]

for i, j in zip(Valplt, range(len(Valplt))):
    if (i > maxmd[0] and j < int(len(Valplt)/2)):
        maxmd[0] = i
        maxmd[1] = float(j)

    if (i > maxme[0] and j > int(len(Valplt)/2)):
        maxme[0] = i
        maxme[1] = float(j)
print(i, j)


plt.figure(figsize=(10, 10))
plt.axes(projection='polar')

x1 = list(range(90, 180, 10))
x2 = sorted(x1, key=int, reverse=True)
x3 = list(range(10, 90, 10))
x4 = sorted(x3, key=int, reverse=True)
x = x1+[180]+x2+x4+[0]+x3

plt.thetagrids(range(0, 360, 10), x)
plt.title("Distribuição de intensidade luminosa na Curva\n", fontsize=16)
plt.quiver(0, 0, maxmd[1]*np.pi/180-np.pi/2, maxmd[0], color='red',
           angles="xy", scale_units='xy', scale=1.)
plt.fill(rad(Valplt), Valplt, '.r', alpha=0.2)
plt.quiver(0, 0, maxme[1]*np.pi/180-np.pi/2, maxme[0], color='blue',
           angles="xy", scale_units='xy', scale=1.)


plt.figure(figsize=(10, 10))
plt.plot(grad(Valplt), Valplt[180:] + Valplt[0:180])
plt.title('Distribuição de intensidade luminosa\n')
plt.show()

'''plt.quiver(0, 0, maxmd[1], maxmd[0], color='red',
           angles="xy", scale_units='xy', scale=1.)
plt.quiver(0, 0, maxme[1], maxme[0], color='blue',
           angles="xy", scale_units='xy', scale=1.)

plt.quiver(0, 0, (maxmd[1]-(maxme[1]+float(90*2-i)*np.pi/180))+np.pi, (maxmd[0]+maxme[0])/2, color='g',
           angles="xy", scale_units='xy', scale=1.)'''

'''plt.plot(rad(coord(ies1.Cd(), angulo+6)),
         coord(ies1.Cd(), angulo+6), '-b', alpha=0.1)'''
'''plt.fill(rad(coord(ies1.Cd(), angulo+6)),
         coord(ies1.Cd(), angulo+6), '-b', alpha=0.1)'''
# plt.savefig(page+'Saida.png')
