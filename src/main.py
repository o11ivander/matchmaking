from data import players_first, players_second
from schema import Player
from task1 import form_matches, split_match_to_teams
from task2 import make_matches_with_squads

if __name__ == "__main__":

    # For first task:
    players = [Player(**data) for data in players_first]
    players_matches, players_without_matches = form_matches(players=players)
    for cnt_match, player_match in enumerate(players_matches, 1):
        team1, team2 = split_match_to_teams(player_match)
        print(f"Match {cnt_match}:")
        print("Team 1: ", team1)
        print("Team 2: ", team2)
    print(f"Players without match[{len(players_without_matches)}]:")
    print(players_without_matches)

    # For second task:
    players = [Player(**data) for data in players_second]
    matches, leftover = make_matches_with_squads(
        players=players,
    )
    for cnt_match, player_match in enumerate(matches, 1):
        team1, team2 = player_match
        print(f"Match {cnt_match}:")
        print("Team 1: ", team1)
        print("Team 2: ", team2)
    print(f"Players without match[{len(players_without_matches)}]:")
    print(players_without_matches)
