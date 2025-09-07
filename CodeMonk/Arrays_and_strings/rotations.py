"""
Array Rotation Exercise

Description:
-------------
This program rotates an array of integers to the right by k positions.
Rotation means shifting each element forward, with items that "fall off"
the end wrapping back to the beginning.
"""

t = int(input("Enter number of test cases: "))

while t != 0:
    # Read n (size of array) and k (number of rotations)
    n, k = map(int, input().split())

    # Convert input into a list of integers
    arr = list(map(int, input().split()))

    # Compute effective rotation using modulo to avoid unnecessary full rotations
    index = n - (k % n)

    # Print rotated array using slicing (cleaner than two loops)
    rotated = arr[index:] + arr[:index]
    print(*rotated)  # * unpacks list into space-separated values

    t -= 1


