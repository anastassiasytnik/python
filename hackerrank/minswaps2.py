#!/bin/python3

# Complete the minimumSwaps function below.

def minimumSwaps(arr):
    """You are given an unordered array consisting of consecutive integers [1, 2, 3, ..., n] without any duplicates. 
       You are allowed to swap any two elements. 
       Find the minimum number of swaps required to sort the array in ascending order.
    """
    pointIdx = 0
    swapCount = 0
    # repeat until all numbers in their places
    while pointIdx < len(arr):
        # 1. Find first number in a wrong spot
        while pointIdx < len(arr) and pointIdx + 1 == arr[pointIdx]:
            pointIdx += 1
        # either end of the array or found the element out of place
        if (len(arr) == pointIdx):
            return swapCount
        pointNum = arr[pointIdx]
        arr[pointIdx] = arr[pointNum - 1]
        arr[pointNum - 1] = pointNum
        swapCount += 1
    return swapCount


if __name__ == '__main__':
    test1 = [7, 1, 3, 2, 4, 5, 6]
    expectedResult1 = 5
    print("Correct?: ", (minimumSwaps(test1) == expectedResult1))

    test2 = [4, 3, 1, 2]
    expectedResult2 = 3
    print("Correct?: ", (minimumSwaps(test2) == expectedResult2))
