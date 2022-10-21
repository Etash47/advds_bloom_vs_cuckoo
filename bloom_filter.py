import math
import time
from tracemalloc import start

class BloomFilter:

    # Params:
    # m_bit_v_size: The size of the bit vector we are working with
    # k_hash_fxns: The number of hash functions which an insertion will be hashed amongst
    # hash_fxns: An array of the hash functions we work with

    # Other object attributes:
    # n_inserted: number of elements inserted thus far
    # bit_vector: An array of binary values of size m_bit_v_size

    def __init__(self, m_bit_v_size, k_hash_fxns, hash_fxns):
        self.m_bit_v_size = m_bit_v_size
        self.k_hash_fxns = k_hash_fxns
        self.hash_fxns = hash_fxns
        
        self.bit_vector = [0] * self.m_bit_v_size
        self.n_inserted = 0
        
        self.test_n_non_duplicate = []

    def remove_all_insertions(self):
        self.bit_vector = [0] * self.m_bit_v_size
        self.n_inserted = 0
        self.test_n_non_duplicate = []

    def replace_hash_fxns(self, k_hash_fxns, hash_fxns):
        self.k_hash_fxns = k_hash_fxns
        self.hash_fxns = hash_fxns

    def insert_with_time_elapsed(self, key):
        start = time.time()
        for h in self.hash_fxns:
            hash_val = h(key)
            #print("ins: ", h, key, hash_val)
            self.bit_vector[hash_val] = 1
        
        end = time.time()

        # This part should not be timed (checking for duplicates for accurate false prob)
        if key not in self.test_n_non_duplicate:
            self.test_n_non_duplicate.append(key)
        # Resume timing

        return True, (end-start)

    def check_with_false_prob_and_time_elapsed(self, key):

        self.n_inserted = len(self.test_n_non_duplicate)

        start = time.time()

        for h in self.hash_fxns:
            hash_val = h(key)
            #print(h, key, hash_val)
            if self.bit_vector[hash_val] == 0:
                return False, 0, (time.time() - start)

        end = time.time()

        false_prob = (1 - 
            math.exp(
                    float(-self.k_hash_fxns * self.n_inserted) / float(self.m_bit_v_size)
                )
            ) ** self.k_hash_fxns

        return True, false_prob, (end - start)
