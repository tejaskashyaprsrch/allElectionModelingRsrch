"""
EXAMPLE OUTLINE: Multi-Party Voter Simulation Refactoring
Following the minimal-change approach with Party class
"""

import random
import math

# ============================================================================
# 1. PARTY CLASS - Simple class to encapsulate party data
# ============================================================================

class Party:
    """Simple class to represent a political party"""
    def __init__(self, name, position, share, turnout_boost, issue_weights, penalty, color):
        self.name = name
        self.position = position  # list of 10 ideology values [-1 to 1]
        self.share = share  # voter share percentage (0.0 to 1.0)
        self.turnout_boost = turnout_boost  # multiplier for turnout calculation
        self.issue_weights = issue_weights  # list of 10 weights for each issue
        self.penalty = penalty  # distance penalty (for "wasted vote" effect)
        self.color = color  # color for visualization
    
    def calculate_firmness(self):
        """Calculate firmness (distance from center) of the party"""
        total = 0
        for x in self.position:
            total += x * x
        return math.sqrt(total / len(self.position))
    
    def calculate_leaning(self):
        """Calculate leaning (average of all dimensions) of the party"""
        total = 0
        for x in self.position:
            total += x
        return total / len(self.position)


# ============================================================================
# 2. INITIALIZE PARTIES - Create parties list (can add as many as needed)
# ============================================================================

# Keep old variables for backward compatibility (optional, can remove later)
democrat = [-0.7]*10
republican = [0.7]*10
thirdParty = [0.0]*10

# Create parties list - this is the key change
parties = [
    Party(
        name="Democrat",
        position=[-0.7]*10,
        share=0.35,
        turnout_boost=0.01,
        issue_weights=[1.2, 1.25, 1.3, 1.15, 1.15, 1.0, 1.0, 1.05, 1.0, 1.0],
        penalty=0.0,
        color="blue"
    ),

    Party(
        name="Communist",
        position = [-1]*10,
        share=0.002,
        turnout_boost=0.05,
        issue_weights=[3.0]*10,
        penalty=1.25,
        color="maroon"
    ),

    Party(
        name="Socialist",
        position=[-0.9]*10,
        share=0.007,
        turnout_boost=0.03,
        issue_weights=[1.5]*10,
        penalty=1.0,
        color="pink",
    ),

    Party(
        name="Libertarian",
        position=[1.0]*10,
        share=0.004,
        turnout_boost=0.03,
        issue_weights=[1.5]*10,
        penalty=1.0,
        color="gold",

    ),

    Party(
        name="Republican",
        position=[0.7]*10,
        share=0.355,
        turnout_boost=0.012,
        issue_weights=[1.3, 1.05, 1.0, 1.15, 1.0, 1.25, 1.15, 1.2, 1.0, 1.0],
        penalty=0.0,
        color="red"
    ),
    Party(
        name="Third Party",
        position=[0.0]*10,
        share=0.0168,
        turnout_boost=0.0,
        issue_weights=[1.0]*10,
        penalty=1.0,
        color="green"
    ),
    # Add more parties here as needed:
    # Party("Green", [-0.5]*10, 0.05, 0.0, [1.0]*10, 0.5, "green"),
    # Party("Libertarian", [0.3]*10, 0.03, 0.0, [1.0]*10, 0.5, "yellow"),
]


# ============================================================================
# 3. VOTER GENERATION - Minimal changes to original function
# ============================================================================

def generateRealisticVoters(numVoters, parties, centerShare, crossShare, noise=0.15):
    """
    Generate voters with party affiliations based on parties list.
    
    MINIMAL CHANGE: Added parties parameter, kept same logic flow.
    Instead of hardcoded if/elif for 3 parties, loop through parties list.
    """
    voters = []
    center = [0,0,0,0,0,0,0,0,0,0]
    cross = [0,0,0,0,0,0,0,0,0,0]
    
    # Initialize cross positions (same as before)
    for i in range(10):
        cross[i] = random.uniform(-1, 1)
    
    # Calculate cumulative party shares
    party_cumulative = 0
    for party in parties:
        party_cumulative += party.share
    
    for i in range(numVoters):
        ideology = [0,0,0,0,0,0,0,0,0,0]
        r = random.random()
        
        # MINIMAL CHANGE: Loop through parties instead of hardcoded if/elif
        party_found = False
        cumulative = 0
        for party in parties:
            if r < cumulative + party.share:
                base = party.position
                noise_val = noise  # Could also use party.noise if added to class
                party_found = True
                break
            cumulative += party.share
        
        # Handle center voters (same as before)
        if not party_found and r < party_cumulative + centerShare:
            base = center
            noise_val = 0.25
        # Handle cross voters (same as before)
        elif not party_found and r < party_cumulative + centerShare + crossShare:
            base = cross
            noise_val = 0.6
        # Remaining are also cross (edge case)
        else:
            base = cross
            noise_val = 0.6
        
        # Apply noise (same as before)
        for j in range(10):
            ideology[j] = base[j] + random.uniform(-noise_val, noise_val)
            ideology[j] = max(-1, min(1, ideology[j]))
        
        voters.append(ideology)
    
    return voters


# ============================================================================
# 4. CENTER DISTANCE - No changes needed
# ============================================================================

def centerDistance(voter):
    """Calculate distance from center (no changes)"""
    return math.sqrt(sum(x*x for x in voter) / len(voter))


# ============================================================================
# 5. DETERMINE PARTY - Minimal changes: loop through parties
# ============================================================================

def determineParty(voter, parties):
    """
    Determine which party a voter is closest to.
    
    MINIMAL CHANGE: Added parties parameter, loop through parties instead of
    hardcoded 3 calculations. Return party index (0, 1, 2, ...) instead of (1, -1, 0).
    """
    distances = []
    
    # MINIMAL CHANGE: Loop through parties instead of hardcoded calculations
    for party in parties:
        dist = 0
        for k in range(10):
            diff = voter[k] - party.position[k]
            dist += diff * diff
        dist = math.sqrt(dist) + party.penalty  # Apply party-specific penalty
        distances.append(dist)
    
    # Find closest party (same logic as before, just generalized)
    min_index = distances.index(min(distances))
    return min_index

# ============================================================================
# 9. VISUALIZATION - Updated to use parties list
# ============================================================================

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def plot_voter_distribution(voters, votes, parties):
    """
    Plot voter distribution with colors from parties list.
    
    MINIMAL CHANGE: Use parties list for color mapping instead of hardcoded colors.
    """
    leaning = []
    for v in voters:
        leaning.append(sum(v) / len(v))
    firmness = []
    for v in voters:
        firmness.append(math.sqrt(sum(x*x for x in v) / len(v)))
    
    # MINIMAL CHANGE: Map votes to colors using parties list
    colors = []
    for vote in votes:
        if vote == 99:  # No vote
            colors.append('lightgray')
        elif 0 <= vote < len(parties):
            colors.append(parties[vote].color)
        else:
            colors.append('lightgray')
    
    plt.figure(figsize=(10, 6))
    plt.scatter(leaning, firmness, c=colors, alpha=0.6, s=15)
    
    # Add small blobs for each party position
    for party in parties:
        party_leaning = party.calculate_leaning()
        party_firmness = party.calculate_firmness()
        # Draw a circle with radius 1 around the party position
        circle = Circle((party_leaning, party_firmness), 1.0, 
                       color=party.color, fill=True, alpha=0.1, edgecolor='black', linewidth=1.5)
        plt.gca().add_patch(circle)
        # Add party name label
        plt.text(party_leaning, party_firmness, party.name, 
                ha='center', va='center', fontsize=8, fontweight='bold')
    
    plt.title("Voter Distribution: Leaning vs. Firmness")
    plt.xlabel("Political Leaning (Left <---> Right)")
    plt.ylabel("Firmness (Distance from Center/Origin)")
    plt.axvline(0, color='black', linestyle='--', alpha=0.5)
    
    # MINIMAL CHANGE: Generate legend dynamically from parties list
    from matplotlib.lines import Line2D
    legend_elements = []
    for party in parties:
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label=party.name, 
               markerfacecolor=party.color, markersize=8))
    legend_elements.append(Line2D([0], [0], marker='o', color='w', 
                                   label='No Vote', markerfacecolor='lightgray', markersize=8))
    plt.legend(handles=legend_elements)
    
    plt.grid(True, alpha=0.2)
    plt.show()




# ============================================================================
# 6. SIMULATE ELECTIONS - Minimal changes: use parties list
# ============================================================================

def simulateRandomElections(voters, parties):
    """
    Simulate election voting.
    
    MINIMAL CHANGE: Added parties parameter. Replace hardcoded vote counts
    with list. Loop through parties for distance calculations.
    """
    votes = []
    
    # MINIMAL CHANGE: Use list instead of separate variables
    vote_counts = [0] * len(parties)
    
    for voter in voters:
        centerDist = centerDistance(voter)
        rigidity = min(1, centerDist / 0.6)
        firmness = centerDist
        turnout_chance = 0.4 + (firmness / 2)
        
        # MINIMAL CHANGE: Use parties list for polarization and turnout boost
        voterLean = determineParty(voter, parties)
        if voterLean is not None:
            party_polarization = centerDistance(parties[voterLean].position)
            turnout_chance += (party_polarization * parties[voterLean].turnout_boost)
        
        turnout_chance = max(0, min(1, turnout_chance))
        
        if random.random() > turnout_chance:
            votes.append(99)  # No vote
            continue
        
        # MINIMAL CHANGE: Get weights from party object instead of hardcoded if/elif
        if rigidity > 0.3 and voterLean is not None:
            weights = parties[voterLean].issue_weights
        else:
            weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        
        # MINIMAL CHANGE: Calculate distances for all parties in loop
        distances = []
        for party in parties:
            dist = 0
            for k in range(10):
                diff = weights[k] * (voter[k] - party.position[k])
                dist += diff**2
            distances.append(math.sqrt(dist))
        
        # Negative partisanship - MATCH ORIGINAL: Only apply between Dem (index 0) and Rep (index 2)
        # Find Democrat and Republican indices (they should be at specific positions, but find them by name to be safe)
        dem_idx = 0
        rep_idx = 2
        for i in range(len(parties)):
            if parties[i].name == "Democrat":
                dem_idx = i
                break
        for i in range(len(parties)):
            if parties[i].name == "Republican":
                rep_idx = i
                break
        
        if dem_idx < len(distances) and rep_idx < len(distances):
            if distances[dem_idx] < distances[rep_idx]:  # Regular democrat
                repExtreme = centerDistance(parties[rep_idx].position)
                distances[dem_idx] -= (repExtreme * 0.4)  # If republicans are scary and extreme, be more loyal to dem
            else:  # Regular republican
                demExtreme = centerDistance(parties[dem_idx].position)
                distances[rep_idx] -= (demExtreme * 0.4)  # If democrats are scary and extreme, be more loyal to rep
        
        # Apply party penalties (like original: distThird += 1)
        for i, party in enumerate(parties):
            distances[i] += party.penalty
        
        # Find minimum distance party
        min_index = distances.index(min(distances))
        vote_counts[min_index] += 1
        votes.append(min_index)  # Store party index instead of 1, -1, 0
    
    # Determine winner (MINIMAL CHANGE: find max in list)
    winner_index = 0
    max_votes = vote_counts[0]
    for i in range(1, len(vote_counts)):
        if vote_counts[i] > max_votes:
            max_votes = vote_counts[i]
            winner_index = i
    winner = parties[winner_index]
    
    # Calculate total happiness (same as before)
    totalHappiness = 0
    maxDist = math.sqrt(40)
    for voter in voters:
        dist = 0
        for k in range(10):
            diff = voter[k] - winner.position[k]
            dist += diff * diff
        dist = math.sqrt(dist)
        happiness = 1 - (dist / maxDist)
        totalHappiness += happiness
    
    # MINIMAL CHANGE: Return list instead of [demCount, repCount, thirdCount, ...]
    return [vote_counts, totalHappiness, votes]


# ============================================================================
# 7. DETERMINE WINNER - Minimal changes: find max in list
# ============================================================================

def determineWinner(result, parties):
    """
    Determine winner from election results.
    
    MINIMAL CHANGE: Added parties parameter. result[0] is now a list of vote counts.
    """
    vote_counts = result[0]  # Now a list instead of separate variables
    winner_index = 0
    max_votes = vote_counts[0]
    for i in range(1, len(vote_counts)):
        if vote_counts[i] > max_votes:
            max_votes = vote_counts[i]
            winner_index = i
    return winner_index


# ============================================================================
# 8. MAIN EXECUTION - Updated to use parties list
# ============================================================================

# Example usage:
if __name__ == "__main__":
    # Generate voters using parties list
    voters = generateRealisticVoters(10000, parties, centerShare=0.255, crossShare=0.04)
    
    # Track wins for each party
    party_wins = [0] * len(parties)
    diff = 0
    
    for i in range(100):
        voters = generateRealisticVoters(10000, parties, centerShare=0.255, crossShare=0.04)
        result = simulateRandomElections(voters, parties)
        
        votes = result[2]  # votes list
        
        # MINIMAL CHANGE: Update adaptive party positions (generalize to all parties)
        for party_idx, party in enumerate(parties):
            if party.penalty > 0:  # Only update parties that allow adaptation
                for d in range(10):
                    total = 0
                    count = 0
                    for j in range(len(voters)):
                        if votes[j] == party_idx:
                            total += voters[j][d]
                            count += 1
                    if count > 0:
                        mean = total / count
                        party.position[d] = 0.9 * party.position[d] + 0.1 * mean
        
        # Calculate difference between top two parties
        vote_counts = result[0]
        sorted_counts = sorted(vote_counts, reverse=True)
        if len(sorted_counts) >= 2:
            diff += abs(sorted_counts[0] - sorted_counts[1])
        
        # Track wins
        outcome = determineWinner(result, parties)
        party_wins[outcome] += 1
    
    # Print results
    for i, party in enumerate(parties):
        print(f"{party.name} won {party_wins[i]} times")
    print(f"Average difference between top two parties: {diff/100}")
    
    # Print final vote counts from last election
    print("\nFinal election vote counts:")
    for i, party in enumerate(parties):
        print(f"{party.name}: {result[0][i]} votes")
    
    # Plot the final voter distribution
    plot_voter_distribution(voters, result[2], parties)


# ============================================================================
# NOTES ON MINIMAL CHANGES:
# ============================================================================
#
# 1. Party class: Simple class with __init__, no methods needed
# 2. Parties list: Single source of truth for all party data
# 3. Function signatures: Just add 'parties' parameter, keep rest same
# 4. Logic flow: Keep same structure, just loop through parties
# 5. Vote representation: Use party indices (0, 1, 2, ...) instead of (1, -1, 0)
# 6. Return values: Use lists instead of separate variables
# 7. Visualization: Dynamic color mapping from parties list
#
# To add more parties, just add more Party objects to the parties list!
# ============================================================================
