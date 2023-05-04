from AST import *
from Visitor import *
from StaticError import *

class FunctionPrototype:
    def __init__(self, parameter_name, parameter_type, return_type):
        self.parameter_name, self.parameter_type, self.return_type = parameter_name, parameter_type, return_type
class Symbol:
    def __init__(self, symbol_name, symbol_type, symbol_inherit = False, symbol_value = None, symbol_inherit_list = -1):
        self.name, self.type, self.inherit, self.value, self.inherit_list = symbol_name, symbol_type, symbol_inherit, symbol_value, symbol_inherit_list
def compareType(operandLeft, operandRight):
    typeLeft, typeRight = type(operandLeft), type(operandRight)
    if typeLeft != ArrayType or typeRight != ArrayType: return typeLeft == typeRight
    else:
        if len(operandLeft.dimensions) != len(operandRight.dimensions): return False
        for index in range(len(operandLeft.dimensions)):
            if operandLeft.dimensions[index] != operandRight.dimensions[index]: return False
        return type(operandLeft.typ) == type(operandRight.typ)    

class StaticChecker(Visitor):
    def __init__(self, ast):
        self.ast, self.visitTask = ast, []
        self.symbol_table = [   Symbol("readInteger", FunctionPrototype([], [],IntegerType())), Symbol("printInteger", FunctionPrototype(['anArg'], [IntegerType()],VoidType())),   Symbol("readFloat", FunctionPrototype([], [],FloatType())),     Symbol("printFloat", FunctionPrototype(['anArg'], [FloatType()],VoidType())),   Symbol("writeFloat", FunctionPrototype(['anArg'], [FloatType()],VoidType())), 
                                Symbol("readBoolean", FunctionPrototype([], [],BooleanType())), Symbol("printBoolean", FunctionPrototype(['anArg'], [BooleanType()],VoidType())),   Symbol("readString", FunctionPrototype([], [],StringType())),   Symbol("printString", FunctionPrototype(['anArg'], [StringType()],VoidType()))]
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
                if(declaration.name == 'super' or declaration.name == 'preventDefault'): raise Redeclared(Function(), declaration.name)
                self.visit(declaration, [param])
                param.append(self.visitTask[0])
            elif isinstance(declaration, VarDecl): param.append(self.visit(declaration, [param]))
            self.visitTask.pop(0)

        entry_point = False
        for declaration in ast.decls:
            if isinstance(declaration, FuncDecl) and declaration.name == "main" and declaration.params == [] and isinstance(declaration.return_type, VoidType): entry_point = True
        if entry_point == False: raise NoEntryPoint()

    def visitVarDecl(self, ast, param):
        for declaration in param[0]:
            if declaration.name == ast.name: raise Redeclared(Variable(), ast.name)
        if ast.init is None:
            if isinstance(ast.typ, AutoType): raise Invalid(Variable(), ast.name)
            return Symbol(ast.name, self.visit(ast.typ, param))
        else:
            tempParam = param; tempParam.append([Symbol(ast.name, self.visit(ast.typ, param))])
            expression_type, variable_type = self.visit(ast.init, tempParam), self.visit(ast.typ, tempParam)
            if isinstance(expression_type, VoidType): raise TypeMismatchInVarDecl(ast)
            if isinstance(variable_type, AutoType): variable_type = expression_type
            else:
                if not isinstance(variable_type, ArrayType) or not isinstance(expression_type, ArrayType):
                    if isinstance(expression_type, AutoType):
                        if isinstance(ast.init, (Id, FuncCall)): self.inferTypeForSymbol(ast.init.name, variable_type, isinstance(ast.init, FuncCall), tempParam)
                        elif isinstance(variable_type, StringType) or isinstance(variable_type, BooleanType): raise TypeMismatchInVarDecl(ast)
                    elif isinstance(variable_type, FloatType):
                        if not (isinstance(expression_type, FloatType) or isinstance(expression_type, IntegerType)): raise TypeMismatchInVarDecl(ast)
                    elif not compareType(variable_type, expression_type): raise TypeMismatchInVarDecl(ast)
                else:
                    if len(expression_type.dimensions) <= len(variable_type.dimensions) and variable_type.dimensions[:len(expression_type.dimensions)] == expression_type.dimensions:
                        if isinstance(expression_type.typ, AutoType):
                            self.arrayLiteralTypeInference(variable_type, ast.init, tempParam)
                            expression_type = self.visit(ast.init, tempParam)
                        elif len(expression_type.dimensions) < len(variable_type.dimensions): raise TypeMismatchInVarDecl(ast)
                        else:
                            if isinstance(variable_type.typ, FloatType):
                                if not (isinstance(expression_type.typ, IntegerType) or isinstance(expression_type.typ, FloatType)): raise TypeMismatchInVarDecl(ast)
                            elif not compareType(variable_type, expression_type): raise TypeMismatchInVarDecl(ast)
                    else: raise TypeMismatchInVarDecl(ast)
            return Symbol(ast.name, variable_type, False, ast.init)

    def visitParamDecl(self, ast, param):
        for declarartion in param:
            if declarartion.name == ast.name: raise Invalid(Parameter(), declarartion.name) if declarartion.inherit == True else Redeclared(Parameter(), ast.name)
        return Symbol(ast.name, self.visit(ast.typ, param), False)
    
    def visitFuncDecl(self, ast, param):
        for declaration in param[0]:
            if declaration.name == ast.name: raise Redeclared(Function(), ast.name)

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
                                if oldLen == len(setParentParam): raise Redeclared(Parameter(), parameter.name)
                                local.append(Symbol(parameter.name, self.visit(parameter.typ, param), True, None, index)); 
            
            for declaration in self.symbol_table:
                if declaration.name == ast.inherit and isinstance(declaration.type, FunctionPrototype):
                    foundParent = True
                    if not(len(ast.body.body) > 0 and isinstance(ast.body.body[0], CallStmt) and ast.body.body[0].name == 'preventDefault'):
                        for index in range(len(declaration.type.parameter_name)):
                            local.append(Symbol(declaration.type.parameter_name[index], declaration.type.parameter_type[index], True, None, 0))
        if ast.inherit is not None and foundParent == False: raise Undeclared(Function(), ast.inherit)
        
        setParam = set()
        for index in range(len(ast.params)):
            oldLen = len(setParam); setParam.add(ast.params[index].name)
            if (oldLen == len(setParam)): raise Redeclared(Parameter(), ast.params[index].name)

        for index in range(len(ast.params)):
            parameter = ParamDecl(ast.params[index].name, self.visitTask[0].type.parameter_type[index], ast.params[index].out, ast.params[index].inherit)
            local += [self.visit(parameter, local)]

        functionBody = ast.body.body
        if ast.inherit is not None:
            for declaration in param[0] + self.visitTask:
                if declaration.name == ast.inherit and isinstance(declaration.type, FunctionPrototype):
                    parentParamList = len(declaration.type.parameter_type) > 0
                    if parentParamList and len(ast.body.body) == 0: raise InvalidStatementInFunction(ast.name)
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
                            except TypeMismatchInStatement: raise TypeMismatchInStatement(ast.body.body[0])
                        elif ast.body.body[0].name == 'preventDefault':
                            if len(ast.body.body[0].args) != 0: raise TypeMismatchInExpression(ast.body.body[0].args[0])
                        elif parentParamList: raise InvalidStatementInFunction(ast.name)

                        if ast.body.body[0].name == 'super' or ast.body.body[0].name == 'preventDefault':
                            functionBody = ast.body.body[1:] if len(ast.body.body) > 1 else []
                    elif parentParamList: raise InvalidStatementInFunction(ast.name)
        elif len(ast.body.body) > 0 and isinstance(ast.body.body[0], CallStmt) and (ast.body.body[0].name == 'super' or ast.body.body[0].name == 'preventDefault'): raise InvalidStatementInFunction(ast.name)

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
                if not isinstance(operandLeft, (IntegerType, FloatType, AutoType)) or not isinstance(operandRight, (IntegerType, FloatType, AutoType)): raise TypeMismatchInExpression(ast)
                return FloatType() if (isinstance(operandLeft, FloatType) or isinstance(operandRight, FloatType)) else IntegerType()
            else:
                if not isinstance(operandLeft, (IntegerType, AutoType)) or not isinstance(operandRight, (IntegerType, AutoType)): raise TypeMismatchInExpression(ast)
                return IntegerType()
            
        elif ast.op in ['&&', '||']:
            if isinstance(operandLeft, AutoType):
                operandLeft = BooleanType(); self.inferTypeForSymbol(ast.left.name, BooleanType(), isinstance(ast.left, FuncCall), param)
            if isinstance(operandRight, AutoType):
                operandRight = BooleanType() ; self.inferTypeForSymbol(ast.right.name, BooleanType(), isinstance(ast.right, FuncCall), param)         
            if not isinstance(operandLeft, BooleanType) or not isinstance(operandRight, BooleanType): raise TypeMismatchInExpression(ast)
            return BooleanType()

        elif ast.op == '::':
            if isinstance(operandLeft, AutoType):
                operandLeft = StringType(); self.inferTypeForSymbol(ast.left.name, StringType(), isinstance(ast.left, FuncCall), param)
            if isinstance(operandRight, AutoType):
                operandRight = StringType(); self.inferTypeForSymbol(ast.right.name, StringType(), isinstance(ast.right, FuncCall), param)
            if not isinstance(operandLeft, StringType) or not isinstance(operandRight, StringType): raise TypeMismatchInExpression(ast)
            return StringType()
    
        elif ast.op in ['==', '!=', '<', '>', '<=', '>=']:
            if ast.op in ['==', '!=']:
                if not isinstance(operandLeft, (IntegerType, BooleanType, AutoType)) or not isinstance(operandRight, (IntegerType, BooleanType, AutoType)): raise TypeMismatchInExpression(ast)
            else:
                if not isinstance(operandLeft, (IntegerType, FloatType, AutoType)) or not isinstance(operandRight, (IntegerType, FloatType, AutoType)): raise TypeMismatchInExpression(ast)
            return BooleanType()

    def visitUnExpr(self, ast, param):
        operand = self.visit(ast.val, param)
        if isinstance(operand, AutoType) and ast.op != '!': return AutoType()
        if ast.op == '!':
            if isinstance(operand, AutoType):
                operand = BooleanType(); self.inferTypeForSymbol(ast.val.name, BooleanType(), isinstance(ast.val, FuncCall), param)
                if isinstance(ast.val, FuncCall): self.jump(ast.val, param)
            if not isinstance(operand, BooleanType): raise TypeMismatchInExpression(ast)
            return BooleanType()
        elif ast.op == '-':
            if not (isinstance(operand, IntegerType) or isinstance(operand, FloatType)): raise TypeMismatchInExpression(ast)
            return operand
# ------------------------------------ ID -----------------------------------
    def visitId(self, ast, param):
        for scope in param:
            for declaration in scope:
                if declaration.name == ast.name and not isinstance(declaration.type, FunctionPrototype): return declaration.type
        raise Undeclared(Identifier(), ast.name)
# ------------------------------------ ARRAY CELL ----------------------------
    def visitArrayCell(self, ast, param): 
        available = False; res = param[-1][-1] 
        for scope in param:
            for declaration in scope:
                if ast.name == declaration.name:
                    available = True; res = declaration; break
            if available == True: break

        if available == True and not isinstance(res.type, ArrayType): raise TypeMismatchInExpression(ast)
        elif available == False: raise Undeclared(Identifier(), ast.name)
        
        expression_dimension, array_dimension = len(ast.cell), len(res.type.dimensions)
        if expression_dimension > array_dimension: raise TypeMismatchInExpression(ast)
        for expression in ast.cell:
            if isinstance(self.visit(expression, param), AutoType): 
                self.inferTypeForSymbol(expression.name, IntegerType(), isinstance(expression, FuncCall), param)
                if isinstance(expression, FuncCall): self.jump(expression, param)
            if not isinstance(self.visit(expression, param), IntegerType): raise TypeMismatchInExpression(expression)
        if expression_dimension == array_dimension: return res.type.typ
        elif expression_dimension < array_dimension: return ArrayType(res.type.dimensions[(expression_dimension):], res.type.typ)     
# ------------------------------ STATEMENT ---------------------------------
    def calling(self, ast, param, option):
        if option != 3 and (ast.name == 'super' or ast.name == 'preventDefault'): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast)
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
        else: raise Undeclared(Function(), ast.name)

        if func is None: raise Undeclared(Function(), ast.name)
        if not isinstance(func.type, FunctionPrototype): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast)
        if option == 1 and isinstance(func.type.return_type, VoidType): raise TypeMismatchInExpression(ast)

        if len(ast.args) > len(func.type.parameter_type): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[len(func.type.parameter_type)])
        elif len(ast.args) < len(func.type.parameter_type): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression()
        
        for index in range(min(len(func.type.parameter_type), len(ast.args))):
            rhs, lhs = self.visit(ast.args[index], param), func.type.parameter_type[index]
            if isinstance(rhs, VoidType): raise TypeMismatchInExpression(ast) if option == 1 else  TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[index])
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
                        if not (isinstance(rhs, FloatType) or isinstance(rhs, IntegerType)): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[index])
                    elif not compareType(lhs, rhs): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[index])
                else:
                    if len(rhs.dimensions) <= len(lhs.dimensions) and lhs.dimensions[:len(rhs.dimensions)] == rhs.dimensions:
                        if isinstance(rhs.typ, AutoType):
                            self.arrayLiteralTypeInference(lhs, ast.args[index], param)
                            rhs = self.visit(ast.init, param)
                        elif len(rhs.dimensions) < len(lhs.dimensions): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[index])
                        else:
                            if isinstance(lhs.typ, FloatType):
                                if not (isinstance(rhs.typ, IntegerType) or isinstance(rhs.typ, FloatType)): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[index])
                            elif not compareType(lhs, rhs): raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[index])
                    else: raise TypeMismatchInExpression(ast) if option == 1 else TypeMismatchInStatement(ast) if option == 2 else TypeMismatchInExpression(ast.args[index])

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
                elif isinstance(rhs, (StringType, BooleanType)): raise TypeMismatchInStatement(ast)
            elif isinstance(lhs, FloatType):
                if not isinstance(rhs, FloatType) and not isinstance(rhs, IntegerType): raise TypeMismatchInStatement(ast)
            elif isinstance(lhs, VoidType) or isinstance(lhs, ArrayType): raise TypeMismatchInStatement(ast)
            elif type(lhs) != type(rhs): raise TypeMismatchInStatement(ast)
        else: raise TypeMismatchInStatement(ast)
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
        if not isinstance(self.visit(ast.cond, param[0]), BooleanType): raise TypeMismatchInStatement(ast)
        self.visitClause(ast, param, ast.tstmt, False)
        if ast.fstmt is not None: self.visitClause(ast, param, ast.fstmt, False)

    def visitForStmt(self, ast, param):
        if not isinstance(self.visit(ast.init, param[0]), IntegerType) or not isinstance(self.visit(ast.cond, param[0]), BooleanType) \
            or not isinstance(self.visit(ast.upd, param[0]), IntegerType): raise TypeMismatchInStatement(ast)   
        self.visitClause(ast, param, ast.stmt, True)  

    def visitWhileStmt(self, ast, param):
        if not isinstance(self.visit(ast.cond, param[0]), BooleanType): raise TypeMismatchInStatement(ast)
        self.visitClause(ast, param, ast.stmt, True)   

    def visitDoWhileStmt(self, ast, param): 
        reference_environment = param[0][:]; reference_environment.insert(0, [])
        self.visit(ast.stmt, [reference_environment, True, param[2], param[3]])
        if not isinstance(self.visit(ast.cond, param[0]), BooleanType): raise TypeMismatchInStatement(ast)

    def visitBreakStmt(self, ast, param): 
        if param[1] == False: raise MustInLoop(ast)
    def visitContinueStmt(self, ast, param):
        if param[1] == False: raise MustInLoop(ast)

    def visitReturnStmt(self, ast, param):
        if param[3] == False:
            param[2] = self.visitTask[0].type.return_type
            if ast.expr is None:
                if isinstance(param[2], AutoType): self.visitTask[0].type.return_type = VoidType(); param[2] = VoidType()
                if not isinstance(param[2], VoidType): raise TypeMismatchInStatement(ast)
            else:
                return_expression = self.visit(ast.expr, param[0])
                if isinstance(param[2], FloatType):
                    if not isinstance(return_expression, FloatType) and not isinstance(return_expression, IntegerType): raise TypeMismatchInStatement(ast)
                elif isinstance(param[2], AutoType):
                    param[2] = return_expression; self.visitTask[0].type.return_type = return_expression
                elif isinstance(return_expression, AutoType):
                    return_expression = param[2]; self.inferTypeForSymbol(ast.expr.name, param[2], isinstance(ast.expr, FuncCall), param[0])
                elif not compareType(param[2], return_expression): raise TypeMismatchInStatement(ast)
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
                if not compareType(firstElementType, currentElementType): raise IllegalArrayLiteral(fullAST)
            else: return ArrayType([len(ast.explist)], firstElementType) if not isinstance(firstElementType, ArrayType) else ArrayType([len(ast.explist)] + firstElementType.dimensions, firstElementType.typ)
        else: return ArrayType([0], AutoType()) 
    def visitArrayLit(self, ast, param): return self.arrayLiteralHelper(ast, ast, param)
    def visitArrayType(self, ast, param): return ArrayType(ast.dimensions, self.visit(ast.typ, param))
    def visitAutoType(self, ast, param): return AutoType()  
    def visitVoidType(self, ast, param): return VoidType()