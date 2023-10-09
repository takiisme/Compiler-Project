import unittest
from TestUtils import TestAST
from AST import *


class ASTGenSuite(unittest.TestCase):
    def test_201(self):
        input = """x, y, z: integer = false, true, 1;"""
        expect = """Program([\n\tVarDecl(x, IntegerType, BooleanLit(False))\n\tVarDecl(y, IntegerType, BooleanLit(True))\n\tVarDecl(z, IntegerType, IntegerLit(1))\n])"""
        self.assertTrue(TestAST.test(input, expect, 201))

    def test_202(self):
        input = """main: function void() {
            // This is a comment line
        }"""
        expect = """Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"""
        self.assertTrue(TestAST.test(input, expect, 202))

    def test_203(self):
        input = """_x6_yz, a69, XYZ: auto = !5, 7-69, "Hello String \\b" :: "I am another string \\t";"""
        expect = "Program([\n\tVarDecl(_x6_yz, AutoType, UnExpr(!, IntegerLit(5)))\n\tVarDecl(a69, AutoType, BinExpr(-, IntegerLit(7), IntegerLit(69)))\n\tVarDecl(XYZ, AutoType, BinExpr(::, StringLit(Hello String \\b), StringLit(I am another string \\t)))\n])"
        self.assertTrue(TestAST.test(input, expect, 203))

    def test_204(self):
        input = """_123, Yz, Aaa: auto = -5 || "Watch movie please", 5::7, {56 && false, 1, 7};"""
        expect = "Program([\n\tVarDecl(_123, AutoType, BinExpr(||, UnExpr(-, IntegerLit(5)), StringLit(Watch movie please)))\n\tVarDecl(Yz, AutoType, BinExpr(::, IntegerLit(5), IntegerLit(7)))\n\tVarDecl(Aaa, AutoType, ArrayLit([BinExpr(&&, IntegerLit(56), BooleanLit(False)), IntegerLit(1), IntegerLit(7)]))\n])"
        self.assertTrue(TestAST.test(input, expect, 204))

    def test_205(self):
        input = """Tai: array[2] of string = "I love watching films?" == "Hmmmm";"""
        expect = "Program([\n\tVarDecl(Tai, ArrayType([2], StringType), BinExpr(==, StringLit(I love watching films?), StringLit(Hmmmm)))\n])"
        self.assertTrue(TestAST.test(input, expect, 205))

    def test_206(self):
        input = """X_yz, _121, dunno: float = 2, false, "true";"""
        expect = "Program([\n\tVarDecl(X_yz, FloatType, IntegerLit(2))\n\tVarDecl(_121, FloatType, BooleanLit(False))\n\tVarDecl(dunno, FloatType, StringLit(true))\n])"
        self.assertTrue(TestAST.test(input, expect, 206))

    def test_207(self):
        input = """
            /*
                This is a block comment
            */
            X, y, z: boolean;
            """
        expect = "Program([\n\tVarDecl(X, BooleanType)\n\tVarDecl(y, BooleanType)\n\tVarDecl(z, BooleanType)\n])"
        self.assertTrue(TestAST.test(input, expect, 207))

    def test_208(self):
        input = """main: function void() {
            // Line comment
            /*
                Block comment between line comments
            */
            // Line comment
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 208))

    def test_209(self):
        input = """// This is a comment
            X : auto;"""
        expect = "Program([\n\tVarDecl(X, AutoType)\n])"
        self.assertTrue(TestAST.test(input, expect, 209))

    def test_210(self):
        input = """x: array[7, 8] of integer;"""
        expect = "Program([\n\tVarDecl(x, ArrayType([7, 8], IntegerType))\n])"
        self.assertTrue(TestAST.test(input, expect, 210))

    def test_211(self):
        input = """taki: function void() {
            i : integer = 7 + 5;
            for(i = 1 :: 2, i < 5 + 1, i + 1) {
                continue;
            }
            }"""
        expect = "Program([\n\tFuncDecl(taki, VoidType, [], None, BlockStmt([VarDecl(i, IntegerType, BinExpr(+, IntegerLit(7), IntegerLit(5))), ForStmt(AssignStmt(Id(i), BinExpr(::, IntegerLit(1), IntegerLit(2))), BinExpr(<, Id(i), BinExpr(+, IntegerLit(5), IntegerLit(1))), BinExpr(+, Id(i), IntegerLit(1)), BlockStmt([ContinueStmt()]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 211))

    def test_212(self):
        input = """main: function integer() {}"""
        expect = "Program([\n\tFuncDecl(main, IntegerType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 212))

    def test_213(self):
        input = """jowd: function void() {
            if(t - 4 == 0) return false;
            }"""
        expect = "Program([\n\tFuncDecl(jowd, VoidType, [], None, BlockStmt([IfStmt(BinExpr(==, BinExpr(-, Id(t), IntegerLit(4)), IntegerLit(0)), ReturnStmt(BooleanLit(False)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 213))

    def test_214(self):
        input = """main: function void() {
            for(i=1,i<5,i+1){
                a = a+1;
                if(b > f[4]) b = f[4];
            }
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([ForStmt(AssignStmt(Id(i), IntegerLit(1)), BinExpr(<, Id(i), IntegerLit(5)), BinExpr(+, Id(i), IntegerLit(1)), BlockStmt([AssignStmt(Id(a), BinExpr(+, Id(a), IntegerLit(1))), IfStmt(BinExpr(>, Id(b), ArrayCell(f, [IntegerLit(4)])), AssignStmt(Id(b), ArrayCell(f, [IntegerLit(4)])))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 214))

    def test_215(self):
        input = """main: function boolean() {}"""
        expect = "Program([\n\tFuncDecl(main, BooleanType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 215))

    def test_216(self):
        input = """alvis: function boolean() {}"""
        expect = "Program([\n\tFuncDecl(alvis, BooleanType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 216))

    def test_217(self):
        input = """_55, a5: integer;"""
        expect = "Program([\n\tVarDecl(_55, IntegerType)\n\tVarDecl(a5, IntegerType)\n])"
        self.assertTrue(TestAST.test(input, expect, 217))

    def test_218(self):
        input = """demo: function void() {
            if(btl_ppl == 10) dedung();
            else shout("desaitumlum");
            }"""
        expect = "Program([\n\tFuncDecl(demo, VoidType, [], None, BlockStmt([IfStmt(BinExpr(==, Id(btl_ppl), IntegerLit(10)), CallStmt(dedung, ), CallStmt(shout, StringLit(desaitumlum)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 218))

    def test_219(self):
        input = """main: function void() { a = {2, 3_44, 5} == "String"; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), BinExpr(==, ArrayLit([IntegerLit(2), IntegerLit(344), IntegerLit(5)]), StringLit(String)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 219))

    def test_220(self):
        input = """alvis: function integer() {}"""
        expect = "Program([\n\tFuncDecl(alvis, IntegerType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 220))

    def test_221(self):
        input = """main: function auto() { x: boolean = 57; }"""
        expect = "Program([\n\tFuncDecl(main, AutoType, [], None, BlockStmt([VarDecl(x, BooleanType, IntegerLit(57))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 221))

    def test_222(self):
        input = """empty: array[1,2] of boolean;"""
        expect = "Program([\n\tVarDecl(empty, ArrayType([1, 2], BooleanType))\n])"
        self.assertTrue(TestAST.test(input, expect, 222))

    def test_223(self):
        input = """main: function void() {
            if(x || 7) a = 5;
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(||, Id(x), IntegerLit(7)), AssignStmt(Id(a), IntegerLit(5)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 223))

    def test_224(self):
        input = """x: integer = 1234;"""
        expect = "Program([\n\tVarDecl(x, IntegerType, IntegerLit(1234))\n])"
        self.assertTrue(TestAST.test(input, expect, 224))

    def test_225(self):
        input = """jowd: function string() {
            if(true) {
                a[5] = a[1] + 2;
                b[9] = b[5] || false;
            }
        }"""
        expect = "Program([\n\tFuncDecl(jowd, StringType, [], None, BlockStmt([IfStmt(BooleanLit(True), BlockStmt([AssignStmt(ArrayCell(a, [IntegerLit(5)]), BinExpr(+, ArrayCell(a, [IntegerLit(1)]), IntegerLit(2))), AssignStmt(ArrayCell(b, [IntegerLit(9)]), BinExpr(||, ArrayCell(b, [IntegerLit(5)]), BooleanLit(False)))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 225))

    def test_226(self):
        input = """jowd: function integer() {
            if(Xyz == 2)
                if(Yzx == Xyz) jowd();
                else eliminate("PPL");
            else music = false;
        }"""
        expect = "Program([\n\tFuncDecl(jowd, IntegerType, [], None, BlockStmt([IfStmt(BinExpr(==, Id(Xyz), IntegerLit(2)), IfStmt(BinExpr(==, Id(Yzx), Id(Xyz)), CallStmt(jowd, ), CallStmt(eliminate, StringLit(PPL))), AssignStmt(Id(music), BooleanLit(False)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 226))

    def test_227(self):
        input = """main: function void() {
            do {increase();}
            while(i < 2);
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([DoWhileStmt(BinExpr(<, Id(i), IntegerLit(2)), BlockStmt([CallStmt(increase, )]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 227))

    def test_228(self):
        input = """cone: function integer() {}"""
        expect = "Program([\n\tFuncDecl(cone, IntegerType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 228))

    def test_229(self):
        input = """test: boolean = call(2, 3, 4);"""
        expect = "Program([\n\tVarDecl(test, BooleanType, FuncCall(call, [IntegerLit(2), IntegerLit(3), IntegerLit(4)]))\n])"
        self.assertTrue(TestAST.test(input, expect, 229))

    def test_230(self):
        input = """main: function void() {
            for(i=0,i<5,i+1){
                if(i>1){
                    a=a+1;
                    b=true;
                    return a;
                }
                else return b;
            }
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([ForStmt(AssignStmt(Id(i), IntegerLit(0)), BinExpr(<, Id(i), IntegerLit(5)), BinExpr(+, Id(i), IntegerLit(1)), BlockStmt([IfStmt(BinExpr(>, Id(i), IntegerLit(1)), BlockStmt([AssignStmt(Id(a), BinExpr(+, Id(a), IntegerLit(1))), AssignStmt(Id(b), BooleanLit(True)), ReturnStmt(Id(a))]), ReturnStmt(Id(b)))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 230))

    def test_231(self):
        input = """main: function auto() {
            i: integer;
            for(i = 11 * ab, i < 23, i + 1) {
                writeInt(i);
            }
        }"""
        expect = "Program([\n\tFuncDecl(main, AutoType, [], None, BlockStmt([VarDecl(i, IntegerType), ForStmt(AssignStmt(Id(i), BinExpr(*, IntegerLit(11), Id(ab))), BinExpr(<, Id(i), IntegerLit(23)), BinExpr(+, Id(i), IntegerLit(1)), BlockStmt([CallStmt(writeInt, Id(i))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 231))

    def test_232(self):
        input = """main: function void() { a[1] = "A string \\t"; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(ArrayCell(a, [IntegerLit(1)]), StringLit(A string \\t))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 232))

    def test_233(self):
        input = """x, y, z: integer;"""
        expect = "Program([\n\tVarDecl(x, IntegerType)\n\tVarDecl(y, IntegerType)\n\tVarDecl(z, IntegerType)\n])"
        self.assertTrue(TestAST.test(input, expect, 233))

    def test_234(self):
        input = """x: array[1, 2] of boolean;"""
        expect = "Program([\n\tVarDecl(x, ArrayType([1, 2], BooleanType))\n])"
        self.assertTrue(TestAST.test(input, expect, 234))

    def test_235(self):
        input = """main: function void() {
            if(false) {
                x = b + 29.99;
                b = x && true;
            } else {
                _xyz();
            }
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BooleanLit(False), BlockStmt([AssignStmt(Id(x), BinExpr(+, Id(b), FloatLit(29.99))), AssignStmt(Id(b), BinExpr(&&, Id(x), BooleanLit(True)))]), BlockStmt([CallStmt(_xyz, )]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 235))

    def test_236(self):
        input = """main: function float() {
            if(true) a[7] = 2;
            else continue;
        }"""
        expect = "Program([\n\tFuncDecl(main, FloatType, [], None, BlockStmt([IfStmt(BooleanLit(True), AssignStmt(ArrayCell(a, [IntegerLit(7)]), IntegerLit(2)), ContinueStmt())]))\n])"
        self.assertTrue(TestAST.test(input, expect, 236))

    def test_237(self):
        input = """demo: function auto() {
            i: boolean;
            for(i = i == 4, x != i, x / x) {
                Chillies("GiacMoKhac");
                aut = aut + 3;
                if(aut < 3) continue;
            }
        }"""
        expect = "Program([\n\tFuncDecl(demo, AutoType, [], None, BlockStmt([VarDecl(i, BooleanType), ForStmt(AssignStmt(Id(i), BinExpr(==, Id(i), IntegerLit(4))), BinExpr(!=, Id(x), Id(i)), BinExpr(/, Id(x), Id(x)), BlockStmt([CallStmt(Chillies, StringLit(GiacMoKhac)), AssignStmt(Id(aut), BinExpr(+, Id(aut), IntegerLit(3))), IfStmt(BinExpr(<, Id(aut), IntegerLit(3)), ContinueStmt())]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 237))

    def test_238(self):
        input = """main: function void() {
            do {increase();}
            while(i < 2);
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([DoWhileStmt(BinExpr(<, Id(i), IntegerLit(2)), BlockStmt([CallStmt(increase, )]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 238))

    def test_239(self):
        input = """main: function void() { a = {2, 3_44, 5} == "String" + 333; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), BinExpr(==, ArrayLit([IntegerLit(2), IntegerLit(344), IntegerLit(5)]), BinExpr(+, StringLit(String), IntegerLit(333))))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 239))

    def test_240(self):
        input = """jowd: function void() {
            if(a != 2) {a = 5;} else {a = 6;}
            }"""
        expect = "Program([\n\tFuncDecl(jowd, VoidType, [], None, BlockStmt([IfStmt(BinExpr(!=, Id(a), IntegerLit(2)), BlockStmt([AssignStmt(Id(a), IntegerLit(5))]), BlockStmt([AssignStmt(Id(a), IntegerLit(6))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 240))

    def test_241(self):
        input = """main: function void() {
            do {functio();}
            while(i < 2);
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([DoWhileStmt(BinExpr(<, Id(i), IntegerLit(2)), BlockStmt([CallStmt(functio, )]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 241))

    def test_242(self):
        input = """main: function void() { do {a = a - 5;} while(true); }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([DoWhileStmt(BooleanLit(True), BlockStmt([AssignStmt(Id(a), BinExpr(-, Id(a), IntegerLit(5)))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 242))

    def test_243(self):
        input = """jowd: function void() {
            i: integer;
            for(t = 12 && 75, x + y != 7, i / 0) {
                Call("\\t\\t\\t");
                a[75.5] = 7.8 + 0.9;
                break;
            }
        }"""
        expect = "Program([\n\tFuncDecl(jowd, VoidType, [], None, BlockStmt([VarDecl(i, IntegerType), ForStmt(AssignStmt(Id(t), BinExpr(&&, IntegerLit(12), IntegerLit(75))), BinExpr(!=, BinExpr(+, Id(x), Id(y)), IntegerLit(7)), BinExpr(/, Id(i), IntegerLit(0)), BlockStmt([CallStmt(Call, StringLit(\\t\\t\\t)), AssignStmt(ArrayCell(a, [FloatLit(75.5)]), BinExpr(+, FloatLit(7.8), FloatLit(0.9))), BreakStmt()]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 243))

    def test_244(self):
        input = """Xyz, bct, _caA: integer = 20, 13, 74;"""
        expect = "Program([\n\tVarDecl(Xyz, IntegerType, IntegerLit(20))\n\tVarDecl(bct, IntegerType, IntegerLit(13))\n\tVarDecl(_caA, IntegerType, IntegerLit(74))\n])"
        self.assertTrue(TestAST.test(input, expect, 244))

    def test_245(self):
        input = """main: function void() { fact(intege, "999", "2222"); }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([CallStmt(fact, Id(intege), StringLit(999), StringLit(2222))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 245))

    def test_246(self):
        input = """x: integer = 5 :: 70;"""
        expect = "Program([\n\tVarDecl(x, IntegerType, BinExpr(::, IntegerLit(5), IntegerLit(70)))\n])"
        self.assertTrue(TestAST.test(input, expect, 246))

    def test_247(self):
        input = """paper: function boolean(n: integer) {}"""
        expect = "Program([\n\tFuncDecl(paper, BooleanType, [Param(n, IntegerType)], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 247))

    def test_248(self):
        input = """Xyz, bct, _caA: auto = 20, 13, 74;"""
        expect = "Program([\n\tVarDecl(Xyz, AutoType, IntegerLit(20))\n\tVarDecl(bct, AutoType, IntegerLit(13))\n\tVarDecl(_caA, AutoType, IntegerLit(74))\n])"
        self.assertTrue(TestAST.test(input, expect, 248))

    def test_249(self):
        input = """main: function void() { a = a :: 32 < ("34" :: _randomF12()); }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), BinExpr(::, Id(a), BinExpr(<, IntegerLit(32), BinExpr(::, StringLit(34), FuncCall(_randomF12, [])))))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 249))

    def test_250(self):
        input = """jowd: function void(jowd: integer, out jowd: float) inherit jowd {
            i: integer;
            for(i = attackOnTitan("Levi \\b"), i != 3, i / 4) {
                Eren("Roar");
                t = t - 4;
                if(x < 3) break;
            }
        }"""
        expect = "Program([\n\tFuncDecl(jowd, VoidType, [Param(jowd, IntegerType), OutParam(jowd, FloatType)], jowd, BlockStmt([VarDecl(i, IntegerType), ForStmt(AssignStmt(Id(i), FuncCall(attackOnTitan, [StringLit(Levi \\b)])), BinExpr(!=, Id(i), IntegerLit(3)), BinExpr(/, Id(i), IntegerLit(4)), BlockStmt([CallStmt(Eren, StringLit(Roar)), AssignStmt(Id(t), BinExpr(-, Id(t), IntegerLit(4))), IfStmt(BinExpr(<, Id(x), IntegerLit(3)), BreakStmt())]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 250))

    def test_251(self):
        input = """main: function void() { b = "Another random string \\t"; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(b), StringLit(Another random string \\t))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 251))

    def test_252(self):
        input = """kuro: function array[2] of boolean() inherit demo {}"""
        expect = "Program([\n\tFuncDecl(kuro, ArrayType([2], BooleanType), [], demo, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 252))

    def test_253(self):
        input = """X_yz, _121, var: boolean = 2, false, "true";"""
        expect = "Program([\n\tVarDecl(X_yz, BooleanType, IntegerLit(2))\n\tVarDecl(_121, BooleanType, BooleanLit(False))\n\tVarDecl(var, BooleanType, StringLit(true))\n])"
        self.assertTrue(TestAST.test(input, expect, 253))

    def test_254(self):
        input = """// This is a comment X:: void; 
                    x : integer = 3;"""
        expect = "Program([\n\tVarDecl(x, IntegerType, IntegerLit(3))\n])"
        self.assertTrue(TestAST.test(input, expect, 254))

    def test_255(self):
        input = """main: function array [6,9,6,9] of integer() {
            i: integer;
            for(i = i::i, i != i, i / i) {
                i("i");
                i = i + 3;
                if(i < i) break;
            }
        }"""
        expect = "Program([\n\tFuncDecl(main, ArrayType([6, 9, 6, 9], IntegerType), [], None, BlockStmt([VarDecl(i, IntegerType), ForStmt(AssignStmt(Id(i), BinExpr(::, Id(i), Id(i))), BinExpr(!=, Id(i), Id(i)), BinExpr(/, Id(i), Id(i)), BlockStmt([CallStmt(i, StringLit(i)), AssignStmt(Id(i), BinExpr(+, Id(i), IntegerLit(3))), IfStmt(BinExpr(<, Id(i), Id(i)), BreakStmt())]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 255))

    def test_256(self):
        input = """main: function void() { accuracy = "This string contains a tab symbol: \\t"; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(accuracy), StringLit(This string contains a tab symbol: \\t))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 256))

    def test_257(self):
        input = """main: function void() { do {} while(true); }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([DoWhileStmt(BooleanLit(True), BlockStmt([]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 257))

    def test_258(self):
        input = """x, y, z: auto;"""
        expect = "Program([\n\tVarDecl(x, AutoType)\n\tVarDecl(y, AutoType)\n\tVarDecl(z, AutoType)\n])"
        self.assertTrue(TestAST.test(input, expect, 258))

    def test_259(self):
        input = """dsas: function integer() {}"""
        expect = "Program([\n\tFuncDecl(dsas, IntegerType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 259))

    def test_260(self):
        input = """t: function boolean() {}"""
        expect = "Program([\n\tFuncDecl(t, BooleanType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 260))

    def test_261(self):
        input = """main: function void() { a = "A string \\t" * 1_021.E+832 && a_12 != arr[23]; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), BinExpr(!=, BinExpr(&&, BinExpr(*, StringLit(A string \\t), FloatLit(inf)), Id(a_12)), ArrayCell(arr, [IntegerLit(23)])))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 261))

    def test_262(self):
        input = """jowd: function void() { jowd(1, 2, 3); }"""
        expect = "Program([\n\tFuncDecl(jowd, VoidType, [], None, BlockStmt([CallStmt(jowd, IntegerLit(1), IntegerLit(2), IntegerLit(3))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 262))

    def test_263(self):
        input = """main: function void() {
            while(i < 1) increase(i, 1);
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([WhileStmt(BinExpr(<, Id(i), IntegerLit(1)), CallStmt(increase, Id(i), IntegerLit(1)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 263))

    def test_264(self):
        input = """aut: function void(inherit n: boolean) {}"""
        expect = "Program([\n\tFuncDecl(aut, VoidType, [InheritParam(n, BooleanType)], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 264))

    def test_265(self):
        input = """main: function void() { a = a - 3 * 12 || b % 3e2 / "Siuuuuuuu \\b"; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), BinExpr(||, BinExpr(-, Id(a), BinExpr(*, IntegerLit(3), IntegerLit(12))), BinExpr(/, BinExpr(%, Id(b), FloatLit(300.0)), StringLit(Siuuuuuuu \\b))))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 265))

    def test_266(self):
        input = """ltnc: function integer() {}"""
        expect = "Program([\n\tFuncDecl(ltnc, IntegerType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 266))

    def test_267(self):
        input = """joseph: function void() { alice(); }"""
        expect = "Program([\n\tFuncDecl(joseph, VoidType, [], None, BlockStmt([CallStmt(alice, )]))\n])"
        self.assertTrue(TestAST.test(input, expect, 267))

    def test_268(self):
        input = """data: function void() {}"""
        expect = "Program([\n\tFuncDecl(data, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 268))

    def test_269(self):
        input = """main: function void() { 
        a = arr[23 :: "Concat tis \\f" && ("Eeeee lol" :: 34)]; 
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), ArrayCell(arr, [BinExpr(::, IntegerLit(23), BinExpr(&&, StringLit(Concat tis \\f), BinExpr(::, StringLit(Eeeee lol), IntegerLit(34))))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 269))

    def test_270(self):
        input = """main: function void() { lhs = "PPL" * a[5] && -33_9402.21 || {n, h, d}; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(lhs), BinExpr(||, BinExpr(&&, BinExpr(*, StringLit(PPL), ArrayCell(a, [IntegerLit(5)])), UnExpr(-, FloatLit(339402.21))), ArrayLit([Id(n), Id(h), Id(d)])))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 270))

    def test_271(self):
        input = """main: function void() {
            while(true) a = 1 + 5;
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([WhileStmt(BooleanLit(True), AssignStmt(Id(a), BinExpr(+, IntegerLit(1), IntegerLit(5))))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 271))

    def test_272(self):
        input = """x: boolean = 5;"""
        expect = "Program([\n\tVarDecl(x, BooleanType, IntegerLit(5))\n])"
        self.assertTrue(TestAST.test(input, expect, 272))

    def test_273(self):
        input = """main: function void() { a = a[2]; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), ArrayCell(a, [IntegerLit(2)]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 273))

    def test_274(self):
        input = """main: function void() { a = "A random string"; }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(a), StringLit(A random string))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 274))

    def test_275(self):
        input = """demo: function integer() inherit pct {}"""
        expect = "Program([\n\tFuncDecl(demo, IntegerType, [], pct, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 275))

    def test_276(self):
        input = """t: integer = -7 + 0 * 91;
            example: function integer(out test: integer) {}"""
        expect = "Program([\n\tVarDecl(t, IntegerType, BinExpr(+, UnExpr(-, IntegerLit(7)), BinExpr(*, IntegerLit(0), IntegerLit(91))))\n\tFuncDecl(example, IntegerType, [OutParam(test, IntegerType)], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 276))

    def test_277(self):
        input = """Y, z, d: auto = 1 * 2, foo(), 1 % 2;"""
        expect = "Program([\n\tVarDecl(Y, AutoType, BinExpr(*, IntegerLit(1), IntegerLit(2)))\n\tVarDecl(z, AutoType, FuncCall(foo, []))\n\tVarDecl(d, AutoType, BinExpr(%, IntegerLit(1), IntegerLit(2)))\n])"
        self.assertTrue(TestAST.test(input, expect, 277))

    def test_278(self):
        input = """main: function void() {
            while(i > 5) minus(i, 1);
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([WhileStmt(BinExpr(>, Id(i), IntegerLit(5)), CallStmt(minus, Id(i), IntegerLit(1)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 278))

    def test_279(self):
        input = """Tai: array[20] of float = "Float number" :: "is fun";"""
        expect = "Program([\n\tVarDecl(Tai, ArrayType([20], FloatType), BinExpr(::, StringLit(Float number), StringLit(is fun)))\n])"
        self.assertTrue(TestAST.test(input, expect, 279))

    def test_280(self):
        input = """x, y, z: boolean;"""
        expect = "Program([\n\tVarDecl(x, BooleanType)\n\tVarDecl(y, BooleanType)\n\tVarDecl(z, BooleanType)\n])"
        self.assertTrue(TestAST.test(input, expect, 280))

    def test_281(self):
        input = """_Xyz, Ya, z09, t: integer = 5, 6, 7, intege;"""
        expect = "Program([\n\tVarDecl(_Xyz, IntegerType, IntegerLit(5))\n\tVarDecl(Ya, IntegerType, IntegerLit(6))\n\tVarDecl(z09, IntegerType, IntegerLit(7))\n\tVarDecl(t, IntegerType, Id(intege))\n])"
        self.assertTrue(TestAST.test(input, expect, 281))

    def test_282(self):
        input = """a, b, x, y: boolean = 1, 2, 3, 5;"""
        expect = "Program([\n\tVarDecl(a, BooleanType, IntegerLit(1))\n\tVarDecl(b, BooleanType, IntegerLit(2))\n\tVarDecl(x, BooleanType, IntegerLit(3))\n\tVarDecl(y, BooleanType, IntegerLit(5))\n])"
        self.assertTrue(TestAST.test(input, expect, 282))

    def test_283(self):
        input = """main: function void() {
            i : integer = 5;
            while(true) add(i, 1);
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([VarDecl(i, IntegerType, IntegerLit(5)), WhileStmt(BooleanLit(True), CallStmt(add, Id(i), IntegerLit(1)))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 283))

    def test_284(self):
        input = """x: boolean = -5 * 9 + 6;
            example: function integer(out test: auto) {}"""
        expect = "Program([\n\tVarDecl(x, BooleanType, BinExpr(+, BinExpr(*, UnExpr(-, IntegerLit(5)), IntegerLit(9)), IntegerLit(6)))\n\tFuncDecl(example, IntegerType, [OutParam(test, AutoType)], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 284))

    def test_285(self):
        input = """taki: function void() {
            i : integer = 7 + 5;
            for(i = 1 :: 2, i < 5 + 1, i + 1) {
                continue;
            }
            }"""
        expect = "Program([\n\tFuncDecl(taki, VoidType, [], None, BlockStmt([VarDecl(i, IntegerType, BinExpr(+, IntegerLit(7), IntegerLit(5))), ForStmt(AssignStmt(Id(i), BinExpr(::, IntegerLit(1), IntegerLit(2))), BinExpr(<, Id(i), BinExpr(+, IntegerLit(5), IntegerLit(1))), BinExpr(+, Id(i), IntegerLit(1)), BlockStmt([ContinueStmt()]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 285))

    def test_286(self):
        input = """mouse: function void(inherit n: boolean) {}"""
        expect = "Program([\n\tFuncDecl(mouse, VoidType, [InheritParam(n, BooleanType)], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 286))

    def test_287(self):
        input = """_123, Yz, Aaa: auto = -5 || "Watch movie please", 5::7, {56 && false, 1, 7};"""
        expect = "Program([\n\tVarDecl(_123, AutoType, BinExpr(||, UnExpr(-, IntegerLit(5)), StringLit(Watch movie please)))\n\tVarDecl(Yz, AutoType, BinExpr(::, IntegerLit(5), IntegerLit(7)))\n\tVarDecl(Aaa, AutoType, ArrayLit([BinExpr(&&, IntegerLit(56), BooleanLit(False)), IntegerLit(1), IntegerLit(7)]))\n])"
        self.assertTrue(TestAST.test(input, expect, 287))

    def test_288(self):
        input = """_x6_yz, a69, XYZ: auto = 1 + 2, 3 - 4, "abc" :: "def";"""
        expect = "Program([\n\tVarDecl(_x6_yz, AutoType, BinExpr(+, IntegerLit(1), IntegerLit(2)))\n\tVarDecl(a69, AutoType, BinExpr(-, IntegerLit(3), IntegerLit(4)))\n\tVarDecl(XYZ, AutoType, BinExpr(::, StringLit(abc), StringLit(def)))\n])"
        self.assertTrue(TestAST.test(input, expect, 288))

    def test_289(self):
        input = """dsa: function boolean() {}"""
        expect = "Program([\n\tFuncDecl(dsa, BooleanType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 289))

    def test_290(self):
        input = """g: array[5] of boolean;"""
        expect = "Program([\n\tVarDecl(g, ArrayType([5], BooleanType))\n])"
        self.assertTrue(TestAST.test(input, expect, 290))

    def test_291(self):
        input = """_55, a5: integer;"""
        expect = "Program([\n\tVarDecl(_55, IntegerType)\n\tVarDecl(a5, IntegerType)\n])"
        self.assertTrue(TestAST.test(input, expect, 291))

    def test_292(self):
        input = """main: function void() {
                for(i = -1, i > -10, i - 1) {
                    print(i);
                }   
            }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([ForStmt(AssignStmt(Id(i), UnExpr(-, IntegerLit(1))), BinExpr(>, Id(i), UnExpr(-, IntegerLit(10))), BinExpr(-, Id(i), IntegerLit(1)), BlockStmt([CallStmt(print, Id(i))]))]))\n])"
        self.assertTrue(TestAST.test(input, expect, 292))

    def test_293(self):
        input = """main: function void() {
            // This is a comment line
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 293))

    def test_294(self):
        input = """main: function void() {
            // This is a comment line
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 294))

    def test_295(self):
        input = """main: function void() {
            /* This is a comment line */
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 295))

    def test_296(self):
        input = """main: function void() {
            // if(1 < 2) increase(i, 1);
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 296))

    def test_297(self):
        input = """main: function void() {
            /*
                This is a block comment
            */
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 297))

    def test_298(self):
        input = """main: function void() {
            /*
                This is a block comment
                if(1 < 2) increase(i, 1);
            */
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 298))

    def test_299(self):
        input = """Y, z, d: auto = 11*24, call(), 175%22;"""
        expect = "Program([\n\tVarDecl(Y, AutoType, BinExpr(*, IntegerLit(11), IntegerLit(24)))\n\tVarDecl(z, AutoType, FuncCall(call, []))\n\tVarDecl(d, AutoType, BinExpr(%, IntegerLit(175), IntegerLit(22)))\n])"
        self.assertTrue(TestAST.test(input, expect, 299))

    def test_300(self):
        input = """main: function void() {
            /*
                Block comment and then line comment
            */
            // Line comment
        }"""
        expect = "Program([\n\tFuncDecl(main, VoidType, [], None, BlockStmt([]))\n])"
        self.assertTrue(TestAST.test(input, expect, 300))
