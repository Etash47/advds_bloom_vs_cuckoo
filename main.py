import hash_functions
import bloom_filter
import cuckoo_filter
from random import randint, choice
import matplotlib.pyplot as plt
import numpy as np
import string
import hashlib

letters = string.ascii_lowercase
inserting_num = 2**11
num_random_checks = 500

# def test_bloom_filter():
#     # k = 10 hash functions
#     k = 10
#     a_vals = [randint(0, 9) for _ in range(k)]
#     b_vals = [randint(0, 20) for _ in range(k)]
#     p_vals = [choice([53, 97, 193, 389]) for _ in range(k)]
#     # We let m (bit vector size) = 1000

#     m = 1000

#     hash_fxns = hash_functions.universal_hash_functions(a_vals, b_vals, p_vals, m)

#     bloomFilter = bloom_filter.BloomFilter(m, k, hash_fxns)

#     to_insert = list(set([randint(0, 100) for _ in range(100)]))

#     insertion_times = [bloomFilter.insert_with_time_elapsed(i) for i in to_insert]
#     for i,j in insertion_times:
#         print(i,j)

#     plt.plot(list(range(len(insertion_times))), [x[1] for x in insertion_times])
#     plt.title("Speeds for 100 insertions at m = 1000, k = 10")
#     #plt.show()

#     in_set_probabilities = [bloomFilter.check_with_false_prob_and_time_elapsed(i) for i in range(100)]
#     print("\n-----\n-----\n-----\n")

#     for i, j, k in in_set_probabilities:
#         print(i, j, k)

#     plt.plot(list(range(100)), [1 - x[1] if x[1] > 0 else 0 for x in in_set_probabilities])
#     plt.title("Probability of x in set")
#     #plt.show()


def analyse_bloom_filter():
    # Goal 1A: Test theoretical rate of false positives on bloom filter as n -> inf
    # Goal 2A: Test empirical rate of false positives on bloom filter as n -> inf
    # Goal 3A: Test insertion speed as n -> inf
    # Goal 1B, 2B, 2C: Repeat goals 1, 2, and 3 with Murmur3, SHA-256
    # Goal 5: Repeat goals 1, 2, and 3 with Kirsh-Mitzenmacher

    # POLYNOMIAL HASH (GOAL 1, 2, 3)
    k = 4
    # a_vals = [randint(1, 5000) for _ in range(k)]
    # b_vals = [randint(-500000, 500000) for _ in range(k)]
    p_vals = [7, 3, 11, 17, 13]
    q_vals = [1000123465987, 468395662504823, 657835997711, 18826507658281, 921023456789]   
    # print(a_vals)
    # print(b_vals)
    # We let m (bit vector size) = 10000

    #m = 2885
    #m = 18996
    m = 12000

    # hash_fxns = hash_functions.universal_hash_functions(a_vals, b_vals, p, m)
    hash_fxns = hash_functions.polynomial_hash_functions(p_vals, q_vals, m)

    bloomFilter = bloom_filter.BloomFilter(m, k, hash_fxns)

    bloomFilter.remove_all_insertions()
    f = goal_1_theoretial_false_pos_rate(bloomFilter=bloomFilter, label="Polynomial Hash Family", graphTitle="")
    
    bloomFilter.remove_all_insertions()
    g = goal_2_polynomial_hash(bloomFilter=bloomFilter, label="Polynomial Hash Family", graphTitle="Empirical False Positive Rate as Increasing Elements \n (Poly Hash)")

    bloomFilter.remove_all_insertions()
    h = goal_3_polynomial_hash(bloomFilter=bloomFilter, label="Polynomial Hash Family", graphTitle="Insertion time with increasing insertions \n (Poly Hash)")

    hash_fxns = [
        hashlib.sha256,
        hashlib.sha512,
        hashlib.sha3_256,
        hashlib.sha3_512,
    ]

    bloomFilter.remove_all_insertions()
    f2 = goal_1_theoretial_false_pos_rate(bloomFilter=bloomFilter, label="SHA Hash Family", graphTitle="Thereotical False Positive Rate As Increasing Elements \n (Poly vs. SHA Hash)")
    
    bloomFilter.remove_all_insertions()
    g2 = goal_2_polynomial_hash(bloomFilter=bloomFilter, label="SHA Hash Family", graphTitle="Empirical False Positive Rate as Increasing Elements \n (Poly vs. SHA Hash)")

    bloomFilter.remove_all_insertions()
    h2 = goal_3_polynomial_hash(bloomFilter=bloomFilter, label="SHA Hash Family", graphTitle="Insertion time with increasing insertions \n (Poly vs. SHA Hash)")
    
    plt.figure(1).legend(loc='center')

    plt.figure(2).legend(loc='center')
    
    plt.figure(3).legend(loc='lower right')
    
    plt.show()

def goal_1_theoretial_false_pos_rate(bloomFilter: bloom_filter, label, graphTitle):
    #to_insert = list(set([randint(0, 1000000) for _ in range(500)]))
    to_insert = [(''.join(choice(letters) for i in range(30))) for _ in range(inserting_num)]

    false_probs = []

    i = 0
    for inserting in to_insert:
        success, insertion_time = bloomFilter.insert_with_time_elapsed(inserting)
        found, false_prob, check_time = bloomFilter.check_with_false_prob_and_time_elapsed(inserting)
        false_probs.append(false_prob)
        i += 1

    f = plt.figure(1)
    plt.plot(range(i), false_probs, label=label)
    plt.xlabel('Number of Elements Inserted')
    plt.ylabel('False Positive Rate')
    plt.title(graphTitle)
    return(f)

def goal_2_polynomial_hash(bloomFilter: bloom_filter, label, graphTitle):
    to_insert = [(''.join(choice(letters) for i in range(30))) for _ in range(inserting_num)]

    false_probs_empirical = []
    false_probs_theoretical = []

    uninserted_elements = [(''.join(choice(letters) for i in range(30))) for _ in range(500)]

    inserted = []
    for inserting in to_insert:
        success, insertion_time = bloomFilter.insert_with_time_elapsed(inserting)
        inserted.append(inserting)
        # Now we test for false positives on all elements not in the set
        if inserting in uninserted_elements:
            uninserted_elements.remove(inserting)

        false_finds = 0

        for ri in range(num_random_checks):
            #print('ri', end=' ')
            #uninserted = choice(uninserted_elements)
            uninserted = (''.join(choice(letters) for i in range(30)))
            while uninserted in inserted:
                uninserted = (''.join(choice(letters) for i in range(30)))
            found, false_prob_theor, _ = bloomFilter.check_with_false_prob_and_time_elapsed(uninserted)
            if found:
                false_finds += 1
                    
        false_probs_empirical.append(float(false_finds) / num_random_checks)

    g = plt.figure(2)
    smoothed_empirical = np.convolve(false_probs_empirical, np.ones(10) / 10)[:len(to_insert)]
    plt.plot(range(len(to_insert)), smoothed_empirical, label=label)
    plt.xlabel('Number of Elements Inserted')
    plt.ylabel('False Positive Rate')
    plt.title(graphTitle)

    #print(inserted)
    #print(uninserted_elements)

    return(g)

def goal_3_polynomial_hash(bloomFilter: bloom_filter, label, graphTitle):
    to_insert = [(''.join(choice(letters) for i in range(30))) for _ in range(inserting_num)]

    times = []
    for inserting in to_insert:
        success, time_e = bloomFilter.insert_with_time_elapsed(inserting)
        times.append(time_e)

    h = plt.figure(3)

    smoothed_times = np.convolve(times, np.ones(10) / 10)[:len(to_insert)]

    plt.plot(range(len(to_insert)), smoothed_times, label=label)
    plt.title(graphTitle)
    plt.xlabel('Number of Elements Inserted')
    plt.ylabel('Insertion Time')


def main():
    #test_bloom_filter()
    analyse_bloom_filter()

if __name__=='__main__':
    main()