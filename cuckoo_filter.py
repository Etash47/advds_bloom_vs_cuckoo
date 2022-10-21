import numpy as np
import time
from tracemalloc import start
from random import randint, choice, getrandbits

class Bucket:
    
    # Params:
    # b: the number of fingerprints we allow each bucket to hold (usually 2,4, or 8)
    
    # Other attributes:
    # fingerprint_lst: contains all fingerprints that hash to the bucket
    # full: Boolean that indicates whether a bucket is full or not
    
    def __init__(self, b):
        self.fingerprint_lst = []
        self.capacity = b
        self.full = False
        
    # Insert a fingerprint to the bucket    
    def insert(self, f):
        # Only insert if there is room in the bucket
        if not self.full:
            self.fingerprint_lst.append(f)
            if len(self.fingerprint_lst) == self.capacity:
                self.full = True
            return True
        return False
    
    # Use this method when deleting from the Cuckoo Filter
    def remove(self, f):
        if f in self.fingerprint_lst:
            self.fingerprint_lst.remove(f)
            self.full = False

class CuckooFilter:
    
    # Params:
    # array_size: The size of the array we are working with
    # bucket_size: The number of entries allowed in each bucket
    # h_fcn: The hash function used to hash each inserted element
    # f_bit_size: The size of the fingerprint in bits
    # max_kicks: The maximum number of times we will allow "kicking" an entry from a bucket to its alternate bucket
    
    # Other attributes:
    # filter: The data structure itself - array of buckets where each bucket contains a list of fingerprints
    # num_occupied_buckets: The number of non-empty buckets in the filter - used to calculate load factor
    
    def __init__(self, array_size, bucket_size, f_bit_size, max_kicks):
        self.array_size = array_size
        # self.h_fcn = h_fcn
        self.f_bit_size = f_bit_size
        self.max_kicks = max_kicks
        self.filter = []
        self.num_occupied_buckets = 0
        self.num_entries = 0
        
        # Initialize each index to store an empty Bucket
        for _ in range(self.array_size):
            self.filter.append(Bucket(bucket_size))
            
    def multiplicative_hash(self, x):
        p = 32779
        a = randint(0,p)
        b = randint(0,p+1)
        m = self.array_size
        return (((a*x) + b) % p) % m
    
    def fingerprint(self, x):
        '''
        Computes the fingerprint of a given string using polynomial hashing.
        Params:
        x - the key to be hashed
        f_size - the number of desired bits in the fingerprint
        '''
        p = 53
        a = 47
        b = 13
        m = 2**self.f_bit_size
        return (((a*x) + b) % p) % m
        
    def insert(self, x):
        start = time.time()
        f = self.fingerprint(x)
        i1 = self.multiplicative_hash(x)
        i2 = i1 ^ self.multiplicative_hash(f) # Partial Key Cuckoo Hashing

        if not self.filter[i1].full:
            self.filter[i1].insert(f)
            self.num_entries += 1
            return True, time.time()-start
        elif not self.filter[i2].full:                
            self.filter[i2].insert(f)
            self.num_entries += 1
            return True, time.time()-start

        # Must relocate existing items
        i = choice(np.array((i1, i2)))
        for _ in range(self.max_kicks):
            # Randomly select bucket entry to kick out
            idx = np.random.choice(len(self.filter[i].fingerprint_lst))
            entry = self.filter[i].fingerprint_lst[idx]
            self.filter[i].fingerprint_lst[idx] = f
            # Compute alternate bucket index for kicked out entry
            i = i ^ self.multiplicative_hash(entry)
            # Attempt to insert kicked out entry into its alternate bucket
            if not self.filter[i].full:
                self.filter[i].insert(f)
                self.num_entries += 1
                return True, time.time()-start
        # reached max number of kicks, return failure  
        return False, time.time()-start

    def lookup(self, x):
        f = self.fingerprint(x)
        i1 = self.multiplicative_hash(x)
        i2 = i1 ^ self.multiplicative_hash(f) # May want to change how we hash the fingerprint
        if f in self.filter[i1].fingerprint_lst or f in self.filter[i2].fingerprint_lst:
            return True
        return False
        
    def delete(self, x):
        f = self.fingerprint(x)
        i1 = self.multiplicative_hash(x)
        i2 = i1 ^ self.multiplicative_hash(f) # May want to change how we hash the fingerprint
        if f in self.filter[i1].fingerprint_lst:
            self.filter[i1].remove(f)
            self.num_entries -= 1
            return True

        elif f in self.filter[i2].fingerprint_lst:
            self.filter[i2].remove(f)
            self.num_entries -= 1
            return True
        return False
    
    def get_load_factor(self):
        # print("occupancy: {}".format(self.num_entries))
        # print("size: {}".format(4 * self.array_size))
        return self.num_entries / (len(self.filter[0].fingerprint_lst) * self.array_size)
    
    # Method to display the fingerprints stored in each bucket in the filter
    def print_filter(self):
        for i in range(len(self.filter)):
            if len(self.filter[i].fingerprint_lst):
                print('-----------------------------------')
                print('at index: {}, we have fingerprints:'.format(i))
            for j in range(len(self.filter[i].fingerprint_lst)):
                print(bin(self.filter[i].fingerprint_lst[j])[2:])
        
def main():
    cf = CuckooFilter(array_size=2**15, bucket_size=4, f_bit_size=4, max_kicks=10)
    insertion_lst = []
    insert_success = True
    start = time.time()
    while insert_success:
        key = getrandbits(64)
        insertion_lst.append(key)
        insert_success = cf.insert(key)
    end = time.time()
    print(end-start)

if __name__=='__main__':
    main()