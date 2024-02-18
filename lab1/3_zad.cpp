#include <stdio.h>
#include <stdlib.h>

class CoolClass{
public:
    virtual void set(int x){x_=x;};
    virtual int get(){return x_;};
private:
    int x_;
};
class PlainOldClass{
public:
    void set(int x){x_=x;};
    int get(){return x_;};
private:
    int x_;
};

int main() {

    printf("%d\n", sizeof(PlainOldClass));
    printf("%d", sizeof(CoolClass));

/*
    Pri ispisu dobivamo da je velicina PlainOldClass 4 bajta dok je veličina CoolClass 8 bajtova. PlainOldClass se sastoji
    od jedne članske varijable tipa int koji svojom veličinom iznosi 4 bajta. Nevirtualne funkcije ne utječu na veličinu klase.
    CoolClass se također sastoji od jedne članske varijable tipa int koji iznosi 4 bajta, no pošto ima i virtualne funkcije
    ta klasa sadrži i pokazivač na virtualnu tablicu funkcija koji iznosi 4 bajta. Dodavanjem drugih virtualnih funkcija ne
    povećavamo veličinu klase. Čini se da se ovo vrti na 32-bitnom sustavu?
    Da je na 64-bitnom onda bi bilo 4 bajta za PlainOldClass i 16 bajta za CoolClass(8 vtrptr, 4 int, 4 padding).
*/

    return 0;
}