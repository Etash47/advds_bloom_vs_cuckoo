import cuckoo_filter
import math
from random import getrandbits
import matplotlib.pyplot as plt

def test_false_positives(f_size):
    M = 2**10
    n = math.ceil(0.95*4*M)
    print("n: " + str(n))
    n_vals = [x for x in range(1,n+1)]
    
    cf = cuckoo_filter.CuckooFilter(array_size=M, bucket_size=4, f_bit_size=f_size, max_kicks=500)
    # List of false keys to use for determing false positve rate
    false_key_lst = [getrandbits(64) for x in range(n)]
    epsilon_lst = []
    
    for _ in range(n):
        key = getrandbits(64)
        while key in false_key_lst:
            key = getrandbits(64)
        cf.insert(key)
        num_false_pos = 0
        for i in range(n):
            if cf.lookup(false_key_lst[i]):
                num_false_pos += 1
        epsilon = num_false_pos / n
        epsilon_lst.append(epsilon)
        
    plt.plot(n_vals, epsilon_lst)
    plt.title("False Positive Rate for Cuckoo Filter with f = {}".format(f_size))
    plt.show()
                
    return epsilon_lst    

def time_insertion():
    # Create a (2,4)-cuckoo filter with array size of 2^10 and fingerprints of 4 bits
    n = 2**11
    cf = cuckoo_filter.CuckooFilter(array_size=2**10, bucket_size=4, f_bit_size=4, max_kicks=500)
    time_lst = []
    for _ in range(n):
        key = getrandbits(64)
        _, t = cf.insert(key)
        time_lst.append(t)
        
    n_vals = [x for x in range(1,n+1)]
    
    plt.plot(n_vals, time_lst)
    plt.title("Insertion speed for Cuckoo filter")
    plt.show()
    
def main():
    f = 9
    time_lst = time_insertion()
    epsilon_lst = test_false_positives(f)
    
if __name__ == "__main__":
    main()