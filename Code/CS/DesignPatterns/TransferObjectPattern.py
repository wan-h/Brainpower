# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建传输对象。
class StudentVO(object):
    def __init__(self, name: str, rollNo: int):
        self.name = name
        self.rollNo = rollNo

    def getName(self):
        return self.name

    def setName(self, name: str):
        self.name = name

    def getRollNo(self):
        return self.rollNo

    def setRollNo(self, rollNo: int):
        self.rollNo = rollNo

# 创建业务对象。
class StudentBO(object):
    def __init__(self):
        self.students = []
        student1 = StudentVO("Robert", 0)
        student2 = StudentVO("John", 1)
        self.students.append(student1)
        self.students.append(student2)
    def deleteStudent(self, student: StudentVO):
        self.students.remove(student)
        print("Student: Roll No {}, deleted from database".format(student.getRollNo()))
    def getAllStudents(self):
        return self.students
    def getStudent(self, rollNo: int):
        return self.students[rollNo]
    def updateStudent(self, student: StudentVO):
        self.students[student.getRollNo()].setName(student.getName())
        print("Student: Roll No: {}, updated in the database".format(student.getRollNo()))

# 使用 StudentBO 来演示传输对象设计模式。
if __name__ == '__main__':
    studentBusinessObject = StudentBO()
    # 输出所有的学生
    for student in studentBusinessObject.getAllStudents():
        print("Student: [RollNo : {}, Name {}]".format(student.getRollNo(), student.getName()))
    # 更新学生
    student = studentBusinessObject.getAllStudents()[0]
    student.setName("Michael")
    studentBusinessObject.updateStudent(student)
    # 获取学生
    student = studentBusinessObject.getStudent(0)
    print("Student: [RollNo : {}, Name {}]".format(student.getRollNo(), student.getName()))