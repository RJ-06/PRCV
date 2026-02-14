from parse_csv import parse_google_form_csv
from prcv import election

ranking_columns = ["1st Choice", "2nd Choice", "3rd Choice", "4th Choice"]

ballots, candidate_to_id = parse_google_form_csv(
    "election.csv",
    ranking_columns
)

NUM_POSITIONS = 2
winners = election(ballots, NUM_POSITIONS)

# Convert to names
id_to_candidate = {v: k for k, v in candidate_to_id.items()}
winner_names = [id_to_candidate[w] for w in winners]

print(winner_names)