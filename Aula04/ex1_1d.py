import random

colors = ['red', 'green', 'green', 'red' , 'red']

measurements = ['green']                                            # test 1
motions = [[1]]                                                     # test 1
#measurements = ['green', 'green', 'green' ,'green', 'green','red']  # test 2
#motions = [[1],[0],[-1],[1],[1],[0]]                                # test 2

sensor_right = {}
sensor_right['green'] = 0.6
sensor_right['red'] = 0.8

p_move = 0.8

def sense(p, Z):
    """Update particle array p according to new measurement Z"""

    #  Associate it with the weight, that comes from the sensor model
    #  Example: sees green: P(Gm|Gc) = 0.6, P(Gm|Rc) = 0.2

    #  Then resample to get the new particle set
    #  Get the weights and uniform distribution
    #  Sample [0, 1] uniformally

    newParticleSet = []

    sumOfWeights = 0
    
    for particle in p:
        partColour = colors[particle]

        partWeight = abs((partColour != Z) - sensor_right[partColour])

        newParticleSet.append((particle, sumOfWeights))
        sumOfWeights += partWeight

    finalParticleSet = []

    #newParticleSet.sort(key = lambda x: x[1], reverse=True)
     
    for i in range(0, len(newParticleSet)):

        r = random.random() * (sumOfWeights - partWeight)

        newPartID = 0
        currWeightSum = 0

        while r > newParticleSet[newPartID][1]:
            newPartID += 1

        finalParticleSet.append(newParticleSet[newPartID][0])



    finalParticleSet.sort()

    return finalParticleSet


    """ for particle in p:
    #  Associate it with the weight, that comes from the sensor model
    #  Example: sees green: P(Gm|Gc) = 0.6, P(Gm|Rc) = 0.2

    #  Then resample to get the new particle set
    #  Get the weights and uniform distribution
    #  Sample [0, 1] uniformally

    w = 0
    while weigths[w] < particle:
        w += 1


    particleWeight = sensor_right[colors[w]]
    
    #print(particle, calVal, w, weigths[w])


    newParticleSet.append(round(calVal, 4)) """


def move(p, U):
    """Update p after movement U"""

    newParticleSet = []

    for particle in p:

        #  Move
        if random.random() < p_move:
            newParticle = (particle + U[0]) % len(colors)

        #  Stay
        else:
            newParticle = particle

        newParticleSet.append(newParticle)

    return newParticleSet

    
#main
p = []

width  = len(colors)
n = width

#for c in range(width):
#    p.append(1./n)
#    print(p)

# p = [0.5, 0.2, 0.1, 0.1, 0.1]             #  OLD Bayes
p = [0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 4, 4]  #  New particles
#p = [0, 1, 2]
print(p)
#p = [round(random.random() * 4, 0) for _ in range(0, 5)]

for s in range(len(measurements)):
    print("sense ",measurements[s])
    p = sense(p,measurements[s])
    print(p)
    print("move ", motions[s])
    p = move(p, motions[s])
    print(p)


