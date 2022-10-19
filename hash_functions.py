
# Generates a sequence of universal hash functions.
# (( ax + b ) mod p ) mod m
def universal_hash_functions(a_vals, b_vals, p_vals, m):
    if not (len(a_vals) == len(b_vals) and len(b_vals) == len(p_vals)):
        return None
    
    hash_functions = []

    for i in range(len(a_vals)):
        a = a_vals[i]
        b = b_vals[i]
        p = p_vals[i]
        lambda_f = lambda x: (((a*x) + b) % p) % m
        hash_functions.append(lambda_f)
        #print(lambda_f)

    return hash_functions
