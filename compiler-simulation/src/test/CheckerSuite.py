import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):    
    def test_entry1(self):
        input = """main1: function void() {}"""
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 1))

    def test_entry2(self):
        input = """main: function integer() {
            return 0;
        }"""
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 2))

    def test_entry3(self):
        input = """main: function void(a: integer) {}"""
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 3))

    def test_entry4(self):
        input = """main: function void(a: integer, b: integer) {}
            main2: function boolean() {
                return true;
            }
            A: float = 5;
            main1: function void() {
                A: integer = 5;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 4))

    def test_entry5(self):
        input = """main: function auto() {}"""
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 5))
    
    def test_redeclared1(self):
        input = """
            A: integer = 5;
            A: boolean = 5;
            main: function void() {}
        """
        expect = """Redeclared Variable: A"""
        self.assertTrue(TestChecker.test(input, expect, 6))

    def test_redeclared2(self):
        input = """
            A: integer = 5;
            main: function void(a: integer, b: float, c: boolean) {}
            main: function void() {}
        """
        expect = """Redeclared Function: main"""
        self.assertTrue(TestChecker.test(input, expect, 7))

    def test_mismatchExpression1(self):
        input = """
            main: function void() {
                a: integer = 1 + "float";
            }
        """
        expect = """Type mismatch in expression: BinExpr(+, IntegerLit(1), StringLit(float))"""
        self.assertTrue(TestChecker.test(input, expect, 8))

    def test_mismatchExpression2(self):
        input = """
            main: function void() {
                a: integer = "int" :: "float";
            }
        """
        expect = """Type mismatch in Variable Declaration: VarDecl(a, IntegerType, BinExpr(::, StringLit(int), StringLit(float)))"""
        self.assertTrue(TestChecker.test(input, expect, 9))

    def test_mismatchExpression3(self):
        input = """
            main: function void() {
                a: integer = 5;
                b: boolean = 7;
                c: integer = (a == 4) == b;
            }
        """
        expect = """Type mismatch in Variable Declaration: VarDecl(b, BooleanType, IntegerLit(7))"""
        self.assertTrue(TestChecker.test(input, expect, 10))

    def test_mismatchExpression4(self):
        input = """
            main: function void() {
                a: integer = 5;
                b: boolean = 5;
                c: float = !b + (a == 5);
            }
        """
        expect = """Type mismatch in Variable Declaration: VarDecl(b, BooleanType, IntegerLit(5))"""
        self.assertTrue(TestChecker.test(input, expect, 11))

    def test_mismatchExpression5(self):
        input = """
            main: function void() {
                a: float;
                b: integer;
                c: string;
                d: boolean;
                e: integer = !(((-a + b) < (7 % 5)) == true);
            }
        """
        expect = """Type mismatch in Variable Declaration: VarDecl(e, IntegerType, UnExpr(!, BinExpr(==, BinExpr(<, BinExpr(+, UnExpr(-, Id(a)), Id(b)), BinExpr(%, IntegerLit(7), IntegerLit(5))), BooleanLit(True))))"""
        self.assertTrue(TestChecker.test(input, expect, 12))

    def test_mismatchExpression6(self):
        input = """
            f1: function void() {
                a: string = "int" :: "float";
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 13))

    def test_declaration(self):
        input = """
            A: integer = 5;
            B: boolean = true || false;
            C: string = "abc" :: "def";
            D: float = 5.0 + A;
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 14))

    def test_redeclared3(self):
        input = """
            A: integer = 5;
            main1: function void(a: integer, b: float, c: boolean) {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 15))

    def test_mismatchExpression7(self):
        input = """
            f1: function void() {
                a: integer = 2 * 3 + 8 % 5 - 7 / 7;
                b: boolean = (2 == 3) && !(true) || (3 != 8);
                c: float = 2 * 3.5 + 8 % 5 - 7 / 7;
                d: string = ("abc" :: "def") :: "xyz";
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 16))

    def test_mismatchExpression8(self):
        input = """
            main: function void() {
                a: integer = 2 * 3 + 8 % 5 - 7 / 7;
                b: boolean = (2 == 3) && !(true) || (3 != 8);
                c: float = 2 * 3.5 + 8 % 5.5 - 7 / 7;
                d: string = ("abc" :: "def") :: "xyz";
            }
        """
        expect = """Type mismatch in expression: BinExpr(%, IntegerLit(8), FloatLit(5.5))"""
        self.assertTrue(TestChecker.test(input, expect, 17))


    def test_mismatchExpression9(self):
        input = """
            foo: function integer() {
                return 2;
            }
            foo2: function integer() {
                return 3;
            }
            f1: function void() {
                a: integer = foo() + foo2();
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 18))

    def test_undeclared9(self):
        input = """
            b: integer = 5;
            c: integer = 6;
            a: integer = b + c;

            foo: function integer(a: string) {
                return 0;
            }

            main: function void() {
                a: integer = 7;
                {
                    a: boolean = b == c;
                    {
                        a: float = 1.0 + b;
                        {
                            a: string = "abc";
                            {
                                d: integer = foo(a);
                            }
                        }
                    }
                }
                a: boolean;
            }
        """
        expect = """Redeclared Variable: a"""
        self.assertTrue(TestChecker.test(input, expect, 19))

    def test_undeclared8(self):
        input = """
            b: integer = 5;
            c: integer = 6;
            a: integer = b + c;

            foo: function void(a: integer) {
            
            }

            main: function void() {
                a: integer = 7;
                {
                    a: boolean = b == c;
                    {
                        a: float = 1.0 + b;
                        {
                            a: string = "abc";
                            {
                                d: integer = foo(a);
                            }
                        }
                    }
                }
            }
        """
        expect = """Type mismatch in expression: FuncCall(foo, [Id(a)])"""
        self.assertTrue(TestChecker.test(input, expect, 20))

    def test_undeclared7(self):
        input = """
            b: integer = 5;
            c: integer = 6;
            a: integer = b + c;

            f1: function void() {
                a: integer = 7;
                {
                    a: boolean = b == c;
                    {
                        a: float = 1.0 + b;
                        {
                            a: string = "abc";
                            {
                                printString(a);
                            }
                            a = "x";
                        }
                        a = 1.0;
                    }
                    a = true;
                }
                a = 5;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 21))


    def test_undeclared6(self):
        input = """
            b: integer = 5;
            c: integer = 6;
            a: integer = b + c;

            f1: function void() {
                a: float = b - c;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 22))

    def test_undeclared5(self):
        input = """
            b: integer;
            foo: function void(c: float) {
                a: float = b + c;
            }
            f1: function void() {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 23))

    def test_undeclared4(self):
        input = """
            b: integer;
            foo: function void() {
                c: integer = 5;
            }
            main: function void() {
                a: integer = b + c;
            }
        """
        expect = """Undeclared Identifier: c"""
        self.assertTrue(TestChecker.test(input, expect, 24))

    def test_undeclared3(self):
        input = """
            b: integer;
            f1: function void() {
                c: integer;
                a: integer = b + c;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 25))

    def test_undeclared2(self):
        input = """
            b: integer;
            c: integer;
            f1: function void() {
                a: integer = b + c;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 26))

    def test_undeclared1(self):
        input = """
            main: function void() {
                a: integer = b + c;
            }
        """
        expect = """Undeclared Identifier: b"""
        self.assertTrue(TestChecker.test(input, expect, 27))


    def test_arraylit1(self):
        input = """
            a : array[2] of integer = {1, 2};
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 28))

    def test_arraylit2(self):
        input = """
            a : array[2, 2] of integer = {{1, 2}, {3, 4}};
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 29))

    def test_arraylit3(self):
        input = """
            a : array[1] of integer = {1, "c"};
            main: function void() {}
        """
        expect = """Illegal array literal: ArrayLit([IntegerLit(1), StringLit(c)])"""
        self.assertTrue(TestChecker.test(input, expect, 30))

    def test_arraylit4(self):
        input = """
            a : array[1] of integer = {1, 2};
            main: function void() {}
        """
        expect = """Type mismatch in Variable Declaration: VarDecl(a, ArrayType([1], IntegerType), ArrayLit([IntegerLit(1), IntegerLit(2)]))"""
        self.assertTrue(TestChecker.test(input, expect, 31))

    def test_arraylit5(self):
        input = """
            a : array[2, 2] of integer = {{1, 2}, {"c", "d"}};
            main: function void() {}
        """
        expect = """Illegal array literal: ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([StringLit(c), StringLit(d)])])"""
        self.assertTrue(TestChecker.test(input, expect, 32))

    def test_arraylit9(self):
        input = """
            a : array[2, 2, 2] of integer = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8.0}}};
            main: function void() {}
        """
        expect = """Illegal array literal: ArrayLit([ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(4)])]), ArrayLit([ArrayLit([IntegerLit(5), IntegerLit(6)]), ArrayLit([IntegerLit(7), FloatLit(8.0)])])])"""
        self.assertTrue(TestChecker.test(input, expect, 33))

    def test_arraylit10(self):
        input = """
            a : array[2, 2, 2] of integer = {{{1,2}, {3, 4}}, {{5.0, 6.1}, {7.8, 9.9}}};
            main: function void() {}
        """
        expect = """Illegal array literal: ArrayLit([ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(4)])]), ArrayLit([ArrayLit([FloatLit(5.0), FloatLit(6.1)]), ArrayLit([FloatLit(7.8), FloatLit(9.9)])])])"""
        self.assertTrue(TestChecker.test(input, expect, 34))

    def test_arraylit6(self):
        input = """
            a : array[2, 2] of integer = {{1, 2}, {3, 4, 5}};
            main: function void() {}
        """
        expect = """Illegal array literal: ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(4), IntegerLit(5)])])"""
        self.assertTrue(TestChecker.test(input, expect, 35))

    def test_arraylit7(self):
        input = """
            a : array[2, 2] of integer = {{1, "c"}, {3, "a", "d"}};
            main: function void() {}
        """
        expect = """Illegal array literal: ArrayLit([ArrayLit([IntegerLit(1), StringLit(c)]), ArrayLit([IntegerLit(3), StringLit(a), StringLit(d)])])"""
        self.assertTrue(TestChecker.test(input, expect, 36))

    def test_arraylit8(self):
        input = """
            a : array[2] of boolean = {1, 2};
            main: function void() {}
        """
        expect = """Type mismatch in Variable Declaration: VarDecl(a, ArrayType([2], BooleanType), ArrayLit([IntegerLit(1), IntegerLit(2)]))"""
        self.assertTrue(TestChecker.test(input, expect, 37))

    def test_param1(self):
        input = """
            a : array[2] of integer = {1, 2};
            func: function auto(e: integer, b: float, c: string, d: boolean) {
                f: integer = 5;
                g: boolean = true;
                return f;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 38))

    def test_conversion1(self):
        input = """
            a: float = 1;
            b: auto = a + 2;
            c: integer = 2.3;
            main: function void() {}
        """
        expect = """Type mismatch in Variable Declaration: VarDecl(c, IntegerType, FloatLit(2.3))"""
        self.assertTrue(TestChecker.test(input, expect, 39))

    def testCaThangTu(self):
        input = """
            foo: function integer(a: integer) {
                return a;
            }
            a, b, c: integer = 3 + 0, a + 1, foo(5);
            f1: function void() {
                printInteger(a + b + c);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 40))

    def test_super1(self):
        input = """
            main: function void() {}
            foo: function integer(a: integer, b: boolean) {
                return a;
            }
            goo: function integer() inherit foo {
                super();
            }
        """
        expect = """Type mismatch in expression: """
        self.assertTrue(TestChecker.test(input, expect, 41))

    def test_super2(self):
        input = """
            foo: function integer(a: integer, b: boolean) {
                return a;
            }
            goo: function integer() inherit foo {
                super(1, true);
                return 3;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 42))

    def test_super3(self):
        input = """
            main: function void() {}
            foo: function integer(a: integer, b: boolean) {
                return a;
            }
            goo: function integer() inherit foo {
                super(1, 2);
            }
        """
        expect = """Type mismatch in expression: IntegerLit(2)"""
        self.assertTrue(TestChecker.test(input, expect, 43))

    def test_super4(self):
        input = """
            foo: function integer(a: integer, b: float) {
                return a;
            }
            goo: function integer() inherit foo {
                super(1, 2);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 44))

    def test_preventDefault1(self):
        input = """
            foo: function integer(a: integer, b: boolean) {
                return a;
            }
            goo: function integer() inherit foo {
                preventDefault();
                return 2;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 45))

    def test_preventDefault2(self):
        input = """
            main: function void() {}
            foo: function integer(a: integer, b: boolean) {
                return a;
            }
            goo: function integer() inherit foo {
                preventDefault(1, 2);
            }
        """
        expect = """Type mismatch in expression: IntegerLit(1)"""
        self.assertTrue(TestChecker.test(input, expect, 46))

    def test_preventDefault3(self):
        input = """
            foo: function integer() {
                return 123;
            }
            goo: function integer() inherit foo {
                super();
                return 2;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 47))

    def test_super5(self):
        input = """
            main: function void() {}
            foo: function integer(a: integer) {
                return 123;
            }
            goo: function integer() inherit foo {
                super(1);
                super(2);
            }
        """
        expect = """Type mismatch in statement: CallStmt(super, IntegerLit(2))"""
        self.assertTrue(TestChecker.test(input, expect, 48))

    def test_if1(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                if(1 == 2) a = a + 1;
                else {
                    return a;
                }
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 49))

    def test_if2(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                if(1 == 2) return a;
                else {
                    return a;
                }
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 50))

    def test_if3(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                if(1 == 2) {
                    a: string = "abc";
                }
                else {
                    a: integer = 6;
                }
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 51))

    def test_if4(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                if(1 == 2) {
                    a: string = "abc";
                    b: integer;
                    return b;
                }
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 52))

    def test_for1(self):
        input = """
            main: function void() {}
            foo: function integer() {
                a: integer = 5;
                for(a = 5, a < 10, a + 1) {
                    a: string = "abc";
                    return a;
                }
            }
        """
        expect = """Type mismatch in statement: ReturnStmt(Id(a))"""
        self.assertTrue(TestChecker.test(input, expect, 53))

    def test_for2(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                for(a = 5, a < 10, a + 1) {
                    a: string = "abc";
                    b: integer = 4;
                    return b;
                }
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 54))

    def test_while1(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                while (a < 10) {
                    a: string = "abc";
                }
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 55))

    def test_while2(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                while (a < 10) {      
                    if(a == 8) {
                        return 0;
                    }
                }
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 56))

    def test_while3(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                while (a < 10) {      
                    if(a == 8) {
                        return a;
                    }
                    else {
                        b: integer = a + 1;
                        return b - 1;
                    }
                }
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 57))

    def test_while4(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                while (a < 10) {      
                    b: auto = 5;
                    for(b = 10, b < 100, b + 2) 
                        return a;
                }
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 58))

    def test_dowhile1(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                do {
                    a: string = "abc";
                } while(a < 10);
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 59))
    
    def test_dowhile2(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                do {      
                    if(a == 8) {
                        return 0;
                    }
                } while(a < 10);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 60))

    def test_dowhile3(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                do {      
                    if(a == 8) {
                        return a;
                    }
                    else {
                        b: integer = a + 1;
                        return b - 1;
                    }
                } while (a < 10);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 61))

    def test_dowhile4(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                do {      
                    b: auto = 5;
                    for(b = 10, b < 100, b + 2) 
                        return a;
                } while (a < 10);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 62))

    def test_break_continue1(self):
        input = """
            main: function void() {}
            foo: function integer() {
                a: integer = 10;
                if(a == 10) {
                    continue;
                    return a;
                }
                else {
                    return a;
                }
            }
        """
        expect = """Must in loop: ContinueStmt()"""
        self.assertTrue(TestChecker.test(input, expect, 63))

    def test_break_continue2(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                for(a = 5, a < 10, a + 1) {
                    continue;
                    a = a + 1;
                }
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 64))

    def test_break_continue3(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                for(a = 5, a < 10, a + 1) {
                    a = a + 1;
                    if(a > 7) {
                        continue;
                    }
                    break;
                }
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 65))

    def test_break_continue4(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                while (a < 10) {
                    continue;
                    a = a + 1;
                    break;
                }
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 66))

    def test_break_continue5(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                while (a < 10) {
                    a = a + 1;
                    if(a > 7) {
                        continue;
                    }
                    break;
                }
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 67))

    def test_break_continue6(self):
        input = """
            foo: function integer() {
                a: integer = 5;
                do {
                    continue;
                    a = a + 1;
                    break;
                } while (a < 10);
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 68))

    def test_declare_later1(self):
        input = """
            foo: function integer() {
                a: integer = foo2() + foo3(5);
                return a;
            }
            foo2: function integer() {
                return 1;
            }
            foo3: function integer(a: integer) {
                return a - 1;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 69))

    def test_declare_later2(self):
        input = """
            foo2: function integer() {
                return foo();
            }
            foo: function integer() {
                a: integer = foo2() + foo3(5);
                return a;
            }
            foo3: function integer(a: integer) {
                return a - 1;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 70))

    def test_invalid_param1(self):
        input = """
            main: function void() {}
            foo: function void(inherit a: integer) {}
            foo2: function void(b: integer, b: float) inherit foo {
                super(b);
            }
        """
        expect = """Redeclared Parameter: b"""
        self.assertTrue(TestChecker.test(input, expect, 71))

    def test_invalid_param2(self):
        input = """
            main: function void() {}
            foo: function void(inherit a: integer) {}
            foo2: function void(a: integer, b: float) inherit foo {
                super(a);
            }
        """
        expect = """Invalid Parameter: a"""
        self.assertTrue(TestChecker.test(input, expect, 72))

    def test_invalid_param3(self):
        input = """
            foo: function void(inherit a: float) {}
            foo2: function void(b: integer) inherit foo {
                super(b);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 73))

    def test_invalid_param4(self):
        input = """
            foo: function void(inherit a: integer) {}
            foo2: function void(inherit b: string) inherit foo {
                super(1);
            }
            foo3: function void(a: string) inherit foo2 {
                preventDefault();
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 74))
    
    def test_array1(self):
        input = """
            main: function void() {}
            foo: function float(a: integer) {
                b: array [2, 3] of float = {{1.0, 2.0, 2.5}, {7.1, 9.3, 10.2}};
                return b[0,0] + b[1];
            }
        """
        expect = """Type mismatch in expression: BinExpr(+, ArrayCell(b, [IntegerLit(0), IntegerLit(0)]), ArrayCell(b, [IntegerLit(1)]))"""
        self.assertTrue(TestChecker.test(input, expect, 75))

    def test_array2(self):
        input = """
            main: function void() {}
            foo: function array [3] of float (a: integer) {
                b: array [3, 2] of float = {{1.0, 2.0}, {4.8, 5.7}, {7.1, 9.3}};
                return b[0];
            }
        """
        expect = """Type mismatch in statement: ReturnStmt(ArrayCell(b, [IntegerLit(0)]))"""
        self.assertTrue(TestChecker.test(input, expect, 76))

    def test_array3(self):
        input = """
            foo: function array [2] of float (a: integer) {
                b: array [3, 2] of float = {{1.0, 2.0}, {4.8, 5.7}, {7.1, 9.3}};
                return b[0];
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 77))

    def test_array4(self):
        input = """
            foo: function void () {
                a: array[0] of string;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 78))

    def test_autoVar(self):
        input = """
            foo: function array [3] of string () {
                a: auto = {"a", "b", "c"};
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 79))

    def test_typeInfer1(self):
        input = """
            foo: function array [3] of string () {
                a: auto = {"a", "b", "c"};
                b: array [3] of string = a;
                c: array [2,3] of string = {a, b};
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 80))

    def test_typeInfer2(self):
        input = """
            foo: function array [3] of string () {
                a: auto = {"a", "b", "c"};
                b: auto = a;
                c: auto = {a, b};
                d: auto = {c, {a, a}};
                e: array [2,2,3] of string = d;
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 81))

    def test_typeInfer3(self):
        input = """
            foo: function array [3] of string () {
                a: auto = {"a", "b", "c"};
                b: auto = a;
                c: auto = {a, b};
                d: auto = {c, {a, a}};
                e: array [2,2,3] of string = d;
                f: array [2,3] of string = e[2];
                return a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 82))

    def test_typeInfer4(self):
        input = """            
            foo: function auto () {
                a: auto = {f1(), "string"};
                b: array [2] of string = a;
                c: string = f1();
            }

            f1: function auto () {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 83))

    def test_typeInfer5(self):
        input = """
            f1: function string () {
                return "abc";
            }
            f3: function auto() {
                return "Yoon Jae";
            }
            
            foo: function auto () {
                a: auto = {f1(), "string"};
                b: array [2] of string = a;
                c: array [6] of string = { f1(), f2(), f3(), f4(), f5(), f6()};
            }
            f4: function auto() {}
            f2: function string() {
                return "Park Ji Bin the SK";
            }
            f5: function auto() {
                return "Blind 2022";
            }
            f6: function auto() {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 84))

    def test_typeInfer6(self):
        input = """
            f1: function string () {
                return "abc";
            }
            f3: function auto() {
                return "Yoon Jae";
            }
            
            foo: function auto () {
                a: auto = {f1(), "string"};
                b: array [2] of string = a;
                c: auto = { f1(), f2(), f3(), f4(), f5(), f6()};
                d: array [6] of string = c;
            }
            f4: function auto() {}
            f2: function string() {
                return "Park Ji Bin the SK";
            }
            f5: function auto() {
                return "Blind 2022";
            }
            f6: function auto() {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 85))

    def test_typeInfer7(self):
        input = """
            f1: function string () {
                return "abc";
            }
            f3: function auto() {
                return "Yoon Jae";
            }
            foo: function auto () {
                a: auto = {f1(), "string"};
                b: array [2] of string = a;
                c: auto = ((f1() :: f2()) :: (f3() :: f4())) :: (f5() :: f6());
                d: string = c;
            }
            f4: function auto() {}
            f2: function string() {
                return "Park Ji Bin the SK";
            }
            f5: function auto() {
                return "Blind 2022";
            }
            f6: function auto() {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 86))

    def test_typeInfer8(self):
        input = """            
            foo: function auto (a: auto) {
                b: integer = a;
                c: integer = f4();
                d: integer = a % f4();
            }

            f4: function auto() {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 87))

    def test_typeInfer9(self):
        input = """
            foo: function auto (a: auto) {
                b: integer;
                b = a;
                c: integer;
                c = f4();
                d: integer;
                d = a % f4();
            }
            f4: function auto() {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 88))

    def test_typeInfer10(self):
        input = """
            f4: function auto() {}
            foo: function integer (a: auto) {
                return a;
                b: integer = a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 89))

    def test_typeInfer0(self):
        input = """
            f4: function auto() {}
            foo: function auto (a: auto) {
                return 1;
                return a;
                b: integer = a;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 90))

    def test_typeInferRecursion(self):
        input = """
            main: function void() {}
            f4: function void (a: auto, b: auto) {}
            foo: function integer (x: auto) {
                f4(1.0, "a");
                f4(2, "a");
                f4(x, "b");
                f4("c", "d");
            }
        """
        expect = """Type mismatch in statement: CallStmt(f4, StringLit(c), StringLit(d))"""
        self.assertTrue(TestChecker.test(input, expect, 91))

    def test_typeInferRecursion2(self):
        input = """
            main: function void() {}
            f4: function void (a: auto, b: auto) {}
            foo: function string (x: auto) {
                c: integer;
                foo(c);
                return x;
            }
        """
        expect = """Type mismatch in statement: ReturnStmt(Id(x))"""
        self.assertTrue(TestChecker.test(input, expect, 92))

    def test_typeInferRecursion3(self):
        input = """
            foo: function boolean (x: auto) {
                c: boolean;
                c = (foo(c) && foo(x)) || f4(c, "a");
                return f4(x, f1());
            }
            f4: function auto (a: auto, b: auto) {}
            f1: function string() {}
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 93))

    def test_typeInferRecursion4(self):
        input = """
            main: function void() {}
            foo: function auto(a: auto, b: auto) {
                if (b || b) {
                    return a :: "abc";
                }
                return 1;
            }
        """
        expect = """Type mismatch in statement: ReturnStmt(IntegerLit(1))"""
        self.assertTrue(TestChecker.test(input, expect, 94))

    def test_typeInferRecursion5(self):
        input = """
            foo: function auto(a: auto, b: auto) {
                if (b || b) {
                    return a && b;
                }
                else {
                    c: boolean;
                    return b && c;
                }
                return a && b;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 95))

    def test_all1(self):
        input = """
            f1: function void() {
                return;
            }
            f2: function integer(inherit a: auto) {
                return a + 1;
            }
            f3: function string(inherit b: string) inherit f2 {
                preventDefault();
                return b :: "abc";
            }
            f4: function auto(x: auto, y: auto) inherit f3 {
                super(x);
                y = 1;
                return 1;
            }
            f9: function array [2] of integer(x: auto, y: auto) inherit f7 {
                super(x);
                y = 1;
                return {y, f2(y)};
            }
            foo: function auto(arg: auto) {
                a: auto = {f2(1), f6(2)};
                b: array [2] of integer = a;

                e: auto = f8("a", 1);
                c: auto = f6(1) + e[0,0];
                d: integer = c;

                if (d == 5) {
                    return 1;
                }
                else {
                    return f6(5);
                }
                return f2(d);
            }
            f5: function float() {
                return 0;
            }
            f6: function auto (inherit a: auto) {
                return a + 1;
            }
            f7: function auto (inherit b: string) inherit f6 {
                preventDefault();
                return {b, "abc"};
            }
            f8: function array [1, 2] of integer(x: auto, y: auto) inherit f7 {
                super(x);
                y = 1;
                return {{y, y}};
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 96))

    def test_all2(self):
        input = """
            main: function void() {}
            a: integer;
            f1: function string(a: auto) {
                a = 1;
                {
                    a: float;
                    {
                        a: string;
                        {
                            return a;
                        }
                    }
                }
                return a;
            }
        """
        expect = """Type mismatch in statement: ReturnStmt(Id(a))"""
        self.assertTrue(TestChecker.test(input, expect, 97))

    def test_all3(self):
        input = """
            f1: function void() {
                a: integer = readInteger();
                printBoolean(isPrime(a));
                return;
            }
            isPrime: function boolean(n: integer) {
                if (n <= 2) {
                    return false;
                }
                i: integer = 2;
                for (i = 2, i * i < n, i + 1) {
                    if (n % i == 0) {
                        return false;
                    }
                }
                return true;
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 98))

    def test_all4(self):
        input = """
            gcd1: function auto(x: auto, y: auto) {
                if ((x == 0) || (y == 0)) return x + y;
                if (x > y) return gcd(y, x % y);
                if (x < y) return gcd(x, y % x);
            }
            f1: function void() {
                a: integer = readInteger();
                b: auto = readInteger();
                printInteger(gcd1(a, b));
                printInteger(gcd(a, b));
            }
            gcd: function auto(x: auto, y: auto) {
                if ((x == 0) || (y == 0)) return x + y;
                if (x > y) return gcd1(y, x % y);
                if (x < y) return gcd1(x, y % x);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 99))

    def test_all5(self):
        input = """
            f3: function void() {}
            f1: function auto(a: auto, b: auto) {
                f2(1, "abc");
            }
            f2: function auto(a: auto, b: auto) {
                f1(a, b);
            }
        """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 100))