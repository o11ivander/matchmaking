from data import players
from schema import Player
from task1 import form_matches, split_match_to_teams

if __name__ == "__main__":

    #For first task:
    players = [Player(**data) for data in players]
    players_matches, players_without_matches = form_matches(players=players)
    for cnt_match, player_match in enumerate(players_matches, 1):
        team1, team2 = split_match_to_teams(player_match)
        print(f"Match {cnt_match}:")
        print("Team 1: ", team1)
        print("Team 2: ", team2)
    print(f"Players without match[{len(players_without_matches)}]:")
    print(players_without_matches)
