# Name: Thái Tài
# ID: 2052246

from MT22Visitor import MT22Visitor
from MT22Parser import MT22Parser
from AST import *


class ASTGeneration(MT22Visitor):
    def visitProgram(self, ctx: MT22Parser.ProgramContext):
        if ctx.variable_declaration(): return Program(self.visit(ctx.variable_declaration()) + self.visit(ctx.program_body()))
        elif ctx.function_declaration(): return Program([self.visit(ctx.function_declaration())] + self.visit(ctx.program_body()))

    def visitProgram_body(self, ctx: MT22Parser.Program_bodyContext):
        if ctx.variable_declaration(): return self.visit(ctx.variable_declaration()) + self.visit(ctx.program_body())
        elif ctx.function_declaration(): return [self.visit(ctx.function_declaration())] + self.visit(ctx.program_body())
        else: return []
    
    def visitVariable_declaration(self, ctx: MT22Parser.Variable_declarationContext):
        if ctx.id_list(): return list(map(lambda ele: VarDecl(ele, self.visit(ctx.variable_type_without_void())), self.visit(ctx.id_list())))
        else:
            lst = self.visit(ctx.variable_declaration_without_semi())
            typ = lst[-1]
            lst = lst[:-1]
            id, exp = [], []
            for i in range(0, len(lst) - 1, 2):
                id.append(lst[i])
                exp.append(lst[i + 1])
            exp = exp[::-1]
            return list(map(lambda identifier, expression: VarDecl(identifier, typ, expression), id, exp))

    def visitVariable_declaration_without_semi(self, ctx: MT22Parser.Variable_declaration_without_semiContext):
        if ctx.variable_declaration_without_semi(): return [ctx.IDENTIFIER().getText()] + [self.visit(ctx.expression())] + self.visit(ctx.variable_declaration_without_semi())
        else: return [ctx.IDENTIFIER().getText()] + [self.visit(ctx.expression())] + [self.visit(ctx.variable_type_without_void())]
    
    def visitId_list(self, ctx: MT22Parser.Id_listContext):
        if ctx.id_list_body(): return [(ctx.IDENTIFIER().getText())] + self.visit(ctx.id_list_body())
        else: return [(ctx.IDENTIFIER().getText())]
    
    def visitId_list_body(self, ctx: MT22Parser.Id_list_bodyContext):
        if ctx.id_list_body(): return [(ctx.IDENTIFIER().getText())] + self.visit(ctx.id_list_body())
        else: return []
    
    def visitFunction_declaration(self, ctx: MT22Parser.Function_declarationContext):
        if ctx.INHERIT(): return FuncDecl(ctx.IDENTIFIER(0).getText(),self.visit(ctx.variable_type()),self.visit(ctx.nullable_parameter_list()),ctx.IDENTIFIER(1).getText(),self.visit(ctx.block_statement()))
        else: return FuncDecl(ctx.IDENTIFIER(0).getText(),self.visit(ctx.variable_type()),self.visit(ctx.nullable_parameter_list()),None,self.visit(ctx.block_statement()))
    
    def visitParameter_one(self, ctx: MT22Parser.Parameter_oneContext):
        if ctx.INHERIT():
            if ctx.OUT(): return ParamDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.variable_type_without_void()), bool(True), bool(True))
            else: return ParamDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.variable_type_without_void()), bool(False), bool(True))
        else:
            if ctx.OUT(): return ParamDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.variable_type_without_void()), bool(True), bool(False))
            else: return ParamDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.variable_type_without_void()), bool(False), bool(False))
    
    def visitNullable_parameter_list(self, ctx: MT22Parser.Nullable_parameter_listContext):
        if ctx.parameter_list_body(): return [self.visit(ctx.parameter_one())] + self.visit(ctx.parameter_list_body())
        else: return []

    def visitParameter_list(self, ctx: MT22Parser.Parameter_listContext):
        if ctx.parameter_list_body(): return [self.visit(ctx.parameter_one())] + self.visit(ctx.parameter_list_body())
        else: return [self.visit(ctx.parameter_one())]
    
    def visitParameter_list_body(self, ctx: MT22Parser.Parameter_list_bodyContext):
        if ctx.parameter_list_body(): return [self.visit(ctx.parameter_one())] + self.visit(ctx.parameter_list_body())
        else: return []
    
    def visitAssign_statement(self, ctx: MT22Parser.Assign_statementContext):
        if ctx.IDENTIFIER(): return AssignStmt(Id(ctx.IDENTIFIER().getText()),self.visit(ctx.expression()))
        else: return AssignStmt(self.visit(ctx.index_operation()),self.visit(ctx.expression()))
    
    def visitIf_statement(self, ctx: MT22Parser.If_statementContext):
        if ctx.ELSE(): return IfStmt(self.visit(ctx.expression()),self.visit(ctx.statement(0)),self.visit(ctx.statement(1)))
        else: return IfStmt(self.visit(ctx.expression()),self.visit(ctx.statement(0)))

    def visitFor_statement(self, ctx: MT22Parser.For_statementContext):
        if ctx.IDENTIFIER(): return ForStmt(AssignStmt(Id(ctx.IDENTIFIER().getText()),self.visit(ctx.expression(0))),self.visit(ctx.expression(1)),self.visit(ctx.expression(2)),self.visit(ctx.statement()))
        else: return ForStmt(AssignStmt(self.visit(ctx.index_operation()),self.visit(ctx.expression(0))),self.visit(ctx.expression(1)),self.visit(ctx.expression(2)),self.visit(ctx.statement()))

    def visitWhile_statement(self, ctx: MT22Parser.While_statementContext):
        return WhileStmt(self.visit(ctx.expression()),self.visit(ctx.statement()))
    
    def visitDo_while_statement(self, ctx: MT22Parser.Do_while_statementContext):
        return DoWhileStmt(self.visit(ctx.expression()),self.visit(ctx.block_statement()))
    
    def visitBreak_statement(self, ctx: MT22Parser.Break_statementContext):
        return BreakStmt()
    
    def visitContinue_statement(self, ctx: MT22Parser.Continue_statementContext):
        return ContinueStmt()
    
    def visitReturn_statement(self, ctx: MT22Parser.Return_statementContext):
        if ctx.expression(): return ReturnStmt(self.visit(ctx.expression()))
        else: return ReturnStmt()
    
    def visitCall_statement(self, ctx: MT22Parser.Call_statementContext):
        return CallStmt(ctx.IDENTIFIER().getText(),self.visit(ctx.nullable_expression_list()))
    
    def visitBlock_statement(self, ctx: MT22Parser.Block_statementContext):
        return BlockStmt(self.visit(ctx.block_statement_body()))
    
    def visitBlock_statement_body(self, ctx: MT22Parser.Block_statement_bodyContext):
        if ctx.statement(): return [self.visit(ctx.statement())] + self.visit(ctx.block_statement_body())
        elif ctx.variable_declaration(): return self.visit(ctx.variable_declaration()) + self.visit(ctx.block_statement_body()) 
        else: return []
    
    def visitStatement(self, ctx: MT22Parser.StatementContext):
        if ctx.assign_statement(): return self.visit(ctx.assign_statement())
        elif ctx.if_statement(): return self.visit(ctx.if_statement())
        elif ctx.for_statement(): return self.visit(ctx.for_statement())
        elif ctx.while_statement(): return self.visit(ctx.while_statement())
        elif ctx.do_while_statement(): return self.visit(ctx.do_while_statement())
        elif ctx.return_statement(): return self.visit(ctx.return_statement())
        elif ctx.call_statement(): return self.visit(ctx.call_statement())
        elif ctx.block_statement(): return self.visit(ctx.block_statement())
        elif ctx.break_statement(): return self.visit(ctx.break_statement())
        elif ctx.continue_statement(): return self.visit(ctx.continue_statement())
    
    def visitExpression(self, ctx: MT22Parser.ExpressionContext):
        if ctx.CONCATENATE(): return BinExpr(ctx.CONCATENATE().getText(),self.visit(ctx.relational_expression(0)),self.visit(ctx.relational_expression(1)))
        else: return self.visit(ctx.relational_expression(0))
    
    def visitRelational_expression(self, ctx: MT22Parser.Relational_expressionContext):
        if ctx.EQUAL(): return BinExpr(ctx.EQUAL().getText(),self.visit(ctx.logical_expression(0)),self.visit(ctx.logical_expression(1)))
        elif ctx.NOT_EQUAL(): return BinExpr(ctx.NOT_EQUAL().getText(),self.visit(ctx.logical_expression(0)),self.visit(ctx.logical_expression(1)))
        elif ctx.SMALL(): return BinExpr(ctx.SMALL().getText(),self.visit(ctx.logical_expression(0)),self.visit(ctx.logical_expression(1)))
        elif ctx.LARGE(): return BinExpr(ctx.LARGE().getText(),self.visit(ctx.logical_expression(0)),self.visit(ctx.logical_expression(1)))
        elif ctx.SMALL_EQUAL(): return BinExpr(ctx.SMALL_EQUAL().getText(),self.visit(ctx.logical_expression(0)),self.visit(ctx.logical_expression(1)))
        elif ctx.LARGE_EQUAL(): return BinExpr(ctx.LARGE_EQUAL().getText(),self.visit(ctx.logical_expression(0)),self.visit(ctx.logical_expression(1)))
        else: return self.visit(ctx.logical_expression(0))
    
    def visitLogical_expression(self, ctx: MT22Parser.Logical_expressionContext):
        if ctx.AND(): return BinExpr(ctx.AND().getText(),self.visit(ctx.logical_expression()),self.visit(ctx.additive_expression()))
        elif ctx.OR(): return BinExpr(ctx.OR().getText(),self.visit(ctx.logical_expression()),self.visit(ctx.additive_expression()))
        else: return self.visit(ctx.additive_expression())
    
    def visitAdditive_expression(self, ctx: MT22Parser.Additive_expressionContext):
        if ctx.ADD(): return BinExpr(ctx.ADD().getText(),self.visit(ctx.additive_expression()),self.visit(ctx.multiplicative_expression()))
        elif ctx.SUBTRACT(): return BinExpr(ctx.SUBTRACT().getText(),self.visit(ctx.additive_expression()),self.visit(ctx.multiplicative_expression()))
        else: return self.visit(ctx.multiplicative_expression())
    
    def visitMultiplicative_expression(self, ctx: MT22Parser.Multiplicative_expressionContext):
        if ctx.MULTIPLY(): return BinExpr(ctx.MULTIPLY().getText(),self.visit(ctx.multiplicative_expression()),self.visit(ctx.not_expression()))
        elif ctx.DIVIDE(): return BinExpr(ctx.DIVIDE().getText(),self.visit(ctx.multiplicative_expression()),self.visit(ctx.not_expression()))
        elif ctx.MODULO(): return BinExpr(ctx.MODULO().getText(),self.visit(ctx.multiplicative_expression()),self.visit(ctx.not_expression()))
        else: return self.visit(ctx.not_expression())
    
    def visitNot_expression(self, ctx: MT22Parser.Not_expressionContext):
        if ctx.NOT(): return UnExpr(str(ctx.NOT().getText()),self.visit(ctx.not_expression()))
        elif ctx.sign_expression(): return self.visit(ctx.sign_expression())
    
    def visitSign_expression(self, ctx: MT22Parser.Sign_expressionContext):
        if ctx.SUBTRACT(): return UnExpr(str(ctx.SUBTRACT().getText()),self.visit(ctx.sign_expression()))
        elif ctx.index_expression(): return self.visit(ctx.index_expression())
    
    def visitIndex_expression(self, ctx: MT22Parser.Index_expressionContext):
        if ctx.index_operation(): return self.visit(ctx.index_operation())
        elif ctx.operand(): return self.visit(ctx.operand())
    
    def visitOperand(self, ctx: MT22Parser.OperandContext):
        if ctx.primitive_lit(): return self.visit(ctx.primitive_lit())
        elif ctx.function_call(): return self.visit(ctx.function_call())
        elif ctx.IDENTIFIER(): return Id(ctx.IDENTIFIER().getText())
        elif ctx.arraylit(): return self.visit(ctx.arraylit())
        elif ctx.expression(): return self.visit(ctx.expression())
    
    def visitNullable_expression_list(self, ctx: MT22Parser.Nullable_expression_listContext):
        if ctx.expression_list_body(): return [self.visit(ctx.expression())] + self.visit(ctx.expression_list_body())
        else: return []
    
    def visitExpression_list(self, ctx: MT22Parser.Expression_listContext):
        if ctx.expression_list_body(): return [self.visit(ctx.expression())] + self.visit(ctx.expression_list_body())
        else: return [self.visit(ctx.expression())]
    
    def visitExpression_list_body(self, ctx: MT22Parser.Expression_list_bodyContext):
        if ctx.expression_list_body(): return [self.visit(ctx.expression())] + self.visit(ctx.expression_list_body())
        else: return []
    
    def visitIndex_operation(self, ctx: MT22Parser.Index_operationContext):
        return ArrayCell(ctx.IDENTIFIER().getText(),self.visit(ctx.expression_list()))
    
    def visitFunction_call(self, ctx: MT22Parser.Function_callContext):
        return FuncCall(ctx.IDENTIFIER().getText(),self.visit(ctx.nullable_expression_list()))
    
    def toBool(self, x):
        return x == "true"
    
    def toFloat(self, x):
        if x[0] == '.' and (x[1] == 'e' or x[1] == 'E'):
            return 0.0
        return float(x)

    def visitPrimitive_lit(self, ctx: MT22Parser.Primitive_litContext):
        if ctx.INTEGER_LIT(): return IntegerLit(int(ctx.INTEGER_LIT().getText()))
        elif ctx.FLOAT_LIT(): return FloatLit(self.toFloat(ctx.FLOAT_LIT().getText()))
        elif ctx.BOOLEAN_LIT(): return BooleanLit(self.toBool(ctx.BOOLEAN_LIT().getText()))
        elif ctx.STRING_LIT(): return StringLit(str(ctx.STRING_LIT().getText()))
    
    def visitArraylit(self, ctx: MT22Parser.ArraylitContext):
        return ArrayLit(self.visit(ctx.nullable_expression_list()))
    
    def visitArray_type(self, ctx: MT22Parser.Array_typeContext):
        if ctx.INTEGER(): return ArrayType(self.visit(ctx.intlit_list()), IntegerType())
        elif ctx.FLOAT(): return ArrayType(self.visit(ctx.intlit_list()), FloatType())
        elif ctx.BOOLEAN(): return ArrayType(self.visit(ctx.intlit_list()), BooleanType())
        elif ctx.STRING(): return ArrayType(self.visit(ctx.intlit_list()), StringType())
    
    def visitIntlit_list(self, ctx: MT22Parser.Intlit_listContext):
        if ctx.intlit_list_body(): return [int(ctx.INTEGER_LIT().getText())] + self.visit(ctx.intlit_list_body())
        else: return [int(ctx.INTEGER_LIT().getText())]
    
    def visitIntlit_list_body(self, ctx: MT22Parser.Intlit_list_bodyContext):
        if ctx.intlit_list_body(): return [int(ctx.INTEGER_LIT().getText())] + self.visit(ctx.intlit_list_body())
        else: return []
    
    def visitVariable_type_without_void(self, ctx: MT22Parser.Variable_type_without_voidContext):
        if ctx.INTEGER(): return IntegerType()
        elif ctx.FLOAT(): return FloatType()
        elif ctx.BOOLEAN(): return BooleanType()
        elif ctx.STRING(): return StringType()
        elif ctx.AUTO(): return AutoType()
        elif ctx.array_type(): return self.visit(ctx.array_type())
    
    def visitVariable_type(self, ctx: MT22Parser.Variable_typeContext):
        if ctx.variable_type_without_void(): return self.visit(ctx.variable_type_without_void())
        elif ctx.VOID(): return VoidType()
