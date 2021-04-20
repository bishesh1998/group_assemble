def changePartner(accepPref, accep, currProp, newProp):
    for i in accepPref[accep]:
        # if the current proposer comes above the new proposer in the preference list of the acceptor,
        # return no change, i.e. False
        # else return change, i.e. True
        if(i == currProp):
            return False
        if(i == newProp):
            return True


def grouping(propPref, accepPref):
    groupSize = len(propPref)
    match = {}
    # freeProp is a list of proposers that are not currently matched
    freeProp = [i for i in range(groupSize)]
    propPrefIndex = [0]*groupSize
    while(freeProp):
        newProp = freeProp.pop(0)
        accep = propPref[newProp][propPrefIndex[newProp]]
        # The else condition of the if statement below should never be triggered,
        # but we are making sure the algorithm never gets to that part even if it triggers
        if(accep<groupSize and accep>=0):
            if(accep in match):
                currProp = match[accep]
                if(changePartner(accepPref, accep, currProp, newProp)):
                    match[accep] = newProp
                    freeProp.append(currProp)
                else:
                    freeProp.append(newProp)
            else:
                match[accep] = newProp
            propPrefIndex[newProp]+=1
    
    return match


group1 = {
     0: [0,3,2,1],
     1: [2,3,1,0],
     2: [0,2,1,3],
     3: [1,2,0,3]
 }

group2 = {
     0:[0,1,2,3],
     1:[1,2,3,0],
     2:[1,3,0,2],
     3:[0,2,1,3]
}
 
result = grouping(group1, group2)
 # the result is picked:picker
 print(result)