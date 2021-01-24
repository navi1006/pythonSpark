# libraries
import json

# function to unjumble the input words and return a list
import sys
from itertools import permutations

import enchant


def findInputWords(inputWordsList):
    # loop through inoutwordlist to find the correct word save it in a list
    english_d = enchant.Dict("en_US")
    unJumbledWordList = []
    for word in inputWordsList:
        letters = [x.lower() for x in word]
        for y in set(permutations(letters)):  # converted from list to set to get unique permuations
            permutationWord = "".join(y)
            if len(permutationWord) > 2:
                if english_d.check(permutationWord):
                    #print(permutationWord)
                    unJumbledWordList.append(permutationWord)
    return unJumbledWordList

# Function to return all the circled letters
def findCircledLetters(correctedInputWordList, circlePostions):
    print("findCircledLetters")
    combinedList = []
    print(circlePostions)
    for i in range(len(correctedInputWordList)):
        for j in range(len(circlePostions[i])):
            combinedList.append(correctedInputWordList[i][circlePostions[i][j]].upper())

    return combinedList

# Function to get the highest priority word
def getFinalWord(size, combinedList, dictData):
    english_d = enchant.Dict("en_US")
    maxfreq = sys.maxsize  # set inital as max value
    currWord = None
    outputDict = dict()

    word = None
    #print(type(dictData))
    # step 1. find word with # no of letters
    for i in set(permutations(combinedList, size)):
        word = "".join(i).lower()

        #if english_d.check(word):
            #print(" English Word ------ ", word)
            #if('word' not in dictData):
                #print(" \nWord not found in the dict")
        if(word in dictData):

            #print(" Word ------ ", word)
            value = dictData.get(word)
            if((value!=0) and (value < maxfreq)):
                maxfreq = value
                currWord = word
                print("Current Value:",value, " ", currWord)

    #print("\nMax Freq : ",maxfreq, " ", currWord)

    outputDict[currWord] = maxfreq
    return outputDict


# Function to remove the letters from list/string
def removeLetters(finalWord, combinedList):
    print("\nremoveLetter comlist: ",combinedList)
    word = list(finalWord.keys())[0]
    word = str(word).upper()
    print("Word Key: ", word)
    modifiedW = combinedList
    print("Type :", type(word[0]), " word[0] : ", word[0])
    for i in range(len(word)):
        modifiedW.remove(word[i])
    #print("\n modifiedW", modifiedW)
    return modifiedW


# processor function to perform all the logic
def processor(inputWordsList, circlePostions, finalSolutionFormat, dictData):
    print("Processor")
    correctedInputWordList = findInputWords(inputWordsList)  # will hold unjumbled input list
    print(correctedInputWordList)
    combinedList = findCircledLetters(correctedInputWordList, circlePostions)
    print("CombinedList :", combinedList)
    print("Final Solution Format :", finalSolutionFormat)
    #outputDict=None
    modifiedList = combinedList
    for i in range(len(finalSolutionFormat)-1):
        finalWord=getFinalWord(finalSolutionFormat[i], modifiedList, dictData)
        print("*********\n", finalWord)
        #send letters to be removed
        modifiedList=removeLetters(finalWord, combinedList)
        print("processor : \n modifiedList : ", modifiedList)



# main function to drive the program
# input - Get all the possible inputs as parameters
# read the dict file and pass as pararmeter to processor
def main():
    print("main")
    # puzzle 1
    inputWordsList = ("NAGLD", "RAMOJ", "CAMBLE", "WRALEY")
    circlePostions = [[1, 3, 4], [2, 3], [0, 1, 3], [0, 2, 4]]  # index values for circled words
    finalSolutionFormat = [3, 4, 4]  # number of letters and words in the final solution

    # puzzle 5
    #inputWordsList = ("GYRINT", "DRIVET", "SNAMEA", "CEEDIT", "SOWDAH", "ELCHEK")

    # read the dict json file
    dictFile = open('freq_dict.json')
    dictData = json.loads(dictFile.read())

    finalSolution = processor(inputWordsList, circlePostions, finalSolutionFormat, dictData)


main()