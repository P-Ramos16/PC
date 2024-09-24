colors = ['red', 'green', 'green', 'red' , 'red']

motions = [[1]]                      # test 1
#motions = [[1],[0],[-1],[1],[0]]     # test 2

# 1 = move to right 
# 0 = stay 
# -1 = move to left

p_move = 0.8

def move(p, U):
    """Update p after movement U"""

    newProbs = []

    for cellID in range(len(p)):
        calVal = p_move * p[(cellID - U[0]) % len(p)]
        calVal = calVal + (1 - p_move) * p[cellID]

        newProbs.append(calVal)

    return newProbs

#main
p = [0.5, 0.5, 0, 0, 0]

width  = len(colors)
n = width

for s in range(len(motions)):
    p = move(p, motions[s])

print(p)

