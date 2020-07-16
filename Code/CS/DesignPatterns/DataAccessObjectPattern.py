# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建数值对象。
class Student(object):
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

# 创建数据访问对象接口。
class StudentDao(object):
    def getAllStudents(self):
        pass
    def getStudent(self, rollNo: int):
        pass
    def updateStudent(self, student: Student):
        pass
    def deleteStudent(self, student: Student):
        pass

# 创建实现了上述接口的实体类。
class StudentDaoImpl(StudentDao):
    def __init__(self):
        self.students = []
        student1 = Student("Robert", 0)
        student2 = Student("John", 1)
        self.students.append(student1)
        self.students.append(student2)

    def deleteStudent(self, student: Student):
        self.students.remove(student)
        print("Student: Roll No {}, deleted from database".format(student.getRollNo()))

    def getAllStudents(self):
        return self.students

    def getStudent(self, rollNo: int):
        return self.students[rollNo]

    def updateStudent(self, student: Student):
        self.students[student.getRollNo()].setName(student.getName())
        print("Student: Roll No {}, updated in the database".format(student.getRollNo()))

# 使用 StudentDao 来演示数据访问对象模式的用法。
if __name__ == '__main__':
    studentDao = StudentDaoImpl()
    for student in studentDao.getAllStudents():
        print("Student: [RollNo : {}, Name: {}]".format(student.getRollNo(), student.getName()))
    student = studentDao.getAllStudents()[0]
    student.setName("Michael")
    studentDao.updateStudent(student)

    student = studentDao.getStudent(0)
    print("Student: [RollNo : {}, Name: {}]".format(student.getRollNo(), student.getName()))