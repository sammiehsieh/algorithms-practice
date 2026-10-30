# Discuss with GPT: https://chatgpt.com/share/6adff011-8a10-83ea-9050-b313d3e0eedd
# Task 2's solution (as LeetCode 74): https://www.cnblogs.com/grandyang/p/4323301.html

# -------------------------------- task 1 --------------------------------


def search_range(nums, target):
    """
    search the target number in array, and results in the first and last position as [f, l]

    it has to be O(log n) time complexity, so use binary search and keep binary search till the end

    space complexity is O(1) with 4 variables: low, high, result, mid
    """

    def find_bound(is_first):
        """
        binary search that keeps going after a hit to find the edge
        """
        low = 0
        high = len(nums) - 1
        result = -1
        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] == target:
                result = mid  # find one but keep searching
                if is_first:
                    high = mid - 1  # keep finding left
                else:
                    low = mid + 1  # keep finding right
            elif nums[mid] < target:
                low = mid + 1  # keep finding right
            else:
                high = mid - 1  # keep finding left
        return result

    return [find_bound(True), find_bound(False)]


# -------------------------------- task 2 --------------------------------


def search_matrix(matrix, target):
    """
    return Boolean to see if the target is in the matrix

    treats the m x n matrix as one sorted array of length m*n.

    it has to be O(log (m*n)) time complexity, so also using binary search mix with `mid` to get which row and column

    space complexity is O(1) with 6 variables: m, n, low, high, mid, value
    """
    if not matrix or not matrix[0]:
        return False  # empty matrix or empty rows

    m = len(matrix)
    n = len(matrix[0])
    low = 0  # first index
    high = m * n - 1  # last index

    while low <= high:
        mid = low + (high - low) // 2  # middle index

        # map the 1D index back to 2D:
        # (1) row = mid // n
        # (2) col = mid % n
        value = matrix[mid // n][mid % n]
        if value == target:
            return True
        elif value < target:
            low = mid + 1
        else:
            high = mid - 1

    return False


# ////////////////////////////// test case below //////////////////////////////


def _test_task_1():
    tests = [
        ([4, 9, 10, 13, 17, 17, 19, 21], 17, [4, 5]),  # from example 1
        ([2, 4, 6, 8, 10, 14, 16], 12, [-1, -1]),  # from example 2
        ([], 0, [-1, -1]),  # from example 3
        ([5], 5, [0, 0]),
        ([5], 3, [-1, -1]),
        ([3, 3, 3, 3], 3, [0, 3]),
        ([1, 3, 5], 9, [-1, -1]),
        ([1, 2, 3, 4], 1, [0, 0]),
        ([1, 2, 3, 4], 4, [3, 3]),
    ]
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~ task 1 test ~~~~~~~~~~~~~~~~~~~~~~~~~")
    for nums, target, expected in tests:
        result = search_range(nums, target)
        # print("-------------------------")
        print()
        print("Array like:", nums)
        print("Target number:", target)
        print("Searching result:", result)
        assert result == expected, (nums, target)


def _test_task_2():
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    tests = [
        (matrix, 3, True),  # from example 1
        (matrix, 13, False),  # from example 2
        (matrix, 1, True),
        (matrix, 60, True),
        (matrix, 0, False),
        (matrix, 100, False),
        ([[5]], 5, True),  # 1x1, found
        ([[5]], 2, False),  # 1x1, missing
        ([[1, 3, 5]], 3, True),  # single row
        ([[1], [3], [5]], 5, True),  # single column
        ([], 1, False),  # empty matrix
        ([[]], 1, False),  # empty row
    ]
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~ task 2 test ~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    for grid, target, expected in tests:
        print()
        print("Matrix like:", grid)
        result = search_matrix(grid, target)
        print(f"Find {target}:", result)
        assert result == expected, (grid, target)


_test_task_1()
_test_task_2()
