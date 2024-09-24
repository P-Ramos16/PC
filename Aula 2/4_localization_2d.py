colors = [['red',  'green',  'green', 'red' ,  'red'],
          ['red',  'red',    'green', 'red',   'red'],
          ['red',  'red',    'green', 'green', 'red'],
          ['red',  'red',    'red',   'red',   'red']]

#motions is a list of 2d lists. each 2d list represents first movement in x (columns in colors) then in y (lines in colors)
#measurements = ['green']                                        # test 1
#motions = [[1,0]]                                               # test 1
measurements = ['green', 'red', 'red' ,'green', 'red','red']    # test 2
motions = [[1,0],[0,0],[0,1],[0,1],[-1,0],[0,0]]                # test 2

sensor_right = {}
sensor_right['green'] = 0.8
sensor_right['red'] = 0.7

p_move = 1.0

def show(p):
    for i in range(len(p)):
        print(p[i])

def sense(p, Z):
    """Update belief array p according to new measurement Z"""
    
    finalMeasurements = []

    for lineID in range(0, len(colors)):
        newMeasurements = []
        #  Calculate the percentages
        for cellID in range(0, len(colors[0])):
            cellColour = colors[lineID][cellID]
            hit = (Z == cellColour)

            newMeasurements.append( hit * sensor_right[cellColour] * p[lineID][cellID] 
                            + (1 - hit) * (1 - sensor_right[cellColour]) * p[lineID][cellID])

        finalMeasurements.append(newMeasurements)

    #  Normalize
    normalization = 1 / sum(map(sum, finalMeasurements))

    result = []

    for line in finalMeasurements:
        resLine = []
        for val in line:
            resLine.append(round(val * normalization, 4))

        result.append(resLine)

    return result

def move(p, U):
    """Update p after movement U"""

    finalMeasurements = []

    for lineID in range(0, len(colors)):
        newProbs = []
        #  Calculate the percentages
        for cellID in range(0, len(colors[0])):
            calVal = p_move * p[lineID][(cellID - U[0]) % len(p)]
            calVal = calVal + (1 - p_move) * p[lineID][cellID]

            newProbs.append(calVal)

        finalMeasurements.append(newProbs)

    return finalMeasurements

#main

height = len(colors)
width  = len(colors[0])

n = height * width

p = []
for l in range(height):
    q=[]
    for c in range(width):
        q.append(1./n)
    p.append(q)

for s in range(len(measurements)):
    print("sense ",measurements[s])
    p = sense(p,measurements[s])
    show(p)
    print("move ", motions[s])
    p = move(p,motions[s])
    show(p)


