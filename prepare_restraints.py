
import numpy as np
from os import listdir
import os

def readFasta(file):
    seq={}
    count=1
    with open(file,'rU') as handle:
        for line in handle:
            if not line.startswith('>'):
	      if line[0]!=' ' and line[0]!='\n':
                line=line.strip()
		sequence=line
		print sequence
                for s in line:
                    seq[count]=s
                    count+=1
    return seq, sequence


rr_f=CONTACT_PREDICTIONS_PATH
rr_8_13_f=DISTANCE_PREDICTIONS_PATH_8_13_A
rr_13_18_f=DISTANCE_PREDICTIONS_PATH_13_18_A
rr_18_23_f=DISTANCE_PREDICTIONS_PATH_18_23_A

seq_f=FASTA_SEQ_PATH

output=OUTPUT_FILE
outputhandle=open(output,'wb')

rr={}
rr_8_13={}
rr_13_18={}
rr_18_23={}

rr_8_13_threshold=0.6
rr_13_18_threshold=0.6
rr_18_23_threshold=0.7

seq,sequence=readFasta(seq_f)
slen=len(sequence)

slen1_5=1.5*slen
slen1_5=np.rint(slen1_5) 

positionList=set()

#read contact predictions
count=0
with open(rr_f,'rU') as handle:
        for line in handle:
            line=line.strip().split()
            if line[0].isdigit():
               left=int(line[0])
               right=int(line[1])
               score=float(line[4])
               count=count+1
               if count>slen1_5:
                 break
               rr[(left,right)]=score
               positionList.add((left,right))

#read distance predictions of bin 8-13A
with open(rr_8_13_f,'rU') as handle:
        count=0
        for line in handle:
           line=line.strip().split()
           left=int(line[0])
           right=int(line[1])
           score=float(line[4])
           if score<rr_8_13_threshold or count>slen1_5:
               break
           rr_8_13[(left,right)]=score
           count+=1
           positionList.add((left,right))

#read distance predictions of bin 13-18A
with open(rr_13_18_f,'rU') as handle:
       count=0
       for line in handle:
            line=line.strip().split()
            left=int(line[0])
            right=int(line[1])
            score=float(line[4])
            if score<rr_13_18_threshold or count>slen:
                break
            rr_13_18[(left,right)]=score
            count+=1
            positionList.add((left,right))

#read distance predictions of bin 18-23A
with open(rr_18_23_f,'rU') as handle:
       count=0
       for line in handle:
            line=line.strip().split()
            left=int(line[0])
            right=int(line[1])
            score=float(line[4])
            if score<rr_18_23_threshold or count>0.5*slen:                                                                                
                break
            rr_18_23[(left,right)]=score
            count+=1
            positionList.add((left,right))
            
for position in positionList:
        if position in rr and position in rr_8_13:
            if rr[position]>rr_8_13[position]-0.3:
                del rr_8_13[position]
            else:
                del rr[position]

for position in positionList:
        if position in rr and position in rr_13_18:
            if rr[position]>rr_13_18[position]-0.3:
                del rr_13_18[position]
            else:
                del rr[position]

for position in positionList:
        if position in rr_8_13 and position in rr_13_18:
            if rr_8_13[position]>rr_13_18[position]:
                del rr_13_18[position]
            else:
                del rr_8_13[position]

for position in positionList:
        if position in rr_18_23 and position in rr:
            if rr[position]>rr_18_23[position]-0.5:
                del rr_18_23[position]
            else:
                del rr[position]

for position in positionList:
        if position in rr_18_23 and position in rr_8_13:
            if rr_8_13[position]>rr_18_23[position]-0.5:
                del rr_18_23[position]
            else:
                del rr_8_13[position]

for position in positionList:
        if position in rr_18_23 and position in rr_13_18:
            if rr_13_18[position]>rr_18_23[position]-0.5:
                del rr_18_23[position]
            else:
                del rr_13_18[position]


                
PredictedDistanceRange={}
for position in rr:
        score=rr[position]
        lowerBound=3.2
        upperBound=-10.8*score+16.7
        lowerBound=round(lowerBound,2)
        upperBound=round(upperBound,2)
        PredictedDistanceRange[position]=(lowerBound,upperBound,'0_8')

for position in rr_8_13:
        score=rr_8_13[position]
        lowerBound=7.5
        upperBound=-12.5*score+23.5
        lowerBound=round(lowerBound,2)
        upperBound=round(upperBound,2)
        PredictedDistanceRange[position]=(lowerBound,upperBound,'8_13')

for position in rr_13_18:
        score=rr_13_18[position]
        lowerBound=8.6*score+4.84
        upperBound=-8.6*score+25.17
        lowerBound=round(lowerBound,2)
        upperBound=round(upperBound,2)
        PredictedDistanceRange[position]=(lowerBound,upperBound,'13_18')

for position in rr_18_23:
        score=rr_18_23[position]
        lowerBound=7.2*score+11.2
        upperBound=-7.2*score+29.2
        lowerBound=round(lowerBound,2)
        upperBound=round(upperBound,2)
        PredictedDistanceRange[position]=(lowerBound,upperBound,'18_23')


for position in PredictedDistanceRange:
        leftPosition=position[0]
        rightPosition=position[1]
        scoreRange=PredictedDistanceRange[position]
        tag=scoreRange[2]
        disLower=scoreRange[0]
        disUpper=scoreRange[1]

        ATOM1='CB'
        ATOM2='CB'
        if seq[leftPosition]=='G':
            ATOM1='CA'
        if seq[rightPosition]=='G':
            ATOM2='CA'

        if tag=='0_8':
            score=rr[position]
            weight=2.5
            std=0.5
            if score<0.9 and score>0.8:
                weight=1.5
                std=0.7
            elif score<0.8:
                weight=1.0
                std=1.0

        elif tag=='8_13':
            score=rr_8_13[position]
            std=1
            weight=1.5
            if score<0.8:
                 weight=0.5
                 std=1.5

        elif tag=='13_18':
            score=rr_13_18[position]
            std=1.5
            weight=0.8
            if score<0.8:
                weight=0.3
                std=1.0

        else:
            score=rr_18_23[position]
            std=1.5
            weight=0.6
            if score<0.8:
                weight=0.3
                std=1.0

        s="AtomPair %s %d %s %d SCALARWEIGHTEDFUNC %4.2f BOUNDED %4.2f %4.2f %3.1f NOE"%(ATOM1,leftPosition,ATOM2,rightPosition,weight,disLower,disUpper,std)
        outputhandle.write(s+'\n')

outputhandle.close()
