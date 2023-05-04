# Generated from main/mt22/parser/MT22.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MT22Parser import MT22Parser
else:
    from MT22Parser import MT22Parser

# This class defines a complete generic visitor for a parse tree produced by MT22Parser.

class MT22Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by MT22Parser#program.
    def visitProgram(self, ctx:MT22Parser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#program_body.
    def visitProgram_body(self, ctx:MT22Parser.Program_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#variable_declaration.
    def visitVariable_declaration(self, ctx:MT22Parser.Variable_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#variable_declaration_without_semi.
    def visitVariable_declaration_without_semi(self, ctx:MT22Parser.Variable_declaration_without_semiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#id_list.
    def visitId_list(self, ctx:MT22Parser.Id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#id_list_body.
    def visitId_list_body(self, ctx:MT22Parser.Id_list_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#function_declaration.
    def visitFunction_declaration(self, ctx:MT22Parser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#parameter_one.
    def visitParameter_one(self, ctx:MT22Parser.Parameter_oneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#nullable_parameter_list.
    def visitNullable_parameter_list(self, ctx:MT22Parser.Nullable_parameter_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#parameter_list.
    def visitParameter_list(self, ctx:MT22Parser.Parameter_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#parameter_list_body.
    def visitParameter_list_body(self, ctx:MT22Parser.Parameter_list_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#assign_statement.
    def visitAssign_statement(self, ctx:MT22Parser.Assign_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#if_statement.
    def visitIf_statement(self, ctx:MT22Parser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#for_statement.
    def visitFor_statement(self, ctx:MT22Parser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#while_statement.
    def visitWhile_statement(self, ctx:MT22Parser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#do_while_statement.
    def visitDo_while_statement(self, ctx:MT22Parser.Do_while_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#break_statement.
    def visitBreak_statement(self, ctx:MT22Parser.Break_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#continue_statement.
    def visitContinue_statement(self, ctx:MT22Parser.Continue_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#return_statement.
    def visitReturn_statement(self, ctx:MT22Parser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#call_statement.
    def visitCall_statement(self, ctx:MT22Parser.Call_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#block_statement.
    def visitBlock_statement(self, ctx:MT22Parser.Block_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#block_statement_body.
    def visitBlock_statement_body(self, ctx:MT22Parser.Block_statement_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#statement.
    def visitStatement(self, ctx:MT22Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#expression.
    def visitExpression(self, ctx:MT22Parser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#relational_expression.
    def visitRelational_expression(self, ctx:MT22Parser.Relational_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#logical_expression.
    def visitLogical_expression(self, ctx:MT22Parser.Logical_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#additive_expression.
    def visitAdditive_expression(self, ctx:MT22Parser.Additive_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#multiplicative_expression.
    def visitMultiplicative_expression(self, ctx:MT22Parser.Multiplicative_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#not_expression.
    def visitNot_expression(self, ctx:MT22Parser.Not_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#sign_expression.
    def visitSign_expression(self, ctx:MT22Parser.Sign_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#index_expression.
    def visitIndex_expression(self, ctx:MT22Parser.Index_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#operand.
    def visitOperand(self, ctx:MT22Parser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#nullable_expression_list.
    def visitNullable_expression_list(self, ctx:MT22Parser.Nullable_expression_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#expression_list.
    def visitExpression_list(self, ctx:MT22Parser.Expression_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#expression_list_body.
    def visitExpression_list_body(self, ctx:MT22Parser.Expression_list_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#index_operation.
    def visitIndex_operation(self, ctx:MT22Parser.Index_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#function_call.
    def visitFunction_call(self, ctx:MT22Parser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#primitive_lit.
    def visitPrimitive_lit(self, ctx:MT22Parser.Primitive_litContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#arraylit.
    def visitArraylit(self, ctx:MT22Parser.ArraylitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#array_type.
    def visitArray_type(self, ctx:MT22Parser.Array_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#intlit_list.
    def visitIntlit_list(self, ctx:MT22Parser.Intlit_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#intlit_list_body.
    def visitIntlit_list_body(self, ctx:MT22Parser.Intlit_list_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#variable_type_without_void.
    def visitVariable_type_without_void(self, ctx:MT22Parser.Variable_type_without_voidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#variable_type.
    def visitVariable_type(self, ctx:MT22Parser.Variable_typeContext):
        return self.visitChildren(ctx)



del MT22Parser