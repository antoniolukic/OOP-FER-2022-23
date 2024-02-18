#include <iostream>
#include <assert.h>
#include <stdlib.h>
#include <list>

class Point{
public:
    int x;
    int y;
};

class Shape{
public:
    virtual void draw()=0;
    virtual void move(int x_pom, int y_pom)=0;
};
class Circle : public Shape {
public:
    double radius_;
    Point center_;
    virtual void draw() {
        std::cerr <<"in drawCircle\n";
    }
    virtual void move(int x_pom, int y_pom) {
        center_.x += x_pom;
        center_.y += y_pom;
    }
};
class Square : public Shape {
public:
    double side_;
    Point center_;
    virtual void draw() {
        std::cerr <<"in drawSquare\n";
    }
    virtual void move(int x_pom, int y_pom) {
        center_.x += x_pom;
        center_.y += y_pom;
    }
};
class Rhomb : public Shape {
public:
    double side_;
    Point center_;
    virtual void draw() {
        std::cerr <<"in drawRhomb\n";
    }
    virtual void move(int x_pom, int y_pom) {
        center_.x += x_pom;
        center_.y += y_pom;
    }
};

void drawShapes(const std::list<Shape *> &fig) {
    std::list <Shape *>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++it) {
        (*it)->draw();
    }
}

void moveShapes(const std::list<Shape *> &fig, int x_pom, int y_pom) {
    std::list <Shape *>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++it) {
        (*it)->move(x_pom, y_pom);
    }
}

int main() {

    std::list<Shape *> shapes;
    Circle *c = new Circle;
    c->center_.x = 0;
    c->center_.y = 0;
    Square *s = new Square;
    s->center_.x = 1;
    s->center_.y = 1;
    Rhomb *r = new Rhomb;
    r->center_.x = 2;
    r->center_.y = 2;
    shapes.push_back(c);
    shapes.push_back(s);
    shapes.push_back(r);

    drawShapes(shapes);

    moveShapes(shapes, 2, 3);

    std::cout <<c->center_.x<<" "<<c->center_.y<<std::endl<<s->center_.x<<" "<<s->center_.y<<std::endl<<r->center_.x<<" "<<r->center_.y;

    return 0;
}