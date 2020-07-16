# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个类，在该类上应用标准。
class Person(object):
    def __init__(self, name: str, gender: str, maritalStatus: str):
        self.name = name
        self.gender = gender
        self.maritalStatus = maritalStatus
    def getName(self):
        return self.name.lower()
    def getGender(self):
        return self.gender.lower()
    def getMaritalStatus(self):
        return self.maritalStatus.lower()

# 为标准（Criteria）创建一个接口。
class Criteria(object):
    def meetCriteria(self, persons: list):
        pass

# 创建实现 Criteria 接口的实体类。
class CriteriaMale(Criteria):
    def meetCriteria(self, persons: list):
        malePersons = list()
        for person in persons:
            if person.getGender() == 'male':
                malePersons.append(person)
        return malePersons
class CriteriaFemale(Criteria):
    def meetCriteria(self, persons: list):
        femalePersons = list()
        for person in persons:
            if person.getGender() == 'female':
                femalePersons.append(person)
        return femalePersons
class CriteriaSingle(Criteria):
    def meetCriteria(self, persons: list):
        singlePersons = list()
        for person in persons:
            if person.getMaritalStatus() == 'single':
                singlePersons.append(person)
        return singlePersons
class AndCriteria(Criteria):
    def __init__(self, criteria: Criteria, otherCriteria: Criteria):
        self.criteria = criteria
        self.otherCriteria = otherCriteria
    def meetCriteria(self, persons: list):
        firstCriteriaPersons = self.criteria.meetCriteria(persons)
        return self.otherCriteria.meetCriteria(firstCriteriaPersons)
class OrCriteria(Criteria):
    def __init__(self, criteria: Criteria, otherCriteria: Criteria):
        self.criteria = criteria
        self.otherCriteria = otherCriteria
    def meetCriteria(self, persons: list):
        firstCriteriaItems = self.criteria.meetCriteria(persons)
        otherCriteriaItems = self.otherCriteria.meetCriteria(persons)
        for person in otherCriteriaItems:
            if person not in firstCriteriaItems:
                firstCriteriaItems.append(person)
        return firstCriteriaItems

def printPersons(persons):
    for person in persons:
        print("Person : [ Name: {}, Gender: {}, Marital Status: {}]".
              format(person.getName(), person.getGender(), person.getMaritalStatus()))

# 使用不同的标准（Criteria）和它们的结合来过滤 Person 对象的列表。
if __name__ == '__main__':
    persons = list()
    persons.append(Person("Robert", "Male", "Single"))
    persons.append(Person("John", "Male", "Married"))
    persons.append(Person("Laura", "Female", "Married"))
    persons.append(Person("Diana", "Female", "Single"))
    persons.append(Person("Mike", "Male", "Single"))
    persons.append(Person("Bobby", "Male", "Single"))

    male = CriteriaMale()
    female = CriteriaFemale()
    single = CriteriaSingle()
    singleMale = AndCriteria(single, male)
    singleOrFemale = OrCriteria(single, female)

    print("Males:")
    printPersons(male.meetCriteria(persons))
    print("Female:")
    printPersons(female.meetCriteria(persons))
    print("Single Males:")
    printPersons(singleMale.meetCriteria(persons))
    print("Single or Females:")
    printPersons(singleOrFemale.meetCriteria(persons))