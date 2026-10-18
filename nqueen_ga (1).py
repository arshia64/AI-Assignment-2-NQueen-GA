# N-Queen Problem (N = 4) using Genetic Algorithm
# Roulette Wheel Selection, One-Point Crossover (after 2nd bit), No Mutation

POP_SIZE = 4
CUT = 2  # crossover point (after 2nd bit)


def conflicts(state):
    """Count pairs of queens in the same row or on the same diagonal."""
    count = 0
    for i in range(4):
        for j in range(i + 1, 4):
            same_row = state[i] == state[j]
            same_diag = abs(state[i] - state[j]) == abs(i - j)
            if same_row or same_diag:
                count += 1
    return count


def fitness(state):
    return 1 / (1 + conflicts(state))


def evaluate(population, title):
    """Print the table and return the expected counts."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    fits = [fitness(s) for s in population]
    total = sum(fits)

    print("State  Chromosome     Conflicts  Fitness  Probability  Expected")
    expected = []
    for i, s in enumerate(population):
        prob = fits[i] / total
        exp = prob * POP_SIZE
        expected.append(exp)
        print(f"S{i + 1}     {str(s):<14} {conflicts(s):<10} {fits[i]:<8.4f} "
              f"{prob:<12.4f} {exp:.4f}")

    print(f"Total fitness = {total:.4f}")
    return expected


def actual_counts(expected):
    """Round expected counts; if total is not 4, fix it."""
    counts = [int(e + 0.5) for e in expected]  # normal rounding

    # Total too big: remove from the smallest expected count
    while sum(counts) > POP_SIZE:
        candidates = [i for i in range(len(counts)) if counts[i] > 0]
        smallest = min(candidates, key=lambda i: (expected[i], -i))
        counts[smallest] -= 1

    # Total too small: add to the largest expected count
    while sum(counts) < POP_SIZE:
        largest = max(range(len(counts)), key=lambda i: expected[i])
        counts[largest] += 1

    return counts


def make_parent_pool(population, counts):
    pool = []
    for state, c in zip(population, counts):
        for _ in range(c):
            pool.append(state)
    return pool


def crossover(p1, p2):
    child1 = p1[:CUT] + p2[CUT:]
    child2 = p2[:CUT] + p1[CUT:]
    return child1, child2


def next_generation(population, title):
    expected = evaluate(population, title)
    counts = actual_counts(expected)
    print("Actual counts:", counts)

    pool = make_parent_pool(population, counts)
    print("Parent pool  :", pool)

    # Pair 1: pool[0] x pool[2]   Pair 2: pool[1] x pool[3]
    c1, c2 = crossover(pool[0], pool[2])
    c3, c4 = crossover(pool[1], pool[3])
    print(f"Crossover 1: {pool[0]} x {pool[2]} -> {c1}, {c2}")
    print(f"Crossover 2: {pool[1]} x {pool[3]} -> {c3}, {c4}")

    return [c1, c2, c3, c4]


# ---------------- MAIN PROGRAM ----------------
generation1 = [
    [2, 4, 3, 1],
    [1, 2, 3, 4],
    [2, 1, 3, 2],
    [4, 3, 1, 1],
]

generation2 = next_generation(generation1, "GENERATION 1 (Initial Population)")
generation3 = next_generation(generation2, "GENERATION 2 (Offspring)")

print("\nNew offspring after Generation 2 crossover:")
for i, s in enumerate(generation3, start=1):
    print(f"O{i} = {s}  (conflicts = {conflicts(s)})")
