def exponential_search(n, m):
    if len(n) > len(m):
        n, m = m, n

    len_m = len(m)
    j = 0
    for x in n:
        if j >= len_m:
            break
        if m[j] == x:
            return True
        elif m[j] > x:
            continue

        step = 1
        while j + step < len_m and m[j + step] < x:
            step *= 2

        low = j + step // 2
        high = min(j + step, len_m - 1)
        while low <= high:
            mid = (low + high) // 2
            val = m[mid]
            if val == x:
                return True
            elif val < x:
                low = mid + 1
            else:
                high = mid - 1
        j = low
    return False
