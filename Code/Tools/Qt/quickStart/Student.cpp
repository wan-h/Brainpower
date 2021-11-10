#include "Student.h"

QString Student::getName() const
{
    return name;
}

void Student::setName(const QString &value)
{
    name = value;
}

QString Student::getSex() const
{
    return sex;
}

void Student::setSex(const QString &value)
{
    sex = value;
}

QString Student::getAge() const
{
    return age;
}

void Student::setAge(const QString &value)
{
    age = value;
}

QString Student::getChinese_score() const
{
    return chinese_score;
}

void Student::setChinese_score(const QString &value)
{
    chinese_score = value;
}

QString Student::getMath_score() const
{
    return math_score;
}

void Student::setMath_score(const QString &value)
{
    math_score = value;
}

QString Student::getEnglish_score() const
{
    return english_score;
}

void Student::setEnglish_score(const QString &value)
{
    english_score = value;
}

QString Student::getID() const
{
    return ID;
}

void Student::setID(const QString &value)
{
    ID = value;
}

