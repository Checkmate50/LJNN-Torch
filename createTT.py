import math
import sys

class Atom:
    def __init__(self, pos, box, symmFun):
        #Note that the box and atom are translated so that the box originates at (0, 0, 0)
        if len(box) != len(pos):
            print("WARNING: an atom was initialized with differing box and pos dimensions")
        self.box = []
        for i in box:
            self.box.append(i[1]-i[0])
        self.pos = []
        for i in range(len(box)):
            self.pos.append(pos[i]+self.box[i]+box[i][0])
        self.symmFun = symmFun

    def symmDist(self, other):
        """
        Figures out the closest 'version' of the other atom assuming the box approximation
        Returns the symmetry function result associated with this closest version
        """
        
        self.checkDim(other)
        diffs = [self.pos[i]-other.pos[i] for i in range(len(self.pos))]
        r_vals = []
        
        r_vals.append(math.sqrt(sum([i**2 for i in diffs])))
        for i in range(len(self.box)):
            diffs[i] += self.box[i]  #positive shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] -= self.box[i]*2  #negative shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] += self.box[i]  #return to original

        return self.symmFun(min(r_vals))

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

def readAtomData(filename, symmFun = lambda x : x):
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
            atoms.append(Atom(pos, box, symmFun))
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

def writeBatch(filename, atoms, pe):
    """
    Given a filename and list of atoms
    This function writes the test batch to the given file
    Note that the values written correspond to the symmetry functions of the atoms
    """
    
    f = open(filename, 'w')

    for i in range(len(atoms)):
        for j in range(len(atoms)):
            if i == j:
                continue
            f.write(str(atoms[i].symmDist(atoms[j])) + " ")
        f.write("\n")

    f.write(str(pe) + "\n")
    f.close()

def main():
    atomData = readAtomData("lammps_data/first.lammpstrj")
    thermoData = readThermoData("lammps_data/log.lammps")
    writeBatch("test.txt", atomData[0], thermoData[0])

if __name__ == "__main__":
    main()
