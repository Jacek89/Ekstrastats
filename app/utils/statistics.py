from collections import defaultdict
from bisect import bisect_left
from typing import Iterable
from ..models import Game
import math


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


def pois_probability_matrix(xg1, xg2):

    def probability(actual, mean):
        p = math.exp(-mean)
        for i in range(actual):
            p *= mean
            p /= i+1
        return p

    matrix = [[probability(g1, xg1) * probability(g2, xg2)*100 for g1 in range(8)] for g2 in range(8)]
    max_prob = max(map(max, matrix))
    max_result = [(index, row.index(max_prob)) for index, row in enumerate(matrix) if max_prob in row]
    return matrix, (max_result[0][1], max_result[0][0], max_prob)
