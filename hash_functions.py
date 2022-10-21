
# Generates a sequence of universal hash functions.
# (( ax + b ) mod p ) mod m

from os import P_ALL


def universal_hash_functions(a_vals, b_vals, p, m):
    if not (len(a_vals) == len(b_vals)):
        return None
    
    hash_functions = []

    for i in range(len(a_vals)):
        a = a_vals[i]
        b = b_vals[i]
        lambda_f = lambda x: (((a*x) + b) % p) % m
        hash_functions.append(lambda_f)
        #print(lambda_f)

    return hash_functions

def polynomial_hash_functions(p_vals, q_vals, m):
    if not (len(p_vals) == len(q_vals)):
        return None

    hash_functions = []

    for i in range(len(p_vals)):
        p = p_vals[i]
        q = q_vals[i]
        #print(p, q, m)
        lambda_f = lambda str=str, p=p, q=q, m=m: sum([ord(str[i]) * (p**i) for i in range(len(str))]) % m
        hash_functions.append(lambda_f)

    return hash_functions
    
