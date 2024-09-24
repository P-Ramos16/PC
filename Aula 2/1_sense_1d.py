colors = ['red', 'green', 'green', 'red' , 'red']

measurements = ['green']                                       # test 1
measurements = ['green', 'green', 'green' ,'green', 'green']   # test 2

sensor_right = {}
sensor_right['green'] = 0.6
sensor_right['red'] = 0.8


def sense(p, Z):
    """Update belief array p according to new measurement Z"""
    
    newMeasurements = []

    #  Calculate the percentages
    for cellID in range(0, len(colors)):       
        cellColour = colors[cellID]
        hit = (Z == cellColour)

        newMeasurements.append( hit * sensor_right[cellColour] * p[cellID] 
                        + (1 - hit) * (1 - sensor_right[cellColour]) * p[s])


    #  Normalize
    normalization = 1 / sum(newMeasurements)

    newMeasurements = [round(val * normalization, 4) for val in newMeasurements]

    return newMeasurements

#main
p = []

width  = len(colors)
n = width

#  Create the initial measurements
for c in range(width):
    p.append(1.0 / n)

#  Run the list of measurements
for s in range(len(measurements)):
    p = sense(p, measurements[s])

print(p)

