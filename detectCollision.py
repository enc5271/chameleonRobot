from math import *
from numpy import dot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def euclideanDist(a,b):
    return sqrt( pow(a[0]-b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2],2))

def plotScene(P0,P1,target):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    xs = [P0[0], P1[0]]
    ys = [P0[1], P1[1]]
    zs = [P0[2], P1[2]]

    ax.plot(xs , ys,zs,c='r',marker='o')
    plt.xlim(0,50)
    plt.ylim(0,50)
    ax.set_zlim(0,50)
    #Check that z and y are not flipped
    ax.scatter(target[0],target[2],target[1])
    ax.set_xlabel( 'X' )
    ax.set_ylabel( 'Z' )
    ax.set_zlabel( 'Y' )
    ax.grid(True)
    ax.legend()
    plt.show()

def detectCollision( baseServo,armServo, targetX,targetY,targetZ, debug=False):
    #Define dimmensions of the experimental setup
    #Units in cm because the american English System is terrible
    # The top right corner of the experiment is the origin 
    # left and right from the base
    #x_offset = 28.0
    x_offset = 30.0
    #up and down from the base
    y_offset = 20.0
    #This should be the depth from the base ie motion directly away from base.
    z_offset = 20.0
    l = 16 #length of the party blower


    yxcomp = l*cos(armServo-pi/2)
    ycomp = yxcomp*sin(baseServo)
    zcomp = l*sin(armServo-pi/2)
    xcomp = yxcomp*cos(baseServo)

    
    #I need to verify that z is the depth and that i havent flipped the coordinates somewhere
    target = [targetX, targetY, targetZ]

    P0 = [x_offset, y_offset, z_offset]
    P1 = [x_offset+xcomp, y_offset+ycomp, z_offset+zcomp]
    
    
    
    V = [xcomp, ycomp, zcomp]
    W = [target[0]-P0[0], target[1]-P0[1], target[2]-P0[2]]
    
    if debug:
        print '(x,y): {0} , {1}'.format(baseServo, armServo)
        print 'xcomp: {0} \nycomp: {1} \nzcomp: {2}'.format(xcomp, ycomp, zcomp)
        print 'P1: {0}'.format(P1)
        print W
        plotScene(P0,P1,target)

    C1 = dot(W,V)
    C2 = dot(V,V)
    #print 'C1: {0}'.format(C1)
    #print 'C2: {0}'.format(C2)
    if C1 <= 0:
        D = euclideanDist(target,P0)
        #print 'D: {0}'.format(D)
    elif C2 <= C1:
        D = euclideanDist(target,P1)
        #print 'D: {0}'.format(D)
    else:
        b = C1/C2
        PB = [P0[0] + b*V[0], P0[1] + b*V[1], P0[2] + b*V[2]]
        D = euclideanDist(target,PB)
        #print 'D: {0}'.format(D)
    
    isHit = 0;
    if D<1:
        #print 'Target was hit!'
        isHit = 1;
    return (isHit, D)


if __name__=='__main__':
    base = 1.08146
    #base 1.56887,
    arm = 1.19026
    tx = 27
    ty =13
    tz = 12.5
    detectCollision(base,arm,tx,ty,tz,True)
    #1.56887,1.57079
    #base 2.05628
    #arm 1.95132
