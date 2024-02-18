#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

typedef struct Tiger {
    //pointer na tablicu pokazivača
    PTRFUN* vtable;
    //pointer na ime ljubimca
    char const* name;
} Tiger;

char const* name(void* this){
  return ((struct Tiger*)this)->name;
}

char const* greet(void){
    return "roarrr!";
}

char const* menu(void){
    return "sirovo meso";
}

PTRFUN functionTableTiger[] = { name, greet, menu };

int size() {
    return sizeof(Tiger);
}

void construct(struct Tiger* this, char const* name) {
    this->name = name;
    this->vtable = &functionTableTiger[0];
}

void* create(char const* name) {
    struct Tiger* ptr = malloc(sizeof(struct Tiger));
    construct(ptr, name);
    return ptr;
}