# how to use the functions:
# after getting the input from discord bot,
# call parseInput with map of pickers and receivers
    # it returns a tuple

# after getting the result from the grouper,
# call parseOutput with map of pickers, receivers and output
    # it returns a map with type <String, String>

def parseOneInput(pickers):
    sortedPick = sorted(pickers)
    sortedReceive = sorted(list(pickers.values())[0])
    parseMap = {}
    parseMap1 = {}
    for i in range(len(sortedPick)):
        parseMap[sortedPick[i]] = i
        parseMap1[sortedReceive[i]] = i
    
    parsedPickers = []
    for i in range(len(sortedPick)):
        indiList = pickers[sortedPick[i]]
        newList = []
        for j in range(len(indiList)):
            associatedNumber = parseMap1[indiList[j]]
            newList.append(associatedNumber)
        parsedPickers.append(newList)

    return parsedPickers


def parseInput(picker, receiver):
    return [parseOneInput(picker), parseOneInput(receiver)]


def parseOutput(picker, receiver, outputMap):
    sortedPick = sorted(picker)
    parseMap = {}

    sortedReceive = sorted(receiver)
    parseMap1 = {}
    for i in range(len(sortedPick)):
        parseMap[i] = sortedPick[i]
        parseMap1[i] = sortedReceive[i]
    
    parsedOutputMap = {}
    for i in outputMap:
        parsedOutputMap[parseMap[i]] = parseMap1[outputMap[i]]
    
    return parsedOutputMap


# a = {'A': ['0', '3', '2', '1'], 'B': ['2', '3', '1', '0'], 'C': ['0', '2', '1', '3'], 'D': ['1', '2', '0', '3']}
# b = {'0': ['A', 'B', 'C', 'D'], '1': ['B', 'C', 'D', 'A'], '2': ['B', 'D', 'A', 'C'], '3': ['A', 'C', 'B', 'D']}
# parsed = parseInput(a,b)
# output = {0: 0, 2: 1, 1: 2, 3: 3}
# parsedOutput = parseOutput(a, b, output)
# print(parsedOutput)