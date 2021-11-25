#ifndef STUDENT_H
#define STUDENT_H

#include <QString>
class Student
{
public:
    QString getName() const;
    void setName(const QString &value);

    QString getSex() const;
    void setSex(const QString &value);

    QString getAge() const;
    void setAge(const QString &value);

    QString getChinese_score() const;
    void setChinese_score(const QString &value);

    QString getMath_score() const;
    void setMath_score(const QString &value);

    QString getEnglish_score() const;
    void setEnglish_score(const QString &value);

    QString getID() const;

    void setID(const QString &value);

private:
    QString ID;
    QString name;
    QString sex;
    QString age;
    QString chinese_score;
    QString math_score;
    QString english_score;
};



#endif // STUDENT_H
