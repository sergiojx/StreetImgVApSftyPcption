%% Urban Safety Perception Project - Phase 0 : Build a cross validation test
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

Vindexer = load('descriptorIndexer_Nov_24.txt');
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
    pairftrV = [image0ftrV(1,:),image1ftrV(1,:),vote];
    set1(i,:) = pairftrV;
end

muset1 = mean(set1);
sigmaset1 = std(set1);

% training aeio test u_____________________________________________________
fprintf("creatign libsvm set1aeio\n");
fileID = fopen('set1aeio','w');
for i=1:floor(votes*0.8)
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
fprintf("creatign libsvm set1u\n");
fileID = fopen('set1u','w');
for i=floor(votes*0.8):votes
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
% training aeiu test o_____________________________________________________
fprintf("creatign libsvm set1aeiu\n");
fileID = fopen('set1aeiu','w');
for i=1:floor(votes*0.6)
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
for i=floor(votes*0.8):votes
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
fprintf("creatign libsvm set1o\n");
fileID = fopen('set1o','w');
for i=floor(votes*0.6):floor(votes*0.8)
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
% training aeou test i_____________________________________________________
fprintf("creatign libsvm set1aeou\n");
fileID = fopen('set1aeou','w');
for i=1:floor(votes*0.4)
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
for i=floor(votes*0.6):votes
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
fprintf("creatign libsvm set1i\n");
fileID = fopen('set1i','w');
for i=floor(votes*0.4):floor(votes*0.6)
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
% training aiou test e_____________________________________________________
fprintf("creatign libsvm set1aiou\n");
fileID = fopen('set1aiou','w');
for i=1:floor(votes*0.2)
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
for i=floor(votes*0.4):votes
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
fprintf("creatign libsvm set1e\n");
fileID = fopen('set1e','w');
for i=floor(votes*0.2):floor(votes*0.4)
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
% training eiou test a_____________________________________________________
fprintf("creatign libsvm set1eiou\n");
fileID = fopen('set1eiou','w');
for i=floor(votes*0.2):votes
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
fprintf("creatign libsvm set1a\n");
fileID = fopen('set1a','w');
for i=1:floor(votes*0.2)
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





