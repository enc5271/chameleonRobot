%Initialize Agent
%load Q table
fid = fopen('QTable.csv');
rawTable = textscan(fid, '%d16 , %d16 , %d8 , %d , %d, %s , %d16')
rawStates = State(rawTable(1:5));
rawActions = rawTable(6);
rawPairs = StateActionPair(rawStates,rawActions)
rewards = rawTable(7);

%Q = containers.Map(rawPairs,rewards)

%load frequency table

%%%%%%%%%%%%%%%%%%%%%
nTargets = 1;
rPrime = 100;

%set Target positions
%targets = randi([0,100],nTargets,3);  
targets = [ 15; 15; 7]

%Map targets actual position to pixels
focalD = 25;
Projected = [1,0,0,0;0,1,0,0;0,0,-1/focalD,0]*targets(1)

%set initial State


for v = 1:nTargets
    T = targets(v,:)
    
    currentState = State;
    currentState.armServo = pi/2;
    currentState.baseServo = pi/2;
    currentState.fire = false;
    
    isHit = detectCollision(currentState, T)
    if isHit
        Q(currentState,none) = rPrime;
    end
    %Write Target to file. 
    %{filename = strcat('trial_',int2str(v),'_',date)
    fid = fopen(filename,'w');
    fprintf(fid, '%f , %f , %f \n\n',T);
    %}
    
    
    
    %write agent state to file
    %fprintf(fid, '%f , %f , %d \n',i,j,isHit); 
    
    
end
%for i = target
    
