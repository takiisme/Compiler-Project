
import unittest
from TestUtils import TestLexer


class LexerSuite(unittest.TestCase):
    def test_101(self):
        self.assertTrue(TestLexer.test("^abc","Error Token ^", 101))
    def test_102(self):
        self.assertTrue(TestLexer.test("##","Error Token #",102))
    def test_103(self):
        self.assertTrue(TestLexer.test("a_b_c","a_b_c,<EOF>",103))
    def test_104(self):
        self.assertTrue(TestLexer.test("AbC","AbC,<EOF>",104))
    def test_105(self):
        self.assertTrue(TestLexer.test("A__________________0","A__________________0,<EOF>",105))
    def test_106(self):
        self.assertTrue(TestLexer.test("A123_456_789","A123_456_789,<EOF>",106))
    def test_107(self):
        self.assertTrue(TestLexer.test("auto","auto,<EOF>",107))
    def test_108(self):
        self.assertTrue(TestLexer.test("autoo","autoo,<EOF>",108))
    def test_109(self):
        self.assertTrue(TestLexer.test("IDENTIFIER","IDENTIFIER,<EOF>",109))
    def test_110(self):
        self.assertTrue(TestLexer.test("main","main,<EOF>",110))
    def test_111(self):
        self.assertTrue(TestLexer.test("01","0,1,<EOF>",111))
    def test_112(self):
        self.assertTrue(TestLexer.test("0","0,<EOF>",112))
    def test_113(self):
        self.assertTrue(TestLexer.test("9","9,<EOF>",113))
    def test_114(self):
        self.assertTrue(TestLexer.test("19","19,<EOF>",114))
    def test_115(self):
        self.assertTrue(TestLexer.test("_123","_123,<EOF>",115))
    def test_116(self):
        self.assertTrue(TestLexer.test("1_2345","12345,<EOF>",116))
    def test_117(self):
        self.assertTrue(TestLexer.test("12_34_56_78","12345678,<EOF>",117))
    def test_118(self):
        self.assertTrue(TestLexer.test("1234_","1234,_,<EOF>",118))
    def test_119(self):
        self.assertTrue(TestLexer.test("0ab","0,ab,<EOF>",119))
    def test_120(self):
        self.assertTrue(TestLexer.test("123__456__789","123,__456__789,<EOF>",120))
    def test_121(self):
        self.assertTrue(TestLexer.test("1_2_3.456","123.456,<EOF>",121))
    def test_122(self):
        self.assertTrue(TestLexer.test("12_3.45_6","123.45,_6,<EOF>",122))
    def test_123(self):
        self.assertTrue(TestLexer.test("123.456","123.456,<EOF>",123))
    def test_124(self):
        self.assertTrue(TestLexer.test("0e0","0e0,<EOF>",124))
    def test_125(self):
        self.assertTrue(TestLexer.test("07e0","0,7e0,<EOF>",125))
    def test_126(self):
        self.assertTrue(TestLexer.test("1_2_3e","123,e,<EOF>",126))
    def test_127(self):
        self.assertTrue(TestLexer.test(".25e+3",".25e+3,<EOF>",127))
    def test_128(self):
        self.assertTrue(TestLexer.test(".25",".,25,<EOF>",128))
    def test_129(self):
        self.assertTrue(TestLexer.test("e10","e10,<EOF>",129))
    def test_130(self):
        self.assertTrue(TestLexer.test("0.25E-3","0.25E-3,<EOF>",130))
    def test_131(self):
        self.assertTrue(TestLexer.test("1.175eE+-3","1.175,eE,+,-,3,<EOF>",131))
    def test_132(self):
        self.assertTrue(TestLexer.test("123E+5","123E+5,<EOF>",132))
    def test_133(self):
        self.assertTrue(TestLexer.test("true","true,<EOF>",133))
    def test_134(self):
        self.assertTrue(TestLexer.test("false","false,<EOF>",134))
    def test_135(self):
        self.assertTrue(TestLexer.test("truee","truee,<EOF>",135))
    def test_136(self):
        self.assertTrue(TestLexer.test(""" "This string \\' contains \\' a tab symbol: \\t" ""","This string \\' contains \\' a tab symbol: \\t,<EOF>",136))
    def test_137(self):
        self.assertTrue(TestLexer.test(""" "This string \\\\ contains \\\\ a backlash symbol: \\\\" ""","This string \\\\ contains \\\\ a backlash symbol: \\\\,<EOF>",137))
    def test_138(self):
        self.assertTrue(TestLexer.test(""" "This string \\t contains \\t a backspace symbol: \\b" ""","This string \\t contains \\t a backspace symbol: \\b,<EOF>",138))
    def test_139(self):
        self.assertTrue(TestLexer.test(""" "This string \\" contains \\" a form feed: \\f and carriage return: \\r" ""","This string \\\" contains \\\" a form feed: \\f and carriage return: \\r,<EOF>",139))
    def test_140(self):
        self.assertTrue(TestLexer.test(""" "Endline symbol endline \\n" ""","Endline symbol endline \\n,<EOF>",140))
    def test_141(self):
        self.assertTrue(TestLexer.test(""" "This string \\' contains \\' a tab symbol: \\t""","Unclosed String: This string \\' contains \\' a tab symbol: \\t",141))
    def test_142(self):
        self.assertTrue(TestLexer.test(""" "This string \\\\ contains \\\\ a backlash symbol: \\\\""","Unclosed String: This string \\\\ contains \\\\ a backlash symbol: \\\\",142))
    def test_143(self):
        self.assertTrue(TestLexer.test(""" "This string \\t contains \\t a backspace symbol: \\b""","Unclosed String: This string \\t contains \\t a backspace symbol: \\b",143))
    def test_144(self):
        self.assertTrue(TestLexer.test(""" "This string \\" contains \\" a form feed: \\f and carriage return: \\r""","Unclosed String: This string \\\" contains \\\" a form feed: \\f and carriage return: \\r",144))
    def test_145(self):
        self.assertTrue(TestLexer.test(""" "Endline symbol endline \\n""","Unclosed String: Endline symbol endline \\n",145))
    def test_146(self):
        self.assertTrue(TestLexer.test(""" "This string \\' contains \\' a tab symbol: \a" ""","This string \\' contains \\' a tab symbol: \a,<EOF>",146))
    def test_147(self):
        self.assertTrue(TestLexer.test(""" "This string \\\\ contains \\\\ a backlash symbol: \\a" ""","Illegal Escape In String: This string \\\\ contains \\\\ a backlash symbol: \\a",147))
    def test_148(self):
        self.assertTrue(TestLexer.test(""" "This string \\\\\\ contains \\\\\\ a backlash symbol: \q" ""","Illegal Escape In String: This string \\\\\\ ",148))
    def test_149(self):
        self.assertTrue(TestLexer.test(""" "This string \\t contains \\t a backspace symbol: \\q" ""","Illegal Escape In String: This string \\t contains \\t a backspace symbol: \\q",149))
    def test_150(self):
        self.assertTrue(TestLexer.test(""" "This string \\" contains \\" a form feed: \w and carriage return: \r" ""","Illegal Escape In String: This string \\\" contains \\\" a form feed: \\w",150))
    def test_151(self):
        self.assertTrue(TestLexer.test(""" "This string \" contains \" a form feed: \\w and carriage return: \\r" ""","This string ,contains,Illegal Escape In String:  a form feed: \\w",151))
    def test_152(self):
        self.assertTrue(TestLexer.test(""" "This string \\" contains \\" a form feed: \endline and carriage return: \\r" ""","Illegal Escape In String: This string \\\" contains \\\" a form feed: \e",152))
    def test_153(self):
        self.assertTrue(TestLexer.test(""" "This string is illegal \\endline" ""","Illegal Escape In String: This string is illegal \\e",153))
    def test_154(self):
        self.assertTrue(TestLexer.test("+-123*/==79","+,-,123,*,/,==,79,<EOF>",154))
    def test_155(self):
        self.assertTrue(TestLexer.test("9>=3.::<","9,>=,3.,::,<,<EOF>",155))
    def test_156(self):
        self.assertTrue(TestLexer.test("&&&","&&,Error Token &",156))
    def test_157(self):
        self.assertTrue(TestLexer.test(":::","::,:,<EOF>",157))
    def test_158(self):
        self.assertTrue(TestLexer.test("<==","<=,=,<EOF>",158))
    def test_159(self):
        self.assertTrue(TestLexer.test("!=!","!=,!,<EOF>",159))
    def test_160(self):
        self.assertTrue(TestLexer.test("{{{)))","{,{,{,),),),<EOF>",160))
    def test_161(self):
        self.assertTrue(TestLexer.test(";<=12_34true>=:",";,<=,1234,true,>=,:,<EOF>",161))
    def test_162(self):
        self.assertTrue(TestLexer.test("123 > 456","123,>,456,<EOF>",162))
    def test_163(self):
        self.assertTrue(TestLexer.test("{a - [(b] + c) / d % e - f >= {g && h} || j :: k, l {m (n [ p ] ) q } r == s - t ! u && v < 01234 }","{,a,-,[,(,b,],+,c,),/,d,%,e,-,f,>=,{,g,&&,h,},||,j,::,k,,,l,{,m,(,n,[,p,],),q,},r,==,s,-,t,!,u,&&,v,<,0,1234,},<EOF>",163))
    def test_164(self):
        self.assertTrue(TestLexer.test("true1.0e","true1,.,0,e,<EOF>",164))
    def test_165(self):
        self.assertTrue(TestLexer.test("9_Abc","9,_Abc,<EOF>",165))
    def test_166(self):
        self.assertTrue(TestLexer.test(".1234",".,1234,<EOF>",166))
    def test_167(self):
        self.assertTrue(TestLexer.test("true.0e","true,.,0,e,<EOF>",167))
    def test_168(self):
        self.assertTrue(TestLexer.test("0_123_4","0,_123_4,<EOF>",168))
    def test_169(self):
        self.assertTrue(TestLexer.test("\n\\","Error Token \\",169))
    def test_170(self):
        self.assertTrue(TestLexer.test("conti,nue","conti,,,nue,<EOF>",170))
    def test_171(self):
        self.assertTrue(TestLexer.test("integer a, b, c = 1, 2, 3;","integer,a,,,b,,,c,=,1,,,2,,,3,;,<EOF>",171))
    def test_172(self):
        self.assertTrue(TestLexer.test("""float a "abc\\n" - integer || > <==""","float,a,abc\\n,-,integer,||,>,<=,=,<EOF>",172))
    def test_173(self):
        self.assertTrue(TestLexer.test("integer?","integer,Error Token ?",173))
    def test_174(self):
        self.assertTrue(TestLexer.test(""" "What does the fox says - ding ding ding \\" What is that?" ""","What does the fox says - ding ding ding \\\" What is that?,<EOF>",174))
    def test_175(self):
        self.assertTrue(TestLexer.test("{1, 2, 3, 4, 5}","{,1,,,2,,,3,,,4,,,5,},<EOF>",175))
    def test_176(self):
        self.assertTrue(TestLexer.test("""{"Principles", "Of", "Programming", "Language"}""","{,Principles,,,Of,,,Programming,,,Language,},<EOF>",176))
    def test_177(self):
        self.assertTrue(TestLexer.test("x = readInteger();","x,=,readInteger,(,),;,<EOF>",177))
    def test_178(self):
        self.assertTrue(TestLexer.test("autobreak","autobreak,<EOF>",178))
    def test_179(self):
        self.assertTrue(TestLexer.test("aut0br3ak;","aut0br3ak,;,<EOF>",179))
    def test_180(self):
        self.assertTrue(TestLexer.test("ID: [a-zA-Z_][a-zA-Z0-9_]*;","ID,:,[,a,-,zA,-,Z_,],[,a,-,zA,-,Z0,-,9,_,],*,;,<EOF>",180))
    def test_181(self):
        self.assertTrue(TestLexer.test("a?b?c?","a,Error Token ?",181))
    def test_182(self):
        self.assertTrue(TestLexer.test("{while (x < 5) x = x + 1;}","{,while,(,x,<,5,),x,=,x,+,1,;,},<EOF>",182))
    def test_183(self):
        self.assertTrue(TestLexer.test("""foo(x + 2; 4.0 / y ");""","foo,(,x,+,2,;,4.0,/,y,Unclosed String: );",183))
    def test_184(self):
        self.assertTrue(TestLexer.test("","<EOF>",184))
    def test_185(self):
        self.assertTrue(TestLexer.test("                     ","<EOF>",185))
    def test_186(self):
        self.assertTrue(TestLexer.test("// Watch the movie!","<EOF>",186))
    def test_187(self):
        self.assertTrue(TestLexer.test("/* Hello /**/ I am comment block */","I,am,comment,block,*,/,<EOF>",187))
    def test_188(self):
        self.assertTrue(TestLexer.test("// /* I am Tai.","<EOF>",188))
    def test_189(self):
        self.assertTrue(TestLexer.test("// /* \n I am TAI.   ","I,am,TAI,.,<EOF>",189))
    def test_190(self):
        self.assertTrue(TestLexer.test("// Watch \n // The // movie","<EOF>",190))
    def test_191(self):
        self.assertTrue(TestLexer.test("checkPrime: function boolean (n : integer) {","checkPrime,:,function,boolean,(,n,:,integer,),{,<EOF>",191))
    def test_192(self):
        self.assertTrue(TestLexer.test("if (n == 0 || n == 1) return false;","if,(,n,==,0,||,n,==,1,),return,false,;,<EOF>",192))
    def test_193(self):
        self.assertTrue(TestLexer.test("i : integer;","i,:,integer,;,<EOF>",193))
    def test_194(self):
        self.assertTrue(TestLexer.test("for(i = 2, i * i <= n, i = i + 1)","for,(,i,=,2,,,i,*,i,<=,n,,,i,=,i,+,1,),<EOF>",194))
    def test_195(self):
        self.assertTrue(TestLexer.test("if (n % i == 0) return false;  ","if,(,n,%,i,==,0,),return,false,;,<EOF>",195))
    def test_196(self):
        self.assertTrue(TestLexer.test("return true;}","return,true,;,},<EOF>",196))
    def test_197(self):
        self.assertTrue(TestLexer.test("main: function void() {","main,:,function,void,(,),{,<EOF>",197))
    def test_198(self):
        self.assertTrue(TestLexer.test("n : float = 7.5","n,:,float,=,7.5,<EOF>",198))
    def test_199(self):
        self.assertTrue(TestLexer.test("""n = n + string_to_int("1.0");   ""","n,=,n,+,string_to_int,(,1.0,),;,<EOF>",199))
    def test_200(self):
        self.assertTrue(TestLexer.test("checkPrime(n);}","checkPrime,(,n,),;,},<EOF>",200))
        
