import numpy as np
from random import uniform
import matplotlib.image as img
from copy import deepcopy
import math
import matplotlib.pyplot as plt

def sigmoid(x):
    try:
        ans = 1 / (1 + math.exp(-x))
    except OverflowError:
        ans = float('inf')
    return ans




class ConvLayer():

    def __init__(self, nbFilters = 1, entryW=4, entryH=4, entryD=3,filterSize = 3, stride=1, zeroPad=1, lr = 0.2): #For 1 channel = for 1 dim im

        # Calcul des dimensions de la sortie
        # depend de zeroPad et de stride
        self.layW = int((entryW-filterSize+2*zeroPad)/stride +1)
        self.layH = int((entryH-filterSize+2*zeroPad)/stride +1)
        self.entryH = entryH
        self.entryW = entryW
        self.entryD = entryD
        self.zeroPad = zeroPad      #Zeropadding : nombre de couches de zeros autour de l'image
        self.stride = stride        #Pas de la convolution
        self.learningRate = lr
        self.nbFilters = nbFilters
        self.filterSize = filterSize

        self.activationTable = []
        self.filterTable = []
        self.biasTable = []
        self.filterErrors = []
        self.biasErrors = []
        self.deltaTable = []
        self.outputD = nbFilters*entryD


        for i in range(nbFilters):
            self.filterTable.append(np.random.uniform(0, 0.05, size = (filterSize, filterSize)))
            self.filterErrors.append( np.zeros(shape = (filterSize, filterSize)))

        for j in range(self.outputD):
            self.biasTable.append(np.random.uniform(0, 0.05, size = (self.layH, self.layW)))
            self.biasErrors.append( np.zeros(shape = (self.layH, self.layW)))
            self.activationTable.append( np.zeros( (self.layH, self.layW) ))
        self.modEntry = np.zeros( shape = (entryD, self.layW +2*self.zeroPad, self.layH +2*self.zeroPad) )

        for k in range(entryD):
            self.deltaTable.append( np.zeros(shape = (self.entryH, self.entryW)))




    def propagation(self, prevLayer):
        # on copie l'image a traiter, elle va etre modifiee
        #prevLayer = np.reshape(prevLayer, (self.nbFilters, ))
        imageCp = deepcopy(prevLayer)
        # ajout de zeros autour de l'image depend de l'entier zeroPad
        for k in range(self.zeroPad):
            imageCp = np.insert(imageCp, imageCp.shape[1], 0, axis = 1)
            imageCp = np.insert(imageCp, imageCp.shape[2], 0, axis = 2)
            imageCp = np.insert(imageCp,0,0, axis = 1)
            imageCp = np.insert(imageCp,0,0, axis = 2)

        # calcul de la sortie
        #imageCp = np.reshape(imageCp, (self.entryD, self.layW+2*self.zeroPad, self.layH+2*self.zeroPad))
        self.modEntry = imageCp
        # pour chaque couleur
        for channel in  range(prevLayer.shape[0]):
            for filters in range(self.nbFilters):
                # i: lignes
                for i in range(0, imageCp.shape[1]-2*self.zeroPad-2, self.stride):
                    # j : colonnes
                    for j in range(0, imageCp.shape[2]-2*self.zeroPad-2, self.stride):
                        # on calcule la sortie (self.activationTable)
                        self.activationTable[(channel+1)*filters][i,j] =sigmoid((np.multiply(
                        # le morceau de l'image a convoluer
                        imageCp[channel,i: i+self.filterSize,
                        j: j+self.filterSize],
                        # le filtre
                        np.rot90(self.filterTable[filters], 2))).sum()) # rot180 pour faire une convolution et pas un correlation
                        # le biais
                        #+ self.filterBias[i,j,channel])



    def computeDeltaTable(self, nextDeltaTable, prevlayer):
        nextDeltaTable = np.reshape(nextDeltaTable, (self.outputD, self.layW,self.layH))
        deltaTableMod = deepcopy(nextDeltaTable)

        for k in range(self.filterSize-1):
            deltaTableMod = np.insert(deltaTableMod, deltaTableMod.shape[1], 0, axis = 1)
            deltaTableMod = np.insert(deltaTableMod, deltaTableMod.shape[2], 0, axis = 2)
            deltaTableMod = np.insert(deltaTableMod,0,0, axis = 1)
            deltaTableMod = np.insert(deltaTableMod,0,0, axis = 2)

        #deltaTable : table des erreurs des activationTables (deltas)
        #weightsTable : table des erreurs des poids
        for channel in range(self.entryD):
            for filters in range(self.nbFilters):
            # print("deltatable mod: ", np.array(deltaTableMod).shape)
            # print("prevLayer: ", np.array(prevlayer).shape)
            # print("input size : ", self.entryH, self.entryW)
            # print("self delta: ", np.array(self.deltaTable).shape)
            #Pour chaque couleur
                for i in range(self.entryH):
                    for j in range(self.entryW):
                        #Calcul de self.deltaTable
                        self.deltaTable[channel][i,j] +=  np.multiply(
                        # la deltaTable de la couche suivante
                        deltaTableMod[filters,i: i+self.filterSize,j: j+self.filterSize],
                        np.rot90(self.filterTable[filters], 0)
                        # derivee de la sigmoide
                        ).sum() * prevlayer[channel][i, j]*(1-prevlayer[channel][i, j])





    def computeWeightsTable(self, prevLayer, deltaTable):

            for filter in range(self.nbFilters):
                print("mod: ", self.modEntry.shape)
                print("prev: ", np.array(prevLayer).shape)
                # ca c'est mieux, verifier les indices
                for m in range(self.filterSize):
                    for n in range(self.filterSize):
                        self.filterErrors[filter][m, n] += np.multiply(
                        np.rot90(deltaTable[filter],2),
                        self.modEntry[filter, m: m+self.layW, n: n+self.layH]
                        ).sum()



    def updateParams(self, nbTrainings):
        for filter in range(self.nbFilters):
            for channel in range(self.entryD):
                        self.filterTable[filter][channel] -= self.learningRate * ( 1/float(nbTrainings) * self.filterErrors[filter][channel])
                        self.filterErrors[filter][ channel] = 0
                        self.biasTable[filter][channel] -= self.learningRate * ( 1/float(nbTrainings) * self.biasErrors[filter][channel])
                        self.biasErrors[filter][channel] = 0

"""
# Petit test
a = ConvLayer2D(entryW = 1200, entryH = 800)
# Matrice de detection de contour par exemple
a.filterWeights = [[[-1,0,1],[-2,0,2],[-1,0,1]],
[[-1,0,1],[-2,0,2],[-1,0,1]],
[[-1,0,1],[-2,0,2],[-1,0,1]]]
image = img.imread('castle.jpg')
a.feedforward(image)
fig = plt.figure(figsize=(image.shape[0],image.shape[1]))


fig.add_subplot(2,2,1)
plt.imshow(image)
fig.add_subplot(2,2,2)
plt.imshow(a.activationTable[::,::,0])
fig.add_subplot(2,2,3)
plt.imshow(a.activationTable[::,::,1])
fig.add_subplot(2,2,4)
plt.imshow(a.activationTable[::,::,2])
plt.show()
"""