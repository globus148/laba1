def binary_search(n, m):
    if len(n) > len(m):
        n, m = m, n

    len_m = len(m)
    for x in n:
        left = 0
        right = len_m - 1
        while left <= right:
            mid = (left + right) // 2
            val = m[mid]
            if val == x:
                return True
            elif val < x:
                left = mid + 1
            else:
                right = mid - 1
    return False
