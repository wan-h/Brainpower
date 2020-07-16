# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建 Employee 类，该类带有 Employee 对象的列表。
class Employee(object):
    def __init__(self, name: str, dept: str, sal: int):
        self.name = name
        self.dept = dept
        self.salary = sal
        self.subordinates = list()
    def add(self, employee):
        self.subordinates.append(employee)
    def remove(self, employee):
        self.subordinates.remove(employee)
    def getSubordinates(self):
        return self.subordinates
    def __str__(self):
        return "Employee: [Name: {}, dept: {}, salary: {}]".format(self.name, self.dept, self.salary)

# 使用 Employee 类来创建和打印员工的层次结构
if __name__ == '__main__':
    CEO = Employee("Jhon", "CEO", 30000)
    headSales = Employee("Robert", "Head Sales", 20000)
    headMarketing = Employee("Michel", "Head Marketing", 2000)
    clerk1 = Employee("Laura", "Marketing", 10000)
    clerk2 = Employee("Bob", "Marketing", 10000)
    salesExecutive1 = Employee("Richard", "Sales", 10000)
    salesExecutive2 = Employee("Rob", "Sales", 10000)

    CEO.add(headSales)
    CEO.add(headMarketing)

    headSales.add(salesExecutive1)
    headSales.add(salesExecutive2)

    headMarketing.add(clerk1)
    headMarketing.add(clerk2)

    print(CEO)
    for headEmployee in CEO.getSubordinates():
        print(headEmployee)
        for employee in headEmployee.getSubordinates():
            print(employee)