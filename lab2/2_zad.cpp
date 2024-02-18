#include <iostream>
#include <string.h>
#include <vector>
#include <set>

template <typename Iterator, typename Predicate>
Iterator mymax(Iterator first, Iterator last, Predicate pred) {
    Iterator largest = first;
    for (; ++first != last;) {
        if (pred(*first, *largest))
            largest = first;
    }
    return largest;
}

int gt_int(const int& a, const int& b) {
    if (a > b)
        return 1;
    else
        return 0;
}

int gt_str(const std::string& a, const std::string& b) {
    if (a > b)
        return 1;
    else
        return 0;
}

int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0};
std::string arr_str[] = {
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"
};
std::vector<int> v = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
std::set<int> s = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };

int main(){
    
    const int* maxint = mymax(&arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int);
    std::cout <<*maxint<<"\n";
    const std::string* maxstr = mymax(&arr_str[0], &arr_str[sizeof(arr_str)/sizeof(*arr_str)], gt_str);
    std::cout <<*maxstr<<"\n";
    auto maxvec = mymax(v.begin(), v.end(), gt_int);
    std::cout <<*maxvec<< "\n";
    auto maxset = mymax(s.begin(), s.end(), gt_int);
    std::cout <<*maxset<< "\n";
    return 0;
}

/*
Prednosti:
Prednosti ovog rješenja su da je funkcija mymax generička i može se primijeniti na bilo koji tip iteratora i bilo koju vrstu predikata.
Ovo znači da ne moramo pisati različite funkcije za različite vrste struktura podataka i predikata. Također predlošci imaju manju
vremensku i prostornu složenost(ne mora se pozivati funkcija iz virtualne tablice te ne mora imati pokazivač na virtualnu tablicu).

Nedostaci:
Ovaj predložak moguće je primjeniti samo na strukture podataka koji su definirani pomoću iteratora.
U prethodnom zadatku, ovi se parametri prenosili kao pokazivači na funkcije, što je omogućavalo veću fleksibilnost (nakon prevođenja).
Obično je nešto duži kod kod predložaka.
*/