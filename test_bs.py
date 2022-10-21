import hash_functions
def main():
    p_vals = [7, 3, 11, 17, 13]
    q_vals = [1000123465987, 468395662504823, 657835997711, 18826507658281, 921023456789]  
    m = 3606
    for i in range(len(p_vals)):
        p = p_vals[i]
        q = q_vals[i]
        #print(p, q, m)
        str = 'msmqhagqymbcyqsumtvtcbitkvqtnx'
        hash_val = sum([ord(str[i]) * (p**i) for i in range(len(str))]) % m
        print(hash_val)


if __name__=='__main__':
    main()