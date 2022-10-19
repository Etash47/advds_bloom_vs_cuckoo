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

    in_set_probabilities = [bloomFilter.check_with_false_prob(i) for i in range(100)]
    print("\n-----\n-----\n-----\n")

    for i, j, k in in_set_probabilities:
        print(i, j, k)

    plt.plot(list(range(100)), [1 - x[1] if x[1] > 0 else 0 for x in in_set_probabilities])
    plt.title("Probability of x in set")
    plt.show()
    

def main():
    test_bloom_filter()

if __name__=='__main__':
    main()