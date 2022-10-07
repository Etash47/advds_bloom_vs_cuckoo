class BloomFilter:

    # Params:
    # n_inserted: number of elements inserted thus far
    # m_bit_v_size: The size of the bit vector we are working with
    # k_hash_fxns: The number of hash functions which an insertion will be hashed amongst

    # Other object attributes:
    # hash_fxns: An array of the hash functions we work with
    # bit_vector: An array of binary values of size m_bit_v_size

    def __init__(self, m_bit_v_size, k_hash_fxns):
        self.n_inserted = 0
        self.m_bit_v_size = m_bit_v_size
        self.k_hash_fxns = k_hash_fxns

        self.bit_vector = [0] * self.m_bit_v_size

        self.hash_fxns = []

    def add_hash_function(self, fxn):
        if len(self.hash_fxns) >= self.k_hash_fxns:
            return False
        else:
            self.hash_fxns.append(fxn)
            return True

    def insert(self, key):
        return False

    def check_with_prob(self, key):
        return False



