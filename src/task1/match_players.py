"""
Core logic for task

You should return the best match that is composed of 2 lists of 6 players
(= 2 teams of 6), that verify those rules :

● Delta Skill between two players in a match have to be minimal
  (id : Players want to play with near skill players).

● Delta between the two team sum skills have to be minimal (id : team are balanced).

● If no match satisfies a "quality criteria", it has to return nothing.

Write code that returns the possible matches using the list of players as input.
After the call, only players that don't belong to a match have to stay in that list.
"""

from functools import lru_cache
from itertools import combinations

from config import MATCH_PLAYERS
from schema import Player

"""
Треба написати функцію для матч майкінгу з оптимізацією по:
 - мінімальній різниці між двома гравцями в матчі.
 - мінімальній різниці між командами

Для вирішення, можна підійти жадібним алгоритмом, що на мій погляд досить легкий спосіб, але не оптимальний. 
Спробувати опрацювати через дин. прогу і 
рекурсивний пошук оптимального результату(при кешуванні результатів складність буде не велика) - спрощене дерео рішень.

Почнемо з того, що розіб'єм гравців на команди, різниця між min і max у яких найменша - це будуть найоптимальніші матчі.  
Після цього розіб'ємо всередині матчу на оптимальні команди. Ту можна навіть перебором це зробити,
бо 12 гравців не так багато.

"""


def prepare_stats(sorted_players: list[Player]) -> list[int]:
    """
    Prepare stats for window of Players(window len 12 - cnt players in one match) like diff between min and max skill;

    :param sorted_players:
    :return: list[int]
    """
    cnt_players = len(sorted_players)
    skills_diffs_in_match: list[int] = []

    for i in range(0, cnt_players - MATCH_PLAYERS + 1):
        propose_match_team = sorted_players[i : i + MATCH_PLAYERS]
        diff_between_min_max = (
            propose_match_team[-1].skill - propose_match_team[0].skill
        )
        skills_diffs_in_match.append(diff_between_min_max)

    return skills_diffs_in_match


def div_players_by_match(
    sorted_players: list[Player], ind_players: list[int]
) -> tuple[list[list[Player]], list[Player]]:
    """
    Divide players byt match in list with 12 Player in each other and list with PLayers without match.

    :param sorted_players:
    :param ind_players:
    :return: tuple[list[list[Player]], list[Player]]
    """

    matches: list[list[Player]] = []
    used_ids: set[str] = set()
    for start_ind in ind_players:
        match_players = sorted_players[start_ind : start_ind + MATCH_PLAYERS]
        matches.append(match_players)
        used_ids.update(player.id for player in match_players)

    players_without_matches = [
        player for player in sorted_players if player.id not in used_ids
    ]

    return matches, players_without_matches


def split_match_to_teams(
    players_in_one_match: list[Player],
) -> tuple[list[Player], list[Player]]:
    """
    DIvide players in one match(12 players) in two teams(1 and 2). This is done by trying out combinations and
    choose best by diff between sum skills.

    :param players:
    :return: list[Player], list[Player]
    """

    skills = [player.skill for player in players_in_one_match]
    total = sum(skills)

    best_delta = None
    best_idx = None

    for ind in combinations(range(12), 6):
        sum_first_team = sum(skills[i] for i in ind)
        delta = abs(total - 2 * sum_first_team)
        if best_delta is None or delta < best_delta:
            best_delta = delta
            best_idx = ind

    team1 = [players_in_one_match[i] for i in best_idx]
    team2 = [players_in_one_match[j] for j in range(12) if j not in best_idx]

    return team1, team2


def form_raw_matches(
    sorted_players: list[Player],
):
    """
    Divide all players to raw matches - 12 players without teams. This done with optimize match stat(diff between min
    and max) by tree decide.

    :param sorted_players:
    :return:
    """
    skills_diffs_in_match = prepare_stats(sorted_players)
    cnt_players = len(sorted_players)

    @lru_cache
    def optimize(i: int) -> tuple:
        if i > cnt_players - MATCH_PLAYERS:
            return (0, 0, ())

        best_cnt, best_diff_between_min_max, best_indx_match_start = optimize(i + 1)

        skill_diff_i = skills_diffs_in_match[i]
        take_cnt, take_diff, take_indx_starts = optimize(i + MATCH_PLAYERS)
        take_state = (take_cnt + 1, take_diff + skill_diff_i, (i,) + take_indx_starts)

        if take_state[0] > best_cnt or (
            take_state[0] == best_cnt and take_state[1] < best_diff_between_min_max
        ):
            return take_state

        return (best_cnt, best_diff_between_min_max, best_indx_match_start)

    total_count, _, starts = optimize(0)
    if total_count == 0:
        return [], []

    matches, players_without_matches = div_players_by_match(sorted_players, starts)

    return matches, players_without_matches


def form_matches(
    players: list[Player],
) -> tuple[list[tuple[list[Player], list[Player]]], list[Player]]:
    """
    Main function that combine algorithm:
    - sort players by skill
    - form match
    - divide players in match to teams

    :param players:
    :return: tuple - [list of matches -> [tuple of twe teams -> list[PLayers], list[PLayers]], list[Players] without matches]
    """
    cnt_players = len(players)

    if cnt_players < MATCH_PLAYERS:
        return [], []

    sorted_players = sorted(players, key=lambda player: player.skill)
    matches, leftovers_players = form_raw_matches(sorted_players)

    matches_with_teams = [split_match_to_teams(match) for match in matches]

    return matches_with_teams, leftovers_players
