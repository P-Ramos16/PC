
import sys
from croblink import *
from math import *
import time

#  CHECK WHAT VALUE THIS SHOULD BE
measureVariance = 1

def kalmanFilter(measure, oldMeasure, oldVar, oldkalmanGainComp):

    estValueComp = oldMeasure + oldkalmanGainComp * (measure - oldMeasure)

    estCovarianceComp = (1 - oldkalmanGainComp) * oldVar

    kalmanGainComp = estCovarianceComp / (estCovarianceComp + measureVariance)

    return [estValueComp, estCovarianceComp, kalmanGainComp]



class MyRob(CRobLinkAngs):
    def __init__(self, rob_name, rob_id, angles, host):
        CRobLinkAngs.__init__(self, rob_name, rob_id, angles, host)


    def run(self):
        if self.status != 0:
            print("Connection refused or error")
            quit()


        estValueComp = 0
        estCovarianceComp = 5
        kalmanGainComp = estCovarianceComp / (estCovarianceComp + measureVariance)

        estValueWall = 0
        estCovarianceWall = 5
        kalmanGainWall = estCovarianceWall / (estCovarianceWall + measureVariance)

        num_iter = 0


        while True:
            self.readSensors()

            if self.measures.endLed:
                print(self.robName + " exiting")
                quit()

            if num_iter > 1000:
                print(f"Final Values:")            
                print(f"Compass Estimate: {estValueComp} | var: {estCovarianceComp} | gain: {kalmanGainComp}")
                print(f"   Wall Estimate: {estValueWall} | var: {estCovarianceWall} | gain: {kalmanGainWall}")

                quit()

            num_iter += 1
            #print(f"Center IR: {self.measures.irSensor[0]}")
            #print(f"Left IR: {self.measures.irSensor[1]}")
            #print(f"Right IR: {self.measures.irSensor[2]}")
            #print(f"Back IR: {self.measures.irSensor[3]}")
            

            estValueComp, estCovarianceComp, kalmanGainComp = kalmanFilter(self.measures.compass, estValueComp, estCovarianceComp, kalmanGainComp)

            print(f"Compass Measurement num {num_iter}: {self.measures.compass}")
            print(f"Estimate for {self.measures.compass}: {estValueComp} | var: {estCovarianceComp} | gain: {kalmanGainComp}")
            

            estValueWall, estCovarianceWall, kalmanGainWall = kalmanFilter(self.measures.irSensor[0], estValueWall, estCovarianceWall, kalmanGainWall)

            print(f"Wall Measurement num {num_iter}: {self.measures.irSensor[0]}")
            print(f"Estimate for {self.measures.irSensor[0]}: {estValueWall} | var: {estCovarianceWall} | gain: {kalmanGainWall}\n")

rob_name = "pClient1"
host = "localhost"
pos = 1
mapc = None

for i in range(1, len(sys.argv),2):
    if (sys.argv[i] == "--host" or sys.argv[i] == "-h") and i != len(sys.argv) - 1:
        host = sys.argv[i + 1]
    elif (sys.argv[i] == "--pos" or sys.argv[i] == "-p") and i != len(sys.argv) - 1:
        pos = int(sys.argv[i + 1])
    elif (sys.argv[i] == "--robname" or sys.argv[i] == "-r") and i != len(sys.argv) - 1:
        rob_name = sys.argv[i + 1]
    else:
        print("Unkown argument", sys.argv[i])
        quit()

if __name__ == '__main__':
    rob=MyRob(rob_name,pos,[0.0,60.0,-60.0,180.0],host)
    
    rob.run()
