# coding: utf-8
# Author: wanhui0729@gmail.com

def quickSort(arr: list) -> list:
    '''
    快速排序，时间复杂度O(nlogn)
    Arguments:
        arr: 需要排序的列表
    Return: 排好顺序的列表
    '''
    # 基线条件
    if len(arr) < 2:
        return arr
    # 递归条件
    else:
        pivot = arr[0]
        lelf = [item for item in arr[1:] if item <= pivot]
        right = [item for item in arr[1:] if item > pivot]
        return quickSort(lelf) + [pivot] + quickSort(right)

if __name__ == '__main__':
    arr = [1, 3, 5, 6, 4, 2]
    assert quickSort(arr.copy()) == [1, 2, 3, 4, 5, 6]