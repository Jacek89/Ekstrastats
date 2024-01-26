from collections import defaultdict
from bisect import bisect_left
from typing import Iterable
from ..models import Game


def count_intervals(sequence, intervals):
    count = defaultdict(int)
    count[15], count[30], count[45], count[60], count[75], count[90] = 0, 0, 0, 0, 0, 0
    intervals.sort()
    for item in sequence:
        pos = bisect_left(intervals, item)
        if pos == len(intervals):
            count[None] += 1
        else:
            count[intervals[pos]] += 1
    return count


def count_score_stats(games: Iterable[Game]):
    score_stats = {'home': 0,
                   'draw': 0,
                   'away': 0}

    for game in games:
        if game.result.split('-')[0] > game.result.split('-')[1]:
            score_stats['home'] += 1
        elif game.result.split('-')[0] < game.result.split('-')[1]:
            score_stats['away'] += 1
        else:
            score_stats['draw'] += 1
    return score_stats
