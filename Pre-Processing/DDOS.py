import numpy as np
import os
import matplotlib.pyplot as plt

##########################
def read_mode():
    f = open("DP_Select.dpdp")
    lines = f.readlines()
    

    return modes

def read_error():
    os.system("cat DP_Select.dpdp ")
    return 


if __name__ == "__main__":
#    res = read_mode()    
#    if res == "none":
#        read_error()
#        print()
#        print("check DP_select.dpdp file!")
#        print("thank you! have a nice day!")
#        print()
#        exit()
#
#    else 
#        print("Dos Plot!")
#        print("    J.H. Lee")
#
#    ################## analysis
    

    ################## file exist check
    now_path = os.getcwd()
    if os.path.exists(now_path + "/PROCAR") == False:
        print("check PROCAR file")
        exit()
    if os.path.exists(now_path + "/POSCAR") == False:
        print("check POSCAR file")
        exit()

    ################## POSCAR analysis
    TEMP = open(now_path + "/POSCAR")
    POSCAR = TEMP.readlines()
    TEMP.close()

    ATOMS = POSCAR[5].split()
    ATOMS_NUMBER = POSCAR[6].split()
        
    ################## PROCAR analysis
    TEMP = open(now_path + "/PROCAR")
    PROCAR = TEMP.readlines()
    TEMP.close()

    kpt = int(PROCAR[1].split()[3])
    band = int(PROCAR[1].split()[7])
    ions = int(PROCAR[1].split()[11])
    SPIN = 2
    ###########################

    RES = []
    RES_TOTAL = []
    ENERGY_LEVELS = []
    FIND_ION = False

    for length_of in range(len(PROCAR)):
        if PROCAR[length_of].find("tot  ") > -1:
            FIND_ION = False
            RES_TOTAL.append(PROCAR[length_of])

        if FIND_ION:
            RES.append(PROCAR[length_of])
        
        if PROCAR[length_of].find("ion  ") > -1:
            FIND_ION = True
        if PROCAR[length_of].find("band  ") > -1:
            ENERGY_LEVELS.append(np.double(PROCAR[length_of].split()[4]))

    ###########################
    ## orbit, ions, energy, kpoints spin
    ## RES[ (spin * kpt * band * ions) + (kpoints * band * ions) + (energy * ions) + ion].split()[orbital+1] <- orbits
    ###########################

    orbits = 17 # s.1 p.3 d.5 f.7 total => 17
    
    ######################### not yet sum kpoints
    
    ATOM = np.zeros((SPIN,ions,kpt,band,orbits))
    for spin in range(SPIN):
        for kpoints in range(kpt):
            for energy in range(band):
                for ion in range(ions):
                        for orbital in range(orbits):
                            ATOM[spin][ion][kpoints][energy][orbital] = np.double(RES[((spin * kpt * band * ions) + (kpoints * band * ions) + (energy * ions) + ion)].split()[orbital+1])*spin*(-1)
    
    ################################ Density of state calculation
    #### options
    PROJECTION_ION = 1
    PROJECTION_AA = [4,7]
    ###### choose Mn.1.4 d orbitals
    ATOM_plt = np.zeros((SPIN,PROJECTION_ION,kpt,band,3*3-2*2))
    for spin in range(SPIN):
        for energy in range(band):
            for ion in PROJECTION_AA:
                for kpoints in range(kpt):
                    for orbital in range(3*3-2*2):
                        for pro_atom in range(PROJECTION_ION):
                            ATOM_plt[spin][pro_atom][kpoints][energy][orbital] += ATOM[spin][ion][kpoints][energy][orbital + 2*2]

    ATOM_ENG = np.zeros((SPIN,PROJECTION_ION,3*3-2*2,kpt*band))
    for spin in range(SPIN):
        for energy in range(band):
            for kpoints in range(kpt):
                for orbital in range(3*3-2*2):
                    for pro_atom in range(PROJECTION_ION):
                        ATOM_ENG[spin][pro_atom][orbital][energy*kpt+kpoints] = ATOM_plt[spin][pro_atom][kpoints][energy][orbital]

    ################################# Ploting    
    fig, axs = plt.subplots(PROJECTION_ION*(3*3-2*2))
    fig.suptitle('dxy, dyz, d3z^2-r^2,dzx,dx^2-y^2')
    for spin in range(SPIN):
        for pro_atom in range(PROJECTION_ION):
            for orbital in range(3*3-2*2):
                alpha = len(ENERGY_LEVELS)
                a = (int(alpha*spin/SPIN))
                b = (int(alpha*(spin + 1)/SPIN))
                ary = ATOM_ENG[spin][pro_atom][orbital]
                axs[pro_atom*(3*3-2*2) + orbital].plot(ENERGY_LEVELS[a:b],ary)
                print(ENERGY_LEVELS)
    #axs[1].plot(ENERGY_LEVELS[0:np.ceil(len(ENERGY_LEVELS)/2)],spin_up[:][1])
    #axs[2].plot(ENERGY_LEVELS[0:np.ceil(len(ENERGY_LEVELS)/2)],spin_up[:][2])
    #axs[3].plot(ENERGY_LEVELS[0:np.ceil(len(ENERGY_LEVELS)/2)],spin_up[:][3])
    #axs[4].plot(ENERGY_LEVELS[0:np.ceil(len(ENERGY_LEVELS)/2)],spin_up[:][4])
    
    plt.show()
