# based on Sebastian Thrun et al., Programming a Robotic Car, Udacity

# --------------
# USER INSTRUCTIONS
#
# Now you will put everything together.
#
# First make sure that your sense and move functions
# work as expected for the test cases provided at the
# bottom of the previous two programming assignments.
# Once you are satisfied, copy your sense and move
# definitions into the robot class on this page, BUT
# now include noise.
#
# A good way to include noise in the sense step is to
# add Gaussian noise, centered at zero with variance
# of self.bearing_noise to each bearing. You can do this
# with the command random.gauss(0, self.bearing_noise)
#
# In the move step, you should make sure that your
# actual steering angle is chosen from a Gaussian
# distribution of steering angles. This distribution
# should be centered at the intended steering angle
# with variance of self.steering_noise.
#
# Feel free to use the included set_noise function.
#
# Please do not modify anything except where indicated
# below.

from math import *
import random

# --------
# 
# some top level parameters
#

max_steering_angle = pi / 4.0 # You do not need to use this value, but keep in mind the limitations of a real car.
bearing_noise = 0.1 # Noise parameter: should be included in sense function.
steering_noise = 0.1 # Noise parameter: should be included in move function.
distance_noise = 5.0 # Noise parameter: should be included in move function.

tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.


# --------
# 
# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks in (y, x) format.
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"

# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------
    # init: 
    #    creates robot and initializes location/orientation 
    #

    def __init__(self, length = 20.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero

    # --------
    # set: 
    #    sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    # --------
    # set_noise: 
    #    sets the noise parameters
    #
    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # measurement_prob
    #    computes the probability of a measurement
    #  

    def measurement_prob(self, measurements):

        # calculate the correct measurement
        predicted_measurements = self.sense(0) # Our sense function took 0 as an argument to switch off noise.


        # compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
            

            # update Gaussian
            error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /  
                      sqrt(2.0 * pi * (self.bearing_noise ** 2)))

        return error
    
    def __repr__(self): #allows us to print robot attributes.
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), 
                                                str(self.orientation))
    
    ############# ONLY ADD/MODIFY CODE BELOW HERE ###################
       
    # --------
    # move: 
    #   
    
    # copy your code from the previous exercise
    # and modify it so that it simulates motion noise
    # according to the noise parameters
    #           self.steering_noise
    #           self.distance_noise

    def move(self, motion): # Do not change the name of this function

        stAngle, distance = motion

        new_x = self.x
        new_y = self.y
        new_orientation = self.orientation

        if stAngle % 90 == 0:
            new_x = self.x + distance * cos(self.orientation)
            new_y = self.y + distance * sin(self.orientation)

        else:

            radius = self.length / tan(stAngle)

            center_x = self.x - radius * sin(self.orientation)
            center_y = self.y + radius * cos(self.orientation)

            beta = distance / radius

            new_x = center_x + radius * sin(self.orientation + beta)
            new_y = center_y - radius * cos(self.orientation + beta)
            new_orientation = self.orientation + beta


        newrobot = robot(self.length)
        newrobot.set(new_x, new_y, new_orientation)

        return newrobot # make sure your move function returns an instance
                        # of the robot class with the correct coordinates.

    # --------
    # sense: 
    #    


    def sense(self, addNoise=1): #do not change the name of this function
        Z = []

        for landmarkX, landmarkY in landmarks:
            currAngle = self.orientation

            landmarkToRobotAngle = atan2(landmarkY-self.y, landmarkX-self.x)


            alphaLandmark = landmarkToRobotAngle - currAngle

            if alphaLandmark < 0:
                alphaLandmark += 2 * pi

            elif alphaLandmark > 2 * pi:
                alphaLandmark -= 2 * pi

            print(degrees(alphaLandmark))

            Z.append(alphaLandmark)

        Z.sort(reverse=True)


        return Z #Leave this line here. Return vector Z of 4 bearings.

    # copy your code from the previous exercise
    # and modify it so that it simulates bearing noise
    # according to
    #           self.bearing_noise

    ############## ONLY ADD/MODIFY CODE ABOVE HERE ####################

# --------
#
# extract position from a particle set
# 

def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi)) 
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]

# --------
#
# The following code generates the measurements vector
# You can use it to develop your solution.
# 


def generate_ground_truth(motions):

    myrobot = robot()
    myrobot.set(10.0, 10.0, 0.0)
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

    Z = []
    T = len(motions)

    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense())
    print('Robot:    ', myrobot)
    return [myrobot, Z]

# --------
#
# The following code prints the measurements associated
# with generate_ground_truth
#

def print_measurements(Z):

    T = len(Z)

    print('measurements = [[%.8s, %.8s, %.8s, %.8s],' % \
        (str(Z[0][0]), str(Z[0][1]), str(Z[0][2]), str(Z[0][3])))
    for t in range(1,T-1):
        print('                [%.8s, %.8s, %.8s, %.8s],' % \
            (str(Z[t][0]), str(Z[t][1]), str(Z[t][2]), str(Z[t][3])))
    print('                [%.8s, %.8s, %.8s, %.8s]]' % \
        (str(Z[T-1][0]), str(Z[T-1][1]), str(Z[T-1][2]), str(Z[T-1][3])))

# --------
#
# The following code checks to see if your particle filter
# localizes the robot to within the desired tolerances
# of the true position. The tolerances are defined at the top.
#

def check_output(final_robot, estimated_position):

    error_x = abs(final_robot.x - estimated_position[0])
    error_y = abs(final_robot.y - estimated_position[1])
    error_orientation = abs(final_robot.orientation - estimated_position[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tolerance_xy and error_y < tolerance_xy \
              and error_orientation < tolerance_orientation
    return correct



def particle_filter(motions, measurements, N=500): # I know it's tempting, but don't change N!
    # --------
    #
    # Make particles
    # 

    p = []

    # --------
    #
    # Update particles
    #     

    for t in range(len(motions)):
    
        # motion update (prediction)

        print('p after motion ', p)

        # measurement update
        w = []

        print('w ', w)

        # resampling

        print('p resamp', p)
    
    return get_position(p)

## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out.
##
## You can test whether your particle filter works using the
## function check_output (see test case 2). We will be using a similar
## function. Note: Even for a well-implemented particle filter this
## function occasionally returns False. This is because a particle
## filter is a randomized algorithm. We will be testing your code
## multiple times. Make sure check_output returns True at least 80%
## of the time.


 
## --------
## TEST CASES:
## 
##1) Calling the particle_filter function with the following
##    motions and measurements should return a [x,y,orientation]
##    vector near [x=93.476 y=75.186 orient=5.2664], that is, the
##    robot's true location.
##
motions = [[2. * pi / 10, 20.] for row in range(8)]
measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
                [3.510067, 2.916300, 2.146394, 1.598332],
                [2.972469, 2.407489, 1.588474, 1.611094],
                [1.906178, 1.193329, 0.619356, 0.807930],
                [1.352825, 0.662233, 0.144927, 0.799090],
                [0.856150, 0.214590, 5.651497, 1.062401],
                [0.194460, 5.660382, 4.761072, 2.471682],
                [5.717342, 4.736780, 3.909599, 2.342536]]

print(particle_filter(motions, measurements))
##

##motions = [[2. * pi / 10, 20.] for row in range(2)]
##measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
##                [3.510067, 2.916300, 2.146394, 1.598332]]
##
##print(particle_filter(motions, measurements))
##
## 2) You can generate your own test cases by generating
##    measurements using the generate_ground_truth function.
##    It will print the robot's last location when calling it.
##
##
##number_of_iterations = 6
##motions = [[2. * pi / 20, 12.] for row in range(number_of_iterations)]
#motions = [[0.0, 0.0] for row in range(number_of_iterations)]

##x = generate_ground_truth(motions)
##final_robot = x[0]
##measurements = x[1]
##estimated_position = particle_filter(motions, measurements)
##print_measurements(measurements)
##print('Ground truth:    ', final_robot)
##print('Particle filter: ', estimated_position)
##print('Code check:      ', check_output(final_robot, estimated_position))
##
##


#### MOTION TESTS

## --------
## TEST CASE:
## 
## 1) The following code should print:
##       Robot:     [x=0.0 y=0.0 orient=0.0]
##       Robot:     [x=10.0 y=0.0 orient=0.0]
##       Robot:     [x=19.861 y=1.4333 orient=0.2886]
##       Robot:     [x=39.034 y=7.1270 orient=0.2886]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.1
distance_noise = 5.0
##
myrobot = robot(length)
myrobot.set(0.0, 0.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
##
motions = [[0.0, 10.0], [pi / 6.0, 10], [0.0, 20.0]]
##
T = len(motions)
##
print('Robot:    ', myrobot)
for t in range(T):
    myrobot = myrobot.move(motions[t])
    print('Robot:    ', myrobot)
##
##

## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## move function with randomized motion data.

    
## 2) The following code should print:
##      Robot:     [x=0.0 y=0.0 orient=0.0]
##      Robot:     [x=9.9828 y=0.5063 orient=0.1013]
##      Robot:     [x=19.863 y=2.0201 orient=0.2027]
##      Robot:     [x=29.539 y=4.5259 orient=0.3040]
##      Robot:     [x=38.913 y=7.9979 orient=0.4054]
##      Robot:     [x=47.887 y=12.400 orient=0.5067]
##      Robot:     [x=56.369 y=17.688 orient=0.6081]
##      Robot:     [x=64.273 y=23.807 orient=0.7094]
##      Robot:     [x=71.517 y=30.695 orient=0.8108]
##      Robot:     [x=78.027 y=38.280 orient=0.9121]
##      Robot:     [x=83.736 y=46.485 orient=1.0135]
##
##
##length = 20.
##bearing_noise  = 0.0
##steering_noise = 0.0
##distance_noise = 0.0
##
##myrobot = robot(length)
##myrobot.set(0.0, 0.0, 0.0)
##myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
##
##motions = [[0.2, 10.] for row in range(10)]
##
##T = len(motions)
##
##print('Robot:    ', myrobot)
##for t in range(T):
##    myrobot = myrobot.move(motions[t])
##    print('Robot:    ', myrobot)
##
## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## move function with randomized motion data.

#### SENSE TESTS

## --------
## TEST CASES:



##
## 1) The following code should print the list [6.004885648174475, 3.7295952571373605, 1.9295669970654687, 0.8519663271732721]
##
##
#length = 20.
##bearing_noise  = 0.0
##steering_noise = 0.0
##distance_noise = 0.0
##
##myrobot = robot(length)
##myrobot.set(30.0, 20.0, 0.0)
##myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
##
##print('Robot:        ', myrobot)
##print('Measurements: ', myrobot.sense())
##

## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## sense function with randomized initial robot coordinates.
    

##
## 2) The following code should print the list [5.376567117456516, 3.101276726419402, 1.3012484663475101, 0.22364779645531352]
##
##
## length = 20.
## bearing_noise  = 0.1
## steering_noise = 0.0
## distance_noise = 0.0

## myrobot = robot(length)
## myrobot.set(30.0, 20.0, pi / 5.0)
## myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

## print('Robot:        ', myrobot)
## print('Measurements: ', myrobot.sense())
##


## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## sense function with randomized initial robot coordinates.
    
