import math
import random
import os
from sys import argv
from createSymmFuncts import get2Functs, get3Functs
from helper import get_data, combine_dicts
from subprocess import call


"""
This script creates the training and testing files for training and neural network from lammps data.  If generateData is True, this script first generates this data before writing the appropriate files.

Input:
lammpstrj and log file names located in ../lammps_data/
Files should be generated via a run of lammps and follow this format
(OPTIONAL)
Give the folder where the train and test files (respectively) should be placed
[default trainFiles/ and testFiles/]
Additionally, give the location where scaling.data and input.nn should be written
[default ../runner/]

Output:
The train/test files generated via running symmetry functions on the given input files
And the scaling and input information for runner
Note that, as usual, this input information relies on the on information given in main.info
So make sure this file is formatted correctly!!
"""


class Atom:
    def __init__(self, pos):
        #Note that the box and atom are translated so that the box originates at (0, 0, 0)
        self.pos = pos

    def calcDist(self, other, box):
        """
        Figures out the closest 'version' of the other atom assuming the box approximation
        Returns the symmetry function result associated with this closest version
        """
        
        self.checkDim(other)
        diffs = [self.pos[i]-other.pos[i] for i in range(len(self.pos))]
        r_vals = []

        #Account for x, y extensions out of box
        r_vals.append(math.sqrt(sum([i**2 for i in diffs])))
        for i in range(len(box)):
            diffs[i] += box[i]  #positive shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] -= box[i]*2  #negative shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] += box[i]  #return to original

        return min(r_vals)

    def checkDim(self, other):
        #Prints dimension warnings as needed
        if len(self.pos) != len(other.pos):
            print("WARNING: two compared atoms have different position dimensions")
                
    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return self.__str__()


def generateData(lammps_file, seed, runner_scaling):
    """
    Given a lammps_file, seed, and a place to write this information to runner
    Generates the data from the lammps file
    """
    with open("bin/genCommand.bash", "w") as f:
        f.write("lammps -echo screen -var seed " + str(seed) + " < " + lammps_file)
    call(["bash", "bin/genCommand.bash"])
    lammps_filename = lammps_file[(max(lammps_file.rfind("/"), lammps_file.rfind("\\")) + 1):]
    lammps_dir = lammps_file[:(len(lammps_file)-len(lammps_filename))]
    lammpstrj = ""
    log = lammps_dir + "log.lammps"
    # Copy lammps file to the runner folder
    with open(lammps_file, "r") as fi:
        with open(runner_scaling + lammps_filename, "w") as fo:
            for line in fi:
                if line.strip().startswith("pair_style"):
                    fo.write("variable        out equal 100         # frequency of writing thermo quantities to output file\n")
                    fo.write("pair_style 	runner showew no showewsum ${out} maxew 10000 resetew yes dir .\n")
                    line = "#" + line
                elif line.strip().startswith("dump"):
                    lammpstrj = lammps_dir + line[:line.find(".lammpstrj")].split()[-1] + ".lammpstrj"
                elif line.strip().startswith("log"):
                    log = lammps_dir + line.split()[-1]
                fo.write(line)
    if not lammpstrj:
        print("ERROR: lammpstrj file not written using dump, cannot proceed")
        exit()
    return lammpstrj, log
    
    
def readAtomData(filename):
    """
    Reads in the atoms of a lammps trj file and assigns them the symmetry function symmFun
    Assumes that the following is dumped in order: id type x y z [whatever else]
    Returns an array of atoms for each time step (each combined as an array)
    """

    if not filename.endswith("lammpstrj"):
        print("WARNING: the atom file " + filename + " is not an apparent lammps trajectory file")
    
    f = open(filename, 'r')
    count = 0
    box = []
    offsets = []
    data = []
    atoms = []
    
    for line in f:
        if line.strip() == "ITEM: TIMESTEP":
            count = 0
            if len(atoms) > 0:
                data.append(atoms)
            atoms = []
        if count in [5, 6, 7]:
            if len(box) < 3: # We live in a 3D world!
                ls = map(float, line.split())
                box.append(ls[1]-ls[0])
                offsets.append(ls[0])
            
        if count > 8:
            ls = line.split()
            pos = [float(ls[i+2]) - offsets[i] for i in range(3)]
            atoms.append(Atom(pos))
        count += 1

    data.append(atoms) #Add the last set of atoms
    f.close()
    return data, box


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


def writeBatch(filename, atoms, box, pe, symmFuncts, info=None):
    """
    Given a filename and list of atoms
    This function writes the test batch to the given file
    Given an info array (containing 'funct' number of size-4 array elements),
    updates the [sum, count, min, max] values contributed by this batch
    Note that the values written correspond to the symmetry functions of the atoms
    """

    with open(filename, 'w') as f:
        for i in atoms:
            for funct in xrange(len(symmFuncts)):
                result = symmFuncts[funct](i=i, atomList=atoms, box=box)
                f.write(str(result) + " ")
                if info == None:
                    continue
                info[0][funct][0] += result
                info[0][funct][1] += 1
                info[0][funct][2] = min(info[0][funct][1], result)
                info[0][funct][3] = max(info[0][funct][2], result)
            f.write("\n")
        f.write(str(pe) + "\n")


# UPDATE TO SUPPORT MULTIPLE ATOM TYPES
def writeScaling(symmFuncts, info, pe, atomCount):
    """
    Given an array of symmetry functions 'symmFuncts'
    The results of applying these symmetry functions to each element in 'info'
    The list of potential energies 'pe'
    And the number of atoms 'atomCount'

    Writes the atom information to "runner/scaling.data"
    And identical symmetry function information to both
    "runner/input.nn" and "runner/input.nn.RuNNer++"

    Details on these outputs can be found in "runner_input.txt"
    """

    with open("runner/input.nn", "w") as f:
        for funct in symmFuncts:
            k = funct.keywords
            f.write("symfunction_short C 2 C ")
            f.write(str(k['eta']) + " " + str(k['Rs']) + " " +  str(k['Rc']))
            f.write("\n")

    os.system("cp runner/input.nn runner/input.nn.RuNNer++")
    
    with open("runner/scaling.data", "w") as f:
        for i in range(len(info)):
            for j in range(len(info[i])):
                funct = info[i][j]
                f.write(str(i + 1) + " ")
                f.write(str(j + 1) + " ")
                f.write(str(funct[2]) + " " + str(funct[3]) + " " + str(funct[0]/funct[1]))
                f.write("\n")
        f.write(str(sum(pe)/len(pe)/atomCount) + " " + str((max(pe)-min(pe))/atomCount))
        
                
def main():
    if len(argv) < 3:
        print("Give the train/test and symmetry function information files")
        return
    # Acquire and read data
    expected = ["trainFolder", "testFolder"]
    defaults = {"generateData" : True, "trainRatio" : 0.9, "runnerScaling" : "../runner/", "verbose" : False}
    data = get_data(argv[1], expected, defaults)
    expected = []
    defaults = {}
    data = combine_dicts(data, get_data(argv[2], expected, defaults))
    verbose = data["verbose"]
    if data["generateData"]:
        print("Generating lammps data")
        if not (data.has_key("lammpsFile") and data.has_key("seedRange")):
            print("Give a lammpsFile and seedRange if you want to generate data")
            return
        seed = random.randint(data["seedRange"][0], data["seedRange"][1])
        lammpstrj, log = generateData(data["lammpsFile"], seed, data["runnerScaling"])
    else:
        if not (data.has_key("lammpstrj") and data.has_key("log") and data.has_key("seed")):
            print("Give a lammpstrj location, log location, and seed if you don't want to generate data")
            return
        seed = data["seed"]
        lammpstrj = data["lammpstrj"]
        log = data["log"]
    print("Reading atomic data")
    atomData, box = readAtomData(lammpstrj)
    print("Reading thermodynamic data")
    thermoData = readThermoData(log)
    print("Shuffling data")
    z = list(zip(atomData, thermoData))
    random.shuffle(z)
    atomData, thermoData = zip(*z)

    #Get Functions
    functs2 = []
    functs3 = []
    if data.has_key("2functions"):
        functs2 = get2Functs(data["2functions"], data["2Rc"], data["2sigma"], data["2count"])
    if data.has_key("3functions"):
        functs2 = get3Functs(data["3functions"], data["3Rc"], data["3sigma"], data["3count"])

    #Sort functions as required by runner
    k2 = lambda x : (x.keywords['Rc'], x.keywords['eta'], x.keywords['Rs'])
    functs2.sort(key=k2)
    k3 = lambda x : (x.keywords['Rc'], x.keywords['eta'],
                     x.keywords['zeta'], x.keywords['lambda'], x.keywords['Rs'])
    functs3.sort(key=k3)

    functs = functs2 + functs3
    
    # Write train and test files
    trainFolder = data["trainFolder"]
    testFolder = data["testFolder"]
    trainRatio = data["trainRatio"]
    trainCutoff = int(trainRatio * len(atomData))
    i = 0
    if (verbose):
        print("Writing " + str(trainCutoff) + " training files and " + str(len(atomData)-trainCutoff) + " testing files")
    info = [list([[0, 0, int(1e10), int(-1e10)] for _ in range(len(functs))])]
    while i < trainCutoff:
        print("Writing Training Batch: " + str(i+1))
        writeBatch(trainFolder + str(i+1) + ".nndata", atomData[i], box, thermoData[i], functs, info)
        i += 1
    while i < len(atomData):
        print("Writing Test Batch: " + str(i+1-trainCutoff))
        writeBatch(testFolder + str(i+1-trainCutoff) + ".nndata", atomData[i], box, thermoData[i], functs)
        i += 1

    print("Writing function information to scaling.data")
    writeScaling(functs, info, thermoData, len(atomData[0]))
    
            
def countInCutoff(atoms, cutoff):
    # Test Function
    with open("dists.txt", 'w') as f:
        for i in atoms:
            count = 0
            for j in atoms:
                if i.calcDist(j) <= cutoff:
                    count += 1
            f.write(str(count) + "\n")
    exit() # Only used for testing stuff...
        
    
if __name__ == "__main__":
    main()
