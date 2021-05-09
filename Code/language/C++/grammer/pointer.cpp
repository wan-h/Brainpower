#include<iostream>
using namespace std;

int* add1(int* array, int* num){
    for (int i = 0; i < *num; i++){
        array[i] += 1;
    }
    return array;
}

int main(){
    int num = 5;
    int *pnum;
    int **ppnum;
    pnum = &num;
    ppnum = &pnum;
    int *res;
    int array[**ppnum] = {1, 2, 3, 4, 5};
    cout << "原始数组: " << endl;
    for (int n : array) {
        cout << n << " ";
    }
    cout << endl;
    res = add1(array, &num);
    cout << "加1数组: " << endl;
    for (int i = 0; i < num; i++){
        cout << *(res + i) << " ";
    }
    cout << endl;
    return 0;
}