# coding: utf-8
# Author: wanhui0729@gmail.com

def heapSort(nums: list, k: int) -> int:
    '''
    快速排序，时间复杂度O(nlogn)
    Arguments:
        nums: 需要排序的列表
        k: 需要返回的第k大值
    Return:
        第k大值
    '''

    def heapify(a, start, end):
        """ 自上向下堆化
        Args:
            a (list): 输入数组
            start (int): 堆化目标在数组的位置
            end (int): 堆在数组的截止位置
        """
        while True:
            max_pos = start  # 初始化最大值所在位置为目标所在
            if start * 2 + 1 <= end and a[start] < a[start * 2 + 1]:
                # 如果左叶子节点存在，且大于目标值，则将最大值所在位置指向该节点所在位置
                max_pos = start * 2 + 1
            if start * 2 + 2 <= end and a[max_pos] < a[start * 2 + 2]:
                # 如果右叶子节点存在，且大于目标值，则将最大值所在位置指向该节点所在位置
                max_pos = start * 2 + 2
            if max_pos == start:
                # 如果目标即为最大，完成该节点堆化，跳出循环
                break
            # 交换位置，将最大值
            a[start], a[max_pos] = a[max_pos], a[start]
            start = max_pos

    # 建堆,只需要对前半节点堆化
    for i in range(len(nums) // 2 - 1, -1, -1):
        heapify(nums, i, len(nums) - 1)
        # 排序，只需要循环K次，排序TOP K个节点
    i = len(nums) - 1
    while i > len(nums) - 1 - k:
        nums[0], nums[i] = nums[i], nums[0]
        i -= 1
        heapify(nums, 0, i)
    return nums[len(nums) - k]


if __name__ == '__main__':
    arr = [3, 2, 3, 1, 2, 4, 5, 5, 6]
    assert heapSort(arr, 4) == 4