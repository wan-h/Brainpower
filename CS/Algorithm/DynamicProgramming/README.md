## Dynamic Programming (DP)
[code](https://github.com/wan-h/BrainpowerCode/blob/master/AlgorithmCode/README.md)  

---
### OVERVIEW  
动态规划(dynamic programming)是运筹学的一个分支，是求解决策过程(decision process)最优化的数学方法。
在解决多阶段决策过程(multistep decision process)的优化问题时，把多阶段过程转化为一系列单阶段问题逐个求解的
方法叫做动态规划。  
动态规划的基本步骤：  
* 确定问题的决策对象  
* 对决策过程划分阶段  
* 对各阶段确定状态变量  
* 根据状态变量确定费用函数和目标函数  
* 建立各阶段状态变量的转移过程，确定状态转移方程  

在代码实现上，主要找到其转换方程并通过递归的方式自顶向下或则自底向上来不断求解子问题。
