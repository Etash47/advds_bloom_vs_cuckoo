import cuckoo_filter
from random import getrandbits
import matplotlib.pyplot as plt

def test_cuckoo_filter(f_size):
    M = 512
    
    cf = cuckoo_filter.CuckooFilter(array_size=M, bucket_size=4, f_bit_size=f_size, max_kicks=500)
    
    insertion_lst = []
    insert_success = True
    while insert_success:
        key = getrandbits(64)
        insertion_lst.append(key)
        insert_success = cf.insert(key)
    
    alpha = cf.get_load_factor()
    
    false_key_lst = generate_false_keys(512, insertion_lst)
    num_false_pos = 0
    for k in false_key_lst:
        if cf.lookup(k):
            num_false_pos += 1
    epsilon = num_false_pos / len(false_key_lst)
    
    return alpha, epsilon

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

def generate_false_keys(n, insert_lst):
    false_key_lst = []
    for _ in range(n):
        k = getrandbits(64)
        while k in insert_lst:
            k = getrandbits(64)
        false_key_lst.append(k)
    return false_key_lst
    
def main():
    f = 9
    # alpha, epsilon = test_cuckoo_filter(f)
    # print("For f = {}:".format(f))
    # print("alpha: {}".format(alpha))
    # print("epsilon: {}".format(epsilon))
    
    time_lst = time_insertion()
    print(time_lst[-50:-1])
    
if __name__ == "__main__":
    main()