function [ isHit ] = detectCollision( baseServo,armServo, targetX,targetY,targetZ)
%detectCollision Calculates if the given state has hit the target
%   Detailed explanation goes here
    
    %Define dimmensions of the experimental setup
    %Units in cm because the american English System is terrible
    % The top right corner of the experiment is the origin 
    % left and right from the base
    x_offset = 28.0;
    %up and down from the base
    y_offset = 18;
    %This should be the depth from the base ie motion directly away from base.
    z_offset = 14.0;
    l = 16; %length of the party blower

    xzcomp = l*cos(armServo-pi/2);
    zcomp = xzcomp*sin(baseServo);
    ycomp = l*sin(armServo-pi/2);
    xcomp = xzcomp*cos(baseServo);

    %I need to verify that z is the depth and that i havent flipped the coordinates somewhere
    target = [targetX, targetY, targetZ];

    P0 = [x_offset y_offset z_offset];
    P1 = [x_offset+xcomp y_offset+ycomp z_offset+zcomp];
    V = [xcomp ycomp zcomp];
    W = target-P0;
    %disp(target);

    C1 = dot(W,V);
    C2 = dot(V,V);
    if C1 <= 0
        D = pdist([target;P0],'euclidean');
    elseif C2 <= C1
        D = pdist([target;P1],'euclidean');
    else
        b = C1/C2;
        PB = P0 + b*V;
        D = pdist([target;PB],'euclidean');
    end
    
    isHit = 0;
    if D<1
        disp('Target was hit!')
        isHit = 1;
    end
    %Scatter plot for debugging
    %xx=[P0(1), P1(1)]
    %yy=[P0(2), P1(2)]
    %zz=[P0(3), P1(3)]
    %plot3(xx,yy,zz)
    %xx=[P0(1), P1(1), target(1)]
    %yy=[P0(2), P1(2), target(2)]
    %zz=[P0(3), P1(3), target(3)]
    %scatter3(xx,yy,zz)
end

