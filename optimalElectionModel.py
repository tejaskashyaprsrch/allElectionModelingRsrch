import random
import math
import matplotlib.pyplot as plt

random.seed(42)

# PARTY CLASS

class Party:
    def __init__(self, name, position, share, color):
        self.name = name
        self.position = position  # list of 10 ideology values [-1 to 1]
        self.share = share        # voter share percentage
        self.color = color

# ============================================================================
# GENERATION METHODS
# ============================================================================

# Generates parties spread across the ideological spectrum with a noise variable.
def generateIdeologicalParties(number_of_parties, noise_epsilon):

    generated_parties = []

    if number_of_parties > 0:
        base_share = 0.80 / number_of_parties
    else:
        base_share = 0

    for i in range(number_of_parties):
        if number_of_parties == 1:
            base_position = 0.0
        else:
            base_position = -0.9 + (1.8 * i / (number_of_parties - 1))
        
        # Apply the uniform noise variable to the fixed location
        # The party moves slightly left or right by the noise_epsilon amount
        jitter = random.uniform(-noise_epsilon, noise_epsilon)
        noisy_position = base_position + jitter
        
        rand_pos = [noisy_position]
        
        for j in range(1, 10):
            val = random.uniform(-0.5, 0.5)
            rand_pos.append(val)
        
        p = Party(
            name="Party " + str(i+1),
            position=rand_pos,
            share=base_share,
            color="grey"
        )
        generated_parties.append(p)

    return generated_parties

def generateRealisticVoters(numVoters, parties, centerShare, crossShare):

    voters = []
    center = [0] * 10
    cross = []
    for i in range(10):
        cross.append(random.uniform(-0.9, 0.9)) 
    
    thresholds = []
    running_sum = 0
    for p in parties:
        running_sum += p.share
        thresholds.append(running_sum)
    
    total_party_share = running_sum

    for i in range(numVoters):
        ideology = [0] * 10
        r = random.random()
        
        base = center
        noise_val = 0.25
        party_found = False

        if r < total_party_share and parties:
            for idx, thresh in enumerate(thresholds):
                if r < thresh:
                    base = parties[idx].position
                    noise_val = 0.15 
                    party_found = True
                    break
        
        if not party_found:
            if r < total_party_share + centerShare:
                base = center
                noise_val = 0.25
            else:
                base = cross
                noise_val = 0.6 
        
        for j in range(10):
            ideology[j] = base[j] + random.uniform(-noise_val, noise_val)
            ideology[j] = max(-1, min(1, ideology[j]))
            
        voters.append(ideology)
    return voters


# ============================================================================
# SIMULATION LOGIC
# ============================================================================

def get_distance(voter, position):
    dist = 0
    for k in range(len(voter)):
        diff = voter[k] - position[k]
        dist += diff ** 2
    return math.sqrt(dist)


def run_single_election(voters, parties):
    if not parties:
        return -1

    vote_counts = [0] * len(parties)
    
    for voter in voters:
        best_party_idx = 0
        min_dist = get_distance(voter, parties[0].position)
        
        for idx in range(1, len(parties)):
            d = get_distance(voter, parties[idx].position)
            if d < min_dist:
                min_dist = d
                best_party_idx = idx
        
        dist_to_origin = get_distance(voter, [0] * 10)
        turnout_chance = 0.4 + (dist_to_origin / 2)
        turnout_chance = max(0, min(1, turnout_chance))
        
        if random.random() <= turnout_chance:
            vote_counts[best_party_idx] += 1

    winner_idx = 0
    max_votes = vote_counts[0]
    for i in range(1, len(vote_counts)):
        if vote_counts[i] > max_votes:
            max_votes = vote_counts[i]
            winner_idx = i
            
    return winner_idx


# ============================================================================
# MAIN EXPERIMENT RUNNER
# ============================================================================

def run_trial(num_parties, noise_input, num_voters=1000, num_elections=100):
    # Pass the noise variable into the generation function
    parties = generateIdeologicalParties(num_parties, noise_input)
    
    trial_distances = []

    for i in range(num_elections):
        voters = generateRealisticVoters(num_voters, parties, 0.15, 0.05)
        winner_idx = run_single_election(voters, parties)
        winner_pos = parties[winner_idx].position
        
        total_distance = 0
        for voter in voters:
            total_distance += get_distance(voter, winner_pos)
        
        avg_distance = total_distance / num_voters
        trial_distances.append(avg_distance)

    return sum(trial_distances) / len(trial_distances)


# ============================================================================
# RUNNER
# ============================================================================
    
TRIALS_PER_COUNT = 50      
ELECTIONS_PER_TRIAL = 200   
MAX_PARTIES = 20 # We can assume that >20 = CHAOS

NOISE_VARIABLE = 0.02 # This is the noise epsilon

print("=" * 70)
print("OPTIMAL PARTY COUNT FINDER SIMULATION (WITH POSITION NOISE)")
print("=" * 70)

all_results = {}
avg_list = []
std_list = []
min_list = []
max_list = []
party_counts = []

for n in range(2, MAX_PARTIES + 1):
    results = []
    for t in range(TRIALS_PER_COUNT):
        # Inputting the noise variable at the start of the trial
        results.append(run_trial(n, NOISE_VARIABLE, num_voters=2000, num_elections=ELECTIONS_PER_TRIAL))
    
    avg = sum(results) / len(results)
    
    if len(results) > 1:
        variance = sum((x - avg) ** 2 for x in results) / (len(results) - 1)
        std = math.sqrt(variance)
    else:
        std = 0
        
    min_val = min(results)
    max_val = max(results)
    
    all_results[n] = avg
    party_counts.append(n)
    avg_list.append(avg)
    std_list.append(std)
    min_list.append(min_val)
    max_list.append(max_val)
    
    print(f"Parties: {n} | Avg Dist: {avg:.4f}")

optimal_parties = 2
min_dist_found = all_results[2]

for p_count in all_results:
    if all_results[p_count] < min_dist_found:
        min_dist_found = all_results[p_count]
        optimal_parties = p_count

print("-" * 70)
print(f"\n OPTIMAL NUMBER OF PARTIES: {optimal_parties}")
print(f"  Minimum average distance: {all_results[optimal_parties]:.4f}")

# ===============================
# MATPLOTLIB VISUALIZATION
# ===============================
plt.figure(figsize=(10,6))

# Average line
plt.plot(party_counts, avg_list, marker='o', label="Average Distance")

# Standard deviation band
upper_std = [avg + std for avg, std in zip(avg_list, std_list)]
lower_std = [avg - std for avg, std in zip(avg_list, std_list)]

plt.fill_between(party_counts, lower_std, upper_std, alpha=0.25, label="±1 Std Dev")

# Min / Max envelope
plt.fill_between(party_counts, min_list, max_list, alpha=0.1, label="Full Range")

# Optimal party line
plt.axvline(optimal_parties, color='red', linestyle=":", label=f"Optimal = {optimal_parties}")

plt.xlabel("Number of Parties")
plt.ylabel("Distance (Voter → Winner)")
plt.title(f"Collective Alienation (Position Noise: {NOISE_VARIABLE})")

plt.legend()
plt.grid(True)

plt.show()
