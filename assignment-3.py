# discuss with GPT: https://chatgpt.com/share/6adffcd6-fb08-83ea-8266-357d845b5c7f
# merge sort: https://ithelp.ithome.com.tw/articles/10384417
# random library simple introduction: https://ithelp.ithome.com.tw/articles/10321407

import random
import time


# -------------------------------- mergesort --------------------------------


def merge_sort(chars):
    """
    divide and conquer, with time complexity O(n log n)
    - from layer, keep divide to hald => log n
    - multiply do `n` things for each layer => n * log n
    """
    # 0 or 1 element is already sorted
    if len(chars) <= 1:
        return chars
    # divide: split in half, sort each half recursively
    mid = len(chars) // 2
    left = merge_sort(chars[:mid])
    right = merge_sort(chars[mid:])
    return _merge(left, right)


def _merge(left, right):
    """
    merge two sorted lists into one sorted list
    """
    out = []
    i = j = 0

    # i point to the left of left data, and j point to the left of right data
    # and also both shouldn't be empty
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1

    # One side ends, append the rest of the other side
    out.extend(left[i:])
    out.extend(right[j:])
    return out


# -------------------------------- quicksort --------------------------------


def quick_sort(chars):
    """
    randomized quicksort, sorts a word of k characters, expected (average) time O(k log k)
    - keep dividing the word in half to layers => log k
    - each layer deals with all k characters => k * log k

    the random pivot makes the O(k^2) worst case very unlikely
    - with a bad pivot, it may not divide in half, so there are k layers instead of log k
    - k layers * k characters = k^2
    > n^2 = n squared / the square of n
    """
    # merge sort will create a new array BUT quick sort will not do this, so we should copy it instead of change it directly
    arr = list(chars)
    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def _quick_sort(arr, lo, hi):
    """
    sort array from low index to high index in place (the same array)
    """
    # 0 or 1 element is already sorted
    if lo >= hi:
        return

    # random pivot: swap a random element to the end, use it as pivot
    r = random.randint(lo, hi)
    arr[r], arr[hi] = arr[hi], arr[r]  # swap
    pivot = arr[hi]

    # move everything smaller than pivot to the left side.
    boundary = lo  # marks the end of the "smaller than pivot" part
    for i in range(lo, hi):
        if arr[i] < pivot:
            # swap the small item into the "smaller than pivot" part
            arr[i], arr[boundary] = arr[boundary], arr[i]
            boundary += 1

    # put the pivot between the small side and the big side
    arr[boundary], arr[hi] = arr[hi], arr[boundary]

    # recurse on both sides (the pivot is already in its final place)
    _quick_sort(arr, lo, boundary - 1)
    _quick_sort(arr, boundary + 1, hi)


# -------------------------------- task --------------------------------


def sortString(s, algo="merge"):
    """
    sort the characters of s by ASCII code

    the 2nd parameter, algo, is either 'merge' or 'quick'
    """
    chars = list(s)
    if algo == "merge":
        result = merge_sort(chars)
    elif algo == "quick":
        result = quick_sort(chars)
    else:
        raise ValueError("algo must be 'merge' or 'quick'")
    return "".join(result)


def groupAnagram(strings, algo="merge"):
    """
    key = sorted characters
    value = words with that key, as an array

    n = number of words
    k = length of the longest word
    - a word with length k keep dividing to half so to layers => log k
    - for each layer this word have `k` characters => k * log k
    - tatally there are `n` words and each do once => n * k log k
    """
    buckets = {}
    for word in strings:
        key = sortString(word, algo)
        # setdefault(key, default): if the key exist then append word directly, otherwise create an array then append word
        buckets.setdefault(key, []).append(word)
    return list(buckets.values())


# ////////////////////////////// test case below //////////////////////////////


def run_tests():
    # sortString
    print("---------------------------------------- sort string")
    for algo in ("merge", "quick"):
        mangoSort = sortString("mango", algo)
        print(f"the word 'mango' sort by {algo}:", mangoSort)
        assert mangoSort == "agmno"

        ogmanSort = sortString("ogman", algo)
        print(f"the word 'ogman' sort by {algo}:", ogmanSort)
        assert ogmanSort == "agmno"

        emptySort = sortString("", algo)
        print(f"the empty word '' sort by {algo}:", emptySort)
        assert emptySort == ""

        oneCharSort = sortString("a", algo)
        print(f"the only character 'a' sort by {algo}:", oneCharSort)
        assert oneCharSort == "a"

        duplicateSort = sortString("aaaa", algo)
        print(f"duplicate characters 'aaaa' sort by {algo}:", duplicateSort)
        assert duplicateSort == "aaaa"

        descendSort = sortString("dcba", algo)
        print(f"descending word 'dcba' sort by {algo}:", descendSort)
        assert descendSort == "abcd"

        upperSort = sortString("Ba", algo)
        print(f"with a upper character 'Ba' sort by {algo}:", upperSort)
        assert upperSort == "Ba"  # 'B'(66) < 'a'(97)

    # groupAnagram: example from the assignment
    data = ["bucket", "rat", "mango", "tango", "ogtan", "tar"]
    expected = [["bucket"], ["rat", "tar"], ["mango"], ["tango", "ogtan"]]
    print("---------------------------------------- group anagram")
    for algo in ("merge", "quick"):
        dataGA = groupAnagram(data, algo)
        print(f"{data} do group anagram by {algo}:", dataGA)
        assert dataGA == expected

        emptyGA = groupAnagram([], algo)
        print(f"empty array do group anagram by {algo}:", emptyGA)
        assert emptyGA == []

        emptyStrGA = groupAnagram([""], algo)
        print(f"{['']} do group anagram by {algo}:", emptyStrGA)
        assert emptyStrGA == [[""]]

        duplicateGA = groupAnagram(["a", "a"], algo)
        print(f"{['a', 'a']} do group anagram by {algo}:", duplicateGA)
        assert duplicateGA == [["a", "a"]]

        allOrderGA = groupAnagram(["abc", "bca", "cab"], algo)
        print(f"{['abc', 'bca', 'cab']} do group anagram by {algo}:", allOrderGA)
        assert allOrderGA == [["abc", "bca", "cab"]]

        partDupliGA = groupAnagram(["ab", "abc"], algo)
        print(f"{['ab', 'abc']} do group anagram by {algo}:", partDupliGA)
        assert partDupliGA == [["ab"], ["abc"]]


def benchmark():
    """
    compare mergesort and quicksort on the same random words
    """
    print("---------------------------------------- benchmark")
    letters = "abcdefghijklmnopqrstuvwxyz"

    for n in (1000, 10000, 50000):
        words = []
        for _ in range(n):
            # make n random words, 5 to 12 letters each
            length = random.randint(5, 12)
            words.append("".join(random.choice(letters) for _ in range(length)))

        # time mergesort for the words
        start = time.perf_counter()
        groupAnagram(words, "merge")
        merge_ms = (time.perf_counter() - start) * 1000

        # time quicksort for the same words
        start = time.perf_counter()
        groupAnagram(words, "quick")
        quick_ms = (time.perf_counter() - start) * 1000

        print(
            f"n = {n} | merge: {round(merge_ms, 2)} ms | quick: {round(quick_ms, 2)} ms"
        )


random.seed(262)
run_tests()
print("groupAnagram example's result:", groupAnagram(["bucket", "rat", "mango", "tango", "ogtan", "tar"]))
benchmark()
