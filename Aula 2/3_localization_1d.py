colors = ['red', 'green', 'green', 'red' , 'red']

#measurements = ['green']                                            # test 1
#motions = [[1]]                                                     # test 1
measurements = ['green', 'green', 'green' ,'green', 'green','red']  # test 2
motions = [[1],[0],[-1],[1],[1],[0]]                                # test 2

sensor_right = {}
sensor_right['green'] = 0.6
sensor_right['red'] = 0.8


p_move = 0.8

def sense(p, Z):
    """Update belief array p according to new measurement Z"""
    
    newMeasurements = []

    #  Calculate the percentages
    for cellID in range(0, len(colors)):       
        cellColour = colors[cellID]
        hit = (Z == cellColour)

        newMeasurements.append( hit * sensor_right[cellColour] * p[cellID] 
                        + (1 - hit) * (1 - sensor_right[cellColour]) * p[cellID])


    #  Normalize
    normalization = 1 / sum(newMeasurements)

    newMeasurements = [round(val * normalization, 4) for val in newMeasurements]

    return newMeasurements

def move(p, U):
    """Update p after movement U"""

    newProbs = []

    for cellID in range(len(p)):
        calVal = p_move * p[(cellID - U[0]) % len(p)]
        calVal = calVal + (1 - p_move) * p[cellID]

        newProbs.append(round(calVal, 4))

    return newProbs

#main
p = []

width  = len(colors)
n = width

for c in range(width):
    p.append(1./n)


for s in range(len(measurements)):
    print("sense ",measurements[s])
    p = sense(p,measurements[s])
    print(p)
    print("move ", motions[s])
    p = move(p,motions[s])
    print(p)


