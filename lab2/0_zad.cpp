#include <iostream>
#include <assert.h>
#include <stdlib.h>

struct Point{
    int x; int y;
};
struct Shape{
    enum EType {circle, square, rhomb};
    EType type_;
};
struct Circle{
    Shape::EType type_;
    double radius_;
    Point center_;
};
struct Square{
    Shape::EType type_;
    double side_;
    Point center_;
};
struct Rhomb{
    Shape::EType type_;
    double side_;
    Point center_;
};
void drawSquare(struct Square*){
    std::cerr <<"in drawSquare\n";
}
void drawCircle(struct Circle*){
    std::cerr <<"in drawCircle\n";
}
void drawShapes(Shape** shapes, int n){
    for (int i=0; i<n; ++i){
        struct Shape* s = shapes[i];
        switch (s->type_){
        case Shape::square:
            drawSquare((struct Square*)s);
            break;
        case Shape::circle:
            drawCircle((struct Circle*)s);
            break;
        default:
            assert(0); 
            exit(0);
        }
    }
}
void moveShapes(Shape** shapes, int n, int x_pom, int y_pom) {
    for (int i = 0; i < n; i++) {
        struct Shape* s = shapes[i];
        switch (s->type_) {
        case Shape::square:
            ((struct Square*)s)->center_.x += x_pom;
            ((struct Square*)s)->center_.y += y_pom;
            break;
        case Shape::circle:
            ((struct Circle*)s)->center_.x += x_pom;
            ((struct Circle*)s)->center_.y += y_pom;
        }
    }
}
int main(){
    Shape* shapes[5];
    shapes[0]=(Shape*)new Circle;
    shapes[0]->type_=Shape::circle;
    shapes[1]=(Shape*)new Square;
    shapes[1]->type_=Shape::square;
    shapes[2]=(Shape*)new Square;
    shapes[2]->type_=Shape::square;
    shapes[3]=(Shape*)new Circle;
    shapes[3]->type_=Shape::circle;

    drawShapes(shapes, 4);

    //shapes[3]=(Shape*)new Rhomb;
    //shapes[3]->type_=Shape::rhomb;
    //drawShapes(shapes, 5);

    Shape* newShapes[2];
    newShapes[0]=(Shape*)new Square;
    newShapes[0]->type_=Shape::square;
    ((struct Square*)newShapes[0])->center_.x = 0;
    ((struct Square*)newShapes[0])->center_.y = 0;
    newShapes[1]=(Shape*)new Circle;
    newShapes[1]->type_=Shape::circle;
    ((struct Circle*)newShapes[1])->center_.x = 2;
    ((struct Circle*)newShapes[1])->center_.y = 3;

    moveShapes(newShapes, 2, 2, 3);
    std::cout << ((struct Square*)newShapes[0])->center_.x << " " <<  ((struct Square*)newShapes[0])->center_.y<<std::endl;
    std::cout << ((struct Circle*)newShapes[1])->center_.x << " " <<  ((struct Circle*)newShapes[1])->center_.y<<std::endl;
}