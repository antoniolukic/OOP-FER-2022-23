class PlainOldClass{
public:
    void set(int x){x_=x;};
    int get(){return x_;};
private:
      int x_;
};
class Base{
public:
    //if in doubt, google "pure virtual"
    virtual void set(int x)=0;
    virtual int get()=0;
};
class CoolClass: public Base{
public:
    virtual void set(int x){x_=x;};
    virtual int get(){return x_;};
private:
    int x_;
};
int main(){
    PlainOldClass poc;
    Base* pb=new CoolClass;
    poc.set(42);
    pb->set(42);
}
/*
    1. Alokacije memorija za objekt poc se odvija na način:
        push    rbp
        mov     rbp, rsp
        push    rbx
        sub     rsp, 24
        - vidimo da se registar rsp smanjio za 24 kako bi se alociralo memorije na stogu za lokalne varijable
       Alokacija memororije za objeckt *pc se odvija redom:
        mov     edi, 16
        call    operator new(unsigned long)
        mov     rbx, rax
        mov     rdi, rbx
        call    CoolClass::CoolClass() [complete object constructor]
        mov     QWORD PTR [rbp-24], rbx
        - stavlja se u edi registar vrijednost 16 koji će se koristiti kao argument operatora new
        - pozovi operator new koji alocira memoriju na heapu
        - u rbx registar vrati vrijednost operatora new odnosto pokazivač na alociranu memoriju
        - u rdi stavi rbx odnosno to će se koristiti kao arguement konstruktora CoolClass klase
        - pozovi CoolClass klasu kako bi se stovrio novi objekt
        - stavi vrijednost rbx na mjesto [rpb-24] gjde je pointer na novo stovreni objekt
    2. Alociranje za poc varijablu se događa na stogu dok se alociranje za pb varijablu događa dinamički na gomili.
    3. Poziv konstruktora objekta poc ne postoji.
    4. Poziv konstruktora se događa ovako:
        mov     rdi, rbx
        call    CoolClass::CoolClass() [complete object constructor]
        mov     QWORD PTR [rbp-24], rbx
        - u rdi stavi rbx odnosno to će se koristiti kao arguement konstruktora CoolClass klase
        - pozovi CoolClass klasu kako bi se stovrio novi objekt
        - stavi vrijednost rbx na mjesto [rpb-24] gjde je pointer na novo stovreni objekt

    CoolClass::CoolClass() [base object constructor]:
        push    rbp               ; spremi bazni pointer na stog
        mov     rbp, rsp          ; stavi banzi pointer na trenutni pokazivač na stogu
        sub     rsp, 16           ; alociraj 16 bajtova memorije na stogu
        mov     QWORD PTR [rbp-8], rdi    ; pohrani prvi argument na memoriju [rbp-8]
        mov     rax, QWORD PTR [rbp-8]    ; učitaj this pokazivač u rax
        mov     rdi, rax          ; stavi prvi argument za Base konstruktor this pokazivač
        call    Base::Base() [base object constructor]  ; pozovi bazni konstruktor
        mov     edx, OFFSET FLAT:vtable for CoolClass+16  ; učitaj adresu virtualne tablice za CoolClass i stavi u edx
        mov     rax, QWORD PTR [rbp-8]    ; učitaj this pointer into rax
        mov     QWORD PTR [rax], rdx      ; pohrani adresu virtualne tablice za CoolClass u memoriju objekta
        nop                         ; no operation
        leave                       ; otputsti sa stoga
        ret                         ; vrati se iz funkcije
    5.
        lea     rax, [rbp-28]               mov     rax, QWORD PTR [rbp-24]
        mov     esi, 42                     mov     rax, QWORD PTR [rax]
        mov     rdi, rax                    mov     rdx, QWORD PTR [rax] 
        call    PlainOldClass::set(int)     mov     rax, QWORD PTR [rbp-24]
                                            mov     esi, 42
                                            mov     rdi, rax
                                            call    rdx

    -  poc.set(42)                          pb->set(42)
    Vidimo kako kod poc.set(42) naredbe prvo adresa memorijske lokacije rbp-28 ubacuje u rax(koristen za povratne vrijednosti funkcije).
    U esi registar(izvorište vrijednosti) se ubacuje broj 42. U rdi(registar za 1. argument funkcije) se posprema rax te se zove set funkcija
    klase PlainOldClass.
    Mozemo vidjeti kako kod pb->set(42) se događa nešto više naredbi. Prvo se mora u registar rax pospremiti pointer na objekt tipa CoolClaas
    dok se u rdx posprema lokacija odredišta za prvi parametar. Nakon tih naredbi se ponavljaju naredbe iz poc.set(42) no na kraju se poziva
    rdx odnosno članska funkcija CoolClass kako bi se postavila vrijednost.
    6.
    Naredba  mov     edx, OFFSET FLAT:vtable for CoolClass+16 stavlja u registar edx adresu virtualne tablice CoolClass koja izgleda:
    vtable for CoolClass:
        .quad   0
        .quad   typeinfo for CoolClass
        .quad   CoolClass::set(int)
        .quad   CoolClass::get()
*/