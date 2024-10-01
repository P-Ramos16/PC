import numpy as np
import matplotlib.pyplot as pp

measureVariance = 1.1666

##  Ex 2
def kalmanFilter(measure, oldMeasure, oldVar, oldKalmanGain):
    #  X = A -> model 
    #  Xt = F * Xt + B ut -> Generic Kalman Filter transition equasion
    #  et is noise (mean of 0)

    estValue = oldMeasure + oldKalmanGain * (measure - oldMeasure)
    estCovariance = (1 - oldKalmanGain) * oldVar

    kalmanGain = estCovariance / (estCovariance + measureVariance)
    
    #    1 since the value is constant
    #xt = 1 * x + et

    #  zt = H * Xt -> General Common Filter equasion
    #zt = 1 * xt

    return [estValue, estCovariance, kalmanGain]




##  Ex 2.1
constValue = 5
noise = np.random.normal(0, 0.25, 1000)
values = [round(constValue + noiseVal.item(), 3) for noiseVal in noise]

estValue = 0
estCovariance = 5
kalmanGain = estCovariance / (estCovariance + measureVariance)


filteredValues = []

for val in values:

    estValue, estCovariance, kalmanGain = kalmanFilter(val, estValue, estCovariance, kalmanGain)

    filteredValues.append(estValue)

    print(f"Estimate for {val}: {estValue} | gain: {kalmanGain}")


pp.plot(filteredValues)

pp.plot(values)
pp.show()
