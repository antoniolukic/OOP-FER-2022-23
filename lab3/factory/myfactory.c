#include <stdio.h>
#include <windows.h>

typedef struct Animal*(__stdcall *PTRFUN1)();

void* myfactory(char const* libname, char const* ctorarg) {

    HINSTANCE hGetProcIDDLL = LoadLibrary(libname);

    if (!hGetProcIDDLL) {
        printf("could not load the dynamic library\n");
        return NULL;
    }

    PTRFUN1 function = (PTRFUN1)GetProcAddress(hGetProcIDDLL, "create");
    if (!function) {
        printf("could not locate the function\n");
        return NULL;
    }
    
    return function(ctorarg);
}