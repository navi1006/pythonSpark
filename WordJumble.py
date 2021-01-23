# libraries
import json

# function to unjumble the input words and return a list
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

# processor function to perform all the logic
def processor(inputWordsList, circlePostions, finalSolutionFormat, dictData):
    print("Processor")
    correctedInputWordList = findInputWords(inputWordsList)  # will hold unjumbled input list
    print(correctedInputWordList)
    combinedList = findCircledLetters(correctedInputWordList, circlePostions)
    print("CombinedList :", combinedList)
    for size in finalSolutionFormat:
        finalWord=getFinalWord(size, combinedList, dictData)



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