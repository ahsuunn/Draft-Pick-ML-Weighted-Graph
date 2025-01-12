import networkx as nx
import os
import json
import random


'''INITIALIZE GRAPH'''
counterGraph = nx.DiGraph()
compatibilityGraph = nx.DiGraph()

heroes = []
counterEdges = []
compatibilityEdges = []

with open("data/HeroData.json", "r") as f1, open("data/heroDictionary.json", "r") as f2:
    hero_data = json.load(f1)
    hero_dictionary = json.load(f2)

for idx in range(127):
    heroName = hero_data[idx]['heroName']
    baseRelation = hero_data[idx]['relationData']
    heroes.append(heroName)
    
    for i in range(5):
        counterId = baseRelation['counter'][i]['hero_id']
        counterWeight = baseRelation['counter'][i]['value']
        reverseRelationWeight = "-" + counterWeight # Menambah minus untuk relasi hero sebaliknya
        subheroNameCounter = hero_dictionary[counterId] 
        counterEdges.append((heroName, subheroNameCounter, counterWeight))
        if not counterGraph.has_edge(subheroNameCounter, heroName):
            counterEdges.append((subheroNameCounter, heroName, reverseRelationWeight))

        counteredId = baseRelation['countered'][i]['hero_id']
        counteredWeight = baseRelation['countered'][i]['value']
        reverseRelationWeight = counteredWeight[1:] # Menghapus minus untuk relasi hero sebaliknya
        subheroNameCountered = hero_dictionary[counteredId]
        counterEdges.append((heroName, subheroNameCountered, counteredWeight))
        if not counterGraph.has_edge(subheroNameCountered, heroName):
            counterEdges.append((subheroNameCountered, heroName, reverseRelationWeight))
        
        compatibleId = baseRelation['compatible'][i]['hero_id']
        compatibleWeight = baseRelation['compatible'][i]['value']
        subheroNameCompatible = hero_dictionary[compatibleId]
        compatibilityEdges.append((heroName, subheroNameCompatible, compatibleWeight))
        if not compatibilityGraph.has_edge(subheroNameCompatible, heroName):
            compatibilityEdges.append((subheroNameCompatible, heroName, compatibleWeight))
        
        incompatibleId = baseRelation['incompatible'][i]['hero_id']
        incompatibleWeight = baseRelation['incompatible'][i]['value']
        subheroNameIncompatible = hero_dictionary[incompatibleId]
        compatibilityEdges.append((heroName, subheroNameIncompatible, incompatibleWeight))
        if not compatibilityGraph.has_edge(subheroNameIncompatible, heroName):
            compatibilityEdges.append((subheroNameIncompatible, heroName, incompatibleWeight))

counterGraph.add_nodes_from(heroes)
counterGraph.add_weighted_edges_from(counterEdges)

compatibilityGraph.add_nodes_from(heroes)
compatibilityGraph.add_weighted_edges_from(compatibilityEdges)

print(compatibilityGraph)
'''DRAFT PICK'''
# Iniatialized Draft
num_teams = 2
picks_per_team = 5
bans_per_team = 0  
available_heroes = heroes.copy()
teams = {"Team A": [], "Team B": []} 
current_team = 0
pick_order = [
    ("Team A", 1),  
    ("Team B", 2),  
    ("Team A", 2),  
    ("Team B", 2),  
    ("Team A", 2),  
    ("Team B", 1),  
]

def calculate_scores(team_heroes, opposing_team_heroes, available_heroes):
    hero_scores = []
    for hero in available_heroes:
        counter_score = 0
        synergy_score = 0
        
        for counter in opposing_team_heroes:
            edge_data = counterGraph[hero].get(counter, {})
            weight = float(edge_data.get('weight', 0))
            counter_score += weight
        
        for compatible in team_heroes:
            edge_data = compatibilityGraph[hero].get(compatible, {})
            weight = float(edge_data.get('weight', 0))           
            synergy_score += weight

        total_score = counter_score + synergy_score
        hero_scores.append((hero, total_score, counter_score, synergy_score))

    return hero_scores

def get_best_and_worst_picks(team_heroes, opposing_team_heroes, available_heroes):
    hero_scores = calculate_scores(team_heroes, opposing_team_heroes, available_heroes)
    sorted_heroes = sorted(hero_scores, key=lambda x: x[1], reverse=True)
    
    best_picks = sorted_heroes[:5]
    worst_picks = sorted_heroes[-5:]
    worst_picks = worst_picks[::-1]
    
    return best_picks, worst_picks

'''BAN PHASE'''
print("BAN PHASE:")
banned_heroes = []
for team in teams:
    print(f"\n{team}, please ban {bans_per_team} heroes:")
    for i in range(bans_per_team):
        print(f"Banned heroes so far: {banned_heroes}")
        while True:
            banned_hero = input(f"Ban hero #{i+1} for {team}: ").strip()
            if banned_hero in available_heroes and banned_hero not in banned_heroes:
                banned_heroes.append(banned_hero)
                available_heroes.remove(banned_hero)
                print(f"{team} has banned {banned_hero}")
                break
            else:
                print(f"{banned_hero} is either already banned or not available. Please pick a valid hero.")
                continue

'''PICK PHASE'''
for team_name, picks_in_this_turn in pick_order:
    print(f"\n---------- PICK PHASE - {team_name} ----------")
    remaining_picks = picks_in_this_turn
    print(f"{team_name} is picking {remaining_picks} hero(s).")
    
    for _ in range(picks_in_this_turn):
        team_heroes = teams[team_name]
        opposing_team_name = "Team B" if team_name == "Team A" else "Team A"
        opposing_team_heroes = teams[opposing_team_name]

        best_picks, worst_picks = get_best_and_worst_picks(team_heroes, opposing_team_heroes, available_heroes)

        print("\nTop 5 Best Picks:")
        for hero, score, counter_score, synergy_score in best_picks:
            print(f"{hero} (Total: {score:.2f}, Counter: {counter_score:.2f}, Synergy: {synergy_score:.2f})")

        print("\nTop 5 Worst Picks:")
        for hero, score, counter_score, synergy_score in reversed(worst_picks): 
            print(f"{hero} (Total: {score:.2f}, Counter: {counter_score:.2f}, Synergy: {synergy_score:.2f})")

        while True:
            print("\nPlease choose your pick from the best picks:")
            chosen_hero = input(f"Pick one hero: ")
            if chosen_hero in available_heroes:
                teams[team_name].append(chosen_hero)
                available_heroes.remove(chosen_hero)
                print(f"{team_name} picks {chosen_hero}")
                break
            else:
                print("Invalid pick.")

def calculate_team_scores(teams, counterGraph, compatibilityGraph):
    team_scores = {}
    
    for team_name, team_heroes in teams.items():
        synergy_score = 0
        counter_score = 0        
        for hero in team_heroes:
            for other_hero in team_heroes:
                if hero != other_hero:
                    edge_data = compatibilityGraph[hero].get(other_hero, {})
                    weight = float(edge_data.get('weight', 0))
                    synergy_score += weight
    
        opposing_team_name = "Team B" if team_name == "Team A" else "Team A"
        opposing_team_heroes = teams[opposing_team_name]
        
        for hero in team_heroes:
            for opposing_hero in opposing_team_heroes:
                edge_data = counterGraph[hero].get(opposing_hero, {})
                weight = float(edge_data.get('weight', 0))
                counter_score += weight
        
        team_scores[team_name] = {"synergy_score": synergy_score, "counter_score": counter_score}
    
    return team_scores

print("\nFinal Draft:")
for team, heroes in teams.items():
    print(f"{team}: {', '.join(heroes)}")

print("\nFinal Score:")
final_scores = calculate_team_scores(teams, counterGraph, compatibilityGraph)
for team, scores in final_scores.items():
    synergy_score = f"{scores['synergy_score']:.2f}" 
    counter_score = f"{scores['counter_score']:.2f}" 
    print(f"{team} - Synergy Score: {synergy_score}, Counter Score: {counter_score}")
