import numpy as np
import matplotlib.pyplot as plt
import math
import statistics as st
import os

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


def dif(v1, v2, p):
    difer = []
    if(p == 1):
        v2.reverse()
        for i, j in zip(v1, v2):
            difer.append(((np.sqrt((i-j)**2))/max(i, j))*100)
    if(p == 3):
        v2.reverse()
        for i, j in zip(v1, v2):
            difer.append(np.sqrt((i-j)**2))

    if(p == 2):
        return ((np.sqrt(v1-v2)**2))

    if(p == 0):
        return (100*(np.sqrt(v1-v2)**2)/max(v1, v2))

    return difer


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


def Visual(arq, sub, ang):

    print('Abrindo...> ' + arq + ' >>>'+'IES_' + arq)

    ies1 = IES(arq)
    number = (len(ies1.AngH())-1)/2-ang*(len(ies1.AngH())-1)/4
    angulo = int(number)

    if (os.path.exists('./out/'+arq[:int(len(arq)-4)]) != 1):
        os.makedirs('./out/' + arq[:int(len(arq)-4)])

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

    meio = ((maxme[1]-maxmd[1])/2)+maxmd[1]+180

    plt.figure(figsize=(10, 10))

    plt.axes(projection='polar')

    x1 = list(range(90, 180, 10))
    x2 = sorted(x1, key=int, reverse=True)
    x3 = list(range(10, 90, 10))
    x4 = sorted(x3, key=int, reverse=True)
    x = x1+[180]+x2+x4+[0]+x3

    plt.thetagrids(range(0, 360, 10), x)
    plt.title("Distribuição de intensidade luminosa na Curva\n" +
              sub, fontsize=16)
    plt.quiver(0, 0, maxmd[1]*np.pi/180-np.pi/2, maxmd[0], color='red',
               angles="xy", scale_units='xy', scale=1.)
    plt.fill(rad(Valplt), Valplt, '.r', alpha=0.2)
    plt.quiver(0, 0, maxme[1]*np.pi/180-np.pi/2, maxme[0], color='blue',
               angles="xy", scale_units='xy', scale=1.)

    plt.quiver(0, 0, meio*np.pi/180-np.pi/2, (maxme[0]+maxme[0])/2, color='g',
               angles="xy", scale_units='xy', scale=1.)

    plt.text((meio+15)*np.pi/180-np.pi/2, (maxme[0]+maxme[0])/4, 'Diferença em graus = ' +
             str(360-meio)[:5]+" °")

    plt.savefig('./out/' + arq[:int(len(arq)-4)] +
                '/'+'Distribuição_'+sub+'.png')
    # plt.show()

    plt.figure(figsize=(10, 10))
    plt.subplot(2, 1, 1)
    plt.title('Simetria da distribuição luminosa\n'+sub)
    plt.plot(grad(Valplt)[:180], Valplt[180:], color='blue')

    plt.plot(grad(Valplt)[180:], Valplt[0:180], color='red')

    plt.axhline(y=max(Valplt[0:180]), color='r', linestyle='-.', alpha=0.5)

    plt.axhline(y=max(Valplt[180:]), color='b', linestyle='-.', alpha=0.5)

    plt.axvline(x=maxmd[1], color='r', linestyle=':', alpha=0.5)

    plt.axvline(x=360-maxme[1], color='b', linestyle=':', alpha=0.5)

    plt.text(8, dif(max(Valplt[0:180]), max(Valplt[180:]), 2), 'Média da diferença = '+str(
        dif(max(Valplt[0:180]), max(Valplt[180:]), 0))[:5]+"%"+"\nDiferença absoluta = "+str(dif(max(Valplt[0:180]), max(Valplt[180:]), 2)).split(".")[0]+"Cd", style='italic')

    plt.subplot(2, 1, 2)
    plt.fill(grad(Valplt)[:180], dif(Valplt[180:],
                                     Valplt[0:180], 3), color='r', alpha=0.2)

    print(dif(max(Valplt[0:180]), max(Valplt[180:]), 0))

    plt.text(8, max(dif(Valplt[180:], Valplt[0:180], 3)), 'Máxima da diferença = '+str(max(dif(Valplt[180:],
                                                                                               Valplt[0:180], 3)))[:5], style='italic')
    plt.text(8, st.mean(dif(Valplt[180:], Valplt[0:180], 3)), 'Média da diferença = '+str(st.mean(dif(Valplt[180:],
                                                                                                      Valplt[0:180], 3)))[:5], style='italic')
    '''plt.scatter(grad(Valplt)[:180], dif(Valplt[180:],
                                        Valplt[0:180]), c=dif(Valplt[180:], Valplt[0:180]))'''
    plt.axhline(y=st.mean(dif(Valplt[180:],
                              Valplt[0:180], 3)), color='r', linestyle='-', alpha=0.6)

    plt.savefig('./out/' + arq[:int(len(arq)-4)]+'/'+'Simetria_'+sub+'.png')


    # plt.show()
key = 's'

while (key == 's'):
    dire = input("\nArraste a pasta aqui!!").replace('\"', '')
    os.system('cls')
    dire = dire.replace('\'', '')
    dire = dire.replace('&', '')
    if (dire[0] == " "):
        dire = dire[1:]
    print(dire)
    os.chdir(dire)

    page = os.getcwd()
    lista = os.listdir(page)
    IESs = []
    cwd = page

    for i in lista:
        arq = i.split('.')
        if (len(arq) > 1):
            if arq[1] == 'ies':
                if (arq[0].count('IES_') != 1):
                    IESs.append(i)

    if (os.path.exists('out') != 1):
        os.makedirs(page+'//out')
        page += page+'//out'

    # convert('m2.ies')
    u = 0
    for i in IESs:
        Visual(i, '90_270', 0)
        Visual(i, '180_90', 1)
        u += 1

    print('\n', u, 'Arquivos convertidos')
