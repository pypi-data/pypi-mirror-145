"""
QuickSort is a Divide and Conquer algorithm.
It picks an element as pivot and partitions the given arr around the picked pivot.
"""

def partition(arr: list, start: int, end: int) -> int:
     
    # Initializing pivot's index to start
    pivot_index = start
    pivot = arr[pivot_index]
     
    # This loop runs till start pointer crosses
    # end pointer, and when it does we swap the
    # pivot with element on end pointer
    while start < end:
         
        # Increment the start pointer till it finds an
        # element greater than  pivot
        while start < len(arr) and arr[start] <= pivot:
            start += 1
             
        # Decrement the end pointer till it finds an
        # element less than pivot
        while arr[end] > pivot:
            end -= 1
         
        # If start and end have not crossed each other,
        # swap the numbers on start and end
        if(start < end):
            arr[start], arr[end] = arr[end], arr[start]
     
    # Swap pivot element with element on end pointer.
    # This puts pivot on its correct sorted place.
    arr[end], arr[pivot_index] = arr[pivot_index], arr[end]
    
    # Returning end pointer to divide the array into 2
    return end
     

def quickSort(arr: list, start: int, end: int) -> None:
     
    if (start < end):
         
        # p is partitioning index, arr[p]
        # is at right place
        p = partition(arr, start, end)
         
        # Sort elements before partition
        # and after partition
        quickSort(arr, start, p - 1)
        quickSort(arr, p + 1, end)


def quick_sort(arr: list) -> list:
    quickSort(arr, 0, len(arr) - 1)
    return arr