#from ctypes import cdll
import ctypes
lib = ctypes.cdll.LoadLibrary('./libfoo.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()
        lib.hello_func.restype = ctypes.c_char_p # override the default return type (int)

    def bar(self):
        lib.Foo_bar(self.obj)

    def retrun_data(self):
        result = lib.Foo_retrun_data(self.obj)
        print(result)
        data = ctypes.c_char_p(result).value.decode('utf-8')
        return data

    def hello(self):
        result = lib.hello_func(self.obj)
        print(result)


f = Foo()
f.bar() #and you will see "Hello" on the screen
f.hello()
print(f.retrun_data())

# import ctypes
# hello = ctypes.cdll.LoadLibrary('./libfoo.so')
# name = "Frank"
# c_name = ctypes.c_char_p()
# hello.hello_func.restype = ctypes.c_char_p # override the default return type (int)
# foo = hello.hello_func()

# print(foo)
# print (ctypes.c_char_p(foo).value)