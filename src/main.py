from data import players_first, players_second
from schema import Player
from task1 import form_matches
from task2 import form_matches_squads

if __name__ == "__main__":

    # For first task:
    players = [Player(**data) for data in players_first]
    players_matches, leftover = form_matches(players=players)
    for cnt_match, player_match in enumerate(players_matches, 1):
        team1, team2 = player_match
        print(f"Match {cnt_match}:")
        print("Team 1: ", team1)
        print("Team 2: ", team2)
    print(f"Players without match[{len(leftover)}]:")
    print(leftover)

    # For second task:
    players = [Player(**data) for data in players_second]
    matches, leftover = form_matches_squads(
        players=players,
    )
    for cnt_match, player_match in enumerate(matches, 1):
        team1, team2 = player_match
        print(f"Match {cnt_match}:")
        print("Team 1: ", team1)
        print("Team 2: ", team2)
    print(f"Players without match[{len(leftover)}]:")
    print(leftover)
