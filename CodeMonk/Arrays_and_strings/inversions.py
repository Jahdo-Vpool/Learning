"""
Problem Description:
--------------------
Monk's best friend, Micro, gave him an integer matrix M of size N x N.
Monk recently learned about array inversions (counting pairs (i, j) where
arr[i] > arr[j] and i < j). Micro challenged him to extend this concept
to 2D matrices.

Definition:
-----------
An inversion in the matrix is defined as the number of unordered pairs of
cells (i, j), (p, q) such that:
    - i <= p (row index condition)
    - j <= q (column index condition)
    - M[i][j] > M[p][q]

That means for each element, we only compare it with elements to the
right and/or below (including diagonals), never to the left or above.

Task:
-----
For each test case, count and print the total number of inversions
in the given N x N matrix.
"""

# Read number of test cases
t = int(input())

while t:
    # Read the dimension of the matrix (N x N)
    n = int(input())

    # Read the matrix as a list of lists
    # Each row is read, split into integers, and appended
    arr = [list(map(int, input().split())) for ij in range(n)]

    # Variable to store the inversion count
    count = 0

    # Loop over every cell (i, j) in the matrix
    for i in range(n):
        for j in range(n):

            # For each (i, j), loop over all cells (p, q)
            # such that p >= i and q >= j
            for p in range(i, n):
                for q in range(j, n):

                    # Skip comparing the cell with itself (i,j) == (p,q)
                    if p == i and q == j:
                        continue

                    # If inversion condition holds, increment counter
                    if arr[i][j] > arr[p][q]:
                        count += 1

    # Print the total inversion count for this test case
    print(count)

    # Move on to the next test case
    t -= 1
