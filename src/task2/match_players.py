"""
Improve the previous function for squads management (group of friends playing together).
Now you receive a list of 1000 to 2000 entries (PlayerID, Skill, SquadId).

If SquadId is -1, Player doesn’t belong to any Squad,
while all players with the same SquadId have to be in the same match, and the same team.
Modify the previous code.

"""

"""
Тепер потрібно розбити так, щоб гравці були в одній команді, однак сходу маємо проблему - різні скіли гравців.
В реальному проекті, думаю є обмеження на додавання в групу з великою різницею в рейтингу, однак це прог. задача, тому
уявимо що це реально. В такому випадку, думаю, що варто всіх гравців поділити на squad(з 1, або більше гравцем), а їх 
рейтинг взяти са середнє арифметичне. Наступна проблема - це розбиття на матчі, бо група може не влізти в один матч,
або буде неможливо поділити на команди всередині матчу. Це потрібно врахувати при розбитті на матчі і команди.
"""

from config import CNT_TEAM_PLAYERS, MATCH_PLAYERS
from schema import Player, Squad


def group_to_squads(players: list[Player]) -> list[Squad]:
    """
    Combine players in squad - players with one squad_id.

    :param players:
    :return: squads
    """
    buckets: dict[int, list[Player]] = {}
    for player in players:
        key = f"-{player.id}" if player.squad_id == -1 else player.squad_id
        buckets.setdefault(key, []).append(player)

    squads: list[Squad] = []
    for key, players_bucket in buckets.items():
        cnt = len(players_bucket)
        avg_skill = sum(player.skill for player in players_bucket) / cnt
        sid = (
            -1
            if all(player.squad_id == -1 for player in players_bucket)
            else players_bucket[0].squad_id
        )
        squads.append(
            Squad(id=sid, avg_skill=avg_skill, cnt_players=cnt, players=players_bucket)
        )
    return squads


def squad_key(squad: Squad) -> tuple:
    """
    Create squad unique key(player id) for solo players(squad_id = -1) and for "group" players - squad id

     :param players:
     :return: squads
    """
    return ("solo", squad.players[0].id) if squad.id == -1 else ("squad", squad.id)


def enumerate_candidate_windows_once(squads_sorted: list[Squad]) -> list[tuple]:
    """
     This function scans through the sorted list of Squads (by avg_skill) using a sliding window approach:
    - Expands the window (right pointer) until the total player count >= MATCH_PLAYERS.
    - Shrinks from the left if the count exceeds MATCH_PLAYERS.
    - When exactly MATCH_PLAYERS are reached, saves the window boundaries
      and the skill range (max(avg_skill) - min(avg_skill)).

    :param squads_sorted:
    :return:
    """
    len_squads = len(squads_sorted)
    prop_stats_matches = []
    left_pointer = 0
    cur_cnt_players = 0
    for right_pointer in range(len_squads):
        cur_cnt_players += squads_sorted[right_pointer].cnt_players
        while cur_cnt_players > MATCH_PLAYERS and left_pointer <= right_pointer:
            cur_cnt_players -= squads_sorted[left_pointer].cnt_players
            left_pointer += 1
        if cur_cnt_players == MATCH_PLAYERS:
            skill_diff = (
                squads_sorted[right_pointer].avg_skill
                - squads_sorted[left_pointer].avg_skill
            )
            prop_stats_matches.append((left_pointer, right_pointer, skill_diff))
            cur_cnt_players -= squads_sorted[left_pointer].cnt_players
            left_pointer += 1
    prop_stats_matches.sort(key=lambda t: (t[2], t[1] - t[0], t[0]))
    return prop_stats_matches


def sum_skill(squad: Squad) -> int | None:
    """
    Sum of player's skills in one squad/
    :param squad:
    :return:
    """
    return sum(player.skill for player in squad.players)


def split_two_teams_by_squads(
    squads: list[Squad],
) -> tuple[list[Player], list[Player], int]:
    """
    Uses dynamic programming (subset-sum style) to select the best subset of Squads that fills exactly
    slots(6 players) and minimizes the difference in total skill between the two teams.

    :param squads:
    :return:
    """

    squad_stats = [(s.cnt_players, sum_skill(s)) for s in squads]

    summ_skill = sum(skill for _, skill in squad_stats)
    teams_opt = [dict() for _ in range(CNT_TEAM_PLAYERS + 1)]
    teams_opt[0][0] = 0
    for squad_ind, (cnt_players, skill_sum) in enumerate(squad_stats):
        for used in range(CNT_TEAM_PLAYERS - cnt_players, -1, -1):
            for val, mask in list(teams_opt[used].items()):
                new_cnt, new_skill_sum = used + cnt_players, val + skill_sum
                if (
                    new_cnt <= CNT_TEAM_PLAYERS
                    and new_skill_sum not in teams_opt[new_cnt]
                ):
                    teams_opt[new_cnt][new_skill_sum] = mask | (1 << squad_ind)

    if not teams_opt[CNT_TEAM_PLAYERS]:
        raise ValueError("Not main!")

    target = summ_skill // 2
    best_val = min(teams_opt[CNT_TEAM_PLAYERS].keys(), key=lambda v: abs(target - v))

    mask = teams_opt[CNT_TEAM_PLAYERS][best_val]

    team1, team2 = [], []
    for squad_ind, squads in enumerate(squads):
        (team1 if (mask >> squad_ind) & 1 else team2).extend(squads.players)
    delta = abs(
        sum(player.skill for player in team1) - sum(player.skill for player in team2)
    )
    return team1, team2, delta


def form_matches_squads(
    players: list[Player],
) -> tuple[list[tuple[list[Player], list[Player]]], list[Player]]:
    """
    Main function that combine algorithm:
      - group players into squads;
      - sort squads by avg_skill;
      - find all squad windows mathc(cnt_players == 12);
      - for each window, try to divide match into two balanced teams(6 players in one);
      - add successful matches to the result list, removing used squads to prevent overlap;
      - repeat until no valid window remains;

    :param players:
    :return: tuple - [list of matches -> [tuple of twe teams -> list[PLayers], list[PLayers]], list[Players] without matches]
    """
    squads = group_to_squads(players)

    for squad in squads:
        if squad.cnt_players > CNT_TEAM_PLAYERS:
            raise ValueError(f"Squad {squad.id} players more than {CNT_TEAM_PLAYERS}")

    matches: list[tuple[list[Player], list[Player]]] = []

    while True:
        squads_sorted = sorted(squads, key=lambda s: s.avg_skill)

        candidates = enumerate_candidate_windows_once(squads_sorted)
        if not candidates:
            break

        taken = False
        for left_pointer, right_pointer, diff_skill in candidates:
            window = squads_sorted[left_pointer : right_pointer + 1]
            try:
                team1, team2, team_delta = split_two_teams_by_squads(window)
            except ValueError:
                continue

            matches.append((team1, team2))
            window_keys = {squad_key(squad) for squad in window}
            squads = [squad for squad in squads if squad_key(squad) not in window_keys]
            taken = True
            break

        if not taken:
            break

    leftovers = [player for squad in squads for player in squad.players]
    return matches, leftovers
