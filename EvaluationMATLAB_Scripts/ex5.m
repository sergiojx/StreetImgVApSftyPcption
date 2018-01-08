%% Urban Safety Perception Project - Phase 0 : Generates evaluation set
%
%  Introduction
%  ------------
% CieLAB, HOG and Gist descriptors have been optained. 5505 
% images were used in this first approach. This script builds
% each vote feature vector and its asociated outcome. This information
% is compiled into a training txt file.

%% Initialization
clear ; close all; clc

%% Load Data
%  The first two columns contains the descriptor index of each image
%  involved in a vote. The third column keeps the vote outcome

Vindexer = load('randomIndexer.txt');
fprintf("descriptorIndexer.txt loaded into Vindexer\n");
GistX = load("/Users/SerG1oAC/Documents/courseraML2017/gistExtrator/gistSet.txt");
fprintf("gistSet.txt loaded into GistX\n");
HogX = load("/Users/SerG1oAC/Documents/courseraML2017/hogExtractor/hogSet.txt");
fprintf("hogSet.txt loaded into HogX\n");
ClabLX = load("/Users/SerG1oAC/Documents/courseraML2017/cielabExtractor/cielabL2.txt");
fprintf("cielabL2.txt loaded into ClabLX\n");
ClabAX = load("/Users/SerG1oAC/Documents/courseraML2017/cielabExtractor/cielabA2.txt");
fprintf("cielabA2.txt loaded into ClabAX\n");
ClabBX = load("//Users/SerG1oAC/Documents/courseraML2017/cielabExtractor/cielabB2.txt");
fprintf("cielabB2.txt loaded into ClabBX\n");

[votes, dc] = size(Vindexer);
[clabLrows, clabLcols] = size(ClabLX);
[clabArows, clabAcols] = size(ClabAX);
[clabBrows, clabBcols] = size(ClabBX);
[gistrows, gistcols] = size(GistX);
[hogrows, hogcols] = size(HogX);

%Set 1 reduce CIELab and Hog descriptors
f1Size = gistcols + 80 + 80 + 300;
set1 = zeros(votes,((f1Size*2) + 1));
for i=1:votes
    image0Index = Vindexer(i,1);
    image1Index = Vindexer(i,2);
    vote = Vindexer(i,3);
    image0ftrV = [GistX(image0Index,:),ClabAX(image0Index,10:89),ClabBX(image0Index,10:89),HogX(image0Index,282:581)];
    image1ftrV = [GistX(image1Index,:),ClabAX(image1Index,10:89),ClabBX(image1Index,10:89),HogX(image1Index,282:581)];
    if vote == 1
        pairftrV = [image0ftrV(1,:),image1ftrV(1,:),1];    
    elseif vote == 2
        pairftrV = [image1ftrV(1,:),image0ftrV(1,:),1];  
    else
        pairftrV = [image0ftrV(1,:),image1ftrV(1,:),0];
    end
    set1(i,:) = pairftrV;
end

muset1 = mean(set1);
sigmaset1 = std(set1);

% training aeio test u_____________________________________________________
fprintf("creatign libsvm evaluation\n");
fileID = fopen('evaluation','w');
for i=1:votes
    if set1(i,((f1Size*2) + 1)) == 1
        fprintf(fileID,'+1 ');
    else
        fprintf(fileID,'-1 ');
    end
    for j=1:(f1Size*2)
        normal = (set1(i,j) - muset1(j))/sigmaset1(j);
        fprintf(fileID,'%i:%2.6f ',j,normal);
    end
    fprintf(fileID,'\n');
end
fclose(fileID);

%--------------------------------------------------------------------------
close all;





