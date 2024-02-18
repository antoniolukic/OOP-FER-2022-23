#include <stdio.h>
#include <string.h>

const void* mymax(const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *)) {
    const void *current = base;
    for (size_t i = 1; i < nmemb; i++)
        if (compar(base + i * size, current))
            current = base + i * size;
    return current;
}

int gt_int(const void *x, const void *y) {
    int *px = (int*)x;
    int *py = (int*)y;
    if (*px > *py)
        return 1;
    else
        return 0;
}

int gt_char(const void *x, const void *y) {
    char *px = (char*)x;
    char *py = (char*)y;
    if (*px > *py)
        return 1;
    else
        return 0;
}

int gt_str(const void *x, const void *y) {
    const char *px = *(const char**)x;
    const char *py = *(const char**)y;
    if (strcmp(px, py) > 0){
        return 1;}
    else
        return 0;
}

int main() {

    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[]="Suncana strana ulice";
    const char* arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };

    int *max_int = (int*)mymax(&arr_int, sizeof(arr_int) /  sizeof(int), sizeof(int), gt_int);
    printf("%d\n", *max_int);
    char *max_char = (char*)mymax(&arr_char, sizeof(arr_char) /  sizeof(char), sizeof(char), gt_char);
    printf("%c\n", *max_char);
    const char *max_str = *(const char**)(mymax(&arr_str, sizeof(arr_str) / sizeof(const char*), sizeof(const char*), gt_str));
    printf("%s", &max_str[0]);
    return 0;
}