def double_binary(n, m):
    if len(m) > len(n):
        m, n = n, m

    def helper(lm, rm, ln, rn):
        if lm > rm or ln > rn:
            return False

        mid_m = (lm + rm) // 2
        target = m[mid_m]
        low, high = ln, rn

        while low <= high:
            mid = (low + high) // 2
            val = n[mid]
            if val == target:
                return True
            elif val < target:
                low = mid + 1
            else:
                high = mid - 1
        return helper(lm, mid_m - 1, ln, high) or helper(mid_m + 1, rm, low, rn)

    return helper(0, len(m) - 1, 0, len(n) - 1)
