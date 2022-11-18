import numpy as np
import matplotlib.pyplot as plt

filt = 0.1
angulo = 1
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

print(len(ies1.Cd()[24]))

# plt.show()
