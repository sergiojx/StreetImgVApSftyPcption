%% Urban Safety Perception Project - Phase 0 : Build a cross validation test No Nolmalized
%
%  Introduction
%  ------------
% CieLAB, HOG and Gist descriptors have been optained. 5505 
% images were used in this first approach. This script builds
% each vote feature vector and its asociated outcome. This information
% is compiled into a training txt file.

%% Initialization
clear ; close all; clc


randomset1 = zeros(20000,3);

% random vote generation
% 2000 entry arrow vector
va = (1:1:2000);
vb = (3505:1:5504);
for x=1:2000
    
    v1 = randi([3505,5504],1,1);
    v2 = randi([3505,5504],1,1);
    v3 = randi([3505,5504],1,1);
    v4 = randi([3505,5504],1,1);
    v5 = randi([3505,5504],1,1);
    offset = x*10 - 10;
    randomset1(offset+1,:) = [v1 va(x) 1];
    randomset1(offset+2,:) = [va(x) v1 1];
    randomset1(offset+3,:) = [v2 va(x) 1];
    randomset1(offset+4,:) = [va(x) v2 1];
    randomset1(offset+5,:) = [v3 va(x) 1];
    randomset1(offset+6,:) = [va(x) v3 1];
    randomset1(offset+7,:) = [v4 va(x) 1];
    randomset1(offset+8,:) = [va(x) v4 1];
    randomset1(offset+9,:) = [v5 va(x) 1];
    randomset1(offset+10,:) = [va(x) v5 1];   
end

csvwrite('randomIndexer.txt',randomset1);
%--------------------------------------------------------------------------
close all;





