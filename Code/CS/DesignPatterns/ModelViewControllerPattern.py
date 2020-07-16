# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建模型。
class Student(object):
    rollNo = ""
    name = ""
    def getRollNo(self):
        return self.rollNo

    def setRollNo(self, rollNo: str):
        self.rollNo = rollNo

    def getName(self):
        return self.name

    def setName(self, name: str):
        self.name = name

# 创建视图。
class StudentView(object):
    def printStudentDetails(self, studentName: str, studentRollNo: str):
        print("Student: ")
        print("Name: {}".format(studentName))
        print("Roll No: {}".format(studentRollNo))

# 创建控制器。
class StudentController(object):
    def __init__(self, model: Student, view: StudentView):
        self.model = model
        self.view = view

    def setStudentName(self, name: str):
        self.model.setName(name)

    def getStudentName(self):
        return self.model.getName()

    def setStudentRollNo(self, rollNo: str):
        self.model.setRollNo(rollNo)

    def getStudentRollNo(self):
        self.model.getRollNo()

    def updateView(self):
        self.view.printStudentDetails(self.model.getName(), self.model.getRollNo())

# 使用 StudentController 方法来演示 MVC 设计模式的用法。
if __name__ == '__main__':
    def retrieveStudentFromDatabase():
        student = Student()
        student.setName("Robert")
        student.setRollNo("10")
        return student
    model = retrieveStudentFromDatabase()
    view = StudentView()
    controller = StudentController(model, view)
    controller.updateView()
    controller.setStudentRollNo("1")
    controller.updateView()