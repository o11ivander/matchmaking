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

