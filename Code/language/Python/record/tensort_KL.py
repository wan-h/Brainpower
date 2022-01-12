# coding: utf-8
# Author: wanhui0729@gmail.com

import numpy as np

# 将P分2048个bin中
def get_distribution(P):
    pmax = max(P)
    distribution = np.zeros(2048)
    interval = 2048 / pmax
    for i in P:
        index = int(np.abs(i * interval))
        if index >= 2048:
            index = 2047
        distribution[index] += 1
    return distribution

# 计算P Q两个分布的KL散度
def compute_kl_divergence(P, Q):
    KL = 0.0
    assert len(P) == len(Q)
    for i in range(len(P)):
        # 防止计算时分母为0
        if Q[i] == 0:
            KL += 1
        else:
            # KL散度计算
            KL += P[i] * np.log(P[i] / Q[i])
    return KL

def threshold_distribution(distribution, target_bin=128):
    length = len(distribution)
    target_threshold = target_bin
    min_kl_divergence = np.inf

    for threshold in range(target_bin, length):
        reference_distribution = distribution[:threshold].copy()
        reference_distribution[threshold - 1] = np.sum(distribution[threshold:])

        # 将reference_distribution量化为128个bins的分布为quantized_distribution
        num_per_bin = threshold / target_bin
        quantized_distribution = np.zeros(target_bin)
        for i in range(128):
            start = i * num_per_bin
            end = (i + 1) * num_per_bin

            # 将distribution映射到quantized_distribution
            # threshold个bins -> 128 bins
            left_upper = int(np.ceil(start))
            if left_upper > start:
                left_scale = left_upper - start
                quantized_distribution[i] += left_scale * distribution[left_upper - 1]

            right_lower = int(np.floor(end))
            if right_lower < end:
                right_scale = end - right_lower
                quantized_distribution[i] += right_scale * distribution[right_lower]

            quantized_distribution[i] += np.sum(distribution[left_upper: right_lower])

        # 因为要和reference_distribution计算KL散度
        # 所以需要将quantized_distribution扩展到和reference_distribution一样个数的bins即expand_distribution
        expand_distribution = np.zeros_like(reference_distribution)
        for i in range(128):
            start = i * num_per_bin
            end = (i + 1) * num_per_bin
            count = 0
            # count是为了做归一化，量化后的一个bin可能是之前几个bins的数据
            left_upper = int(np.ceil(start))
            left_scale = 0
            if left_upper > start:
                left_scale = left_upper - start
                if reference_distribution[left_upper] != 0:
                    count += left_scale

            right_lower = int(np.floor(end))
            right_scale = 0
            if right_lower < end:
                right_scale = end - right_lower
                if reference_distribution[right_lower] != 0:
                    count += right_scale

            for j in range(left_upper, right_lower):
                if reference_distribution[j] != 0:
                    count += 1

            # 归一化后当前bin的数据
            expand_value = quantized_distribution[i] / count

            # 按照比例映射到expand_distribution中
            if left_upper > start:
                if reference_distribution[left_upper - 1] != 0:
                    expand_distribution[left_upper - 1] += expand_value * left_scale
            if right_lower < end:
                if reference_distribution[right_lower] != 0:
                    expand_distribution[right_lower] += expand_value * right_scale
            for j in range(left_upper, right_lower):
                if reference_distribution[j] != 0:
                    expand_distribution[j] += expand_value

        kl_divergence = compute_kl_divergence(reference_distribution, expand_distribution)

        if kl_divergence < min_kl_divergence:
            min_kl_divergence = kl_divergence
            target_threshold = threshold
    return target_threshold

if __name__ == '__main__':
    # 模拟一个卷积参数分布
    p = np.random.standard_normal(96*3*11*11)
    # 把P分到2048个bin中
    distribution = get_distribution(p)

    target_threshold = threshold_distribution(distribution, 128)
    print(target_threshold)
    # 本例中的阈值就是
    threshold = (target_threshold + 0.5) * (max(p) / 2048)
    print(p)
    print(threshold)