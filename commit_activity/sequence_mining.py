from prefixspan import PrefixSpan


def mine_frequent_patterns(issues):
    sequences = []
    for issue_commits in issues.values():
        sequence = [commit.category for commit in issue_commits]
        sequences.append(sequence)

    ps = PrefixSpan(sequences)

    # Find frequent patterns with a minimum support threshold
    # Adjust the minsup parameter based on your dataset size and desired specificity
    frequent_patterns = ps.frequent(minsup=2, closed=True)
    frequent_patterns_max_len3 = [pattern for sup, pattern in frequent_patterns if len(pattern) > 1 and len(pattern) <= 3 and pattern.count('uncategorized') <= 1]
    frequent_patterns_uncat = [pattern for pattern in frequent_patterns_max_len3 if 'uncategorized' in pattern]
    frequent_patterns_categorized = [pattern for pattern in frequent_patterns_max_len3 if 'uncategorized' not in pattern]

    mapping = {}  # Dictionary to store mappings

    for pattern in frequent_patterns_uncat:
        uncat_index = pattern.index('uncategorized')
        # Check previous element
        if uncat_index > 0:
            prev_categorized = pattern[uncat_index - 1]
            # find patterns in frequent_patterns_categorized that contain prev_categorized
            frequent_patterns_prev = [pattern for pattern in frequent_patterns_categorized if prev_categorized in pattern]
            possible_successors = set()
            for p in frequent_patterns_prev:
                for i, item in enumerate(p):
                    if item == prev_categorized and i < len(p) - 1:
                        # Get the successor
                        successor = p[i + 1]
                        possible_successors.add(successor)

            if len(possible_successors) == 1:  # Only one unique successor element
                mapped_pattern = list(pattern)
                mapped_pattern[uncat_index] = list(possible_successors)[0]
                mapping[tuple(pattern)] = tuple(mapped_pattern)

        # Check next element
        if uncat_index < len(pattern) - 1:
            next_categorized = pattern[uncat_index + 1]
            # find patterns in frequent_patterns_categorized that contain next_categorized
            frequent_patterns_next = [pattern for pattern in frequent_patterns_categorized if next_categorized in pattern]
            possible_predecessors = set()
            for p in frequent_patterns_next:
                for i, item in enumerate(p):
                    if item == next_categorized and i > 0:
                        # Get the predecessor
                        predecessor = p[i - 1]
                        possible_predecessors.add(predecessor)

            if len(possible_predecessors) == 1:  # Only one unique predecessor element
                mapped_pattern = list(pattern)
                mapped_pattern[uncat_index] = list(possible_predecessors)[0]
                mapping[tuple(pattern)] = tuple(mapped_pattern)

    return mapping


def apply_freq_pattern_mapping(issues, mapping, category_ids):
    changed_issues = []
    for issue_commits in issues.values():
        for pattern_with_uncategorized, mapped_pattern in mapping.items():
            pattern_len = len(pattern_with_uncategorized)
            for i in range(len(issue_commits) - pattern_len + 1):
                if all(issue_commits[j].category == pattern_with_uncategorized[j] for j in range(pattern_len)):
                    changed_issues.append(issue_commits.get_issue_id())
                    for j in range(pattern_len):
                        issue_commits[i + j].category = mapped_pattern[j]
                        issue_commits[i + j].category_id = category_ids[mapped_pattern[j]]
