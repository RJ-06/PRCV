from collections import defaultdict
import random

def election(ballots: list[list[int]], OPEN_POSITIONS: int) -> list[int]:
    """
    ballots: list of ballots. Has shape (N, M), with N votes 
            cast and M total candidates. ballot[i][j] is the 
            jth-choice candidate on ballot i
    OPEN_POSITIONS: number of positions up for election

    Returns:
        winners: list[int]
    """

    candidate_vote_counts = defaultdict(int)
    candidate_ballots = defaultdict(list)

    THRESHOLD = len(ballots) // (OPEN_POSITIONS + 1) + 1

    winners = []

    # Count all ballots and determine if anyone has a majority
    for ballot in ballots:
        candidate_vote_counts[ballot[0]] += 1
        candidate_ballots[ballot[0]].append(ballot)

    for candidate in candidate_vote_counts.keys():
        if (candidate_vote_counts[candidate] >= THRESHOLD):
            winners.append(candidate)

    while (len(winners) < OPEN_POSITIONS):

        # Move surplus votes
        for winner in winners:
            num_surplus_votes = candidate_vote_counts[winner] - THRESHOLD
            ballots_to_transfer = random.sample(
                [ballot for ballot in candidate_ballots[winner] if ballot.index(winner) + 1 < len(ballot)], 
                num_surplus_votes)
            candidate_ballots[winner] = [ballot for ballot in candidate_ballots[winner] if ballot not in ballots_to_transfer]

            for ballot in ballots_to_transfer:
                candidate_to_transfer_to = ballot[ballot.index(winner) + 1]
                candidate_ballots[candidate_to_transfer_to].append(ballot)
                candidate_vote_counts[candidate_to_transfer_to] += 1

        # Add new winners
        num_winners = len(winners)
        for candidate in candidate_vote_counts.keys():
            if (candidate_vote_counts[candidate] >= THRESHOLD and candidate not in winners):
                winners.append(candidate)

        # Eliminate the last-place candidate 
        if len(winners) == num_winners:
            lowest_ranked_candidate = min(candidate_vote_counts, key=candidate_vote_counts.get)
            for ballot in candidate_ballots[lowest_ranked_candidate]:
                candidate_to_transfer_to = ballot[ballot.index(lowest_ranked_candidate) + 1]
                candidate_ballots[candidate_to_transfer_to].append(ballot)
                candidate_vote_counts[candidate_to_transfer_to] += 1

    return winners