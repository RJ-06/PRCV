import csv

def parse_google_form_csv(
    filepath,
    ranking_columns,
    candidate_list=None,
):
    """
    filepath: path to Google Forms CSV export
    ranking_columns: list of column names in ranking order
                     e.g. ["1st Choice", "2nd Choice", "3rd Choice"]
    candidate_list: optional explicit list of candidate names
                    (otherwise inferred from data)

    Returns:
        ballots: List[List[int]]
        candidate_to_id: dict mapping candidate name -> integer ID
    """

    ballots = []
    seen_candidates = set()

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ballot = []
            for col in ranking_columns:
                candidate = row[col].strip()
                ballot.append(candidate)
                seen_candidates.add(candidate)

            ballots.append(ballot)

    # Determine candidate ordering
    if candidate_list is None:
        candidate_list = sorted(seen_candidates)

    candidate_to_id = {name: i for i, name in enumerate(candidate_list)}

    # Convert ballots to integer format
    int_ballots = []
    for ballot in ballots:
        int_ballot = [candidate_to_id[name] for name in ballot]
        int_ballots.append(int_ballot)

    return int_ballots, candidate_to_id