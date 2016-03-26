from math import *
from numpy import dot

def euclideanDist(a,b):
    return sqrt( pow(a[0]-b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2],2))

def detectCollision( baseServo,armServo, targetX,targetY,targetZ):
    #Define dimmensions of the experimental setup
    #Units in cm because the american English System is terrible
    # The top right corner of the experiment is the origin 
    # left and right from the base
    x_offset = 28.0
    #up and down from the base
    y_offset = 18
    #This should be the depth from the base ie motion directly away from base.
    z_offset = 14.0
    l = 16 #length of the party blower

    xzcomp = l*cos(armServo-pi/2)
    zcomp = xzcomp*sin(baseServo)
    ycomp = l*sin(armServo-pi/2)
    xcomp = xzcomp*cos(baseServo)

    #I need to verify that z is the depth and that i havent flipped the coordinates somewhere
    target = [targetX, targetY, targetZ]

    P0 = [x_offset, y_offset, z_offset]
    P1 = [x_offset+xcomp, y_offset+ycomp, z_offset+zcomp]
    V = [xcomp, ycomp, zcomp]
    W = [target[0]-P0[0], target[1]-P0[1], target[2]-P0[2]]
    #print W
    

    C1 = dot(W,V)
    C2 = dot(V,V)
    if C1 <= 0:
        D = euclideanDist(target,P0)
    elif C2 <= C1:
        D = euclideanDist(target,P1)
    else:
        b = C1/C2
        PB = P0 + b*V
        D = euclideanDist(target,PB)
    
    isHit = 0;
    if D<1:
        print 'Target was hit!'
        isHit = 1;
    return isHit