#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

typedef double (*PTRFUN)();

typedef struct Unary_Function {
    int lower_bound;
    int upper_bound;
    PTRFUN* vtable;
} Unary_Function;

void tabulate(Unary_Function *f) {
    for(int x = f->lower_bound; x <= f->upper_bound; x++) {
        printf("f(%d)=%lf\n", x, f->vtable[0](f, (double)x));
    }
}

int same_functions_for_ints(Unary_Function *f1, Unary_Function *f2, double tolerance) {
    if(f1->lower_bound != f2->lower_bound) return 0;
    if(f1->upper_bound != f2->upper_bound) return 0;
    for(int x = f1->lower_bound; x <= f1->upper_bound; x++) {
        double delta = f1->vtable[0](f1, x) - f2->vtable[0](f2, x);
        if(delta < 0) delta = -delta;
        if(delta > tolerance) return 0;
    }
    return 1;
}

typedef struct Square {
    Unary_Function base;
} Square;

typedef struct Linear {
    Unary_Function base;
    double a;
    double b;
} Linear;


double square(Unary_Function *f, double x) {
    return x * x;
}

double negative_square(Unary_Function *f, double x) {
    return -square(f, x);
}

double linear(Unary_Function *f, double x) {
    Linear *l = (Linear *)f;
    return l->a * x + l->b;
}

double negative_linear(Unary_Function *f, double x) {
    return -linear(f, x);
}

PTRFUN functiontablesquare[] = {square, negative_square};
PTRFUN functiontablelinear[] = {linear, negative_linear};

Square* create_square(int lb, int ub) {
    Square *f = malloc(sizeof(Square));
    f->base.lower_bound = lb;
    f->base.upper_bound = ub;
    f->base.vtable = &functiontablesquare[0];
    return f;
}

Linear* create_linear(int lb, int ub, double a, double b) {
    Linear *f = malloc(sizeof(Linear));
    f->base.lower_bound = lb;
    f->base.upper_bound = ub;
    f->a = a;
    f->b = b;
    f->base.vtable = &functiontablelinear[0];
    return f;
}

int main() {
    Unary_Function *f1 = (Unary_Function*)create_square(-2, 2);
    tabulate(f1); printf("\n");
    Unary_Function *f2 = (Unary_Function*)create_linear(-2, 2, 5, -2);
    tabulate(f2);
    printf("f1==f2: %s\n", same_functions_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", f2->vtable[1](f2, 1.0));
    free(f1);
    free(f2);
    return 0;
}