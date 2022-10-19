import hash_functions
import bloom_filter
import cuckoo_filter
from random import randint, choice
import matplotlib.pyplot as plt

def test_bloom_filter():
    # k = 10 hash functions
    k = 10
    a_vals = [randint(0, 9) for _ in range(k)]
    b_vals = [randint(0, 20) for _ in range(k)]
    p_vals = [choice([53, 97, 193, 389]) for _ in range(k)]
    # We let m (bit vector size) = 1000

    m = 1000

    hash_fxns = hash_functions.universal_hash_functions(a_vals, b_vals, p_vals, m)

    bloomFilter = bloom_filter.BloomFilter(m, k, hash_fxns)

    to_insert = list(set([randint(0, 100) for _ in range(100)]))

    insertion_times = [bloomFilter.insert_with_time_elapsed(i) for i in to_insert]
    for i,j in insertion_times:
        print(i,j)

    plt.plot(list(range(len(insertion_times))), [x[1] for x in insertion_times])
    plt.title("Speeds for 100 insertions at m = 1000, k = 10")
    #plt.show()

    in_set_probabilities = [bloomFilter.check_with_false_prob_and_time_elapsed(i) for i in range(100)]
    print("\n-----\n-----\n-----\n")

    for i, j, k in in_set_probabilities:
        print(i, j, k)

    plt.plot(list(range(100)), [1 - x[1] if x[1] > 0 else 0 for x in in_set_probabilities])
    plt.title("Probability of x in set")
    #plt.show()


def analyse_bloom_filter():
    # Goal 1: Test theoretical rate of false positives on bloom filter as n -> inf
    # Goal 2: Test empirical rate of false positives on bloom filter as n -> inf
    # Goal 3: Test insertion speed as n -> inf
    # Goal 4: Repeat goals 1, 2, and 3 with Murmur3, SHA-256
    # Goal 5: Repeat goals 1, 2, and 3 with Kirsh-Mitzenmacher

    # UNIVERSAL HASH (GOAL 1, 2, 3)
    # k = 100 hash functions
    k = 20
    a_vals = [randint(0, 37) for _ in range(k)]
    b_vals = [randint(0, 47) for _ in range(k)]
    p_vals = [choice([53, 97, 193, 389]) for _ in range(k)]
    # We let m (bit vector size) = 10000

    m = 1000000

    hash_fxns = hash_functions.universal_hash_functions(a_vals, b_vals, p_vals, m)

    bloomFilter = bloom_filter.BloomFilter(m, k, hash_fxns)

    bloomFilter.remove_all_insertions()
    f = goal_1_universal_hash(bloomFilter=bloomFilter)
    
    bloomFilter.remove_all_insertions()
    g = goal_2_universal_hash(bloomFilter=bloomFilter)

    plt.show()

def goal_1_universal_hash(bloomFilter: bloom_filter):
    to_insert = list(set([randint(0, 1000000) for _ in range(1000)]))
    false_probs = []

    i = 0
    for inserting in to_insert:
        success, insertion_time = bloomFilter.insert_with_time_elapsed(inserting)
        found, false_prob, check_time = bloomFilter.check_with_false_prob_and_time_elapsed(inserting)
        false_probs.append(false_prob)
        i += 1

    f = plt.figure(1)
    plt.plot(range(i), false_probs)
    plt.title("Theoretical false positive probability with increasing insertions (universal hash)")
    return(f)

def goal_2_universal_hash(bloomFilter: bloom_filter):
    to_insert = list(set([randint(0, 1000000) for _ in range(1000)]))
    false_probs = []

    uninserted_elements = list(set([randint(0, 1000000) for _ in range(2000)]))

    inserted = []
    for inserting in to_insert:
        success, insertion_time = bloomFilter.insert_with_time_elapsed(inserting)
        inserted.append(inserting)
        # Now we test for false positives on all elements not in the set
        if inserting in uninserted_elements:
            uninserted_elements.remove(inserting)

        false_finds = 0
        num_random_checks = 100

        for ri in range(num_random_checks):
            uninserted = choice(uninserted_elements)
            assert uninserted not in inserted
            found, _, _ = bloomFilter.check_with_false_prob_and_time_elapsed(uninserted)
            if found:
                false_finds += 1
        
        false_probs.append(float(false_finds) / num_random_checks)

    g = plt.figure(2)
    plt.plot(range(len(to_insert)), false_probs)
    plt.title("Empirical false positive probability with increasing insertions (universal hash)")

    print(inserted)
    print(uninserted_elements)

    return(g)




def main():
    #test_bloom_filter()
    analyse_bloom_filter()

if __name__=='__main__':
    main()