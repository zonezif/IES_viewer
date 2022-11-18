import numpy as np
import matplotlib.pyplot as plt

filt = 0.1
angulo = 4
page = './out/'


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


def cord(data, angle):

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
    return vet


def angles():
    x1 = list(range(90, 180, 10))
    x2 = sorted(x1, key=int, reverse=True)
    x3 = list(range(10, 90, 10))
    x4 = sorted(x3, key=int, reverse=True)
    x = x1+[180]+x2+x4+[0]+x3

    return x


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


def distr(vet2, vet1):
    val = []
    l = len(vet2)
    for i in vet1[:len(vet1)-1]:
        val.append(float(i))

    for i in range(len(vet2)-1):
        val.append(float(vet2[l-1-i]))

    return val


def rad(vet):
    rads = []
    x = range(len(vet))
    for i in x:
        rads.append(float(i)*np.pi/180-np.pi/2)
    return rads


def med(data):
    sum = 0
    for i in data:
        sum += float(i)
    return sum/len(data)


def difere(dd1, dd2):
    P = 0
    for ang in range(int(len(dd1)/2)):
        d1 = coord(dd1, ang)
        d2 = coord(dd2, ang)

        result = []

        for i in range(len(coord(dd1, ang))):
            if(d1[i] > (med(d1)*filt) and d2[i] > med(d2)*filt):
                result.append(abs((((d1[i]+0.01)/(d2[i]+0.01))-1)*100))
            else:
                result.append(0)
        sum = 0

        for i in result:
            sum += i
        P += sum/len(result)

    P = P/12
    return P


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

ies2 = IES("m2.ies")

result = []
ignor = []

dd1 = ies1.Cd()
dd2 = ies2.Cd()

df = difere(dd1, dd2)

print(df)

for i in range(len(cord(dd2, angulo))):
    d1 = cord(dd2, angulo)
    d2 = cord(dd2, angulo+12)

    if(d1[i] > (med(d1)*filt) and d2[i] > med(d2)*filt):
        result.append(abs((((d1[i]+0.01)/(d2[i]+0.01))-1)*100))
        ignor.append(0)
    else:
        result.append(0)
        ignor.append(1)

x1 = list(range(90, 180, 10))
x2 = sorted(x1, key=int, reverse=True)

x3 = list(range(10, 90, 10))
x4 = sorted(x3, key=int, reverse=True)

x = x1+[180]+x2+x4+[0]+x3

# tamanho da figura
plt.figure(figsize=(10, 10))
plt.axes(projection='polar')

# divisão de graus
plt.thetagrids(range(0, 360, 10), x)

# titulo do grafico
plt.title("Distribuição de intensidade luminosa na Curva A", fontsize=16)

plt.fill(rad(coord(ies1.Cd(), angulo)), coord(
    ies1.Cd(), angulo), '-r', alpha=0.2)

plt.plot(rad(coord(ies1.Cd(), angulo)), coord(
    ies1.Cd(), angulo), '-r', alpha=0.2)

plt.plot(rad(coord(ies1.Cd(), angulo+6)),
         coord(ies1.Cd(), angulo+6), '-b', alpha=0.2)

plt.fill(rad(coord(ies1.Cd(), angulo+6)),
         coord(ies1.Cd(), angulo+6), '-b', alpha=0.2)

plt.savefig(page+'CurvaA.png')

plt.figure(figsize=(10, 10))
plt.axes(projection='polar')
plt.thetagrids(range(0, 360, 10), x)
plt.title("Distribuição de intensidade luminosa na Curva B", fontsize=16)
plt.plot(rad(coord(ies2.Cd(), angulo)), coord(ies2.Cd(), angulo), '-r')
plt.fill(rad(coord(ies2.Cd(), angulo)), coord(
    ies2.Cd(), angulo), 'r', alpha=0.2)
plt.plot(rad(coord(ies2.Cd(), angulo+6)),
         coord(ies2.Cd(), angulo+6), '-b', alpha=0.2)
plt.fill(rad(coord(ies2.Cd(), angulo+6)),
         coord(ies2.Cd(), angulo+6), '-b', alpha=0.2)

plt.savefig(page+'CurvaB.png')

plt.figure(figsize=(10, 10))
plt.axes(projection='polar')
plt.thetagrids(range(0, 360, 10), x)
plt.title(
    "Distribuição de Difernça da intensidade luminosa de A e B ", fontsize=16)
plt.plot(rad(result), result, '-b')
plt.plot(rad(ignor), ignor, '-r')
plt.quiver(0, 0, 00, 100, color='black',
           angles="xy", scale_units='xy', scale=1.)


plt.legend(["Diferença = "+str(df)[:7]+"%",
           "Filtro de Ruido de fundo"], loc='best', fontsize=16)

plt.savefig(page+'Resultado.png')

print(ies1.Dic()['[_CURRENT]'][0].split()[0])
'''
arquivo = open(page+'Resultados.txt', 'w', encoding='utf-8')
arquivo.write("\tCoparação entre .IES's\n\n")
arquivo.write("Fluxo 1 = "+str(ies1.Lm())+" Lm\n")
arquivo.write("Fluxo 2 = "+str(ies2.Lm())+" Lm\n")
arquivo.write("Diferenca de fluxo = " +
              str((ies1.Lm()/ies2.Lm()-1)*100)[:7]+"%\n")
arquivo.write("\n")
arquivo.write(
    "Difernça de Distribuição da intensidade luminosa = "+str(df)[:7]+"%\n")

arquivo.write("Potência 1 = "+str(float(ies1.Dic()
              ['[_VOLTAGE]'][0].split()[0])*float(ies1.Dic()['[_CURRENT]'][0].split()[0]))+"W\n")
arquivo.write("Potência  2 = "+str(ies2.Dic())+" Lm\n")
arquivo.write("Diferenca de fluxo = " +
              str((ies1.Lm()/ies2.Lm()-1)*100)[:7]+"%\n")
arquivo.close()
'''
# plt.show()
