# -*- coding: utf-8 -*-
"""
A program to analyse the effectiveness of power ratings.  

The program reads in .CSV files with pre-match power ratings and results, and gives 
stats on how many results were successfully predicted for a given threshold.  Stats
are then outputed to a .CSV file.
"""

import pandas as pd
#import pprint

outputfile = "prating.csv"

#create the column header row
#Threshold Value	# Predictions	# Correct Home	# Correct Away	# Wrong Home	# Wrong Away	% Correct	% Correct Home	% Correct Away	% +1 Pred	% +1 Home Handicap	% +1 Away Handicap	% +2 Pred	% +2 Home Handicap	% +2 Away 
headerLine = 'Threshold Value, # Predictions, # Correct Home, # Correct Away, # Wrong Home, # Wrong Away, % Correct, % Correct Home, % Correct Away, % +1 Pred, % +1 Home Handicap, % +1 Away Handicap, % +2 Pred, % +2 Home Handicap, % +2 Away' + '\n'

#create the data  row
contentLine = ''


def get_percentages(predictions, threshold = 0.8):
    
    dataline = ''
    #seperate correct and wrong predictions
    corrPredictions = predictions[predictions['CorrPred'] == 1]
    wrongPredictions = predictions[predictions['CorrPred'] == 0]

    #seperate out the predictions > threshold 
    corrHomePred = corrPredictions[corrPredictions['Difference'] >= threshold]
    corrAwayPred = corrPredictions[corrPredictions['Difference'] <= -threshold]
    wrongHomePred = wrongPredictions[wrongPredictions['Difference'] >= threshold]
    wrongAwayPred = wrongPredictions[wrongPredictions['Difference'] <= -threshold]

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
        
    print ('Threshold value : ', threshold)
    dataline += str(threshold) + ', '
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
    print ('Percentage correct predictions : ', ((numCorrHomePred + numCorrAwayPred) / numPredictions))
    dataline += str(((numCorrHomePred + numCorrAwayPred) / numPredictions)) + ', '
    print ('Percentage correct home predictions : ', (numCorrHomePred / (numCorrHomePred + numWrongHomePred)))
    dataline += str((numCorrHomePred / (numCorrHomePred + numWrongHomePred))) + ', '
    print ('Percentage correct away predictions : ', (numCorrAwayPred / (numCorrAwayPred + numWrongAwayPred)))
    dataline += str((numCorrAwayPred / (numCorrAwayPred + numWrongAwayPred))) + ', '
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
    print ('Percentage of +1 predictions that would have won : ', ((numHomeZero + numAwayZero) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred)))  
    print ('Percentage of +2 predictions that would have won : ', ((numHomeOne + numAwayOne) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred)))   
    print ('Percentage of +3 predictions that would have won : ', ((numHomeTwo + numAwayTwo) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred)))   
    print (' ')	
    print ('Percentage of +1 home predictions that would have won : ',(numHomeZero / (numCorrHomePred + numWrongHomePred)))  
    print ('Percentage of +2 home predictions that would have won : ',(numHomeOne / (numCorrHomePred + numWrongHomePred)))   
    print ('Percentage of +3 home predictions that would have won : ',(numHomeTwo / (numCorrHomePred + numWrongHomePred)))   
    print (' ')   
    print ('Percentage of +1 away predictions that would have won : ',(numAwayZero / (numCorrAwayPred + numWrongAwayPred)))  
    print ('Percentage of +2 away predictions that would have won : ',(numAwayOne / (numCorrAwayPred + numWrongAwayPred)))   
    print ('Percentage of +3 away predictions that would have won : ',(numAwayTwo  / (numCorrAwayPred + numWrongAwayPred)))   
    print (' ')   
    dataline += str(((numHomeZero + numAwayZero) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred))) + ', '
    dataline += str((numHomeZero / (numCorrHomePred + numWrongHomePred))) + ', '
    dataline += str((numAwayZero / (numCorrAwayPred + numWrongAwayPred))) + ', '
	
    dataline += str(((numHomeOne + numAwayOne) / (numCorrHomePred + numWrongHomePred + numCorrAwayPred + numWrongAwayPred))) + ', '
    dataline += str((numHomeOne / (numCorrHomePred + numWrongHomePred))) + ', '
    dataline += str((numAwayOne / (numCorrAwayPred + numWrongAwayPred))) + '\n'
    
    return dataline



droplist = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6']
keeplist = ['Difference','CorrPred', 'FTR', 'FTHG', 'FTAG']


'''
Function takes a csv file and reads to a dataframe, drops colums included in droplist, cuts from nip to the 
end of the frame, then cuts up to tuck from the start of the frame.  Finally the function returns just 
the colums in keeplist.
'''
def load_and_trim(filename, nip, tuck):
    
	full_frame = pd.read_csv(filename, header=0, parse_dates=True) 
	frame = full_frame.drop(droplist, axis=1)
	frame = frame.iloc[:nip]    #cut the last week
	frame = frame.iloc[tuck:]   #cut the first few 'training' weeks (usually 10)
	
	return frame[keeplist]



'''Read in the 2017/18 stats'''
german17 = load_and_trim("german2017.csv", 297, 90)
french17 = load_and_trim("french2017.csv", 370, 99)
italian17 = load_and_trim("italian2017.csv", 370, 99)
scotish17 = load_and_trim("scotish2017.csv", 222, 60)
spanish17 = load_and_trim("spanish2017.csv", 370, 100)
english17 = load_and_trim("english2017.csv", 370, 100)


'''Read in the 2016/17 stats      Note - I'm using the same values as 2017/18 as approximate values.'''
german16 = load_and_trim("german2016.csv", 297, 90)
french16 = load_and_trim("french2016.csv", 370, 99)
italian16 = load_and_trim("italian2016.csv", 370, 99)
scotish16 = load_and_trim("scotish2016.csv", 222, 60)
spanish16 = load_and_trim("spanish2016.csv", 370, 100)
english16 = load_and_trim("english2016.csv", 370, 100)

'''Merge the data frames and see how many predictions were successful.'''
mergedPred = pd.concat([spanish16, italian16, german16, french16, scotish16, english16, spanish17, italian17, german17, french17, scotish17, english17])


contentLine = get_percentages(mergedPred)
contentLine += get_percentages(mergedPred, 0.7)
contentLine += get_percentages(mergedPred, 0.6)
contentLine += get_percentages(mergedPred, 0.4)
#contentLine += get_percentages(mergedPred, 1.5)
#contentLine += get_percentages(mergedPred, 1.6)
#contentLine += get_percentages(mergedPred, 1.8)
#contentLine += get_percentages(mergedPred, 2.0)


#save the header and data out to a file
outputfile = open(outputfile, 'w')
outputfile.write(headerLine)
outputfile.write(contentLine)
outputfile.close()
