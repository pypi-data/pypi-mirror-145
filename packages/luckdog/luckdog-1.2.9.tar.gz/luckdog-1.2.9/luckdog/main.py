# -*- coding: utf-8 -*-

from test.suite import println,test

@test()
def add(a,b,expected=2):
    c = a + b 
    return c == expected

add(1,1,expected=2)  
add(1,"-1",expected=0)   
add(1,3,expected=4)  
