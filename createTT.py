import math
import random
import sys
from createSymmFuncts import getFuncts

class Atom:
    def __init__(self, pos, box):
        #Note that the box and atom are translated so that the box originates at (0, 0, 0)
        if len(box) != len(pos):
            print("WARNING: an atom was initialized with differing box and pos dimensions")
        self.box = []
        for i in box:
            self.box.append(i[1]-i[0]) #Collapse box dimensions
        self.pos = []
        for i in range(len(box)):
            self.pos.append(pos[i]-box[i][0]) #Shift into new box

    def calcDist(self, other):
        """
        Figures out the closest 'version' of the other atom assuming the box approximation
        Returns the symmetry function result associated with this closest version
        """
        
        self.checkDim(other)
        diffs = [self.pos[i]-other.pos[i] for i in range(len(self.pos))]
        r_vals = []

        #Account for x, y extensions out of box
        r_vals.append(math.sqrt(sum([i**2 for i in diffs])))
        for i in range(len(self.box)):
            diffs[i] += self.box[i]  #positive shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] -= self.box[i]*2  #negative shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] += self.box[i]  #return to original

        return min(r_vals)

    def checkDim(self, other):
        #Prints dimension warnings as needed
        if len(self.pos) != len(other.pos):
            print("WARNING: two compared atoms have different position dimensions")
        if len(self.box) != len(other.box):
            print("WARNING: two compared atoms have different box dimensions")
        else:
            for i in range(len(self.box)):
                if self.box[i] != other.box[i]:
                    print("WARNING: two compared atoms have different box values")
                
    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return self.__str__()

def readAtomData(filename):
    """
    Reads in the atoms of a lammps trj file and assigns them the symmetry function symmFun
    Assumes that the following is dumped in order: id type x y z [whatever else]
    Returns an array of atoms for each time step (combined as an array)
    """

    if not filename.endswith("lammpstrj"):
        print("WARNING: the atom file " + filename + " is not an apparent lammps trajectory file")
    
    f = open(filename, 'r')
    count = 0
    box = []
    data = []
    atoms = []
    
    for line in f:
        if line.strip() == "ITEM: TIMESTEP":
            count = 0
            box = []
            if len(atoms) > 0:
                data.append(atoms)
            atoms = []
        if count in [5, 6, 7]:
            box.append([float(i) for i in line.split()])
        if count > 8:
            pos = [float(i) for i in line.split()[2:5]]
            atoms.append(Atom(pos, box))
        count += 1

    data.append(atoms) #Add the last set of atoms
    f.close()
    return data

def readThermoData(filename):
    """
    Given a log file 'filename'
    Reads the potential energy at each timestep
    Returns an array of these energies
    """

    f = open(filename, 'r')
    thermo = []
    while f.readline().strip() != "Step Temp PotEng":
        pass
    while 1:
        vals = f.readline().split()
        if len(vals) != 3:
            break
        thermo.append(float(vals[2]))
        
    f.close()
    return thermo

def shuffleData(atomData, thermoData):
    for i in range(len(atomData)):
        index = random.randint(i, len(atomData)-1)
        atomData[i], atomData[index] = atomData[index], atomData[i]
        thermoData[i], thermoData[index] = thermoData[index], thermoData[i]

def writeBatch(filename, atoms, pe, symmFuncts):
    """
    Given a filename and list of atoms
    This function writes the test batch to the given file
    Note that the values written correspond to the symmetry functions of the atoms
    """

    toWrite = ""

    with open(filename, 'w') as f:
        for i in atoms:
            for funct in symmFuncts:
                f.write(str(funct(i, atoms)) + " ")
            f.write("\n")
        f.write(str(pe) + "\n")

def main():
    if len(sys.argv) < 3:
        print("Must give a path to the train and test folder (respectively) as arguments")
        exit(0)
    trainFolder = sys.argv[1]
    testFolder = sys.argv[2]
    print("Reading atomic data")
    atomData = readAtomData("lammps_data/first.lammpstrj")
    print("Reading thermodynamic data")
    thermoData = readThermoData("lammps_data/log.lammps")
    print("Shuffling data")
    shuffleData(atomData, thermoData)

    #Get Functions
    Rc = 8
    sigma = .5
    count = 20
    functs = getFuncts(Rc, sigma, count)
    
    #Start writing code
    trainRatio = 0.75 #percent of data which becomes training data
    if len(sys.argv) >= 4:
        trainRatio = float(sys.argv[3])
    trainCutoff = int(trainRatio * len(atomData))
    i = 0
    print("Writing " + str(trainCutoff) + " training files and " + str(len(atomData)-trainCutoff) + " testing files")
    while i < trainCutoff:
        print("Writing Training Batch: " + str(i+1))
        writeBatch(trainFolder + str(i+1) + ".nndata", atomData[i], thermoData[i], functs)
        i += 1
    while i < len(atomData):
        print("Writing Test Batch: " + str(i+1-trainCutoff))
        writeBatch(testFolder + str(i+1-trainCutoff) + ".nndata", atomData[i], thermoData[i], functs)
        i += 1

def countInCutoff(atoms, cutoff):
    #Test Function
    with open("dists.txt", 'w') as f:
        for i in atoms:
            count = 0
            for j in atoms:
                if i.calcDist(j) <= cutoff:
                    count += 1
            f.write(str(count) + "\n")
    exit() #Only used for testing stuff...
        
    
if __name__ == "__main__":
    main()
