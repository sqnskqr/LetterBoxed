from spellchecker import SpellChecker
import time

TIMEOUT_THRESHOLD  = 180

spell = SpellChecker()
words = set()
letterSet = set()
for word in spell:
    words.add(word)
#isWord
def isWord(currWord):
    return currWord in words
def couldBe(currWord):
    return  any(word.startswith(currWord) for word in words)

wordPacks = []
for i in range(4):
    letters = list(input("Enter the next 'side' of words: ").lower())
    assert len(letters) == 3
    letterSet.update(letters)
    wordPacks.append(letters)

#not cool code but runs faster
def generateNeighbors(index):
    if index == 0:
        return [1,2,3]
    if index == 1:
        return [0,2,3]
    if index == 2:
        return [1,0,3]
    if index == 3:
        return [1,2,0]
    
def wordNeighbors(inputWord):
    letter = inputWord[-1]
    neighbors = []
    for word in wordList:
        if word.startswith(letter):
            neighbors.append(word)
    return neighbors    

wordList = set()
fringe = [("",i) for i in range(len(wordPacks))]
print("adding words, please be patient")
#could add multiprocessing to have a loading timer or something
while fringe:
    currNode = fringe.pop(0)
    currWord = currNode[0]
    currIndex = currNode[1]
    currPack = wordPacks[currIndex]
    for letter in currPack:
        potentialWord = currWord + letter
        if len(potentialWord) >= 3 and potentialWord not in wordList and isWord(potentialWord):
            wordList.add(potentialWord)
            print("adding "+ potentialWord + " \n")
        if couldBe(potentialWord):
            for neighborIndex in generateNeighbors(currIndex):
                fringe.append([potentialWord, neighborIndex])
#begin solving    
wordList = sorted(wordList,key= lambda word: len(letterSet - set(word)))
finalFringe = []
for word in wordList:
    remaining_letters = letterSet - set(word)
    finalFringe.append([remaining_letters, [word]])
    #this will create a fringe that has the optimal word at the bottom
count = 0
removed = set()
start_time = time.time()
while finalFringe:
    if time.time() - start_time > TIMEOUT_THRESHOLD and count > 1:
        print("Sorry, searching for more options will take too long, hope these options work!")
        break
    currNode = finalFringe.pop(0)
    #the reason we do this is because some words are not recognized by NYT, so we want multiple options that are completely separate
    overlap = set(currNode[1]) & removed
    if overlap:
        continue
    #remaining letters
    currRemaining = currNode[0]
    if len(currRemaining) == 0:
        print("Here's an Option: ")
        print(currNode[1])
        print("\n")
        count += 1
        for word in currNode[1]:
            removed.add(word)
        if count >= 5:
            break
    #current word on the wordlist
    currWord = currNode[1][-1]
    #create the list of neighbors
    neighbors = wordNeighbors(currWord)
    #using the neighbors, let's push them onto the stack from least valuable to most
    neighbors = sorted(neighbors,key= lambda word: len(currRemaining - set(word)))
    for word in neighbors:
        pushSet = currRemaining - set(word)
        pushList = currNode[1] + [word]
        finalFringe.append([pushSet,pushList])