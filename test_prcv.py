from prcv import election

def test_simple_majority():
    # 3 candidates, 2 seats
    ballots = [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [0, 1, 2],
        [2, 1, 0],
    ]
    NUM_POSITIONS = 2

    winners = election(ballots, NUM_POSITIONS)
    assert len(winners) == 2
    assert 0 in winners


def test_equal_support():
    # Perfectly balanced election
    ballots = [
        [0, 1, 2],
        [1, 2, 0],
        [2, 0, 1],
        [0, 2, 1],
        [1, 0, 2],
        [2, 1, 0],
    ]
    NUM_POSITIONS = 3

    winners = election(ballots, NUM_POSITIONS)
    assert set(winners) == {0, 1, 2}


def test_single_seat():
    ballots = [
        [1, 0, 2],
        [1, 2, 0],
        [0, 1, 2],
        [1, 0, 2],
    ]
    NUM_POSITIONS = 1

    winners = election(ballots, NUM_POSITIONS)
    assert winners == [1]


def test_many_voters_many_candidates():
    ballots = [
        [0,1,2,3],
        [0,2,1,3],
        [1,0,2,3],
        [2,1,0,3],
        [2,0,1,3],
        [3,0,1,2],
        [1,2,0,3],
        [0,1,3,2],
    ]
    NUM_POSITIONS = 2

    winners = election(ballots, NUM_POSITIONS)
    assert len(winners) == 2
    assert all(w in {0,1,2,3} for w in winners)


def test_all_ballots_identical():
    ballots = [
        [2, 1, 0],
        [2, 1, 0],
        [2, 1, 0],
        [2, 1, 0],
    ]
    NUM_POSITIONS = 2

    winners = election(ballots, NUM_POSITIONS)
    assert winners[0] == 2

from hypothesis import given, strategies as st
import pytest


# Strategy to generate a single valid ballot (a permutation of candidates)
def ballot_strategy(m):
    return st.permutations(list(range(m)))


# Strategy to generate a valid n x m ballot matrix
def ballots_strategy():
    return st.integers(min_value=1, max_value=20).flatmap(
        lambda m: st.tuples(
            st.integers(min_value=1, max_value=50),  # n voters
            st.just(m)
        ).flatmap(
            lambda nm: st.lists(
                ballot_strategy(nm[1]),
                min_size=nm[0],
                max_size=nm[0]
            ).map(
                lambda ballots: (ballots, nm[1])
            )
        )
    )

import random
from collections import defaultdict

# import your election function here
# from election_module import election


def test_single_winner_majority():
    ballots = [
        [0,1,2],
        [0,2,1],
        [0,1,2],
        [1,0,2],
    ]

    winners = election(ballots, 1)

    assert winners == [0]


def test_two_positions_simple():
    ballots = [
        [0,1,2],
        [0,1,2],
        [1,0,2],
        [1,0,2],
        [2,0,1],
    ]

    winners = election(ballots, 2)

    assert len(winners) == 2
    assert 0 in winners or 1 in winners

def test_all_identical_ballots():
    ballots = [[2,1,0] for _ in range(10)]

    winners = election(ballots, 2)

    assert 2 in winners


def test_winner_ids_valid():
    ballots = [
        [0,1,2],
        [1,2,0],
        [2,0,1],
        [0,1,2],
    ]

    winners = election(ballots, 2)

    assert all(w in {0,1,2} for w in winners)

def generate_random_ballots(n, m):
    import random
    ballots = []
    for _ in range(n):
        ballot = list(range(m))
        random.shuffle(ballot)
        ballots.append(ballot)
    return ballots


def test_random_elections():
    random.seed(0)

    for _ in range(50):
        ballots = generate_random_ballots(20, 4)
        winners = election(ballots, 2)

        assert len(set(winners)) == len(winners)
        assert all(0 <= w < 4 for w in winners)
