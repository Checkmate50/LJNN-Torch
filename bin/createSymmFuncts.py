from functools import partial
import helper
from math import pi
import math


class SymmFunct2:
    def __init__(self, g, f, fatom, tatom, eta, Rs, Rc):
        self.f = f
        self.g = getG(g)
        self.fatom = fatom
        self.tatom = tatom
        self.Rc = Rc
        self.eta = eta
        self.Rs = Rs
        self.data = []
        self.info = []

    def call(self, i, atomList, box):
        # Adds the given calculation to data and returns that value
        self.data.append(self.g(self.f, self.Rc, self.eta, self.Rs, i, atomList, box))
        return self.data[-1]

    def set_info(self):
        self.info = [min(self.data), max(self.data), sum(self.data)/len(self.data)]

    def clean(self):
        self.data = []
    
    def scaled(self, index, scale_min, scale_max):
        datamin = self.info[0]
        datamax = self.info[1]
        value = self.data[index]
        # To confirm this function:  https://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
        return ((scale_max-scale_min)*(value-datamin)/(datamax-datamin)) + scale_min

    def data_info(self):
        return " ".join(map(str, self.info))
        
    def __str__(self):
        return "symfunction_short " + self.fatom + " 2 " + self.tatom + " " + str(self.eta) + " " + str(self.Rs) + " " + str(self.Rc)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if isinstance(other, SymmFunct3):
            return True
        if self.Rc == other.Rc:
            if self.eta == other.eta:
                return self.Rs < other.Rs
            return self.eta < other.eta
        return self.Rc < other.Rc


class SymmFunct3:
    def __init__(self, g, f, fatom, tatom, thatom, Rc, eta, Rs, zeta, lamb):
        self.f = f
        self.g = g
        self.fatom = fatom
        self.tatom = tatom
        self.thatom = thatom
        self.Rc = Rc
        self.eta = eta
        self.Rs = Rs
        self.zeta = zeta
        self.lamb = lamb
        self.data = []

    def call(self, i, atomList, box):
        # UPDATE
        # Adds the given calculation to data and returns that value
        self.data.append(self.g(self.f, self.Rc, self.eta, self.Rs, i, atomList, box))
        return data[-1]

    def set_info(self):
        self.info = [min(self.data), max(self.data), sum(self.data)/len(self.data)]

    def clean(self):
        self.data = []
    
    def scaled(self, index, scale_min, scale_max):
        datamin = self.info[0]
        datamax = self.info[1]
        value = self.data[index]
        # To confirm this function:  https://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
        return ((scale_max-scale_min)*(value-datamin)/(datamax-datamin)) + scale_min

    def data_info(self):
        return " ".join(map(str, self.info))
        
    def __str__(self):
        return "symfunction_short " + self.fatom + " 2 " + self.tatom + " " + self.thatom + " " + str(self.eta) + " " + str(self.lamb) + " " + str(self.zeta) + " " + str(self.Rs) + " " + str(self.Rc)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if isinstance(other, SymmFunct2):
            return False
        if self.Rc == other.Rc:
            if self.eta == other.eta:
                if self.zeta == other.zeta:
                    if self.lamb == other.lamb:
                        return self.Rs < other.Rs
                    return self.lamb < other.lamb
                return self.zeta < other.zeta
            return self.eta < other.eta
        return self.Rc < other.Rc
        

def f1(Rc, Rij):
    if Rij > Rc:
        return 0
    return .5*(math.cos(pi*Rij/Rc)+1)

def f2(Rc, Rij):
    if Rij > Rc:
        return 0
    return math.tanh(1-(Rij/Rc))**3

def getFc(i):
    if i == 1:
        return f1
    elif i == 2:
        return f2
    else:
        helper.print_warning("WARNING: " + str(i) + " unrecognized cutoff function number")

def g1(f, Rc, eta, Rs, i, atomList, box):
    fc = getFc(f)
    sum = 0
    for j in atomList:
        if i == j:
            continue
        Rij = i.calcDist(j, box)
        sum += fc(Rc, Rij)
    return sum

def g2(f, Rc, eta, Rs, i, atomList, box):
    fc = getFc(f)
    sum = 0
    for j in atomList:
        if i == j:
            continue
        Rij = i.calcDist(j, box)
        sum += math.exp(-eta*(Rij-Rs)**2)*fc(Rc, Rij)
    return sum

def getG(i):
    if i == 1:
        return g1
    elif i == 2:
        return g2
    else:
        helper.print_warning("WARNING: " + str(i) + " unrecognized g funciton number")
        return g1
