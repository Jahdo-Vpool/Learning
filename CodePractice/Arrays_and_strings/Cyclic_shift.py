"""
Problem Description:
--------------------
You are given a binary string S of length N (characters are only '0' or '1').
A **cyclic right shift by 1** transforms S = s0 s1 ... s_{N-2} s_{N-1} into
S' = s_{N-1} s0 s1 ... s_{N-2}. Repeating this operation N times cycles back
to the original string.

Define P as the **maximum binary value** (treating the string as a binary
integer without leading sign) that can be obtained by performing the cyclic
shift operation any number of times (possibly zero). Equivalently, P is the
lexicographically largest rotation of S.

You repeatedly (infinitely many times) perform a cyclic right shift on S and,
after each shift, record the current binary value. Your task is to determine
the **total number of cyclic shifts performed** when the value of the string
equals P for the K-th time.

Notes:
- The sequence of rotations repeats every N shifts.
- Each occurrence of P happens at some rotation offset r in [0, N-1]. Across
  infinite shifts, these offsets repeat every N steps.

Input Format:
-------------
- The first line contains an integer T, the number of test cases.
For each test case:
- The first line contains two space-separated integers N and K.
- The second line contains the binary string S of length N.

Output Format:
--------------
For each test case, print a single integer:
the total number of cyclic right shifts performed at the moment when the
current rotation of S equals P **for the K-th time**.

Constraints:
------------
- 1 ≤ T ≤ 10^5
- 1 ≤ N ≤ 10^5
- 1 ≤ K ≤ 10^18
- S consists only of '0' and '1'
- The sum of N over all test cases does not exceed 10^6

Definitions / Clarifications:
-----------------------------
- "Cyclic right shift by 1": move the last character of the string to the front.
- "Maximum binary value P": among all N rotations of S, choose the one that is
  lexicographically largest; that rotation’s string is P.
- Shifts are counted starting from the initial S before any shift is applied.
  If S is already equal to P, that counts as the first occurrence at 0 shifts;
  after that, continue shifting and counting occurrences.

Example (illustrative):
-----------------------
S = "1010", N = 4
All rotations (right shifts from start):
0 shifts: "1010"
1 shift : "0101"
2 shifts: "1010"
3 shifts: "0101"
The maximum rotation P = "1010".
Occurrences of P happen at shift counts: 0, 2, 4, 6, ...
For K = 3, answer = 4 (after 4 shifts, it's the 3rd time we see P).
"""

# CYCLIC SHIFT PROBLEM — EXPLAINED VERSION
# ------------------------------------------------------------

# Read the number of test cases (convert from string to int)
t = int(input())

# Repeat the process for each test case
while t > 0:
    # Read N (length of binary string) and K (the K-th occurrence)
    n, k = map(int, input().split())

    # Read the binary string and remove any extra spaces
    s = input().strip()

    # Initialize variables
    max_str = ""  # stores the maximum (lexicographically largest) binary string seen so far
    p = -1  # stores the period (number of shifts before the pattern repeats)
    displacement = 0  # stores how many shifts we made to reach the maximum string the first time

    # ------------------------------------------------------------
    # STEP 1: Try every possible cyclic shift (up to n times)
    # ------------------------------------------------------------
    for i in range(n):
        # If current string 's' is greater (lexicographically) than the max found so far
        if max_str < s:
            max_str = s  # update the new maximum string
            displacement = i  # record the shift count where we found it

        # If we find the same maximum string again,
        # that means we've completed one full repeating pattern
        elif max_str == s:
            p = i - displacement  # difference gives us the repeating period
            break

        # Perform ONE cyclic RIGHT SHIFT:
        # move the last character to the front
        # Example: "1010" -> "0101"
        s = s[-1] + s[:-1]

    # ------------------------------------------------------------
    # STEP 2: Determine the total shifts for the K-th occurrence
    # ------------------------------------------------------------
    # If we never found the same max string again,
    # it means the period is the full length of the string (n)
    if p == -1:
        # displacement = first occurrence
        # (k - 1) * n = how many full rotations until K-th occurrence
        print(displacement + (k - 1) * n)
    else:
        # displacement = first occurrence
        # (k - 1) * p = how many shifts to reach the K-th time based on period
        print(displacement + (k - 1) * p)

    # Move to the next test case
    t -= 1


