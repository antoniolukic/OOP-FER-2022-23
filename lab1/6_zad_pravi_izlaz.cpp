#include <stdio.h>

class Base{
public:
    Base() {
        metoda();
    }

    virtual void virtualnaMetoda() {
        printf("ja sam bazna implementacija!\n");
    }

    void metoda() {
        printf("Metoda kaze: ");
        virtualnaMetoda();
    }
};

class Derived: public Base{
public:
    Derived(): Base() {
        metoda();
    }
    virtual void virtualnaMetoda() {
        printf("ja sam izvedena implementacija!\n");
    }
};

int main(){
    Derived* pd=new Derived();
    pd->metoda();
}

/*
derived::derived() -> base::base() -> base::metoda() -> "metoda kaze:" -> rdx odnosno Base::vitualnaMetoda() -> "ja sam bazna implementacija" ->
vratimo se nazad -> base::metoda() -> "metoda kaze:" -> rdx odnosno Derived::virtualnaMetoda() -> "ja sam izvedena implementacija" ->
base::metoda() -> "metoda kaze:" -> rdx odnosno Derived::virtualnaMetoda() -> "ja sam izvedena implementacija"

Pošto derived nasljeđuje konstruktor od base prvo se poziva base::base koji onda poziva method() ali pošto base ima virtualnu metodu poziva se
Base::virualMethod (da tu nije virtual pregazila bi se ova metoda, jer da se ne pregazi bilo bi veoma opasno, konstrukcija objekata
se izvodi from base to derived odnso kada bi se overridalo onda bih se dodjeljivale vrijednosti za ne inicijalizirani objekt odnosno
vjerovatno bi došlo do pada programa i c++ nas želi ovjde zaštititi) ispisuje da je bazna implementacija onda se poziva method od derived odnosno
Base::method pa nakon toga Derived::vitualMethod pa ispisuje da je izvedena implementacija. pd->metoda() zapravo ponavlja zadnji korak.
*/

/*u konstruktoru ako se korisni neka overjadana(virtualna) metoda boli ga briga koristi svoju
prvo base pa onda derived se konstruira
https://isocpp.org/wiki/faq/strange-inheritance#calling-virtuals-from-ctors
*/