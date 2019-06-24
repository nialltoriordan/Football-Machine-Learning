# -*- coding: utf-8 -*-
"""
A program to analyse the effectiveness of power ratings.  

The program reads in .CSV files with pre-match power ratings and results, and gives 
stats on how many results were successfully predicted for a given threshold.  Stats
are then outputed to a .CSV file.
"""

import pandas as pd
import pprint
import numpy as np

outputfile = "hrating.csv"

#create the column header row
#Threshold Value	# Predictions	# Correct Home	# Correct Away	# Wrong Home	# Wrong Away	% Correct	% Correct Home	% Correct Away	% +1 Pred	% +1 Home Handicap	% +1 Away Handicap	% +2 Pred	% +2 Home Handicap	% +2 Away 
headerLine = 'Threshold Value, Form Threshold, PP Threshold, Avg Form, Avg PP, # Predictions, # Correct Home, # Correct Away, # Wrong Home, # Wrong Away, % Correct, % Correct Home, % Correct Away, % +1 Pred, % +1 Home Handicap, % +1 Away Handicap, % +2 Pred, % +2 Home Handicap, % +2 Away' + '\n'

#create the data  row
contentLine = ''


def get_percentages(predictions, threshold = 0.8, form_threshold = 5.0, pp_threshold = 0.5):
    
    dataline = ''
    #seperate correct and wrong predictions
    corrPredictions = predictions[predictions['CorrPred'] == 1]
    wrongPredictions = predictions[predictions['CorrPred'] == 0]

    #seperate out the predictions > threshold 
    corrHomePred = corrPredictions[corrPredictions['Difference'] >= threshold]
    corrAwayPred = corrPredictions[corrPredictions['Difference'] <= -threshold]
    wrongHomePred = wrongPredictions[wrongPredictions['Difference'] >= threshold]
    wrongAwayPred = wrongPredictions[wrongPredictions['Difference'] <= -threshold]
	
    print ('Threshold value : ', threshold)
    dataline += str(threshold) + ', '	
    print('Form threshold, pp threshold : ' , form_threshold, pp_threshold)
    dataline += str(form_threshold) + ', '
    dataline += str(pp_threshold) + ', '
    print('Average form for correct predictions : ' , ((  (corrHomePred["Form"].mean() + corrAwayPred["Form"].mean()) / 2)))
    dataline += str( (( (corrHomePred["Form"].mean() + corrAwayPred["Form"].mean()) / 2))) + ', '	
    print('Average pp for correct predictions : ' , ((   (corrHomePred["PPower"].mean() + corrAwayPred["PPower"].mean())  / 2)))
    dataline += str( ((corrHomePred["PPower"].mean() + corrAwayPred["PPower"].mean()) / 2)) + ', '
	
    corrHomePred = corrHomePred[corrHomePred['Form'] >= form_threshold]
    corrAwayPred = corrAwayPred[corrAwayPred['Form'] >= form_threshold]
    wrongHomePred = wrongHomePred[wrongHomePred['Form'] >= form_threshold]
    wrongAwayPred = wrongAwayPred[wrongAwayPred['Form'] >= form_threshold]
	
    corrHomePred = corrHomePred[corrHomePred['PPower'] >= pp_threshold]
    corrAwayPred = corrAwayPred[corrAwayPred['PPower'] >= pp_threshold]
    wrongHomePred = wrongHomePred[wrongHomePred['PPower'] >= pp_threshold]
    wrongAwayPred = wrongAwayPred[wrongAwayPred['PPower'] >= pp_threshold]

    #seperate wrong predictions into categorys
    wrongHomeDraw = wrongHomePred[wrongHomePred['FTR'] == 'D']
    wrongAwayDraw = wrongAwayPred[wrongAwayPred['FTR'] == 'D']  
    
    #generate stats
    numCorrHomePred = len(corrHomePred)
    numCorrAwayPred = len(corrAwayPred)
    numWrongHomePred = len(wrongHomePred)
    numWrongAwayPred = len(wrongAwayPred)
    numPredictions = numCorrHomePred + numCorrAwayPred +numWrongHomePred + numWrongAwayPred
    numWrongHomeDraw = len(wrongHomeDraw)
    numWrongHomeLoss = numWrongHomePred - numWrongHomeDraw
    numWrongAwayDraw = len(wrongAwayDraw)
    numWrongAwayLoss = numWrongAwayPred - numWrongAwayDraw
    
    #generate handicap stats
    wrongHomePredZero = wrongHomePred[(wrongHomePred['FTHG'] - wrongHomePred['FTAG']) == 0 ]
    wrongHomePredOne = wrongHomePred[(wrongHomePred['FTHG'] - wrongHomePred['FTAG']) == -1 ]
    wrongHomePredTwo = wrongHomePred[(wrongHomePred['FTHG'] - wrongHomePred['FTAG']) == -2 ]
    
    numHomeZero = len(wrongHomePredZero) + numCorrHomePred
    numHomeOne = len(wrongHomePredOne) + numHomeZero
    numHomeTwo = len(wrongHomePredTwo) + numHomeOne
    
    wrongAwayPredZero = wrongAwayPred[(wrongAwayPred['FTHG'] - wrongAwayPred['FTAG']) == 0 ]
    wrongAwayPredOne = wrongAwayPred[(wrongAwayPred['FTHG'] - wrongAwayPred['FTAG']) == 1 ]
    wrongAwayPredTwo = wrongAwayPred[(wrongAwayPred['FTHG'] - wrongAwayPred['FTAG']) == 2 ]
    
    numAwayZero = len(wrongAwayPredZero) + numCorrAwayPred
    numAwayOne = len(wrongAwayPredOne) + numAwayZero
    numAwayTwo = len(wrongAwayPredTwo) + numAwayOne
        

    print ('Total number of predictions above threshold : ', numPredictions)
    dataline += str(numPredictions) + ', '
    print ('Total number of correct home predictions : ', numCorrHomePred)
    dataline += str(numCorrHomePred) + ', '
    print ('Total number of correct away predictions : ', numCorrAwayPred)
    dataline += str(numCorrAwayPred) + ', '
    print ('Total number of wrong home predictions : ', numWrongHomePred)
    dataline += str(numWrongHomePred) + ', '
    print ('Total number of wrong home predictions that drew : ', numWrongHomeDraw)
    print ('Total number of wrong home predictions that lost : ', numWrongHomeLoss)
    print ('Total number of wrong away predictions  : ', numWrongAwayPred)
    dataline += str(numWrongAwayPred) + ', '
    print ('Total number of wrong away predictions that drew : ', numWrongAwayDraw)
    print ('Total number of wrong away predictions that lost : ', numWrongAwayLoss)

    print (' ')
    if(numPredictions > 0):
	    print ('Percentage correct predictions : ', ((numCorrHomePred + numCorrAwayPred) / numPredictions))
	    dataline += str(((numCorrHomePred + numCorrAwayPred) / numPredictions)) + ', '
    else:
	    print ('No predictions above threshold.') 
	    dataline += str(0) + ', '
    if((numCorrHomePred + numWrongHomePred) > 0):
	    print ('Percentage correct home predictions. ', (numCorrHomePred / (numCorrHomePred + numWrongHomePred)))
	    dataline += str((numCorrHomePred / (numCorrHomePred + numWrongHomePred))) + ', '
    else:
	    print ('Error generating percentage correct home predictions. ')
	    dataline += str(0) + ', '
    if((numCorrAwayPred + numWrongAwayPred) > 0):
	    print ('Percentage correct away predictions : ', (numCorrAwayPred / (numCorrAwayPred + numWrongAwayPred)))
	    dataline += str((numCorrAwayPred / (numCorrAwayPred + numWrongAwayPred))) + ', '
    else:
	    print ('Error generating percentage correct away predictions. ')
	    dataline += str(0) + ', '
    print (' ')
    '''
    print ('Percentage of wrong home predictions that drew : ',(numWrongHomeDraw / numWrongHomePred))
    print ('Percentage of wrong home predictions that lost ', (numWrongHomeLoss / numWrongHomePred))
    print (' ')
    print ('Percentage of wrong away predictions that drew : ', (numWrongAwayDraw / numWrongAwayPred))
    print ('Percentage of wrong away predictions that lost ', (numWrongAwayLoss / numWrongAwayPred))
    print (' ')   
    '''
    print (' ')
    if((numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred) > 0):
        print ('Percentage of +1 predictions that would have won : ', ((numHomeZero + numAwayZero) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred)))  
        dataline += str(((numHomeZero + numAwayZero) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred))) + ', '
    else:
        print ('Error generating percentage +1 predictions that would have won. ')
        dataline += str(0) + ', '
    if((numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred) > 0):
        print ('Percentage of +2 predictions that would have won : ', ((numHomeOne + numAwayOne) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred))) 
        dataline += str(((numHomeOne + numAwayOne) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred))) + ', '
    else:
        print ('Error generating percentage +2 predictions that would have won. ')
        dataline += str(0) + ', '	
    #print ('Percentage of +3 predictions that would have won : ', ((numHomeTwo + numAwayTwo) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred)))   
    print (' ')	
    if((numCorrHomePred + numWrongHomePred) > 0):
        print ('Percentage of +1 home predictions that would have won : ',(numHomeZero / (numCorrHomePred + numWrongHomePred))) 
        dataline += str((numHomeZero / (numCorrHomePred + numWrongHomePred))) + ', '
    else:
        print ('Error generating percentage +1 home predictions that would have won. ')
        dataline += str(0) + ', '
    if((numCorrHomePred + numWrongHomePred) > 0):
        print ('Percentage of +2 home predictions that would have won : ',(numHomeOne / (numCorrHomePred + numWrongHomePred))) 
        dataline += str((numHomeOne / (numCorrHomePred + numWrongHomePred))) + ', '		
    else:
        print ('Error generating percentage +2 home predictions that would have won. ')
        dataline += str(0) + ', '
    #print ('Percentage of +3 home predictions that would have won : ',(numHomeTwo / (numCorrHomePred + numWrongHomePred)))   
    print (' ')   
     
    if((numCorrAwayPred + numWrongAwayPred) > 0):
        print ('Percentage of +1 away predictions that would have won : ',(numAwayZero / (numCorrAwayPred + numWrongAwayPred)))	
        dataline += str((numAwayZero / (numCorrAwayPred + numWrongAwayPred))) + ', '
    else:
        print ('Error generating percentage +1 away predictions that would have won. ')
        dataline += str(0) + ', '	
    if((numCorrAwayPred + numWrongAwayPred) > 0):
        print ('Percentage of +2 away predictions that would have won : ',(numAwayOne / (numCorrAwayPred + numWrongAwayPred)))   
        dataline += str((numAwayOne / (numCorrAwayPred + numWrongAwayPred))) + '\n'
    else:
        print ('Error generating percentage +2 away predictions that would have won. ')
        dataline += str(0) + '\n'
    #print ('Percentage of +3 away predictions that would have won : ',(numAwayTwo  / (numCorrAwayPred + numWrongAwayPred)))   
    print (' ')   

    
    
	
    
    
    return dataline






'''Read in the stats'''
mergedPred = pd.read_csv("fullfeatures.csv", header=0, parse_dates=True) 

for form in range(5, 18):
    for ppower in np.arange(0.5, 6.0, 0.5):
        contentLine += get_percentages(mergedPred, 1.0, form, ppower)
        contentLine += get_percentages(mergedPred, 1.2, form, ppower)
        contentLine += get_percentages(mergedPred, 1.4, form, ppower)
        contentLine += get_percentages(mergedPred, 1.5, form, ppower)
        contentLine += get_percentages(mergedPred, 1.6, form, ppower)
        contentLine += get_percentages(mergedPred, 1.8, form, ppower)
        contentLine += get_percentages(mergedPred, 2.0, form, ppower)


#save the header and data out to a file
outputfile = open(outputfile, 'w')
outputfile.write(headerLine)
outputfile.write(contentLine)
outputfile.close()
