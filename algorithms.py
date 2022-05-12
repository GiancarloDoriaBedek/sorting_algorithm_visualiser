import time


def bubble_sort(L, draw_data, time_delay):
    """
    Best, Worst, Average: O(n^2)
    """
    old_highlight_idx = [] ## Display data ##

    for i in range(len(L) - 1):
        for j in range(len(L) - 1 - i):
            if L[j] > L[j+1]:
                L[j], L[j+1] = L[j+1], L[j]

        ################ Display data ################
                new_highlight_idx = [j, j+1]
                draw_data(old_highlight_idx, new_highlight_idx)
                old_highlight_idx = new_highlight_idx
                time.sleep(time_delay)
        draw_data(old_highlight_idx, [])
        ##############################################


def selection_sort(L, draw_data, time_delay):
    """
    Best, average, worst: O(n^2)
    """
    old_highlight_idx = [] ## Display data ##

    for i in range(len(L)-1):
        min_index = i

        for j in range(i+1, len(L)):
            if L[j] < L[min_index]:
                min_index = j

        ################ Display data ################
            new_highlight_idx = [i, j]
            draw_data(old_highlight_idx, new_highlight_idx)
            old_highlight_idx = new_highlight_idx
            time.sleep(time_delay)
        draw_data(old_highlight_idx, [])
        ##############################################

        L[i], L[min_index] = L[min_index], L[i]


def quicksort(L, draw_data, time_delay, low=0, high=None):
    """
    Inplace implementation of quicksort using lomuto partition scheme.
    Best, Average: O(n*log(n))
    Worst: O(n^2)
    """
    if high is None:
        high = len(L) - 1

    if low < high:
        partition_index = lomuto_partition_scheme(L, draw_data, time_delay, low, high)
        quicksort(L, draw_data, time_delay, low, partition_index -1)
        quicksort(L, draw_data, time_delay, partition_index+1, high)


def lomuto_partition_scheme(L, draw_data, time_delay, low, high):
    """
    Used as a component in quicksort algorithm.\n
    Prepares partition such that all values up to index i are smaller than
    the pivot and all values from i + 1 are greater than the pivot
    """
    i = low - 1
    pivot = L[high]

    old_highlight_idx = [] ## Display data ##

    for j in range(low, high):
        if L[j] <= pivot:
            i += 1
            L[i], L[j] = L[j], L[i]

    ################ Display data ################
            new_highlight_idx = [i, j]
            draw_data(old_highlight_idx, new_highlight_idx)
            old_highlight_idx = new_highlight_idx
            time.sleep(time_delay)
    draw_data(old_highlight_idx, [])
    ##############################################

    L[i+1], L[high] = L[high], L[i+1]
    return i + 1


algorithm_dict = {
    'Bubble Sort': bubble_sort, 
    'Selection Sort': selection_sort, 
    'Quicksort': quicksort
    }