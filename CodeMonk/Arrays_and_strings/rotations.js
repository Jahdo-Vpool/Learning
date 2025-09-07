/*

Array Rotation Exercise

Description:
-------------
This program rotates an array of integers to the right by k positions.
Rotation means shifting each element forward, with items that "fall off"
the end wrapping back to the beginning.

*/




// Rotate an array by k positions to the right
const rotateArray = (arr, k) => {
    // Get length of array
    const n = arr.length;

    // Find the index where rotation will "cut" the array
    // Use modulo to avoid unnecessary full rotations (e.g., k = n, 2n, etc.)
    const index = n - (k % n);

    // Slice the array into two parts:
    // 1. From index to end
    // 2. From start to index
    // Then concatenate them to form the rotated array
    return arr.slice(index).concat(arr.slice(0, index));
}

// Example usage
const arr = [1, 2, 3, 4, 5];
const k = 4;

// Rotate and print the result as space-separated values
console.log(rotateArray(arr, k).join(" ")); // Output: 2 3 4 5 1
