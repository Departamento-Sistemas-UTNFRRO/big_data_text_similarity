def compare_pairs(questions, distances, comparator, q1_col, q2_col):
    for row in questions:
        question1 = row[q1_col]
        question2 = row[q2_col]

        distance = comparator.compare(question1, question2)

        line_number = row[0]

        # Writes the distances in the shared array
        distances[line_number] = distance


def compare_question(question1, questions, distances, comparator):
    for row in questions:
        question2 = row[1]
        line_number = row[0]

        distance = comparator.compare(question1, question2)

        # Writes the distances in the shared array
        distances[line_number] = distance


def count_matches(questions, distances, threshold, dup_col, count):
    for i, row in enumerate(questions):
        duplicate = 1 if distances[i] <= threshold else 0

        if row[dup_col] == duplicate:
            count.value += 1
