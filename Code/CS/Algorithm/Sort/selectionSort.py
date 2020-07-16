# coding: utf-8
# Author: wanhui0729@gmail.com

def selectionSort(arr: list) -> list:
    '''
    选择排序，时间复杂度O(n^2)
    Arguments:
        arr: 需要排序的列表
    Return: 排好顺序的列表
    '''
    length = len(arr)
    for i in range(length - 1):
        min_i = i
        for j in range(i+1, length):
            if arr[j] < arr[min_i]:
                min_i = j
        arr[i], arr[min_i] = arr[min_i], arr[i]
    return arr

if __name__ == '__main__':
    arr = [1, 3, 5, 6, 4, 2]
    assert selectionSort(arr.copy()) == [1, 2, 3, 4, 5, 6]
