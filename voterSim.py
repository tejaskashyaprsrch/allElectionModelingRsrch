import random
import math
voters = []


polls = {
    "economy":      {"dem": -0.4, "rep": 0.6},
    "healthcare":   {"dem": -0.8, "rep": 0.5},
    "climate":      {"dem": -0.9, "rep": 0.4},
    "immigration":  {"dem": -0.3, "rep": 0.8},
    "education":    {"dem": -0.6, "rep": 0.4},
    "taxes":        {"dem": -0.5, "rep": 0.6},
    "defense":      {"dem": -0.2, "rep": 0.9},
    "civil_rights": {"dem": -0.8, "rep": 0.5},
    "tech":         {"dem": -0.6, "rep": 0.6},
    "foreign":      {"dem": -0.4, "rep": 0.7}
}

# As of 2025, according to Pew Research Center, we are going to say 35% democrat, 35.5% republican, 25.5% center, 4% cross
def generateRealisticVoters(numVoters, noise, demShare, repShare, centerShare, crossShare):

    
    voters = []
    democrat = [-0.5, -0.7, -0.8, -0.3, -0.6, -0.5, -0.2, -0.6, -0.4, -0.3]
    republican = [0.5, 0.6, 0.4, 0.7, 0.3, 0.5, 0.8, 0.4, 0.6, 0.7]
    center = [0,0,0,0,0,0,0,0,0,0]
    cross = [0,0,0,0,0,0,0,0,0,0]
    for i in range(10):
        cross[i] = random.uniform(-1, 1)
    for i in range(numVoters):
        ideology = [0,0,0,0,0,0,0,0,0,0]
        r = random.random()

        if r < demShare:
            base = democrat
            noise = 0.15 # Extreme communist/socialist Democrats
        elif r < demShare + repShare:
            base = republican
            noise = 0.15# Extreme MAGA/KKK Republicans
        elif r < demShare + repShare + centerShare:
            base = center # Surprisingly large share for center, right?
            noise = 0.25
        else:
            base = cross # Crazies
            noise = 0.6

        for j in range(10):
            ideology[j] = base[j] + random.uniform(-noise, noise)
            ideology[j] = max(-1, min(1, ideology[j]))

        voters.append(ideology)

    return voters

def centerDistance(voter):
    return math.sqrt(sum(x*x for x in voter) / len(voter))


def determineParty(voter):
    democrat = [-0.5, -0.7, -0.8, -0.3, -0.6, -0.5, -0.2, -0.6, -0.4, -0.3]
    republican = [0.5, 0.6, 0.4, 0.7, 0.3, 0.5, 0.8, 0.4, 0.6, 0.7]
    
    distDem = 0
    for k in range(10):
        diff = voter[k] - democrat[k]
        distDem += diff * diff
    distDem = math.sqrt(distDem)
    
    distRep = 0
    for k in range(10):
        diff = voter[k] - republican[k]
        distRep += diff * diff
    distRep = math.sqrt(distRep)
    
    if distDem < distRep:
        return 1
    else:
        return -1

'''
def weightVoterValues(voters):
    
    # This function weighs the values and adds a bit of noise as well (ie dems care less abt military, reps care less abt dei)

    adjusted = []

    for v in voters:
        voter = v[:]
        
        centerDist = centerDistance(voter)
        rigidity = min(1, centerDist / 0.6)
        
        noise = 0.06*(1-rigidity)+0.01

        #simple noise for all
        for i in range(len(voter)):
            voter[i] += random.gauss(0, noise)

        if rigidity > 0.3:
            partyLean = determineParty(voter)

        # Only do these if the voter is not too close to the center
            if partyLean == 1: # Democrat
                voter[2] += random.gauss(0.08 * rigidity, 0.03)   # climate
                voter[4] += random.gauss(0.06 * rigidity, 0.03)   # DEI
                voter[3] -= random.gauss(0.05 * rigidity, 0.02)   # military
                voter[0] -= random.gauss(0.04 * rigidity, 0.02)   # economy

            else: # Republican
                voter[2] -= random.gauss(0.08 * rigidity, 0.03)   # climate
                voter[4] -= random.gauss(0.06 * rigidity, 0.03)   # DEI
                voter[3] += random.gauss(0.06 * rigidity, 0.02)   # military
                voter[0] += random.gauss(0.05 * rigidity, 0.02)   # econ

        for i in range(len(voter)):
            voter[i] = max(-1, min(1, voter[i]))      

        adjusted.append(voter)

    return adjusted
    
'''


    

# Dimensions: economy, healthcare, climate, immigration, education, taxes, defense, civil rights, tech regulation, foreign policy
# -1 to 1
def simulateRandomElections(voters):



    democrat = [-0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6]
    republican = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]

    repCount, demCount = 0, 0

    for voter in voters:

        centerDist = centerDistance(voter)
        rigidity = min(1, centerDist / 0.6)

        if rigidity > 0.3:
            partyLean = determineParty(voter)

            if partyLean == 1: # democrat
                weights = [0.9, 1.0, 1.3, 0.95, 1.0, 0.95, 0.7, 1.2, 0.9, 0.95]
            else: # republican
                weights = [1.1, 0.8, 0.5, 1.2, 0.9, 1.1, 1.3, 0.7, 0.8, 1.1]
        else: # centrist
            weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

            distDem = 0
            distRep = 0
            for k in range(10):
                diff_dem = weights[k] * (voter[k] - democrat[k])
                diff_rep = weights[k] * (voter[k] - republican[k])
                distDem += diff_dem**2
                distRep += diff_rep**2
            distDem = math.sqrt(distDem)
            distRep = math.sqrt(distRep)

            if distDem < distRep:
                partyLean = 1
            else:
                partyLean = -1

            # partyLean = determineParty(voter) # party setup - favors democrats because closer to center
            # partyLean = random.choice([1, -1]) # random setup - nearly 50/50

        distDem = 0
        distRep = 0

        for k in range(10):
            diff_dem = weights[k] * (voter[k] - democrat[k])
            diff_rep = weights[k] * (voter[k] - republican[k])
            distDem += diff_dem**2
            distRep += diff_rep**2
        distDem = math.sqrt(distDem)
        distRep = math.sqrt(distRep)

        if distDem < distRep:
            partyLean = 1
            demCount += 1
        else:
            partyLean = -1
            repCount += 1

    if demCount > repCount:
        winner = democrat
    else:
        winner = republican

    totalHappiness = 0
    maxDist = math.sqrt(40)  # max possible distance in 10D (2^2)*10

    for voter in voters:
        dist = 0
        for k in range(10):
            diff = voter[k] - winner[k]
            dist += diff * diff
        dist = math.sqrt(dist)
        happiness = 1 - (dist / maxDist)
        totalHappiness += happiness

    return [demCount, repCount, totalHappiness]




def determineWinner(result):
    if result[0] > result[1]:
        return 1
    else:
        return -1


voters = generateRealisticVoters(10000, 0.4, 0.35, 0.355, 0.255, 0.04)

#results = simulateRandomElections(voters)  

#print(results)
demWins = 0
repWins = 0
diff = 0
averageDiff = 0

for i in range(100):
    voters = generateRealisticVoters(10000, 0.4, 0.35, 0.355, 0.255, 0.04)
    result = simulateRandomElections(voters)

    diff += abs(result[1] - result[0])

    if determineWinner(result) == 1:
        demWins += 1
    else:
        repWins += 1

print("Democrats won", demWins, "times")
print("Republicans won", repWins, "times")
print("Average difference", diff/100)



    
