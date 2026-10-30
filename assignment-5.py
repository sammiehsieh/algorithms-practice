# Discuss with GPT: https://chatgpt.com/share/6ae0de02-7eb4-83e8-9b2d-2deb91aed20f
# Best answer for substring(task 1) - sliding window https://www.youtube.com/watch?v=uCCDOdwYbhg

# -------------------------------- task 1 --------------------------------


def check_inclusion(s1, s2):
    """
    we assume there are only lower case a-z

    Time complexity O(n), Space complexity O(1) because grid is fixed to 26
    """
    patternLength = len(s1)
    textLength = len(s2)
    if patternLength > textLength:
        return False

    need = [0] * 26  # to record how many times that each char show in s1
    window = [0] * 26  # to know the numbers that each char show in current window

    for ch in s1:
        # ord makes "string" to "ASCII/Unicode number"
        # step 1. ord(ch) - ord("a")
        #     we make strings to numbers 0~25 for index in array by doing
        #     因為陣列只有 26 格，位置是 0~25，但 ord 給的編號是 97~122，所以需要把起點平移
        # step 2. need[index_number] += 1
        #     counts for each char into index
        need[ord(ch) - ord("a")] += 1

    size = patternLength
    for i in range(textLength):
        # comes a char from the right side
        window[ord(s2[i]) - ord("a")] += 1

        # the window is out of size
        if i >= size:
            # now remove a char from left
            window[ord(s2[i - size]) - ord("a")] -= 1

        # every char count matches s1, so this window is a permutation of s1
        if window == need:
            return True
    return False


# -------------------------------- task 2 --------------------------------


def generate_solutions():
    """
    use backtracking to find all valid solutions

    solution[i]: means at i column, queen would be placed at which row (1~8)

    time complexity: O(N!)
      - backtracking tries possible queen placements and used rows cannot be reused
    space complexity: O(S * N)
      - store S valid solutions (each contains N queen positions)
    """
    solutions = []
    path = []
    # use set here because it will be faster to see if the thing is inside => O(1)
    rows_used = set()
    diag1 = set()  # same "row - col" means the same diagonal (\)
    diag2 = set()  # same "row + col" means the same diagonal (/)

    def backtrack(col):
        if col == 8:
            solutions.append(list(path))  # copy one into solutions
            return
        for row in range(1, 9):  # doesn't include the last
            if row in rows_used or (row - col) in diag1 or (row + col) in diag2:
                continue  # conflict, cut this subtree

            # trying the assumption
            path.append(row)  # step 1: assume this row
            rows_used.add(row)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(col + 1)  # step 2: recursion, keep moving down(deeper)

            path.pop()  # step 3: undo, so this column can try the next row
            rows_used.remove(row)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)  # start from column[0]
    return solutions


SOLUTIONS = generate_solutions()


def min_moves(positions):
    """
    compare with valid solutions:
    count how many columns that are different and then return the most efficient(smaller) one

    only have to count how many "columns" instead of "steps"

    time complexity: O(S * N)
      - compare S solutions with N columns for each solution
    space complexity: O(1)
      - only uses a few variables for comparison
    """
    fewest_moves = 8  # start with the worst case, then keep the smaller one
    for sol in SOLUTIONS:
        diff = 0
        for i in range(8):
            if positions[i] != sol[i]:
                diff += 1
        fewest_moves = min(fewest_moves, diff)  # real fewest moves to return
    return fewest_moves


# ////////////////////////////// test case below //////////////////////////////


def test_task_1():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~ task 1 test ~~~~~~~~~~~~~~~~~~~~~~~~~")

    result1 = check_inclusion("ab", "eidbaooo")
    print("see if 'ab' is in 'eidbaooo':", result1)
    assert result1 is True  # example 1

    result2 = check_inclusion("ab", "eidboaoo")
    print("see if 'ab' is in 'eidboaoo':", result2)
    assert result2 is False  # example 2

    result3 = check_inclusion("a", "a")
    print("see if 'a' is in 'a':", result3)
    assert result3 is True  # min case

    result4 = check_inclusion("abc", "ab")
    print("see if 'abc' is in 'ab':", result4)
    assert result4 is False  # s1 is longer

    result5 = check_inclusion("adc", "dcda")
    print("see if 'adc' is in 'dcda':", result5)
    assert result5 is True  # substring at last


def test_task_2():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~ task 2 test ~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("How many solutions for the 8 queens issue? A:", len(SOLUTIONS))
    assert len(SOLUTIONS) == 92

    ex1 = min_moves([1, 2, 3, 4, 5, 6, 7, 8])
    print("see how many moves from [1, 2, 3, 4, 5, 6, 7, 8]:", ex1)
    assert ex1 == 7  # example 1

    ex2 = min_moves([1, 1, 1, 1, 1, 1, 1, 1])
    print("see how many moves from [1, 1, 1, 1, 1, 1, 1, 1]:", ex2)
    assert ex2 == 7  # example 2

    valid_sol = min_moves([1, 5, 8, 6, 3, 7, 2, 4])
    print("if already valid [1, 5, 8, 6, 3, 7, 2, 4]:", valid_sol)
    assert valid_sol == 0


test_task_1()
test_task_2()
