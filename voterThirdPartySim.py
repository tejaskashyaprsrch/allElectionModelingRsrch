import random
import math
voters = []
democrat = [-0.7]*10 #democrat polarization
republican = [0.7]*10 #BOTH PARTY POLARIZATION
if 'thirdParty' not in globals():
    thirdParty = [0.0]*10 # Complete neutrality


print("3rd party values are initially", thirdParty)

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
def generateRealisticVoters(numVoters, noise, demShare, repShare, centerShare, crossShare, thirdShare):

    
    voters = []
    center = [0,0,0,0,0,0,0,0,0,0]
    cross = [0,0,0,0,0,0,0,0,0,0]
    thirdParty = [0,0,0,0,0,0,0,0,0,0]
    # Let's give the third party 1.68% - the total of how much they got in 2024
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
        elif r < demShare+ repShare+ centerShare:
            base = center # Surprisingly large share for center, right?
            noise = 0.25
        elif r < demShare + repShare + centerShare + thirdShare:
            base = thirdParty # Surprisingly large share for thirdParty, right?
            noise = 0.4
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
    democrat = [-0.7]*10
    republican = [0.7]*10
    thirdParty = [0.1] * 10
    
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

    distThird = 0
    for k in range(10):
        diff = voter[k] - thirdParty[k]
        distThird += diff * diff
    distThird = math.sqrt(distThird) + 1.0 # The plus 1 is to check only if the 3rd party is really close cause most think a 3rd party vote is a waste
    
    if distDem < distRep and distDem < distThird:
        return 1
    elif distRep < distDem and distRep < distThird:
        return -1
    else:
        return 0

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


    votes = []

    repCount, demCount, thirdCount = 0, 0, 0

    for voter in voters:

        centerDist = centerDistance(voter)
        rigidity = min(1, centerDist / 0.6)

        firmness = centerDist
        turnout_chance = 0.4 + (firmness / 2)

        # Trump effect!! IF you are scared you go vote more often!!
        rep_polarization = centerDistance(republican)
        dem_polarization = centerDistance(democrat)
        voterLean = determineParty(voter)
        if voterLean == -1:
            turnout_chance += (rep_polarization * 0.012) # Republicans are more likely to go out and vote bc of identity
        elif voterLean == 1:
            turnout_chance += (dem_polarization * 0.01) # Democrats are less likely to vote but go bc of fear
        
        turnout_chance = max(0, min(1, turnout_chance))

        if random.random() > turnout_chance:
            votes.append(99)
            continue

        if rigidity > 0.3:
            partyLean = determineParty(voter)

            if partyLean == 1: # democrat
                weights = [
                    1.2,   # Economy
                    1.25,   # Healthcare
                    1.3,  # Climate
                    1.15,  # Education
                    1.15,  # Civil Rights
                    1.0,   # Immigration
                    1.0,   # Defense
                    1.05,  # Taxes
                    1.0,
                    1.0
                ]
            elif partyLean == -1: # republican
                weights = [
                    1.3,   # Economy
                    1.05,  # Healthcare
                    1.0,   # Climate
                    1.15,  # Education
                    1.0,   # Civil Rights
                    1.25,  # Immigration
                    1.15,  # Defense
                    1.2,   # Taxes
                    1.0,
                    1.0
                ]
            else: # third party
                weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        else: # centrist
            weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

            # partyLean = determineParty(voter) # party setup - favors democrats because closer to center
            # partyLean = random.choice([1, -1]) # random setup - nearly 50/50

        distDem = 0
        distRep = 0
        distThird = 0

        for k in range(10):
            diff_dem = weights[k] * (voter[k] - democrat[k])
            diff_rep = weights[k] * (voter[k] - republican[k])
            diff_third = weights[k] * (voter[k] - thirdParty[k])
            distDem += diff_dem**2
            distRep += diff_rep**2
            distThird += diff_third**2
            
        distDem = math.sqrt(distDem)
        distRep = math.sqrt(distRep)
        distThird = math.sqrt(distThird)

        # NEGATIVE PARTISANSHIP THE FEAR FACTOR

        if distDem < distRep: #Regular democrat
            repExtreme = centerDistance(republican)
            distDem -= (repExtreme*0.4) # If republicans are scary and extreme, be more loyal to dem
        else: #Regular republican
            demExtreme = centerDistance(democrat)
            distRep -= (demExtreme*0.4) # If democrats are scary and extreme, be more loyal to rep

        distThird += 1

        if distDem < distRep and distDem < distThird:
            demCount += 1
            votes.append(1)
        elif distRep < distDem and distRep < distThird:
            repCount += 1
            votes.append(-1)
        else:
            thirdCount += 1
            votes.append(0)

    if demCount >= repCount and demCount >= thirdCount:
        winner = democrat
    elif repCount >= demCount and repCount >= thirdCount:
        winner = republican
    else:
        winner = thirdParty

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

    return [demCount, repCount, thirdCount, totalHappiness, votes]




def determineWinner(result):
    if result[0] > result[1] and result[0] > result[2]:
        return 1
    elif result[1] > result[0] and result[1] > result[2]:
        return -1
    else:
        return 0


voters = generateRealisticVoters(10000, 0.4, 0.35, 0.355, 0.255, 0.04, 0.02)

#results = simulateRandomElections(voters)  

#print(results)
demWins = 0
repWins = 0
thirdWins = 0
diff = 0
averageDiff = 0

for i in range(100):
    voters = generateRealisticVoters(10000, 0.4, 0.35, 0.355, 0.255, 0.0232, 0.0168)
    result = simulateRandomElections(voters)

    votes = result[4]

    for d in range(10):
        total = 0
        count = 0

        for j in range(len(voters)):
            if votes[j] == 0:
                total += voters[j][d]
                count += 1

        if count > 0:
            mean = total/count
            thirdParty[d] = 0.9 * thirdParty[d] + 0.1 * mean

    diff += abs(result[1] - result[0])

    outcome = determineWinner(result)
    if outcome == 1:
        demWins += 1
    elif outcome == -1:
        repWins += 1
    else:
        thirdWins += 1

print("Democrats won", demWins, "times")
print("Republicans won", repWins, "times")
print("Third Party won", thirdWins, "times")
print("Average difference between Dem/Rep", diff/100)
print("Third Party values have changed! See:", thirdParty)

import matplotlib.pyplot as plt

def plot_voter_distribution(voters, votes):
    # Calculate Leaning (Average of all dimensions)
    leaning = [sum(v) / len(v) for v in voters]
    
    # Calculate Firmness (Distance from center)
    firmness = [math.sqrt(sum(x*x for x in v) / len(v)) for v in voters]
    
    # Map votes to colors: 1 (Dem) -> blue, -1 (Rep) -> red, 0 (Third) -> gold
    colors = []
    for vote in votes:
        if vote == 1:
            colors.append('blue')
        elif vote == -1:
            colors.append('red')
        elif vote == 0:
            colors.append('gold')
        else:
            colors.append('lightgray')

    plt.figure(figsize=(10, 6))
    plt.scatter(leaning, firmness, c=colors, alpha=0.3, s=10)
    
    # Labels and Styling
    plt.title("Voter Distribution: Leaning vs. Firmness")
    plt.xlabel("Political Leaning (Left <---> Right)")
    plt.ylabel("Firmness (Distance from Center/Origin)")
    plt.axvline(0, color='black', linestyle='--', alpha=0.5)
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Democrat', markerfacecolor='blue', markersize=8),
                       Line2D([0], [0], marker='o', color='w', label='Republican', markerfacecolor='red', markersize=8),
                       Line2D([0], [0], marker='o', color='w', label='3rd Party', markerfacecolor='gold', markersize=8)]
    plt.legend(handles=legend_elements)
    
    plt.grid(True, alpha=0.2)
    plt.show()

# Call this at the very end after your loop
plot_voter_distribution(voters, result[4])