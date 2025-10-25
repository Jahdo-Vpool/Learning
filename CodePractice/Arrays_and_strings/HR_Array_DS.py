"""
Problem Description:
--------------------
An array is a data structure that stores elements of the same type in a contiguous
block of memory. In an array A of size N, each memory location has a unique index i
(where 0 ≤ i < N), which can be referenced as A[i].

Your task is to reverse an array of integers.

Example:
--------
A = [1, 2, 3]
Return [3, 2, 1]

Function Description:
---------------------
Complete the function 'reverseArray' with the following parameter(s):
    int A[n]: the array to reverse

Returns:
    int[n]: the reversed array

Input Format:
-------------
The first line contains an integer, N, the number of integers in A.
The second line contains N space-separated integers that make up A.

Constraints:
------------
1 ≤ N ≤ 10^3
1 ≤ A[i] ≤ 10^4, where A[i] is the i-th integer in
"""

# Function: reverseArray
# ---------------------------------------------
def reverseArray(a):
    N = len(a)
    r = []
    for i in range(N):
        r.append(a[N - 1 - i])  # Append elements in reverse order
    return r

# Example usage
a = [1, 2, 3, 4]
print(reverseArray(a))  # Output: [4, 3, 2, 1]