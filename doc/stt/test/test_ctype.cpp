#include <iostream>

#include <iostream>
#include <cstring>
#include <string>


class Foo{
    public:
        void bar(){
            std::cout << "Hello c'est moi la chose !!" << std::endl;
        }

        char* retrun_data(){
            const char* data = "Toto c'est moi";
            char* result = new char[strlen(data) + 1];
            strcpy(result, data);
            return result;
        }
        char* hello()
        { 
            std::string res = "toto";
            char hello[] = "Hello ";
            char excla[] = "!\n";
            char *greeting = (char*)malloc ( sizeof(char) * ( strlen("toto") + strlen(hello) + strlen(excla) + 1 ) );
            if( greeting == NULL) exit(1);
            strcpy( greeting , hello);
            strcat(greeting, "toto");
            strcat(greeting, excla);
            return (char*)res.c_str();
        }

};

extern "C" {
    Foo* Foo_new(){ return new Foo(); }
    void Foo_bar(Foo* foo){ foo->bar(); }
    char* Foo_retrun_data(Foo* foo) {return foo->retrun_data();}
    char* hello_func(Foo* foo) {printf("%s",foo->hello()) ;return foo->hello();}
}
