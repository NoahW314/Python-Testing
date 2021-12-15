
def generate_derangements(m, used, remaining_hats, remaining_people):
    if m == 0:
        yield used
    elif m == 1:
        return
    else:
        for i in range(1, len(remaining_hats)):
            # First assign a hat i to person 0 (where i\not=0)
            used[remaining_people[0]] = remaining_hats[i]
            # Next assign any hat to person i
            # If this hat is hat 0, then the problem is reduced to m-2 people and m-2 hats
            used[remaining_people[i]] = remaining_hats[0]
            next_people = [remaining_people[j] for j in range(m) if j != 0 and j != i]
            next_hats = [remaining_hats[j] for j in range(m) if j != 0 and j != i]
            yield from generate_derangements(m-2, used, next_hats, next_people)
            # Otherwise, the problem is reduced to m-1 people and m-1 hats
            next_people = [remaining_people[j] for j in range(m) if j != 0]
            next_hats = []
            for j in range(m):
                if j != i and j != 0:
                    next_hats.append(remaining_hats[j])
                elif j == i:
                    next_hats.append(remaining_hats[0])
            yield from generate_derangements(m-1, used, next_hats, next_people)