#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

char const* dogGreet(void){
    return "vau!";
}
char const* dogMenu(void){
    return "kuhanu govedinu";
}
char const* catGreet(void){
    return "mijau!";
}
char const* catMenu(void){
    return "konzerviranu tunjevinu";
}

PTRFUN functionTableDog[] = { dogGreet, dogMenu };
PTRFUN functionTableCat[] = { catGreet, catMenu };

struct Animal {
    //pointer na ime ljubimca
    char const* name;
    //pointer na tablicu pokazivača
    PTRFUN* vtable;
};

void constructDog(struct Animal* mem, char const* name) {
    mem->name = name;
    mem->vtable = &functionTableDog[0];
}

void constructCat(struct Animal* mem, char const* name) {
    mem->name = name;
    mem->vtable = &functionTableCat[0];
}

struct Animal* createDog(char const* name) {
    struct Animal* ptr = (struct Animal*) malloc(sizeof(struct Animal));
    constructDog(ptr, name);
    return ptr;
}

struct Animal* createCat(char const* name) {
    struct Animal* ptr = (struct Animal*) malloc(sizeof(struct Animal));
    constructCat(ptr, name);
    return ptr;
}

void animalPrintGreeting(struct Animal* animal) {
    printf("%s pozdravlja: %s\n", animal->name, animal->vtable[0]());
}

void animalPrintMenu(struct Animal* animal) {
    printf("%s voli %s\n", animal->name, animal->vtable[1]());
}

void testAnimals(void){
  struct Animal* p1=createDog("Hamlet");
  struct Animal* p2=createCat("Ofelija");
  struct Animal* p3=createDog("Polonije");

  animalPrintGreeting(p1);
  animalPrintGreeting(p2);
  animalPrintGreeting(p3);

  animalPrintMenu(p1);
  animalPrintMenu(p2);
  animalPrintMenu(p3);

  free(p1); free(p2); free(p3);
}

void saonice(int n) {
    struct Animal* ptr = (struct Animal*) malloc(n * sizeof(struct Animal));
    struct Animal* pamti = ptr;
    char ime[] = "pas";
    for (int i = 0; i < n; i++) {
        constructDog(ptr, ime);
        animalPrintGreeting(ptr);
        ptr += sizeof(struct Animal);
    }
    free(pamti);
}

int main() {
    //stvaranje na gomili
    testAnimals();
    //stvaranje na stogu
    struct Animal pas;
    pas.name = "pero";
    pas.vtable = functionTableDog;
    printf("\n"); animalPrintGreeting(&pas); animalPrintMenu(&pas); printf("\n");
    saonice(3);
    return 0;
}