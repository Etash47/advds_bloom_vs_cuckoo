
# Generates a sequence of universal hash functions.
# (( ax + b ) mod p ) mod m
def universal_hash_functions(a_vals, b_vals, p_vals, m):
    if not (a_vals == b_vals and b_vals == p_vals):
        return None
    
    hash_functions = []

    for i in range(len(a_vals)):
        a = a_vals[i]
        b = b_vals[i]
        p = p_vals[i]
        hash_functions.append(
            lambda x: (((a*x) + b) % p) % m
        )

    return hash_functions
