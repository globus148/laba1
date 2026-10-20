def two_points(n, m):
    i = 0
    j = 0
    len_n = len(n)
    len_m = len(m)
    while i < len_n and j < len_m:
        val_n = n[i]
        val_m = m[j]
        if val_n < val_m:
            i += 1
        elif val_n > val_m:
            j += 1
        else:
            return True
    return False
