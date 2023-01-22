"""
from mpu6050 import mpu6050
from time import sleep #sleep([seconds]) used to pause ... arduino delay()

MPU = mpu6050(0x68)
"""

import numpy as np
import random
import string

#eventList = ["C3", "B2", "B2", "F6", "C3", "F6", "C3", "F6", "C3", "D4", "A1", "C3"]
eventList1 = []
eventList2 = []

callSign = "KQ4CTL"
matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False

rI = "NE4BAT A1 B2 C3 KQ4CTL C3 A1 D4 C3 F6 E5 F6 C3 F6 B2 B2 C3 CU4TON C3 F6 D3 E5 SB4PAY C3 B2 NE4BAT C3 B2 A1 KQ4CTL B2 A1 D4 C3 CU4TON F6 E5"

rIMatch = "NE4BAT A1 B2 C3 KQ4CTL B2 A1 D4 C3 CU4TON C3 F6 D3 E5 SB4PAY C3 B2 NE4BAT C3 B2 A1 KQ4CTL B2 A1 D4 C3 CU4TON F6 E5"

rIDiff1 = "NE4BAT A1 B2 C3 KQ4CTL B2 A1 D4 B2 CU4TON C3 F6 D3 E5 SB4PAY C3 B2 NE4BAT C3 B2 A1 KQ4CTL B2 A1 D4 C3 CU4TON F6 E5"
rIDiff3 = "NE4BAT A1 B2 C3 KQ4CTL B2 A1 D4 B2 CU4TON C3 F6 D3 E5 SB4PAY C3 B2 NE4BAT C3 B2 A1 KQ4CTL F6 B2 D4 C3 CU4TON F6 E5"
rIDiff6 = "NE4BAT A1 B2 C3 KQ4CTL A1 B2 C3 D4 E5 F6 CU4TON C3 F6 D3 E5 SB4PAY C3 B2 NE4BAT C3 B2 A1 KQ4CTL F6 E5 D4 C3 B2 A1 CU4TON F6 E5"

#Arducam OV5642 Plus

"""
MPU 6050
https://www.youtube.com/watch?v=JTFa5l7zAA4
https://github.com/m-rtijn/mpu6050
https://pypi.org/project/mpu6050-raspberrypi/
https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi

def getAccelGyroMagVal():
    accelVec = np.array(MPU.get_accel_data())
    gyroVec = np.array(MPU.get_gyro_data())
    
    accelMag = np.linalg.norm(accelVec)
    gyroMag = np.linalg.norm(gyroVec)

    print("Acceleration Vector")
    print(accelVec)
    print("Acceleration Mag")
    print(accelMag)

    print("Gyro Vector")
    print(gyroVec)
    print("Acceleration Vector")
    print(gyroMag)
"""
def getTransmittion():
    print("hi")

# XX4XXX C3 A1 D4 C3 F6 C3 F6 C3 F6 B2 B2 C3
# insert to the front of list as we go down the instruction.

"""
need to add in 
gets 2 instructions out of the radio signal...
6 mins record to guarntee at least 2 readings... best case 3 full proper, avg case 2 full 1 partial
"""
# seems like it won't get the instruction if it is at the end of the segment
def getInstructionList(inString):
    tempStr = inString[:]

    tempList = tempStr.rsplit(" ")

    callSignList = [i for i in tempList if len(i) > 2]

    nextCall = callSignList[callSignList.index(callSign)+1]
    
    callIndex1 = tempList.index(callSign)

    nextCallIndex1 = tempList.index(nextCall)
    listEnd = False

    if (nextCallIndex1 < callIndex1):
        nextCallIndex1 = tempList.index(nextCall, nextCallIndex1+1)
        listEnd = True

    outList1 = tempList[callIndex1+1:nextCallIndex1]
    outList1.reverse()
    
    callIndex2 = tempList.index(callSign, callIndex1+1)

    if (listEnd):
        outList2 = tempList[callIndex2+1:]
    else:
        nextCallIndex2 = tempList.index(nextCall, nextCallIndex1+1)

        outList2 = tempList[callIndex2+1:nextCallIndex2]

    outList2.reverse()
    return outList1, outList2

"""
# outputs the command with the most similarity
# if first 2 are the same continue to perform task
# if not the same, get signal again and compare again
"""
def compareInstructions(inList1, inList2):
    matching = True
    differences = 0
    if (len(inList1) == len(inList2)) and (len(inList1) != 0):
        for i in range(len(inList1)):
            if inList1[i] != inList2[i]:
                matching = False
                differences += 1
    else:
        matching = False
        differences = -1

    return matching, differences

# executes base on command ... need to make commands for each case
def executeInstructions(instructionList):
    tempList = instructionList[:]
    listLen = len(tempList)

    while listLen > 0:
        instrCase = tempList.pop()
        
        match instrCase:
            case "A1":
                print("apple")
            case "B2":
                print("banana")
            case "C3":
                print("cake")
            case "D4":
                print("duck")
            case "E5":
                print("eel")
            case "F6":
                print("fruit")

        listLen = len(tempList)

"""
Random team and instruction generator

Parameters:
- teams: number of teams, default of 1
- length: number of instructions, default of 1
- limit: types of instructions, default of 6
"""
def genRandInstr(teams = 1, length = 1, limit = 6):
    reqTeam = "KQ4CTL"
    reqUsed = False
    Instr = ""
    
    if limit > 6:
        limit = 6
    
    for i in range(teams):
        if ((random.randint(0,teams) < int(teams/2)) or i == teams-1) and (not reqUsed):
            Instr += reqTeam + " "
            reqUsed = True
        else:
            tempRandStr1 = ''.join(random.choices(string.ascii_uppercase, k=2))
            tempRandStr2 = ''.join(random.choices(string.ascii_uppercase, k=3))
            Instr += tempRandStr1 + "4" + tempRandStr2 + " "
        
        for i in range(length):
            tempRand = random.randint(1,limit)
            match tempRand:
                case 1:
                    Instr += "A1 "
                case 2:
                    Instr += "B2 "
                case 3:
                    Instr += "C3 "
                case 4:
                    Instr += "D4 "
                case 5:
                    Instr += "E5 "
                case 6:
                    Instr += "F6 "
    
    Instr = Instr + Instr
    
    return Instr

#main tasks
while (not hasFlown):
    hasFlown = True
    deployed = True
    print("Passed 1")
    print()

while (deployed and (not finishedTask)):
    instr1 = genRandInstr(5,2,2)
    instr2 = genRandInstr(5,2,2)
    
    print("Random instruction strings")
    print(instr1)
    print(instr2)
    print()

    eventList1_1, eventList1_2 = getInstructionList(instr1)
    eventList2_1, eventList2_2 = getInstructionList(instr2)

    matchingInstr1, DiffInstr1 = compareInstructions(eventList1_1, eventList2_1)
    matchingInstr2, DiffInstr2 = compareInstructions(eventList1_2, eventList2_2)

    print("Instruction Lists")
    print(eventList1_1)
    print(eventList2_1)
    print()

    print("Matching and # differences")
    print(matchingInstr1)
    print(DiffInstr1)
    print(matchingInstr2)
    print(DiffInstr2)

    #print("First List:")
    #executeInstructions(eventList1)
    #print("\n" + "Second List:")
    #executeInstructions(eventList2)
    print("Passed 2")
    finishedTask = True