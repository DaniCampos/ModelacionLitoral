# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import tqdm
import random
import math
import matplotlib as mpl
from multiprocessing import Process
from matplotlib import cm

ITERATIONS = 1000


def atmosfera(tmar, pos, dh):
    return (tmar - (6 * (pos - dh)) / 1000)


def tempmar(hora):
    if hora in range(0, 8 + 1):
        return 4
    if hora in range(8 + 1, 16 + 1):
        return 4 + 2 * (hora - 8)
    if hora in range(16 + 1, 24 + 1):
        return 20 - 2 * (hora - 16)


def tempfabrica(hora):

    return 500 * (math.cos(hora*math.pi/12) + 2)


def solve(lit,hora):

    for j in range(0, lit.cantmar):
        lit.matrix[lit.h - 1, j] = tempmar(hora)

    for i in range(0, lit.h):
        for j in range(0, lit.w):
            if math.isnan(lit.matrix[i, j]):
                continue
            else:
                lit.matrix[i, j] = atmosfera(tempmar(hora), (lit.h - 1 - i) * lit.dh, lit.dh)

    lit.iterate()
    print lit
    lit.plot(("Litoral sin Planta Industrial, en t = " + str(hora)))


def solvefab(lit,hora):

    for j in range(0, lit.cantmar):
        lit.matrix[lit.h - 1, j] = tempmar(hora)

    for i in range(0, lit.h):
        for j in range(0, lit.w):
            if math.isnan(lit.matrix[i, j]):
                continue
            else:
                lit.matrix[i, j] = atmosfera(tempmar(hora), (lit.h - 1 - i) * lit.dh, lit.dh)

    cantfabrica = 100/lit.dh

    for k in range(lit.cantmar - 1, lit.cantmar - 1 - cantfabrica, -1):
        lit.matrix[lit.h - 1 , k] = tempfabrica(hora)

    lit.iterate()
    print lit
    lit.plotfab(("Litoral con Planta Industrial, en t = " + str(hora)))

class Litoral(object):
    def __init__(self, ancho, alto, h):
        """
        Constructor
        :param ancho: Ancho del sistema
        :param alto: Alto del sistema
        :param h: Espaciado de la malla
        """
        # Almacenamos valores
        self.ancho = ancho
        self.alto = alto
        self.dh = h

        # Almacenamos cantidad de celdas de mi matriz
        self.w = ancho / h
        self.h = alto / h

        # Creamos la matriz (mallado)
        self.matrix = np.zeros((self.h, self.w))

        # Condición de borde

        # :param i: porcentaje de mar
        i = random.randrange(30, 40)

        # :param cantmar = cantidad de celdas que tienen mar
        # cantmar - 1 es el índice donde termina el mar, cerro comienza en el indice cantmar
        cantmar = self.w * i / 100
        self.cantmar = cantmar
        # Creamos la primera linea de la matriz
        #for j in range(0, cantmar):
          #  self.matrix[self.h - 1, j] = tempmar(self.hora)
        for k in range(self.cantmar, self.w):
            self.matrix[self.h - 1, k] = np.nan;


        # Creamos el borde de la coordillera

        ei = self.h - 2
        ej = cantmar
        self.matrix[ei,ej] = np.nan

        for l in range(cantmar + 1, self.w, 1):
            if (ei>self.h - 2):
                ei = ei - 1
            elif (ei < 1):
                ei = ei + 1

            ie = random.randint(ei - 1, ei + 1)
            self. matrix[ie,l] = np.nan
            ei  = ie

        # Rellenamos la coordillera con nan's

        for n in range(0, self.h):
            for m in range(0,self.w):
                if math.isnan(self.matrix[n,m]):
                    for p in range(n + 1, self.h - 1,1):
                        self.matrix[p,m] = np.nan



    def __str__(self):
        """
        Imprime la matriz,
        :return:
        """
        print self.matrix
        return ''

    def iterate(self):
        """
        Itera
        :return: Retorna nada, hace algo
        """

        for _ in tqdm.tqdm(range(ITERATIONS)):

            # Trabajamos en el interior del sistema
            for i in range(self.h - 2, 0 , -1):  # fila
                for j in range(1, self.w - 1):  # columnas

                    if math.isnan(self.matrix[i,j]):
                        continue

                    elif (math.isnan(self.matrix[i + 1, j]) & math.isnan(self.matrix[i, j - 1]) & math.isnan(self.matrix[i, j + 1])):
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + 3*15)

                    elif (math.isnan(self.matrix[i + 1, j]) & math.isnan(self.matrix[i, j - 1])):
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + 15 + 15 + self.matrix[i, j + 1])

                    elif (math.isnan(self.matrix[i + 1, j]) & math.isnan(self.matrix[i, j + 1])):
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + 15 + self.matrix[i, j - 1] + 15)

                    elif (math.isnan(self.matrix[i, j - 1]) & math.isnan(self.matrix[i, j + 1])):
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + self.matrix[i + 1, j] + 15*2)

                    elif math.isnan(self.matrix[i + 1, j]):
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + 15 + self.matrix[i, j - 1] - self.matrix[i, j + 1])

                    elif math.isnan(self.matrix[i, j - 1]):
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + self.matrix[i + 1, j] + 15 + self.matrix[i, j + 1])

                    elif math.isnan(self.matrix[i, j + 1]):
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + self.matrix[i + 1, j] + self.matrix[i, j - 1] + 15)


                    else:
                        self.matrix[i, j] = 0.25 * (self.matrix[i - 1, j] + self.matrix[i + 1, j] + self.matrix[i, j - 1] + self.matrix[i, j + 1])




    def plot(self,titulo):
        """
        Plotea la solución
        :return:
        
        """

        mpl.rcParams['axes.facecolor'] = '000000'

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(titulo)
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        extnt = [0, self.ancho, 0, self.alto];


        # Se agrega grafico al plot

        cax = ax.imshow(self.matrix,interpolation='none', extent=extnt)
        fig.colorbar(cax)

        plt.show()

    def plotfab(self, titulo):
        """
        Plotea la solución
        :return:

        """

        mpl.rcParams['axes.facecolor'] = '000000'

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(titulo)
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        extnt = [0, self.ancho, 0, self.alto];

        # Se agrega grafico al plot

        cax = ax.imshow(self.matrix, interpolation='none', extent=extnt, cmap=cm.gist_stern)
        fig.colorbar(cax)

        plt.show()


if __name__ == '__main__':

    lit = Litoral(4000, 2000, 50)

    p1 = Process(target=solve(lit,0))
    p1.start()
    p1f = Process(target=solvefab(lit, 0))
    p1f.start()

    p2 = Process(target=solve(lit,8))
    p2.start()
    p2f = Process(target=solvefab(lit, 8))
    p2f.start()

    p3 = Process(target=solve(lit,12))
    p3.start()
    p3f = Process(target=solvefab(lit, 12))
    p3f.start()

    p4 = Process(target=solve(lit, 16))
    p4.start()
    p4f = Process(target=solvefab(lit, 16))
    p4f.start()

    p5 = Process(target=solve(lit, 20))
    p5.start()
    p5f = Process(target=solvefab(lit, 20))
    p5f.start()


