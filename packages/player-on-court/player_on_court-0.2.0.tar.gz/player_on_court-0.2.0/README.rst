|License| |Contact|

Adding data about players on court in NBA games.
================================================

Player_on_court package allows you to add to  play-by-play data information
about players who were on court at any given time.

**Important: This package does not request play-by-play data from NBA website.
You need to get them in advance, for example, using nba_api package.**

https://github.com/swar/nba_api

How it work
-----------

Play-by-play NBA data contains information about each event in the game
(throw, substitution, foul, etc.) and players who participated in it
(PLAYER1_ID, PLAYER2_ID, PLAYER3_ID).

From this data, we get a list of players who were on court in this
quarter. Then, we need to filter this list to 10 people who started
quarter. This is done by analyzing substitutions in quarter.

I will soon describe a more complete mechanism for processing
play-by-play data to obtain information about players on court in an
article.

Code example
------------
.. code:: python

    >>> from nba_api.stats.endpoints import playbyplayv2
    >>> import player_on_court.player_on_court as poc
    >>>
    >>> pbp = playbyplayv2.PlayByPlayV2(game_id="0022100001").play_by_play.get_data_frame()
    >>> pbp_with_players = poc.adding_player_on_court(pbp)
    >>> len(pbp_with_players.columns) - len(pbp.columns)
    10
    >>> players_id = list(pbp_with_players.iloc[0, 34:].reset_index(drop=True))
    >>> print(players_id)
    [201142, 1629651, 201933, 201935, 203925, 201572, 201950, 1628960, 203114, 203507]
    >>> players_name = poc.replace_id_on_name(players_id)
    >>> print(players_name)
    ['Kevin Durant', 'Nic Claxton', 'Blake Griffin', 'James Harden', 'Joe Harris',
    'Brook Lopez', 'Jrue Holiday', 'Grayson Allen', 'Khris Middleton', 'Giannis Antetokounmpo']

.. |License| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target:  https://opensource.org/licenses/MIT
.. |Contact| image:: https://img.shields.io/badge/telegram-write%20me-blue.svg
    :target:  https://t.me/nbaatlantic
