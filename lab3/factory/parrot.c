#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

typedef struct Parrot {
    //pointer na tablicu pokazivača
    PTRFUN* vtable;
    //pointer na ime ljubimca
    char const* name;
} Parrot;

char const* name(void* this){
  return ((struct Parrot*)this)->name;
}

char const* greet(void){
    return "pozdrav od papige!";
}

char const* menu(void){
    return "sjeme";
}

PTRFUN functionTableParrot[] = { name, greet, menu };

int size() {
    return sizeof(Parrot);
}

void construct(struct Parrot* this, char const* name) {
    this->name = name;
    this->vtable = &functionTableParrot[0];
}

void* create(char const* name) {
    struct Parrot* ptr = malloc(sizeof(struct Parrot));
    construct(ptr, name);
    return ptr;
}