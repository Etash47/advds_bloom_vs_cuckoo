import numpy as np

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
    # bucket_array: the data structure itself - array of buckets where each bucket contains a list of fingerprints
    
    def __init__(self, array_size, bucket_size, h_fcn, f_bit_size, max_kicks):
        self.array_size = array_size
        self.h_fcn = h_fcn
        self.f_bit_size = f_bit_size
        self.max_kicks = max_kicks
        self.bucket_array = []
        # Initialize each index to store an empty Bucket
        for _ in range(self.array_size):
            self.bucket_array.append(Bucket(bucket_size))
        
    def insert(self, x):
        f = fingerprint(x, self.f_bit_size)
        i1 = self.h_fcn(x)
        i2 = i1 ^ self.h_fcn(x) # Partial Cuckoo Hashing
        if not self.bucket_array[i1].full:
            self.bucket_array[i1].insert(f)
            return True
        elif not self.bucket_array[i2].full:
            self.bucket_array[i2].insert(f)
            return True

        # Must relocate existing items
        i = np.random.choice(np.array((i1, i2)))
        for n in range(self.max_kicks):
            # Randomly select bucket entry to kick out
            idx = np.random.choice(len(self.bucket_array[i].fingerprint_lst))
            entry = self.bucket_array[i].fingerprint_lst[idx]
            self.bucket_array[i].fingerprint_lst[idx] = f
            # Compute alternate bucket index for kicked out entry
            i = i ^ self.h_fcn(entry)
            # Attempt to insert kicked out entry into its alternate bucket
            if not self.bucket_array[i].full:
                self.bucket_array[i].insert(f)
                return True
        # reached max number of kicks, return failure  
        return False

    def lookup(self, x):
        f = fingerprint(x, self.f_bit_size)
        i1 = self.h_fcn(x)
        i2 = i1 ^ self.h_fcn(str(f)) # May want to change how we hash the fingerprint
        if f in self.bucket_array[i1].fingerprint_lst or f in self.bucket_array[i2].fingerprint_lst:
            return True
        return False
        
    def delete(self, x):
        f = fingerprint(x, self.f_bit_size)
        i1 = self.h_fcn(x)
        i2 = i1 ^ self.h_fcn(str(f)) # May want to change how we hash the fingerprint
        if f in self.bucket_array[i1].fingerprint_lst or f in self.bucket_array[i2].fingerprint_lst:
            self.bucket_array[i1].remove(f)
            return True
        return False
    
    # Method to display the fingerprints stored in each bucket in the filter
    def print_filter(self):
        for i in range(len(self.bucket_array)):
            if len(self.bucket_array[i].fingerprint_lst):
                print('-----------------------------------')
                print('at index: {}, we have fingerprints:'.format(i))
            for j in range(len(self.bucket_array[i].fingerprint_lst)):
                print(bin(self.bucket_array[i].fingerprint_lst[j])[2:])
    
def fingerprint(s, f_bit_size):
    '''
    Computes the fingerprint of a given string using polynomial hashing.
    Params:
    s - the string to be hashed
    f_size - the number of desired bits in the fingerprint
    '''
    f_print = 0
    p = 31
    n = len(s) # Number of terms in the polynomial
    m = 2**f_bit_size # Size of the integer for modulo operation
    for i in range(n):
        f_print += (ord(s[i]) * p**i) % m
    return f_print % m


# --------Functions for testing the Cuckoo Filter----------

def polynomial_hash(s):
    m = 100 # Would like to not have to hard code this value
    h_val = 0
    p = 31
    n = len(s)
    for i in range(n):
        h_val += (ord(s[i]) * p**i) % m
    return h_val % m

# Simple function to generate n random strings of length k
def generate_insertion_list(n,k):
    l = []
    for i in range(n):
        s = ''
        for j in range(k):
            s += chr(np.random.choice(range(97,123)))
        l.append(s)
    return l  
        
def main():
    cf = CuckooFilter(array_size=100, bucket_size=4, h_fcn=polynomial_hash, f_bit_size=4, max_kicks=10)
    N = 100
    f_print_size = 4
    l = generate_insertion_list(N, 10)
    for i in range(N):
        if not cf.insert(l[i]):
            print('returned false for key: {}'.format(l[i]))
            
    # Code for testing insertion and deletion
    # cf.print_filter()
    # test_elt = l[0]
    # print('test_elt: {}'.format(test_elt))
    # print('hash of test_elt: {}'.format(polynomial_hash(test_elt)))
    # print('fingerprint of test_elt: {}'.format(fingerprint(test_elt, f_print_size)))
    # cf.delete(test_elt)
    # cf.print_filter()

if __name__=='__main__':
    main()