"""
Array Rotation Exercise

Description:
-------------
This program rotates an array of integers to the right by k positions.
Rotation means shifting each element forward, with items that "fall off"
the end wrapping back to the beginning.
"""

def rotate_arr(arr, k):
    """
    Rotate an array to the right by k positions.
    Example:
      arr = [1, 2, 3, 4, 5], k = 2
      result = [4, 5, 1, 2, 3]
    """
    n = len(arr)                  # length of the array
    index = n - (k % n)           # find the rotation cut point using modulo
    return arr[index:] + arr[:index]  # rotated array: tail part + head part


# --- Main program ---

# Read number of test cases (t)
t = int(input("Enter number of test cases: "))

# Loop until all test cases are processed
while t != 0:
    # Read number of rotations (k)
    k = int(input("Enter number of rotations: "))

    # Read the array, converting input string into a list of integers
    arr = list(map(int, input("Enter values in the array and separate them using a space: ").split()))

    # Call rotation function and print result
    print(rotate_arr(arr, k))
    print("")   # print a blank line for readability

    # Decrease test case count
    t -= 1


