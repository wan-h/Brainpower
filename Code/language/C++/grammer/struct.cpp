#include <iostream>
#include <cstring>

using namespace std;

typedef struct
{
   char  title[50];
   char  author[50];
   char  subject[100];
   int   book_id;
} Books;

void printBook(Books *book);

int main() {
    Books book1;
    Books book2;

    // Book1 详述
    strcpy(book1.title, "Learn C++ Programming");
    strcpy(book1.author, "Chand Miyan");
    strcpy(book1.subject, "C++ Programming");
    book1.book_id = 6495407;

    // Book2 详述
    strcpy(book2.title, "Telecom Billing");
    strcpy(book2.author, "Yakit Singha");
    strcpy(book2.subject, "Telecom");
    book2.book_id = 6495700;

    // 通过传 Book1 的地址来输出 Book1 信息
    printBook(&book1);
    printBook(&book2);

    return 0;
}

// 该函数以结构指针作为参数
void printBook(Books* book) {
    cout << "Book title: " << book->title << endl;
    cout << "Book author: " << book->author << endl;
    cout << "Book subject: " << book->subject << endl;
    cout << "Book id: " << book->book_id << endl;
}
