#include <stdio.h>
#include <stdlib.h>

class B{
public:
    virtual int __cdecl prva()=0;
    virtual int __cdecl druga(int)=0;
};

class D: public B{
public:
    virtual int __cdecl prva(){return 42;}
    virtual int __cdecl druga(int x){return prva()+x;}
};

typedef int (*PTRFUN1)(void*);
typedef int (*PTRFUN2)(void*, int);

void ispis (B* var){
    void** vptr =  *(void***)var;
    PTRFUN1 fun1 = (PTRFUN1)vptr[0];
    PTRFUN2 fun2 = (PTRFUN2)vptr[1];
    printf("Prva:%d\n", fun1(var));
    printf("Druga:%d\n", fun2(var, 10));
}

int main() {
    B *pb = new D();
    ispis(pb);

    return 0;
}