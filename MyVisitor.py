from SDLVisitor import *
from SDLParser import SDLParser
import copy
import math


class SDLError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def print_msg(self):
        print(self.msg)


class MyVisitor(SDLVisitor):
    my_temp = {}
    my_func = {}
    build_func = ["lg", "ln", "sin", "cos", "tan", "asin", "acos", "atan", "read", "write"]

    def visitName_func(self, ctx:SDLParser.Name_funcContext):
        if self.my_func.get(ctx.ID(0).getText()) != None or ctx.ID(0).getText() in self.build_func:
            raise SDLError("Function '" + ctx.ID(0).getText() + "' is already defined in the scope")
        i = 1
        value = {}
        while ctx.ID(i) != None:
            value[i] = {'name': ctx.ID(i).getText(), 'type': ctx.TYPE(i - 1).getText()}
            i = i + 1
        self.my_func[ctx.ID(0).getText()] = {'stat': ctx.stat_block(), 'value': value}
        return

    def visitOp_func(self, ctx:SDLParser.Op_funcContext):
        if ctx.ID() != None:
            return ctx.ID().getText()
        elif ctx.expr() != None:
            return  self.visitExpr(ctx.expr())
        elif ctx.call_func() != None:
            return self.visitCall_func(ctx.call_func())

    def visitBuildFunc(self, name_func, op_func):
        if type(op_func) == "str" and self.my_temp.get(op_func) == None:
            raise NameError("'" + str(op_func) + "' is not defined")
        if name_func == 'read':
            if str(type(op_func)).split("'")[1] != "str":
                raise SDLError("Read function argument is variable name")
            tmp_input = str(input("Input: "))
            try:
                if self.my_temp.get(op_func)['type'] == 'int':
                    self.my_temp[op_func]['value'] = int(tmp_input)
                elif self.my_temp.get(op_func)['type'] == 'float':
                    self.my_temp[op_func]['value'] = float(tmp_input)
                elif self.my_temp.get(op_func)['type'] == 'bool':
                    self.my_temp[op_func]['value'] = bool(tmp_input)
            except Exception:
                raise SDLError("Incorrect input type")
            return
        if name_func == 'write':
            if str(type(op_func)).split("'")[1] == "str":
                if self.my_temp.get(op_func) == None:
                    raise NameError("'" + str(op_func) + "' is not defined")
                print(self.my_temp[op_func]['value'])
                return
            else:
                print(op_func)
                return
        if str(type(op_func)).split("'")[1] == "str":
            if self.my_temp.get(op_func)['type'] == 'bool':
                raise SDLError("Incorrect input type")
            else:
                if name_func == 'ln':
                    return math.log(self.my_temp.get(op_func)['value'])
                elif name_func == 'lg':
                    return math.log10(self.my_temp.get(op_func)['value'])
                elif name_func == 'sin':
                    return math.sin(self.my_temp.get(op_func)['value'])
                elif name_func == 'cos':
                    return math.cos(self.my_temp.get(op_func)['value'])
                elif name_func == 'tan':
                    return math.tan(self.my_temp.get(op_func)['value'])
                elif name_func == 'asin':
                    return math.asin(self.my_temp.get(op_func)['value'])
                elif name_func == 'acos':
                    return math.acos(self.my_temp.get(op_func)['value'])
                elif name_func == 'atan':
                    return math.atan(self.my_temp.get(op_func)['value'])
                return
        elif  str(type(op_func)).split("'")[1] == 'int'  or  str(type(op_func)).split("'")[1] == 'float':
            if name_func == 'ln':
                return math.log(op_func)
            elif name_func == 'lg':
                return math.log10(op_func)
            elif name_func == 'sin':
                return math.sin(op_func)
            elif name_func == 'cos':
                return math.cos(op_func)
            elif name_func == 'tan':
                return math.tan(op_func)
            elif name_func == 'asin':
                return math.asin(op_func)
            elif name_func == 'acos':
                return math.acos(op_func)
            elif name_func == 'atan':
                return math.atan(op_func)
            return
        else:
            raise SDLError("Incorrect input type")
        return

    def visitCall_func(self, ctx:SDLParser.Call_funcContext):
        if ctx.ID().getText() in self.build_func:
            if ctx.op_func(1) != None:
                raise SDLError("Function '" + ctx.ID().getText() + "' got too many arguments")
            return self.visitBuildFunc(ctx.ID().getText(), self.visitOp_func(ctx.op_func(0)))
        op_value = {}
        i = 0
        while ctx.op_func(i) != None:
            if ctx.AMPERSAND(i) == None:
                raise SDLError("Function '" + ctx.ID().getText() + "' got incorrect argument")
            op_value[i+1] = self.visitOp_func(ctx.op_func(i))
            i = i + 1
        self.visitUserFuncStat(ctx.ID().getText(), self.my_func[ctx.ID().getText()], op_value)
        return

    def visitUserFuncStat(self, name_func, func, op):
        tmp_variable_list = copy.copy(self.my_temp)
        for i in range(1, len(list(op.keys()))+1):
            if self.my_temp[op[i]]['type'] != func['value'][i]['type']:
                raise SDLError("Function '" + name_func + "' got incorrect argument")
            if self.my_temp.get(func['value'][i]['name']) != None:
                raise SDLError("Variable '" + func['value'][i]['name'] + "' is already defined in the scope")
            self.my_temp[func['value'][i]['name']] = {'type': func['value'][i]['type'], 'value': self.my_temp[op[i]]['value']}
        self.visitStat_block(func['stat'])
        for i in range(1, len(list(op.keys())) + 1):
            tmp_variable_list[op[i]]['value'] = self.my_temp[func['value'][i]['name']]['value']
        self.my_temp = copy.copy(tmp_variable_list)








    def visitStat_block(self, ctx:SDLParser.Stat_blockContext):
        tmp_variable_list = copy.copy(self.my_temp)
        self.visitChildren(ctx)
        self.my_temp = copy.copy(tmp_variable_list)
        return

    def visitComp_expr(self, ctx:SDLParser.Comp_exprContext):
        if ctx.AND() != None:
            return True if (self.visitComp_expr(ctx.comp_expr(0)) == True and self.visitComp_expr(ctx.comp_expr(1)) == True) else False
        elif ctx.OR() != None:
            return True if (self.visitComp_expr(ctx.comp_expr(0)) == True or self.visitComp_expr(ctx.comp_expr(1)) == True) else False
        elif ctx.LTEQ() != None:
            return True if self.visitExpr(ctx.expr(0)) <= self.visitExpr(ctx.expr(1)) else False
        elif ctx.GTEQ() != None:
            return True if self.visitExpr(ctx.expr(0)) >= self.visitExpr(ctx.expr(1)) else False
        elif ctx.GT() != None:
            return True if self.visitExpr(ctx.expr(0)) > self.visitExpr(ctx.expr(1)) else False
        elif ctx.LT() != None:
            return True if self.visitExpr(ctx.expr(0)) < self.visitExpr(ctx.expr(1)) else False
        elif ctx.EQ() != None:
            return True if self.visitExpr(ctx.expr(0)) == self.visitExpr(ctx.expr(1)) else False
        elif ctx.NEQ() != None:
            return True if self.visitExpr(ctx.expr(0)) != self.visitExpr(ctx.expr(1)) else False

    def visitWhile_stat(self, ctx: SDLParser.While_statContext):
        while self.visitComp_expr(ctx.comp_expr()):
            self.visitStat_block(ctx.stat_block())
        return

    def visitUntil_stat(self, ctx:SDLParser.Until_statContext):
        self.visitStat_block(ctx.stat_block())
        while self.visitComp_expr(ctx.comp_expr()):
            self.visitStat_block(ctx.stat_block())
        return

    def visitFor_stat(self, ctx:SDLParser.For_statContext):
        self.visitAssignment(ctx.assignment(0))
        while self.visitComp_expr(ctx.comp_expr()):
            self.visitStat_block(ctx.stat_block())
            self.visitAssignment(ctx.assignment(1))
        return

    def visitSwitch_stat(self, ctx:SDLParser.Switch_statContext):
        if self.my_temp.get(ctx.ID().getText()) == None:
            raise NameError("'" + str(ctx.ID()) + "' is not defined")
        if self.my_temp[ctx.ID().getText()]['value'] == None:
            raise SDLError("Variable '" + ctx.ID().getText() + "' has not value")
        i = 0
        while ctx.INTEGER(i) != None:
            if self.my_temp[ctx.ID().getText()]['value'] == int(ctx.INTEGER(i).getText()):
                self.visitStat_block(ctx.stat_block(i))
                return
            i = i + 1
        return

    def visitIf_stat(self, ctx:SDLParser.If_statContext):
        i = 0
        while ctx.comp_expr(i) != None:
            if self.visitComp_expr(ctx.comp_expr(i)) == True:
                self.visitStat_block(ctx.stat_block(i))
                return
            i = i + 1
        if ctx.ELSE() != None:
            self.visitStat_block(ctx.stat_block(i))
        return

    def visitAssignment(self, ctx:SDLParser.AssignmentContext):
        if ctx.TYPE() != None:
            if self.my_temp.get(ctx.ID().getText()) != None:
                raise SDLError("Variable '" + ctx.ID().getText() + "' is already defined in the scope")
            self.my_temp[ctx.ID().getText()] = {'type': ctx.TYPE().getText(), 'value': None}
            if ctx.expr() != None:
                expr = self.visitExpr(ctx.expr())
                if str(type(expr)).split("'")[1] != self.my_temp[ctx.ID().getText()]['type']:
                    if self.my_temp[ctx.ID().getText()]['type'] == 'int' and str(type(expr)).split("'")[1] == 'float':
                        self.my_temp[ctx.ID().getText()]['value'] = int(expr)
                        return
                    elif self.my_temp[ctx.ID().getText()]['type'] == 'float' and str(type(expr)).split("'")[1] == 'int':
                        self.my_temp[ctx.ID().getText()]['value'] = float(expr)
                        return
                    else:
                        raise TypeError("'" + str(ctx.ID()) + "' is not " + str(type(expr)))
                self.my_temp[ctx.ID().getText()] = {'type': ctx.TYPE().getText(), 'value': expr}
        else:
            if self.my_temp.get(ctx.ID().getText()) == None:
                raise NameError("'" + str(ctx.ID()) + "' is not defined")
            expr = self.visitExpr(ctx.expr())
            if str(type(expr)).split("'")[1] != self.my_temp[ctx.ID().getText()]['type']:
                if self.my_temp[ctx.ID().getText()]['type'] == 'int' and str(type(expr)).split("'")[1] == 'float':
                    self.my_temp[ctx.ID().getText()]['value'] = int(expr)
                    return
                elif self.my_temp[ctx.ID().getText()]['type'] == 'float' and str(type(expr)).split("'")[1] == 'int':
                    self.my_temp[ctx.ID().getText()]['value'] = float(expr)
                    return
                else:
                    raise TypeError("'" + str(ctx.ID()) + "' is not " + str(type(expr)))
            self.my_temp[ctx.ID().getText()]['value'] = expr
        return

    def visitExpr(self, ctx:SDLParser.ExprContext):
        if ctx.atom() != None:
            return self.visitAtom(ctx.atom())
        elif ctx.expr(1) == None:
            return -1 * self.visitExpr(ctx.expr(0))
        elif ctx.POW() != None:
            return self.visitExpr(ctx.expr(0)) ** self.visitExpr(ctx.expr(1))
        elif ctx.MULT() != None:
            return self.visitExpr(ctx.expr(0)) * self.visitExpr(ctx.expr(1))
        elif ctx.DIV() != None:
            return self.visitExpr(ctx.expr(0)) / self.visitExpr(ctx.expr(1))
        elif ctx.DOUBLEDIV() != None:
            return self.visitExpr(ctx.expr(0)) // self.visitExpr(ctx.expr(1))
        elif ctx.MOD() != None:
            return self.visitExpr(ctx.expr(0)) % self.visitExpr(ctx.expr(1))
        elif ctx.PLUS() != None:
            return self.visitExpr(ctx.expr(0)) + self.visitExpr(ctx.expr(1))
        elif ctx.MINUS() != None:
            return self.visitExpr(ctx.expr(0)) - self.visitExpr(ctx.expr(1))
        return self.visitChildren(ctx)

    def visitAtom(self, ctx:SDLParser.AtomContext):
        if ctx.expr() != None:
            return self.visitExpr(ctx.expr())
        elif ctx.INTEGER() != None:
            return int(ctx.INTEGER().getText())
        elif ctx.FLOAT() != None:
            return float(ctx.FLOAT().getText())
        elif ctx.BOOL() != None:
            return bool(ctx.BOOL().getText())
        elif ctx.ID() != None:
            return self.my_temp[ctx.ID().getText()]['value']