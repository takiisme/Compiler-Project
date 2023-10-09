from Emitter import Emitter
from functools import reduce

from Frame import Frame
from abc import ABC
from Visitor import *
from AST import *
import copy

class Access():
    def __init__(self, frame, sym, isLeft = False, assign = False):
        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.assign = assign

class CName:
    def __init__(self, value):
        self.value = value

class Index:
    def __init__(self, value):
        self.value = value

class Type(ABC): pass
class ClassType(Type):
    def __init__(self, cname):
        self.cname = cname

class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self, symbol_name, symbol_type, symbol_inherit = False, symbol_value = None, symbol_inherit_list = -1):
        self.name, self.type, self.inherit, self.value, self.inherit_list = symbol_name, symbol_type, symbol_inherit, symbol_value, symbol_inherit_list

def compareSymbol(a: Symbol, b: Symbol):
    if not isinstance(a, Symbol) or not isinstance(b, Symbol):
        return False
    if a.type != None and b.type != None:
        return a.name == b.name and ((isinstance(a.type, MType) and isinstance(b.type, MType)) \
                            or (not isinstance(a.type, MType) and not isinstance(b.type, MType)))
    return a.name == b.name

def differSymbol(a: Symbol, b: Symbol):
    if not isinstance(a, Symbol) or not isinstance(b, Symbol):
        return False
    if a.type != None and b.type!= None:
        return a.name != b.name and ((isinstance(a.type, MType) and isinstance(b.type, MType)) \
                        or (not isinstance(a.type, MType) and not isinstance(b.type, MType)))
    return a.name != b.name

def helper(element, lst):
    for sym in lst:
        if not isinstance(sym, Symbol) or not isinstance(element, Symbol):
            continue
        if sym == element:
            return True
    return False

class CodeGenerator():
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [Symbol("readInteger", MType([], IntegerType()), symbol_value=CName(self.libName)), 
                Symbol("printInteger", MType([IntegerType()],VoidType()), symbol_value=CName(self.libName)),
                Symbol("readFloat", MType([], FloatType()), symbol_value=CName(self.libName)), 
                Symbol("printFloat", MType([FloatType()],VoidType()), symbol_value=CName(self.libName)),
                Symbol("readBoolean", MType([], BooleanType()), symbol_value=CName(self.libName)), 
                Symbol("printBoolean", MType([BooleanType()],VoidType()), symbol_value=CName(self.libName)),
                Symbol("readString", MType([], StringType()), symbol_value=CName(self.libName)), 
                Symbol("printString", MType([StringType()],VoidType()), symbol_value=CName(self.libName)),]

    def gen(self, ast, dir_):
        # ast: AST
        # dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

def search(name, lst):
    for index in range(len(lst)):
        if lst[index].name == name:
            return lst[index], index

class CodeGenVisitor(Visitor):
    def __init__(self, astTree, env, path):
        self.astTree = astTree
        self.env = env
        self.path = path
        self.cname = "MT22Class"
        self.emit = Emitter(self.path + "/" + self.cname + ".j")
        self.infer_agent = InferType(self.astTree)

################## VARIABLE - FUNCTION DECLARATION #####################
    def visitProgram(self, ast, param):
        self.emit.printout(self.emit.emitPROLOG(self.cname, "java.lang.Object"))
        o = Access(Frame("<clinit>", MType([], VoidType())), self.env)
        init_code = ""

        env = self.env
        # env = self.infer_agent.infer(copy.deepcopy(self.env))

        for declaration in ast.decls:
            if isinstance(declaration, FuncDecl): 
                env += [Symbol(declaration.name, MType([item.typ for item in declaration.params], declaration.return_type), declaration.inherit, symbol_value=CName(self.cname))]
            elif isinstance(declaration, VarDecl): 
                env += [Symbol(declaration.name, declaration.typ, symbol_value=CName(self.cname))]

        for declaration in ast.decls:
            if isinstance(declaration, VarDecl):
                o, code = self.visit(declaration, Access(o.frame, env))
                init_code = init_code + code
            elif isinstance(declaration, FuncDecl):
                self.visit(declaration, Access(o.frame, env))

        self.genInit()
        self.genClassInit(o.frame, init_code)
        self.emit.emitEPILOG()
        return param

    def genClassInit(self, frame, init_code):
        declarationName, declarationType = frame.name, frame.returnType
        self.emit.printout(self.emit.emitMETHOD(declarationName, declarationType, False, frame))
        
        frame.enterScope(False)
        label_start = frame.getStartLabel()
        label_end = frame.getEndLabel()
        
        self.emit.printout(self.emit.emitLABEL(label_start, frame))
        self.emit.printout(init_code)
        self.emit.printout(self.emit.emitLABEL(label_end, frame))
        self.emit.printout(self.emit.emitRETURN(declarationType.rettype, frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def genInit(self):
        frame = Frame("<init>", VoidType())
        declarationName, declarationType = "<init>", MType([], VoidType())
        self.emit.printout(self.emit.emitMETHOD(declarationName, declarationType, False, frame))

        frame.enterScope(True)
        variableName = "this"
        variableType = ClassType(self.cname)
        variableIndex = frame.getNewIndex()
        label_start = frame.getStartLabel()
        label_end = frame.getEndLabel()

        self.emit.printout(self.emit.emitVAR(variableIndex, variableName, variableType, label_start, label_end, frame))
        self.emit.printout(self.emit.emitLABEL(label_start, frame))
        self.emit.printout(self.emit.emitREADVAR(variableName, variableType, variableIndex, frame))
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        self.emit.printout(self.emit.emitLABEL(label_end, frame))
        self.emit.printout(self.emit.emitRETURN(declarationType.rettype, frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def visitVarDecl(self, ast, param, typeIn=None):
        variableCode, variableType = "", None
        if ast.init:
            variableCode, variableType = self.visit(ast.init, param)
        else:
            variableCode, variableType = "", ast.typ

        if param.frame.name == "<clinit>":
            self.emit.printout(self.emit.emitATTRIBUTE(ast.name, variableType, False, ""))
            param.sym.insert(0, Symbol(ast.name, variableType, symbol_value=CName(self.cname)))
        else:
            index = param.frame.getNewIndex()
            self.emit.printout(self.emit.emitVAR(index, ast.name, variableType, param.frame.getStartLabel(), param.frame.getEndLabel(), param.frame))
            param.sym.insert(0, Symbol(ast.name, variableType, symbol_value=Index(index)))
        
        res = ""
        if variableCode != "":
            if not isinstance(variableType, ArrayType):
                var_assign, _ = self.visit(Id(ast.name), Access(param.frame, param.sym, isLeft=True))
                res = variableCode + var_assign
            else:
                array_code, _ = self.visit(Id(ast.name), Access(param.frame, param.sym, isLeft=True))
                array_assign = ""

                if param.frame.name == "<clinit>":
                    array_assign = self.emit.emitSTOREGLARRAY(self.cname + "." + ast.name, variableCode, variableType, param.frame)
                else:
                    array_assign = self.emit.emitSTORELCARRAY(param.frame.getCurrIndex() - 1, variableCode, variableType, param.frame)
                res = array_code + array_assign

        if param.frame.name == "<clinit>":
            return param, res        
        else:
            self.emit.printout(res)
            return param

    def visitParamDecl(self, ast, param): pass
    def visitFuncDecl(self, ast, param):
        functionName = ast.name; functionSymbol, _ = search(functionName, param.sym)
        functionType = MType([ArrayType(None, StringType())],VoidType()) if functionName == "main" else functionSymbol.type
        functionFrame = Frame(functionName, functionType)
        
        self.emit.printout(self.emit.emitMETHOD(functionName, functionType, True, functionFrame))
        
        # Open the scope for param and body
        functionFrame.enterScope(isinstance(functionType.rettype, VoidType))
        label_start = functionFrame.getStartLabel()
        label_end = functionFrame.getEndLabel()

        if functionName == "main":
            variableName = "args"; variableType = functionType.partype[0]
            variableIndex = functionFrame.getNewIndex()
            self.emit.printout(self.emit.emitVAR(variableIndex, variableName, variableType, label_start, label_end, functionFrame))

        ############# PARAMETERS ##################
        self.emit.printout(self.emit.emitLABEL(label_start, functionFrame))

	    ############ BODY ##################
        innerScope = copy.deepcopy(param)
        innerScope.frame = functionFrame
        innerScope = reduce(lambda acc, ele: self.visit(ele, acc), [VarDecl(z.name, z.typ) for z in ast.params] + ast.body.body, innerScope)

        ############### RETURN TYPE #################
        hasReturn = False
        for decl in ast.body.body:
            if isinstance(decl, ReturnStmt): hasReturn = True

        if hasReturn == False:
            if isinstance(functionSymbol.type.rettype, VoidType):
                self.emit.printout(self.emit.emitRETURN(VoidType(), functionFrame))

            elif isinstance(functionSymbol.type.rettype, IntegerType):
                self.emit.printout(self.emit.emitPUSHICONST(0, functionFrame))
                self.emit.printout(self.emit.emitRETURN(IntegerType(), functionFrame))
            
            elif isinstance(functionSymbol.type.rettype, FloatType):
                self.emit.printout(self.emit.emitPUSHFCONST(str(0.0), functionFrame))
                self.emit.printout(self.emit.emitRETURN(FloatType(), functionFrame))

            elif isinstance(functionSymbol.type.rettype, BooleanType):
                self.emit.printout(self.emit.emitPUSHICONST("False", functionFrame))
                self.emit.printout(self.emit.emitRETURN(BooleanType(), functionFrame))

            elif isinstance(functionSymbol.type.rettype, StringType):
                self.emit.printout(self.emit.emitPUSHCONST("", StringType(), functionFrame))
                self.emit.printout(self.emit.emitRETURN(StringType(), functionFrame))
            
            elif isinstance(functionSymbol.type.rettype, ArrayType):
                index = functionFrame.getNewIndex()
                self.emit.printout(self.emit.emitVAR(index, "_default", functionSymbol.type.rettype, functionFrame.getStartLabel(), functionFrame.getEndLabel(), functionFrame))
                self.emit.printout(self.emit.emitLOCALARRAY(index, functionSymbol.type.rettype.dimension, functionSymbol.type.rettype.elementType, functionFrame))
                self.emit.printout(self.emit.emitREADVAR("_default", functionSymbol.type.rettype, index, functionFrame))
                self.emit.printout(self.emit.emitRETURN(functionSymbol.type.rettype, functionFrame))
        
        self.emit.printout(self.emit.emitLABEL(label_end, functionFrame))
        self.emit.printout(self.emit.emitENDMETHOD(functionFrame))
        functionFrame.exitScope()
        return param

########################### EXPRESSION ########################
    def visitBinExpr(self, ast, param):
        lhs, leftType = self.visit(ast.left, Access(param.frame, param.sym, isLeft=False))
        rhs, rightType = self.visit(ast.right, Access(param.frame, param.sym, isLeft=False))
        resType = leftType
        param.frame.push()
        param.frame.push()

        if isinstance(leftType, FloatType) or isinstance(rightType, FloatType):
            resType = FloatType()
            if isinstance(leftType, IntegerType):
                lhs = lhs + self.emit.emitI2F(param.frame)
            if isinstance(rightType, IntegerType):
                rhs = rhs + self.emit.emitI2F(param.frame)

        if ast.op in ["+", "-", "*", "/", "%"]:
            if ast.op in ["+", "-"]:
                return lhs + rhs + self.emit.emitADDOP(ast.op, resType, param.frame), resType
            elif ast.op in ["*", "/"]:
                return lhs + rhs + self.emit.emitMULOP(ast.op, resType, param.frame), resType  
            elif ast.op == '%':
                return lhs + rhs + self.emit.emitMOD(param.frame), IntegerType()

        elif ast.op in ["&&", "||"]:
            if ast.op == "&&":
                res = self.emit.emitANDOP(param.frame)
                label_start = param.frame.getNewLabel()
                label_end = param.frame.getNewLabel()

                lhs = lhs + self.emit.emitIFFALSE(label_start, param.frame)
                rhs = self.emit.emitPUSHCONST("True", BooleanType(), param.frame) + rhs + self.emit.emitGOTO(label_end, param.frame)
                return lhs + rhs + self.emit.emitLABEL(label_start, param.frame) + self.emit.emitPUSHCONST("False", BooleanType(), param.frame) + self.emit.emitPUSHCONST("False", BooleanType(), param.frame) + self.emit.emitLABEL(label_end, param.frame) + res, BooleanType()

            elif ast.op == "||":
                res = self.emit.emitOROP(param.frame)
                label_start = param.frame.getNewLabel()
                label_end = param.frame.getNewLabel()

                lhs = self.emit.emitIFTRUE(label_start, param.frame)
                rhs = self.emit.emitPUSHCONST("False", BooleanType(), param.frame) + rhs + self.emit.emitGOTO(label_end, param.frame)
                return lhs + rhs + self.emit.emitLABEL(label_start, param.frame) + self.emit.emitPUSHCONST("True", BooleanType(), param.frame) + self.emit.emitPUSHCONST("True", BooleanType(), param.frame) + self.emit.emitLABEL(label_end, param.frame) + res, BooleanType()

        elif ast.op == "::":
            return lhs + rhs + self.emit.emitINVOKEVIRTUAL("java/lang/String/concat", MType([StringType()], StringType()), param.frame), StringType()

        elif ast.op in ["==", "!=", "<", ">", "<=", ">="]:
            return lhs + rhs + self.emit.emitREOP(ast.op, resType, param.frame), BooleanType()
        
    def visitUnExpr(self, ast, param): 
        expression, expressionType = self.visit(ast.val, Access(param.frame, param.sym, isLeft=False))
        if ast.op == '!':
            return expression + self.emit.emitNOT(expressionType, param.frame), expressionType
        elif ast.op == '-':
            return expression + self.emit.emitNEGOP(expressionType, param.frame), expressionType

    def visitId(self, ast, param):
        idSymbol, _ = search(ast.name, param.sym)
        res = ""
        if param.isLeft and isinstance(idSymbol.type, ArrayType) and param.assign:
            if isinstance(idSymbol.value, CName):
                res = self.emit.emitPUTSTATIC(idSymbol.value.value + "." + ast.name, idSymbol.type, param.frame)
            elif isinstance(idSymbol.value, Index):
                res = self.emit.emitWRITEVAR(ast.name, idSymbol.type, idSymbol.value.value, param.frame)
        elif param.isLeft and not (isinstance(idSymbol.type, ArrayType) and param.assign):
            if isinstance(idSymbol.value, CName):
                if isinstance(idSymbol.type, ArrayType):
                    res = self.emit.emitGLOBALARRAY(idSymbol.value.value + "." + ast.name, idSymbol.type.dimensions, idSymbol.type.typ, param.frame)
                else:
                    res = self.emit.emitPUTSTATIC(idSymbol.value.value + "." + ast.name, idSymbol.type, param.frame)
            elif isinstance(idSymbol.value, Index):
                if isinstance(idSymbol.type, ArrayType):
                    res = self.emit.emitLOCALARRAY(idSymbol.value.value, idSymbol.type.dimensions, idSymbol.type.typ, param.frame)
                else:
                    res = self.emit.emitWRITEVAR(ast.name, idSymbol.type, idSymbol.value.value, param.frame)
        else:
            if isinstance(idSymbol.value, CName):
                res = self.emit.emitGETSTATIC(idSymbol.value.value + "." + ast.name, idSymbol.type, param.frame)
            elif isinstance(idSymbol.value, Index):
                res = self.emit.emitREADVAR(ast.name, idSymbol.type, idSymbol.value.value, param.frame)
        return res, idSymbol.type

    def visitArrayCell(self, ast, param): 
        arr_code, arr_type = self.visit(Id(ast.name), Access(param.frame, param.sym))
        index_code, _ = self.visit(ast.cell[0], Access(param.frame, param.sym))
        param.frame.push()

        for index in ast.cell[1:]:
            param.frame.push()
            index_code = index_code + self.emit.jvm.emitAALOAD()
            index_code = index_code + self.visit(index, Access(param.frame, param.sym))[0]

        if param.isLeft:
            return [arr_code + index_code, self.emit.emitASTORE(arr_type.typ, param.frame)], arr_type.typ
        param.frame.push()
        return arr_code + index_code + self.emit.emitALOAD(arr_type.typ, param.frame), arr_type.typ

########################## STATEMENT ##########################
    def visitAssignStmt(self, ast, param):
        if isinstance(ast.lhs, ArrayCell):
            rhs_code, _ = self.visit(ast.rhs, Access(param.frame, param.sym, isLeft=False))
            lhs_code, _ = self.visit(ast.lhs, Access(param.frame, param.sym, isLeft=True, assign=True))
            self.emit.printout(lhs_code[0] + rhs_code + lhs_code[1])
        
        elif isinstance(ast.rhs, ArrayLit):
            rhs_code, _ = self.visit(ast.rhs, Access(param.frame, param.sym, isLeft=False))
            lhs_code, lhs_type = self.visit(ast.lhs, Access(param.frame, param.sym, isLeft=False))
            self.emit.printout(self.emit.emitSTORELCARRAY(-1, rhs_code, lhs_type, param.frame, init = lhs_code))

        else:
            rhs_code, _ = self.visit(ast.rhs, Access(param.frame, param.sym, isLeft=False))
            lhs_code, _ = self.visit(ast.lhs, Access(param.frame, param.sym, isLeft=True, assign=True))
            self.emit.printout(rhs_code + lhs_code)
        return param

    def visitBlockStmt(self, ast, param): pass
    def visitIfStmt(self, ast, param): 
        label_end = param.frame.getNewLabel()
        parent_scope = copy.deepcopy(param.sym)

        if isinstance(ast.tstmt, BlockStmt):
            expression = ast.cond
            list_vardecl = list(filter(lambda x: isinstance(x, VarDecl), ast.tstmt.body))
            list_stmt = list(filter(lambda x: not isinstance(x, VarDecl), ast.tstmt.body))

            expression_code, expression_type = self.visit(expression, param)
            self.emit.printout(expression_code)

            param.frame.enterScope(False)

            label_true = param.frame.getStartLabel()
            label_false = param.frame.getEndLabel()

            self.emit.printout(self.emit.emitIFFALSE(label_false, param.frame))
            self.emit.printout(self.emit.emitLABEL(label_true, param.frame))

            # Var declare
            param = reduce(lambda x, y: y.accept(self, x), list_vardecl, param)

            # Statments
            param = reduce(lambda x, y: y.accept(self, x), list_stmt, param)

            self.emit.printout(self.emit.emitGOTO(label_end, param.frame))
            self.emit.printout(self.emit.emitLABEL(label_false, param.frame))

            param.sym = copy.deepcopy(parent_scope)
            param.frame.exitScope()
        else:
            self.visit(ast.tstmt, param)
        
        if ast.fstmt:
            if isinstance(ast.fstmt, BlockStmt):
                param = reduce(lambda x,y: y.accept(self, x), list(filter(lambda x: isinstance(x, VarDecl), ast.fstmt.body)), param)
                param = reduce(lambda x,y: y.accept(self, x), list(filter(lambda x: not isinstance(x, VarDecl), ast.fstmt.body)), param)
            else:
                self.visit(ast.fstmt, param)
            
        self.emit.printout(self.emit.emitLABEL(label_end, param.frame))
        param.sym = parent_scope
        return param

    def visitForStmt(self, ast, param): 
        parent_scope = copy.deepcopy(param.sym)
        index_code, index_type = self.visit(ast.init.lhs, param)
        exp1_code, exp1_type = self.visit(ast.init.rhs, param)
        exp2_code, exp2_type = self.visit(ast.cond, param)
        exp3_code, exp3_type = self.visit(ast.upd, param)

        self.emit.printout(exp1_code)
        index_code_write, index_type = self.visit(ast.init.lhs, Access(param.frame, param.sym, isLeft=True))
        self.emit.printout(index_code_write)

        param.frame.enterScope(False)

        label_start = param.frame.getStartLabel()
        label_end = param.frame.getEndLabel()
        param.frame.enterLoop()

        self.emit.printout(self.emit.emitLABEL(label_start, param.frame))
        self.emit.printout(exp2_code)
        self.emit.printout(self.emit.emitIFFALSE(label_end, param.frame))

        if isinstance(ast.stmt, BlockStmt):
            param = reduce(lambda x, y: self.visit(y, x), list(filter(lambda z: isinstance(z, VarDecl), ast.stmt.body)), param)
            param = reduce(lambda x, y: self.visit(y, x), list(filter(lambda z: not isinstance(z, VarDecl), ast.stmt.body)), param)
        else:
            self.visit(ast.stmt, param)
        self.emit.printout(self.emit.emitLABEL(param.frame.getContinueLabel(), param.frame))
        self.emit.printout(index_code)
        self.emit.printout(exp3_code)
        self.emit.printout(self.emit.emitADDOP("+", index_type, param.frame))
        index_code_write, _ = self.visit(ast.init.lhs, Access(param.frame, param.sym, isLeft=True))
        self.emit.printout(self.emit.emitGOTO(label_start, param.frame))
        self.emit.printout(self.emit.emitLABEL(label_end, param.frame))
        self.emit.printout(self.emit.emitLABEL(param.frame.getBreakLabel(), param.frame))

        param.frame.exitLoop()
        param.frame.exitScope()
        param.sym = parent_scope
        return param

    def visitWhileStmt(self, ast, param): 
        param_scope = copy.deepcopy(param.sym)
        expression_code, _ = self.visit(ast.cond, param)

        param.frame.enterScope(False)

        label_start = param.frame.getStartLabel()
        label_end = param.frame.getEndLabel()
        param.frame.enterLoop()

        self.emit.printout(self.emit.emitLABEL(label_start, param.frame))
        self.emit.printout(expression_code)
        self.emit.printout(self.emit.emitIFFALSE(label_end, param.frame))

        if isinstance(ast.stmt, BlockStmt):
            param = reduce(lambda x, y: self.visit(y, x), list(filter(lambda z: isinstance(z, VarDecl), ast.stmt.body)), param)
            param = reduce(lambda x, y: self.visit(y, x), list(filter(lambda z: not isinstance(z, VarDecl), ast.stmt.body)), param)
        else:
            self.visit(ast.stmt, param)

        self.emit.printout(self.emit.emitLABEL(param.frame.getContinueLabel(), param.frame))
        self.emit.printout(self.emit.emitGOTO(label_start, param.frame))
        self.emit.printout(self.emit.emitLABEL(label_end, param.frame))
        self.emit.printout(self.emit.emitLABEL(param.frame.getBreakLabel(), param.frame))

        param.frame.exitLoop()
        param.frame.exitScope()
        param.sym = param_scope
        return param

    def visitDoWhileStmt(self, ast, param):
        parent_sym = copy.deepcopy(param.sym)
        expression_code, _ = self.visit(ast.cond, param)

        param.frame.enterScope(False)

        label_start = param.frame.getStartLabel()
        label_end = param.frame.getEndLabel()
        param.frame.enterLoop()

        self.emit.printout(self.emit.emitLABEL(label_start, param.frame))
        
        param = reduce(lambda x, y: self.visit(y, x), list(filter(lambda z: isinstance(z, VarDecl), ast.stmt.body)), param)
        param = reduce(lambda x, y: self.visit(y, x), list(filter(lambda z: not isinstance(z, VarDecl), ast.stmt.body)), param)

        self.emit.printout(self.emit.emitLABEL(param.frame.getContinueLabel(), param.frame))
        self.emit.printout(expression_code)
        self.emit.printout(self.emit.emitIFFALSE(label_end, param.frame))
        self.emit.printout(self.emit.emitGOTO(label_start, param.frame))
        self.emit.printout(self.emit.emitLABEL(label_end, param.frame))
        self.emit.printout(self.emit.emitLABEL(param.frame.getBreakLabel(), param.frame))

        param.frame.exitLoop()

        param.frame.exitScope()
        param.sym = parent_sym
        return param

    def visitBreakStmt(self, ast, param):
        self.emit.printout(self.emit.emitGOTO(param.frame.getBreakLabel(), param.frame))
        return param
    
    def visitContinueStmt(self, ast, param):
        self.emit.printout(self.emit.emitGOTO(param.frame.getContinueLabel(), param.frame))
        return param

    def visitReturnStmt(self, ast, param): 
        if not isinstance(param.frame.returnType, VoidType) and ast.expr:
            if not isinstance(ast.expr, ArrayLit):
                expression_code, expression_type = self.visit(ast.expr, param)
                self.emit.printout(expression_code)

            else:
                expression_code, expression_type = self.visit(ast.expr, param)
                index = param.frame.getNewIndex()
                
                res = self.emit.emitVAR(index, "_return", expression_type, param.frame.getStartLabel(), param.frame.getEndLabel(), param.frame)
                res = res + self.emit.emitLOCALARRAY(index, expression_type.dimensions, expression_type.typ, param.frame)
                res = res + self.emit.emitSTORELCARRAY(param.frame.getCurrentIndex() - 1, expression_code, expression_type, param.frame)
                res = res + self.emit.emitREADVAR("_return", expression_type, index, param.frame)
                self.emit.printout(res)
        self.emit.printout(self.emit.emitRETURN(param.frame.returnType.rettype, param.frame))
        return param
    
    def helperFunction(self, ast, param, option):
        function_symbol, _ = search(ast.name, param.sym)
        param_code = ""

        for i, parameter in enumerate(ast.args):
            p_code, p_type = self.visit(parameter, param)

            if isinstance(parameter, ArrayLit):
                index = param.frame.getNewIndex()
                param_code = param_code + self.emit.emitVAR(index, "_param%d"%i, p_type, param.frame.getStartLabel(), param.frame.getEndLabel(), param.frame)
                param_code = param_code + self.emit.emitLOCALARRAY(index, p_type.dimensions, p_type.typ, param.frame)
                param_code = param_code + self.emit.emitSTORELCARRAY(index, p_code, p_type, param.frame)
                param_code = param_code + self.emit.emitREADVAR("_param%d"%i, p_type, index, param.frame)
            else:
                param_code = param_code + p_code
        
        funcCall = self.emit.emitINVOKESTATIC(function_symbol.value.value + "/" + function_symbol.name, function_symbol.type, param.frame)

        if option == 1:
            self.emit.printout(param_code + funcCall)
            return param
        elif option == 2:
            return param_code + funcCall, function_symbol.type.rettype

    def visitCallStmt(self, ast, param): 
        return self.helperFunction(ast, param, 1)
    def visitFuncCall(self, ast, param):
        return self.helperFunction(ast, param, 2)

########################### LITERAL ##########################
    def visitIntegerLit(self, ast, param): 
        return self.emit.emitPUSHICONST(ast.val, param.frame), IntegerType()
    def visitIntegerType(self, ast, param): pass
    def visitFloatLit(self, ast, param): 
        return self.emit.emitPUSHFCONST(str(ast.val), param.frame), FloatType()
    def visitFloatType(self, ast, param): pass
    def visitBooleanLit(self, ast, param):
        return self.emit.emitPUSHICONST(str(ast.val), param.frame), BooleanType()
    def visitBooleanType(self, ast, param): pass
    def visitStringLit(self, ast, param): 
        return self.emit.emitPUSHCONST(ast.val, StringType(), param.frame), StringType()
    def visitStringType(self, ast, param): pass
    def visitArrayLit(self, ast, param):
        literal_code, literal_type = [], []

        for literal in ast.explist:
            code, typE = self.visit(literal, param)
            literal_code = literal_code + [code]
            literal_type = literal_type + [typE]
        
        if len(literal_type) == 0:
            return ArrayType([0], AutoType), list()
        
        checkList = set()
        for item in literal_type:
            checkList.add(type(item))
        checkList = list(checkList)

        if not isinstance(checkList[0], ArrayType):
            return literal_code, ArrayType([len(literal_type)], literal_type[0])
        else:
            return literal_code, ArrayType([len(literal_type)] + literal_type[0].dimensions, literal_type[0].typ)

    def visitArrayType(self, ast, param): pass
    def visitAutoType(self, ast, param): pass
    def visitVoidType(self, ast, param): pass

############################ ASSIGNMENT 3 ########################
class FunctionPrototype:
    def __init__(self, parameter_name, parameter_type, return_type):
        self.parameter_name, self.parameter_type, self.return_type = parameter_name, parameter_type, return_type

def compareType(operandLeft, operandRight):
    typeLeft, typeRight = type(operandLeft), type(operandRight)
    if typeLeft != ArrayType or typeRight != ArrayType: return typeLeft == typeRight
    else:
        if len(operandLeft.dimensions) != len(operandRight.dimensions): return False
        for index in range(len(operandLeft.dimensions)):
            if operandLeft.dimensions[index] != operandRight.dimensions[index]: return False
        return type(operandLeft.typ) == type(operandRight.typ)    

class InferType(Visitor):
    def __init__(self, ast):
        self.ast, self.visitTask = ast, []
        self.symbol_table = [   Symbol("readInteger", FunctionPrototype([], [],IntegerType())), Symbol("printInteger", FunctionPrototype(['anArg'], [IntegerType()],VoidType())),   Symbol("readFloat", FunctionPrototype([], [],FloatType())),     Symbol("printFloat", FunctionPrototype(['anArg'], [FloatType()],VoidType())),   Symbol("writeFloat", FunctionPrototype(['anArg'], [FloatType()],VoidType())), 
                                Symbol("readBoolean", FunctionPrototype([], [],BooleanType())), Symbol("printBoolean", FunctionPrototype(['anArg'], [BooleanType()],VoidType())),   Symbol("readString", FunctionPrototype([], [],StringType())),   Symbol("printString", FunctionPrototype(['anArg'], [StringType()],VoidType()))]
    def infer(self, param):
        return self.visit(self.ast, param)

    def inferTypeForSymbol(self, namE, typE, isFuncCall, param, option = 1, index = 0):
        if option == 1:
            inParam = False
            for scope in param:
                for declaration in scope:
                    if declaration.name == namE:
                        if isinstance(declaration.type, FunctionPrototype): declaration.type.return_type = typE
                        else: declaration.type = typE
                        inParam = True; break
                if inParam == True: break
            if inParam == False:
                for declaration in self.visitTask:
                    if declaration.name == namE:
                        if isinstance(declaration.type, FunctionPrototype): declaration.type.return_type = typE
                        else: declaration.type = typE
            
            if isFuncCall == False and isinstance(self.visitTask[0].type, FunctionPrototype):
                for index in range(len(self.visitTask[0].type.parameter_name)):
                    if self.visitTask[0].type.parameter_name[index] == namE: self.visitTask[0].type.parameter_type[index] = typE
        elif option == 2:
            inParam = False
            for scope in param:
                for declaration in scope:
                    if declaration.name == namE:
                        declaration.type.parameter_type[index] = typE; inParam = True; break
                if inParam == True: break
            if inParam == False:
                for declaration in self.visitTask:
                    if declaration.name == namE:
                        declaration.type.parameter_type[index] = typE
    
    def arrayLiteralTypeInference(self, lhs, rhs, symbol_table):
        typeToInfer = ArrayType(lhs.dimensions[1:], lhs.typ) if len(lhs.dimensions) > 1 else lhs.typ
        for index in range(len(rhs.explist)):
            if isinstance(rhs.explist[index], ArrayLit):
                self.arrayLiteralTypeInference(typeToInfer, rhs.explist[index], symbol_table)
            elif isinstance(rhs.explist[index], (FuncCall, Id)): 
                self.inferTypeForSymbol(rhs.explist[index].name, typeToInfer, isinstance(rhs.explist[index], FuncCall), symbol_table, 1)

    def check(self): return self.visit(self.ast, self.symbol_table[:])
    def visitProgram(self, ast, param):
        for declaration in ast.decls:
            if isinstance(declaration, FuncDecl): self.visitTask += [Symbol(declaration.name, FunctionPrototype([item.name for item in declaration.params], \
                    [self.visit(item, param).type for item in declaration.params], self.visit(declaration.return_type, param)), declaration.inherit, declaration)]
            elif isinstance(declaration, VarDecl): self.visitTask += [Symbol(declaration.name, self.visit(declaration.typ, param))]
        for declaration in ast.decls:
            if isinstance(declaration, FuncDecl):
                if(declaration.name == 'super' or declaration.name == 'preventDefault'): pass
                self.visit(declaration, [param])
                param.append(self.visitTask[0])
            elif isinstance(declaration, VarDecl): param.append(self.visit(declaration, [param]))
            self.visitTask.pop(0)

        entry_point = False
        for declaration in ast.decls:
            if isinstance(declaration, FuncDecl) and declaration.name == "main" and declaration.params == [] and isinstance(declaration.return_type, VoidType): entry_point = True
        if entry_point == False: pass
        return param

    def visitVarDecl(self, ast, param):
        for declaration in param[0]:
            if declaration.name == ast.name: pass
        if ast.init is None:
            if isinstance(ast.typ, AutoType): pass
            return Symbol(ast.name, self.visit(ast.typ, param))
        else:
            tempParam = param; tempParam.append([Symbol(ast.name, self.visit(ast.typ, param))])
            expression_type, variable_type = self.visit(ast.init, tempParam), self.visit(ast.typ, tempParam)
            if isinstance(expression_type, VoidType): pass
            if isinstance(variable_type, AutoType): variable_type = expression_type
            else:
                if not isinstance(variable_type, ArrayType) or not isinstance(expression_type, ArrayType):
                    if isinstance(expression_type, AutoType):
                        if isinstance(ast.init, (Id, FuncCall)): self.inferTypeForSymbol(ast.init.name, variable_type, isinstance(ast.init, FuncCall), tempParam)
                        elif isinstance(variable_type, StringType) or isinstance(variable_type, BooleanType): pass
                    elif isinstance(variable_type, FloatType):
                        if not (isinstance(expression_type, FloatType) or isinstance(expression_type, IntegerType)): pass
                    elif not compareType(variable_type, expression_type): pass
                else:
                    if len(expression_type.dimensions) <= len(variable_type.dimensions) and variable_type.dimensions[:len(expression_type.dimensions)] == expression_type.dimensions:
                        if isinstance(expression_type.typ, AutoType):
                            self.arrayLiteralTypeInference(variable_type, ast.init, tempParam)
                            expression_type = self.visit(ast.init, tempParam)
                        elif len(expression_type.dimensions) < len(variable_type.dimensions): pass
                        else:
                            if isinstance(variable_type.typ, FloatType):
                                if not (isinstance(expression_type.typ, IntegerType) or isinstance(expression_type.typ, FloatType)): pass
                            elif not compareType(variable_type, expression_type): pass
                    else: pass
            return Symbol(ast.name, variable_type, False, ast.init)

    def visitParamDecl(self, ast, param):
        for declarartion in param:
            if declarartion.name == ast.name: pass
        return Symbol(ast.name, self.visit(ast.typ, param), False)
    
    def visitFuncDecl(self, ast, param):
        for declaration in param[0]:
            if declaration.name == ast.name: pass

        local = []; foundParent = False
        if ast.inherit is not None:
            for declaration in self.ast.decls:
                if declaration.name == ast.inherit and isinstance(declaration, FuncDecl):
                    foundParent = True
                    if not(len(ast.body.body) > 0 and isinstance(ast.body.body[0], CallStmt) and ast.body.body[0].name == 'preventDefault'):
                        setParentParam = set()
                        for index in range(len(declaration.params)):
                            parameter = declaration.params[index]
                            if parameter.inherit == True: 
                                oldLen = len(setParentParam); setParentParam.add(parameter.name)
                                if oldLen == len(setParentParam): pass
                                local.append(Symbol(parameter.name, self.visit(parameter.typ, param), True, None, index)); 
            
            for declaration in self.symbol_table:
                if declaration.name == ast.inherit and isinstance(declaration.type, FunctionPrototype):
                    foundParent = True
                    if not(len(ast.body.body) > 0 and isinstance(ast.body.body[0], CallStmt) and ast.body.body[0].name == 'preventDefault'):
                        for index in range(len(declaration.type.parameter_name)):
                            local.append(Symbol(declaration.type.parameter_name[index], declaration.type.parameter_type[index], True, None, 0))
        if ast.inherit is not None and foundParent == False: pass
        
        setParam = set()
        for index in range(len(ast.params)):
            oldLen = len(setParam); setParam.add(ast.params[index].name)
            if (oldLen == len(setParam)): pass

        for index in range(len(ast.params)):
            parameter = ParamDecl(ast.params[index].name, self.visitTask[0].type.parameter_type[index], ast.params[index].out, ast.params[index].inherit)
            local += [self.visit(parameter, local)]

        functionBody = ast.body.body
        if ast.inherit is not None:
            for declaration in param[0] + self.visitTask:
                if declaration.name == ast.inherit and isinstance(declaration.type, FunctionPrototype):
                    parentParamList = len(declaration.type.parameter_type) > 0
                    if parentParamList and len(ast.body.body) == 0: pass
                    if isinstance(ast.body.body[0], CallStmt):
                        if ast.body.body[0].name == 'super':
                            temp_return_type = VoidType()
                            for func in param[0] + self.visitTask:
                                if func.name == ast.inherit and isinstance(func.type, FunctionPrototype): temp_return_type = func.type.return_type
                            try:
                                self.calling(CallStmt(ast.inherit, ast.body.body[0].args), [local] + param, 3)
                                if isinstance(temp_return_type, AutoType):
                                    for func in param[0] + self.visitTask:
                                        if func.name == ast.inherit: func.type.return_type = temp_return_type
                            except: pass
                        elif ast.body.body[0].name == 'preventDefault':
                            if len(ast.body.body[0].args) != 0: pass
                        elif parentParamList: pass

                        if ast.body.body[0].name == 'super' or ast.body.body[0].name == 'preventDefault':
                            functionBody = ast.body.body[1:] if len(ast.body.body) > 1 else []
                    elif parentParamList: pass
        elif len(ast.body.body) > 0 and isinstance(ast.body.body[0], CallStmt) and (ast.body.body[0].name == 'super' or ast.body.body[0].name == 'preventDefault'): pass

        return_type = self.visit(ast.return_type, param)
        reference_environment = param[:]; reference_environment.insert(0, local)
        self.visit(BlockStmt(functionBody), [reference_environment, False, return_type, False])
# ---------------------------------- EXPRESSION -------------------------------------
    def jump(self, ast, param):
        func = None
        for declaration in self.visitTask:
            if isinstance(declaration.type, FunctionPrototype) and declaration.name == ast.name: func = declaration; break

        temp = None; indexFound = -1
        for i in range(len(self.visitTask)):
            if isinstance(self.visitTask[i].type, FunctionPrototype) and self.visitTask[i].name == func.name:
                temp = self.visitTask[i]; self.visitTask.pop(i); self.visitTask.insert(0, temp); temp = self.visitTask[0]; indexFound = i
        for i in range(len(self.ast.decls)):
            if isinstance(self.ast.decls[i], FuncDecl) and self.ast.decls[i].name == temp.name:
                paramList = []
                for index in range(len(temp.type.parameter_name)):
                    paramList += [ParamDecl(temp.type.parameter_name[index], temp.type.parameter_type[index], None, self.ast.decls[i].params[index].inherit)]
                self.visit(FuncDecl(temp.name, temp.type.return_type, paramList, temp.inherit, self.ast.decls[i].body), [param[-1]])
        self.visitTask.pop(0)
        self.visitTask.insert(indexFound, temp)

    def visitBinExpr(self, ast, param):
        operandLeft, operandRight = self.visit(ast.left, param), self.visit(ast.right, param)
        if isinstance(operandLeft, AutoType) and not isinstance(operandRight, AutoType):
            operandLeft = operandRight; self.inferTypeForSymbol(ast.left.name, operandRight, isinstance(ast.left, FuncCall), param)
            if isinstance(ast.left, FuncCall): self.jump(ast.left, param)
        elif isinstance(operandRight, AutoType) and not isinstance(operandLeft, AutoType):
            operandRight = operandLeft; self.inferTypeForSymbol(ast.right.name, operandRight, isinstance(ast.right, FuncCall), param) 
            if isinstance(ast.right, FuncCall): self.jump(ast.right, param)       
        elif isinstance(operandLeft, AutoType) and isinstance(operandRight, AutoType) and ast.op in ['+', '-', '*', '/']: return AutoType()

        if ast.op in ['-', '+', '*', '/', '%']:
            if ast.op != '%':
                if not isinstance(operandLeft, (IntegerType, FloatType, AutoType)) or not isinstance(operandRight, (IntegerType, FloatType, AutoType)): pass
                return FloatType() if (isinstance(operandLeft, FloatType) or isinstance(operandRight, FloatType)) else IntegerType()
            else:
                if not isinstance(operandLeft, (IntegerType, AutoType)) or not isinstance(operandRight, (IntegerType, AutoType)): pass
                return IntegerType()
            
        elif ast.op in ['&&', '||']:
            if isinstance(operandLeft, AutoType):
                operandLeft = BooleanType(); self.inferTypeForSymbol(ast.left.name, BooleanType(), isinstance(ast.left, FuncCall), param)
            if isinstance(operandRight, AutoType):
                operandRight = BooleanType() ; self.inferTypeForSymbol(ast.right.name, BooleanType(), isinstance(ast.right, FuncCall), param)         
            if not isinstance(operandLeft, BooleanType) or not isinstance(operandRight, BooleanType): pass
            return BooleanType()

        elif ast.op == '::':
            if isinstance(operandLeft, AutoType):
                operandLeft = StringType(); self.inferTypeForSymbol(ast.left.name, StringType(), isinstance(ast.left, FuncCall), param)
            if isinstance(operandRight, AutoType):
                operandRight = StringType(); self.inferTypeForSymbol(ast.right.name, StringType(), isinstance(ast.right, FuncCall), param)
            if not isinstance(operandLeft, StringType) or not isinstance(operandRight, StringType): pass
            return StringType()
    
        elif ast.op in ['==', '!=', '<', '>', '<=', '>=']:
            if ast.op in ['==', '!=']:
                if not isinstance(operandLeft, (IntegerType, BooleanType, AutoType)) or not isinstance(operandRight, (IntegerType, BooleanType, AutoType)): pass
            else:
                if not isinstance(operandLeft, (IntegerType, FloatType, AutoType)) or not isinstance(operandRight, (IntegerType, FloatType, AutoType)): pass
            return BooleanType()

    def visitUnExpr(self, ast, param):
        operand = self.visit(ast.val, param)
        if isinstance(operand, AutoType) and ast.op != '!': return AutoType()
        if ast.op == '!':
            if isinstance(operand, AutoType):
                operand = BooleanType(); self.inferTypeForSymbol(ast.val.name, BooleanType(), isinstance(ast.val, FuncCall), param)
                if isinstance(ast.val, FuncCall): self.jump(ast.val, param)
            if not isinstance(operand, BooleanType): pass
            return BooleanType()
        elif ast.op == '-':
            if not (isinstance(operand, IntegerType) or isinstance(operand, FloatType)): pass
            return operand
# ------------------------------------ ID -----------------------------------
    def visitId(self, ast, param):
        for scope in param:
            for declaration in scope:
                if declaration.name == ast.name and not isinstance(declaration.type, FunctionPrototype): return declaration.type
# ------------------------------------ ARRAY CELL ----------------------------
    def visitArrayCell(self, ast, param): 
        available = False; res = param[-1][-1] 
        for scope in param:
            for declaration in scope:
                if ast.name == declaration.name:
                    available = True; res = declaration; break
            if available == True: break

        if available == True and not isinstance(res.type, ArrayType): pass
        elif available == False: pass
        
        expression_dimension, array_dimension = len(ast.cell), len(res.type.dimensions)
        if expression_dimension > array_dimension: pass
        for expression in ast.cell:
            if isinstance(self.visit(expression, param), AutoType): 
                self.inferTypeForSymbol(expression.name, IntegerType(), isinstance(expression, FuncCall), param)
                if isinstance(expression, FuncCall): self.jump(expression, param)
            if not isinstance(self.visit(expression, param), IntegerType): pass
        if expression_dimension == array_dimension: return res.type.typ
        elif expression_dimension < array_dimension: return ArrayType(res.type.dimensions[(expression_dimension):], res.type.typ)     
# ------------------------------ STATEMENT ---------------------------------
    def calling(self, ast, param, option):
        if option != 3 and (ast.name == 'super' or ast.name == 'preventDefault'): pass
        def inner(): 
            resList = []
            for scope in param:
                for declaration in scope:
                    if declaration.name == ast.name: resList.append([declaration, True])
            for declaration in self.visitTask:
                if declaration.name == ast.name: resList.append([declaration, False])
            return resList
            
        resList = inner(); func = None; inParam = False
        for itemFound in resList:
            if isinstance(itemFound[0].type, FunctionPrototype): func = resList[0][0]; inParam = resList[0][1]; break

        if func is None: pass
        if not isinstance(func.type, FunctionPrototype): pass
        if option == 1 and isinstance(func.type.return_type, VoidType): pass

        if len(ast.args) > len(func.type.parameter_type): pass
        elif len(ast.args) < len(func.type.parameter_type): pass
        
        for index in range(min(len(func.type.parameter_type), len(ast.args))):
            rhs, lhs = self.visit(ast.args[index], param), func.type.parameter_type[index]
            if isinstance(rhs, VoidType): pass
            if isinstance(lhs, AutoType):
                lhs = rhs; func.type.parameter_type[index] = rhs
                for item in self.ast.decls:
                    if isinstance(item, FuncDecl) and item.name == func.name:
                        for parameter in item.params:
                            if parameter.name == func.type.parameter_name[index] and parameter.inherit == True:
                                self.inferTypeForSymbol(func.type.parameter_name[index], rhs, isinstance(lhs, FuncCall), param, 1)
                self.inferTypeForSymbol(func.name, rhs, isinstance(lhs, FuncCall), param, 2, index)   
                # Recursion
                if ast.name == self.visitTask[0].name:
                    for scope in param:
                        for declaration in scope:
                            if declaration.name == func.type.parameter_name[index]: declaration.type = rhs
                # Super() -> Update inherit param
                elif option == 3:
                    for scope in param: 
                        for declaration in scope:
                            if declaration.inherit_list >= 0: declaration.type = func.type.parameter_type[declaration.inherit_list]
            else:
                if not isinstance(lhs, ArrayType) or not isinstance(rhs, ArrayType):
                    if isinstance(rhs, AutoType):
                        rhs = lhs; self.inferTypeForSymbol(ast.args[index].name, lhs, False, param)
                    elif isinstance(lhs, FloatType):
                        if not (isinstance(rhs, FloatType) or isinstance(rhs, IntegerType)): pass
                    elif not compareType(lhs, rhs): pass
                else:
                    if len(rhs.dimensions) <= len(lhs.dimensions) and lhs.dimensions[:len(rhs.dimensions)] == rhs.dimensions:
                        if isinstance(rhs.typ, AutoType):
                            self.arrayLiteralTypeInference(lhs, ast.args[index], param)
                            rhs = self.visit(ast.init, param)
                        elif len(rhs.dimensions) < len(lhs.dimensions): pass
                        else:
                            if isinstance(lhs.typ, FloatType):
                                if not (isinstance(rhs.typ, IntegerType) or isinstance(rhs.typ, FloatType)): pass
                            elif not compareType(lhs, rhs): pass
                    else: pass

        if inParam == True:
            for scope in param:
                for declaration in scope:
                    if declaration.name == ast.name:
                        declaration = func; break
        elif inParam == False:
            for declaration in self.visitTask:
                if declaration.name == ast.name: declaration = func
        
        return func.type.return_type

    def visitFuncCall(self, ast, param): return self.calling(ast, param, 1)
    def visitCallStmt(self, ast, param): self.calling(ast, param, 2)
    def visitAssignStmt(self, ast, param):
        lhs, rhs = self.visit(ast.lhs, param), self.visit(ast.rhs, param)    
        inParam = False
        for scope in param:
            for decl in scope:
                if decl.name == ast.lhs.name: decl.value = ast.rhs; inParam = True; break
            if inParam == True: break

        if not isinstance(lhs, ArrayType) and not isinstance(lhs, FunctionPrototype):
            if isinstance(lhs, AutoType) and not isinstance(rhs, AutoType):
                lhs = rhs; self.inferTypeForSymbol(ast.lhs.name, rhs, isinstance(ast.lhs, FuncCall), param); infer = False
                for declaration in param[0]:
                    if declaration.name == ast.lhs.name and declaration.inherit_list >= 0: infer = True
                if infer == True:
                    for scope in param + [self.visitTask]:
                        for item in scope:
                            if isinstance(item.type, FunctionPrototype) and item.name == self.visitTask[0].inherit:
                                for index in range(len(item.type.parameter_name)):
                                    if item.type.parameter_name[index] == ast.lhs.name: item.type.parameter_type[index] = lhs
            elif isinstance(rhs, AutoType) and not isinstance(lhs, AutoType):
                rhs = lhs
                if isinstance(ast.rhs, (FuncCall, Id)): 
                    self.inferTypeForSymbol(ast.rhs.name, lhs, isinstance(ast.rhs, FuncCall), param)
                    if isinstance(ast.rhs, FuncCall): self.jump(ast.rhs, param)
                elif isinstance(rhs, (StringType, BooleanType)): pass
            elif isinstance(lhs, FloatType):
                if not isinstance(rhs, FloatType) and not isinstance(rhs, IntegerType): pass
            elif isinstance(lhs, VoidType) or isinstance(lhs, ArrayType): pass
            elif type(lhs) != type(rhs): pass
        else: pass
        return lhs
    
    def visitBlockStmt(self, ast, param):
        local = param[0][0] 
        for declaration in ast.body:
            reference_environment = param[0][:]; reference_environment[0] = local
            if isinstance(declaration, VarDecl):
                local.append(self.visit(declaration, reference_environment))
            elif isinstance(declaration, Stmt):
                if isinstance(declaration, AssignStmt) or isinstance(declaration, CallStmt): self.visit(declaration, reference_environment)
                else:
                    if isinstance(declaration, BlockStmt): reference_environment.insert(0, [])
                    self.visit(declaration, [reference_environment, param[1], param[2], param[3] if not isinstance(declaration, BlockStmt) else False])
                    if isinstance(declaration, ReturnStmt): param[3] = True
                    
    def visitClause(self, ast, param, stmt, inLoop = False):
        if isinstance(stmt, BlockStmt):
            reference_environment = param[0][:]; reference_environment.insert(0, [])
            self.visit(stmt, [reference_environment, param[1] if inLoop == False else True, param[2], param[3] if not isinstance(stmt, BlockStmt) else False])
        elif isinstance(stmt, AssignStmt) or isinstance(stmt, CallStmt): self.visit(stmt, param[0])
        else: self.visit(stmt, [param[0], param[1] if inLoop == False else True, param[2], param[3]])

    def visitIfStmt(self, ast, param):
        if not isinstance(self.visit(ast.cond, param[0]), BooleanType): pass
        self.visitClause(ast, param, ast.tstmt, False)
        if ast.fstmt is not None: self.visitClause(ast, param, ast.fstmt, False)

    def visitForStmt(self, ast, param):
        if not isinstance(self.visit(ast.init, param[0]), IntegerType) or not isinstance(self.visit(ast.cond, param[0]), BooleanType) \
            or not isinstance(self.visit(ast.upd, param[0]), IntegerType): pass   
        self.visitClause(ast, param, ast.stmt, True)  

    def visitWhileStmt(self, ast, param):
        if not isinstance(self.visit(ast.cond, param[0]), BooleanType): pass
        self.visitClause(ast, param, ast.stmt, True)   

    def visitDoWhileStmt(self, ast, param): 
        reference_environment = param[0][:]; reference_environment.insert(0, [])
        self.visit(ast.stmt, [reference_environment, True, param[2], param[3]])
        if not isinstance(self.visit(ast.cond, param[0]), BooleanType): pass

    def visitBreakStmt(self, ast, param): 
        if param[1] == False: pass
    def visitContinueStmt(self, ast, param):
        if param[1] == False: pass

    def visitReturnStmt(self, ast, param):
        if param[3] == False:
            param[2] = self.visitTask[0].type.return_type
            if ast.expr is None:
                if isinstance(param[2], AutoType): self.visitTask[0].type.return_type = VoidType(); param[2] = VoidType()
                if not isinstance(param[2], VoidType): pass
            else:
                return_expression = self.visit(ast.expr, param[0])
                if isinstance(param[2], FloatType):
                    if not isinstance(return_expression, FloatType) and not isinstance(return_expression, IntegerType): pass
                elif isinstance(param[2], AutoType):
                    param[2] = return_expression; self.visitTask[0].type.return_type = return_expression
                elif isinstance(return_expression, AutoType):
                    return_expression = param[2]; self.inferTypeForSymbol(ast.expr.name, param[2], isinstance(ast.expr, FuncCall), param[0])
                elif not compareType(param[2], return_expression): pass
# ---------------------------------------------------------------------------------------------
    def visitIntegerLit(self, ast, param): return IntegerType()
    def visitIntegerType(self, ast, param): return IntegerType()  
    def visitFloatLit(self, ast, param): return FloatType()
    def visitFloatType(self, ast, param): return FloatType()   
    def visitBooleanLit(self, ast, param): return BooleanType()
    def visitBooleanType(self, ast, param): return BooleanType()   
    def visitStringLit(self, ast, param): return StringType()
    def visitStringType(self, ast, param): return StringType() 
    def arrayLiteralHelper(self, ast, fullAST, param):
        if len(ast.explist) >= 1:
            firstElementType = self.visit(ast.explist[0], param) if not isinstance(ast.explist[0], ArrayLit) else self.arrayLiteralHelper(ast.explist[0], fullAST, param)
            for index in range(len(ast.explist)):
                literal = ast.explist[index]
                currentElementType = self.visit(literal, param) if not isinstance(literal, ArrayLit) else self.arrayLiteralHelper(literal, fullAST, param)
                if isinstance(firstElementType, AutoType) and not isinstance(currentElementType, AutoType):
                    firstElementType = currentElementType
                    self.inferTypeForSymbol(ast.explist[0].name, currentElementType, isinstance(ast.explist[0], FuncCall), param)
                    if isinstance(ast.explist[0], FuncCall): self.jump(ast.explist[0], param)
                elif isinstance(currentElementType, AutoType) and not isinstance(firstElementType, AutoType):
                    currentElementType = firstElementType
                    self.inferTypeForSymbol(literal.name, firstElementType, isinstance(literal, FuncCall), param)
                    if isinstance(ast.explist[index], FuncCall): self.jump(ast.explist[index], param)
                if not compareType(firstElementType, currentElementType): pass
            else: return ArrayType([len(ast.explist)], firstElementType) if not isinstance(firstElementType, ArrayType) else ArrayType([len(ast.explist)] + firstElementType.dimensions, firstElementType.typ)
        else: return ArrayType([0], AutoType()) 
    def visitArrayLit(self, ast, param): return self.arrayLiteralHelper(ast, ast, param)
    def visitArrayType(self, ast, param): return ArrayType(ast.dimensions, self.visit(ast.typ, param))
    def visitAutoType(self, ast, param): return AutoType()  
    def visitVoidType(self, ast, param): return VoidType()