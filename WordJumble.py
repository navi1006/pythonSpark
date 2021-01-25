# libraries
import json
# function to unjumble the input words and return a list
import sys
from itertools import permutations

import enchant

from pyspark.sql import SparkSession


def findInputWords(inputWordsList):
    # loop through inputwordlist to find the correct word save it in a list
    english_d = enchant.Dict("en_US")
    unJumbledWordList = []
    for word in inputWordsList:
        letters = [x.lower() for x in word]
        for y in set(permutations(letters)):  # converted from list to set to get unique permutations
            permutationWord = "".join(y)
            if len(permutationWord) > 2:
                if english_d.check(permutationWord):
                    # print(permutationWord)
                    unJumbledWordList.append(permutationWord)
    return unJumbledWordList


# Function to return all the circled letters
def findCircledLetters(correctedInputWordList, circlePostions):
    #print("findCircledLetters")
    combinedList = []
    #print(circlePostions)
    for i in range(len(correctedInputWordList)):
        for j in range(len(circlePostions[i])):
            combinedList.append(correctedInputWordList[i][circlePostions[i][j]].upper())

    return combinedList


# Function to get the highest priority word
def getFinalWord(size, combinedList, dictData):
    english_d = enchant.Dict("en_US")
    maxfreq = sys.maxsize  # set inital as max value
    currWord = None
    # outputDict = SortedDict()
    outputDict = dict()
    word = None
    # print(type(dictData))
    # step 1. find word with # no of letters
    perms = set(permutations(combinedList, size))
    sorted(perms)# sort the permutations to get certainty on the result
    for i in perms:
        word = "".join(i).lower()

        # if english_d.check(word):
        # print(" English Word ------ ", word)
        # if('word' not in dictData):
        # print(" \nWord not found in the dict")

        if (word in dictData):
            # print(" Word ------ ", word)
            value = dictData.get(word)
            if ((value != 0) and (value < maxfreq)):
                maxfreq = value
                currWord = word
                print("Current Value:", value, " ", currWord)
                outputDict[currWord] = maxfreq
    # sort the dict based on the values(freq)
    outputDict = {k: v for k, v in sorted(outputDict.items(), key=lambda item: item[1])}
    # print("\nMax Freq : ",maxfreq, " ", currWord)

    # outputDict[currWord] = maxfreq
    return outputDict


# Function to remove the letters from list/string
def removeLetters(finalWord, combinedList):
    #print("\nremoveLetter comlist: ", combinedList)
    # word = list(finalWord.keys())[0]
    word = finalWord
    word = str(word).upper()
    print("Word Key: ", word)
    modifiedW = combinedList
    for i in range(len(word)):
        modifiedW.remove(word[i])
    # print("\n modifiedW", modifiedW)
    return modifiedW

"""
def checkIfAlreadyExists(solution, fword):
    existingWords = [val for d in solution for val in d.values()]
    #print("\n existingWords :", existingWords)
    if fword in existingWords:
        return True
    return False
"""

# processor function to perform all the logic
def processor(inputWordsList, circlePositions, finalSolutionFormat, dictData):
    #print("Processor")
    correctedInputWordList = findInputWords(inputWordsList)  # will hold unjumbled input list
    #print(correctedInputWordList)
    combinedList = findCircledLetters(correctedInputWordList, circlePositions)
    #print("CombinedList :", combinedList)
    #print("Final Solution Format :", finalSolutionFormat)
    modifiedList = combinedList
    solList = []

    #comList = combinedList
    #noOfWordsInResult = len(finalSolutionFormat) # to keep track of number of words in final answer
    #allPossibleSolution = [] # to store all solutions
    #result=[]

    #getNextWord(0, finalSolutionFormat, comList, dictData, result, solList)
    #print(result)

    for i in finalSolutionFormat:
        finalWords = getFinalWord(i, modifiedList, dictData)  # get the whole ordered list

        #for fword in finalWords:
            #if not checkIfAlreadyExists(solList, fword):

        outputDict = {}
        if len(modifiedList) == i:
            if len(finalWords)==0:
                fword = ''.join(map(str, modifiedList)).lower()
            else :
                fword = list(finalWords.keys())[0]
            outputDict[i] = fword
            solList.append(outputDict)
        else :  # to take out edge case
            fword = list(finalWords.keys())[0]
            outputDict[i] = fword
            solList.append(outputDict)
            # send letters to be removed
            modifiedList = removeLetters(fword, combinedList)
            #getNextWord(allPossibleSolution, i+1, finalSolutionFormat, modifiedList, dictData, result)

        print("processor : \n modifiedList : ", modifiedList)

    print("\nsolList :", solList)


""" 
# Recursive backtracking function implementation
def getNextWord(i, finalSolutionFormat, comList, dictData, result, solList):
    #if (i == len(finalSolutionFormat)):
        #finalWords = getFinalWord(finalSolutionFormat[i], modifiedList, dictData)  # get the whole ordered list

    if (i >= len(finalSolutionFormat)):
        result.append({"solution": '-'.join(solList)})
        return
    if (len(comList) <= 0):
        result.append(solList)
        return

    words = getFinalWord(finalSolutionFormat[i], comList, dictData)  # get the whole ordered list
    if len(words) == 0:
        return
    for word in words:
        solList = list(solList)
        solList.append(word)
        modifiedList = removeLetters(word, comList)
        getNextWord(i+1, finalSolutionFormat, modifiedList, dictData, result, solList)
"""

# populate freq_dict values from 0->9999
def updateDict(dictData):
    for i, k in dictData.items():
        if k == 0:
            dictData[i] = sys.maxsize

# main function to drive the program
# input - Get all the possible inputs as parameters
# read the dict file and pass as parameter to processor
def main():
    print("main")
    inputWordsList = []
    circlePostions = []
    finalSolutionFormat = []

    # puzzle 1
    inputWords = ("NAGLD", "RAMOJ", "CAMBLE", "WRALEY")
    inputWordsList.append(inputWords)
    circlePos = [[1, 3, 4], [2, 3], [0, 1, 3], [0, 2, 4]]  # index values for circled words
    circlePostions.append(circlePos)
    finalSol = [3, 4, 4]  # number of letters and words in the final solution
    finalSolutionFormat.append(finalSol)
    #print(" +++++++++ \n", inputWordsList, finalSolutionFormat)
    
    # puzzle 2
    inputWords = ("BNELD", "IDOVA", "SEHEYC", "ARACEM")
    inputWordsList.append(inputWords)
    circlePos = [[0, 4], [0, 3, 4], [1, 5], [1, 4, 5]]  # index values for circled words
    circlePostions.append(circlePos)
    finalSol = [3, 4, 3]  # number of letters and words in the final solution
    finalSolutionFormat.append(finalSol)

    # puzzle 3
    inputWords = ("SHAST", "DOORE", "DITNIC", "CATILI")
    inputWordsList.append(inputWords)
    circlePos = [[0, 3, 4], [0, 1, 3], [0, 1, 2], [0, 2, 5]]  # index values for circled words
    circlePostions.append(circlePos)
    finalSol = [4, 8]  # number of letters and words in the final solution
    finalSolutionFormat.append(finalSol)

    # puzzle 4
    inputWords = ("KNIDY", "LEGIA", "CRONEE", "TUVEDO")
    inputWordsList.append(inputWords)
    circlePos = [[0, 1], [0, 2], [1, 3], [0, 5]]  # index values for circled words
    circlePostions.append(circlePos)
    finalSol = [8]  # number of letters and words in the final solution
    finalSolutionFormat.append(finalSol)
    
    # puzzle 5
    inputWords = ("GYRINT", "DRIVET", "SNAMEA", "CEEDIT", "SOWDAH", "ELCHEK")
    inputWordsList.append(inputWords)
    circlePos = [[0, 1, 3], [2, 5], [0, 5], [1, 3, 5], [0, 3], [1, 5]]  # index values for circled words
    circlePostions.append(circlePos)
    finalSol = [6, 8]  # number of letters and words in the final solution
    finalSolutionFormat.append(finalSol)

    # read the dict json file
    #dictFile = open('freq_dict.json')
    #dictData = json.loads(dictFile.read())
    #updateFreqDict(dictData)
    # sort the dict based on the vales to main the reading order
    #dictData = {k: v for k, v in sorted(dictData.items(), key=lambda item: item[1])}
    # print("Main -------", dictData)
    # call processor function
    for i in range(5):
        finalSolution = processor(inputWordsList[i], circlePostions[i], finalSolutionFormat[i], dictData)





if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("Jumbled words puzzle") \
        .getOrCreate()

    sc = spark.sparkContext
    # read the dict json file
    global dictData
    dictFile = open('freq_dict.json')
    dictData = json.loads(dictFile.read())
    updateDict(dictData)
    #dictData = sc.parallelize(dictData)
    #print(dictData)
    dictData = {k: v for k, v in sorted(dictData.items(), key=lambda item: item[1])} # sorting the dict
    main()