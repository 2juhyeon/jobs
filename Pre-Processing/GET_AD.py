import numpy as np
import os

########### add translational vector!
def vector_calculus(lattice_vector, position, magnitude):
    res = []
    
    ########### position to vector
    for i in range(3):
        temp = np.double(0.0)
        for j in range(3):
            temp += lattice_vector[i][j] * position[j]
        res.append(temp * magnitude)
    return res

def position2vector(POSCAR, POSITION):
    magnitude = np.double(POSCAR[1])

    lattice_vector = []
    for i in range(2,5):
        lattice_vector.append(np.double(POSCAR[i].split()))
    ret_vector = vector_calculus(lattice_vector, POSITION, magnitude)

    return ret_vector

def get_angle(A, B, C):
    alpha = []
    beta = []

    ########### two vector calculation
    for i in range(3):
        alpha.append(A[i]-B[i])
        beta.append(C[i]-B[i])

    ########### inner product
    inner = np.double(0.0)
    for i in range(3):
        inner += alpha[i]*beta[i]

    ########### vector norm calculation
    norm1 = np.double(0)
    norm2 = np.double(0)
    for i in range(3):
        norm1 += alpha[i]**2
        norm2 += beta[i]**2
    norm1 = np.sqrt(norm1)
    norm2 = np.sqrt(norm2)
    ##################### A*B/(|A||B|)
    return np.arccos(inner/norm1/norm2) * 180.0 / np.pi

def get_distance(A, B):
    RES = 0
    for i in range(3):
        RES += (A[i]-B[i])**2
    return np.sqrt(RES)

def get_position(POSCAR, ATOM, NUMBER):
    ATOMS = POSCAR[5].split()
    NUMBERS = POSCAR[6].split()

    it = 0
    for i in range(len(ATOMS)):
        if ATOM in ATOMS[i]: it = i; break

    index_number = 0
    for i in range(it):
        index_number += int(NUMBERS[i])

    index_number += (int(NUMBER) - 1)
    ret_vector = np.double(POSCAR[8+index_number].split())

    return ret_vector

######### do not use this function! has error...
###def find_nearposition(POSITION1, POSITION2):
    position_ = []
    for i in range(3):
        position_.append(int(np.double(POSITION2[i]) + 0.5))

    want_change_ = []
    for i in range(3):
        want_change_.append(int(np.double(POSITION1[i]) + 0.5))

    for i in range(3):
        if position_[i] > 0:
            if want_change_[i]  > 0:
                continue
            else: 
                POSITION1[i] += np.double(1.0)

        else :
            if want_change_[i] > 0:
                POSITION1[i] -= np.double(1.0)
            else:
                continue
    return POSITION1

######### using translational vector, find near position!
def find_nearposition2(POSITION1, POSITION2):
    for i in range(3):
        alpha = POSITION2[i] - POSITION1[i]

        if alpha > 0.5:
            POSITION1[i] += np.double(1.0)
        elif alpha < -0.5:
            POSITION1[i] -= np.double(1.0)

    return POSITION1

    return 


print("************************************************")
print("*********************GET_AD*********************")
print("************************************************")
print("******************Kunsan National University****")
print("********************Juhyeon Lee in CMP Group****")
print("************************************************")


## file exist check before read using os module!
if os.path.exists("POSCAR") == 0 :
    print("\n\n\n")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!check POSCAR!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    exit()
else :
    file = open("POSCAR","r")
    POSCAR = file.readlines()

if os.path.exists("GETAD") == 0 :
    print("\n\n\n")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!check GETAD!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    file = open("GETAD","a")
    file.write("GETAD_order_file\nDISTANCE\n\nANGLE")
    exit()
else :
    file  = open("GETAD")
    GETAD = file.readlines()

con = 0
while True:
    if "DISTANCE" in GETAD[con] : break ########### string compare
    con += 1

con += 1
dis_con = 0
DISTANCE_RES = []
while True:
    if "ANGLE" in GETAD[con] : break

    temp = GETAD[con].split()
    
    ATOM1 = temp[0]; POSITION1 = temp[1]
    ATOM2 = temp[2]; POSITION2 = temp[3]

    vector1 = get_position(POSCAR, ATOM1, POSITION1)
    vector2 = get_position(POSCAR, ATOM2, POSITION2)

    vector1 = find_nearposition2(vector1, vector2)

    vector1 = position2vector(POSCAR, vector1)
    vector2 = position2vector(POSCAR, vector2)

    got_distance = get_distance(vector1, vector2)

    DISTANCE_RES.append([ATOM1, POSITION1, ATOM2, POSITION2, got_distance])

    dis_con += 1
    con += 1

con += 1


ANGLE_RES = []
ang_con = 0
while True:
    if con >= len(GETAD): break
    elif GETAD[con].isspace(): break

    temp = GETAD[con].split()

    ATOM1 = temp[0]; POSITION1 = temp[1]
    ATOM2 = temp[2]; POSITION2 = temp[3]
    ATOM3 = temp[4]; POSITION3 = temp[5]

    vector1 = get_position(POSCAR, ATOM1, POSITION1)
    vector2 = get_position(POSCAR, ATOM2, POSITION2)
    vector3 = get_position(POSCAR, ATOM3, POSITION3)

    vector1 = find_nearposition2(vector1, vector2)
    vector3 = find_nearposition2(vector3, vector2)

    vector1 = position2vector(POSCAR, vector1)
    vector2 = position2vector(POSCAR, vector2)
    vector3 = position2vector(POSCAR, vector3)
    
    got_angle = get_angle(vector1, vector2, vector3)

    ANGLE_RES.append([ATOM1, POSITION1, ATOM2, POSITION2, ATOM3, POSITION3, got_angle])
    ang_con += 1
    con += 1

GETAD_RES = open("RES","w")

########### distance, angle OUTPUT
for i in range(dis_con):
    str = ''
    for j in range(5):
        str += np.str_(DISTANCE_RES[i][j])
        if j < 4: str += " "
    print("DIS",str)
    GETAD_RES.write("DIS ")
    GETAD_RES.write(str)
    GETAD_RES.write("\n")

for i in range(ang_con):
    str = ''
    for j in range(7):
        str += np.str_(ANGLE_RES[i][j])
        if j < 6 : str += " "
    print("ANG",str)
    GETAD_RES.write("ANG ")
    GETAD_RES.write(str)
    if i < ang_con-1: GETAD_RES.write("\n")
