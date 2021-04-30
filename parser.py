from compiler import Scanner
from First import first
from Follow import follow
from anytree import Node, RenderTree


class Parser:
    my_scanner = None
    lookahead = None
    cpl_token = None

    illigal_error = 'illegal lookahead on line N'
    missing_error = 'missing Statement on line N'
    syn_err_l = []


    def __init__(self, input):
        self.my_scanner = Scanner(input)
        self.next_token()
        self.root = Node("Program")
        self.Program_sub(self.root)

    def next_token(self):
        self.cpl_token = self.my_scanner.get_next_token()

        if not self.cpl_token==None:
            if self.cpl_token[0]=='NUM' or self.cpl_token[0]=='ID':
                self.lookahead=self.cpl_token[0]
            elif self.cpl_token == '$':
                self.lookahead = '$'
            else:
                self.lookahead = self.cpl_token[1]



    def match(self, node, exp_token):

        if self.lookahead == exp_token:
            temp = Node(self.cpl_token, node)
            if not self.lookahead=='$':
                self.next_token()


    ###### write subroutine for each N.T:

    def Program_sub(self, node):
        if self.lookahead in first['Program']:
            temp = Node("Declaration-list", node)
            self.Declaration_list_sub(temp)
            self.match(node, '$')
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)

    def Declaration_list_sub(self, node):

        if self.lookahead in first['Declaration']:
            temp1 = Node("Declaration", parent=node)
            self.Declaration_sub(temp1)
            temp2 = Node("Declaration-list", parent=node)
            self.Declaration_list_sub(temp2)
            ##
        elif self.lookahead in follow['Declaration']:
            temp = Node("epsilon", node)
        ## handle tree
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Declaration_list_sub(node)

    def Declaration_sub(self, node):
        if self.lookahead in first['Declaration-initial']:
            temp1 = Node("Declaration-initial", parent=node)
            self.Declaration_initial_sub(temp1)
            temp2 = Node("Declaration-prime", parent=node)
            self.Declaration_prime_sub(temp2)

        elif self.lookahead in follow['Declaration']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Declaration")


        elif self.lookahead == '$':

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Declaration_sub(node)

    def Declaration_initial_sub(self, node):
        if self.lookahead in first['Type-specifier']:
            temp1 = Node("Type-specifier", parent=node)
            self.Type_specifier(temp1)
            self.match(node, 'ID')

        elif self.lookahead in follow['Declaration-initial']:

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Declaration")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            # error
            self.syn_err_l.append(self.my_scanner.line_num + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Declaration_initial_sub(node)

    def Declaration_prime_sub(self, node):
        if self.lookahead in first['Fun-declaration-prime']:
            # change node
            temp1 = Node("Fun-declaration-prime", parent=node)
            self.Fun_declaration_prime_sub(temp1)
        elif self.lookahead in first['Var-declaration-prime']:
            # change node
            temp2 = Node("Var-declaration-prime", parent=node)
            self.Var_declaration_prime_sub(temp2)
        elif self.lookahead in follow['Declaration-prime']:
            # missing error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Declaration-prime")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Declaration_prime_sub(node)

    def Var_declaration_prime_sub(self, node):
        if self.lookahead == ';':
            # change node
            self.match(node, ';')
        elif self.lookahead == '[':
            # change node
            self.match(node, '[')
            self.match(node, 'NUM')
            self.match(node, ']')
            self.match(node, ';')

        elif self.lookahead in follow['Var-declaration-prime']:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Var-Declaration-prime")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_declaration_prime_sub(node)

    def Fun_declaration_prime_sub(self, node):
        if self.lookahead == '(':
            self.match(node, '(')
            temp = Node("Params", node)
            self.Params_sub(temp)
            self.match(node, ')')
            temp = Node("Compound-stmt", node)
            self.Compound_stmt_sub(temp)

        elif self.lookahead in follow['Fun-declaration-prime']:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Fun-Declaration-prime")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Fun_declaration_prime_sub(node)

    def Type_specifier(self, node):
        if self.lookahead == 'int':
            # change node
            self.match(node, 'int')
        elif self.lookahead == 'void':
            # change node
            self.match(node, 'void')
        elif self.lookahead in follow['Type-specifier']:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Type-specifier")

        elif self.lookahead == '$':

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            #
            self.Type_specifier(node)

    def Params_sub(self, node):   ## check it
        if self.lookahead == 'int':
            # change node
            self.match(node, 'int')
            self.match(node, 'ID')
            # call subs of param prime & param list
            self.Param_prime_sub(node)
            self.Param_list(node)
        elif self.lookahead == 'void':

            self.match(node, 'void')
            # call sub of aram-list-void-abtar
            temp = Node('Param_list_void_abtar', node)
            self.Param_list_void_abtar(temp)
        elif self.lookahead in follow['Params']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Params")
        elif self.lookahead == '$':

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            # error
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Params_sub(node)

    def Param_list_void_abtar(self, node):
        if self.lookahead in first['Param-list-void-abtar']:
            self.match(node, "ID")
            temp = Node("Param-prime", node)
            self.Param_prime_sub(temp)
            temp = Node("Param-list", node)
            self.Param_list(temp)

        elif self.lookahead in follow['Param-list-void-abtar']:
            # node epsilon
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Param_list_void_abtar(node)

    def Param_list(self, node):
        if self.lookahead == ',':
            temp = Node("Param", node)
            self.Param_sub(temp)
            temp = Node("Param-list", node)
            self.Param_list(temp)
        elif self.lookahead in follow['Param-list']:
            # node epsilon
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Param_list(node)

    def Param_sub(self, node):
        if self.lookahead in first['Param']:
            temp = Node("Declaration-initial", node)
            self.Declaration_initial_sub(temp)
            temp = Node("Param-prime", node)

            self.Param_prime_sub(temp)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Param_sub(node)

    def Param_prime_sub(self, node):
        if self.lookahead == '[':
            # node
            self.match(node, '[')
            self.match(node, ']')
        elif self.lookahead in follow['Param-prime']:
            #TODO
            print("what?")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        # error + termn
        else:
            # error
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Param_prime_sub(node)

    def Compound_stmt_sub(self, node):
        if self.lookahead == '{':
            # node
            self.match(node, '{')
            temp1 = Node("Declaration-list", node)
            self.Declaration_list_sub(temp1)
            temp2 = Node("Statement-list", node)
            self.Statement_list_sub(temp2)
            self.match(node, '}')
        elif self.lookahead in follow['Compound-stmt']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Compound-stmt")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Compound_stmt_sub(node)

    def Statement_list_sub(self, node):
        if self.lookahead in first['Statement']:

            temp2 = Node("Statement", node)
            self.Statement_sub(temp2)

            temp1 = Node("Statement-list", node)
            self.Statement_list_sub(temp1)

        elif self.lookahead in follow['Statement-list']:
            temp = Node("epsilon", node)

        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Statement_list_sub(node)

    def Statement_sub(self, node):
        if self.lookahead in first['Statement']:
            if self.lookahead in first['Expression-stmt']:
                temp2 = Node("Expression-stmt", node)
                self.Expression_stmt_sub(temp2)
            elif self.lookahead in first['Compound-stmt']:
                temp2 = Node("Compound-stmt", node)
                self.Compound_stmt_sub(temp2)
            elif self.lookahead in first['Selection-stmt']:
                temp2 = Node("Selection-stmt", node)
                self.Selection_stmt_sub(temp2)
            elif self.lookahead in first['Iteration-stmt']:
                temp2 = Node("Iteration-stmt", node)
                self.Iteration_stmt_sub(temp2)
            elif self.lookahead in first['Return-stmt']:
                temp2 = Node("Return-stmt", node)
                self.Return_stmt_sub(temp2)
            elif self.lookahead in first['For-stmt']:
                temp2 = Node("For-stmt", node)
                self.For_stmt_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Statement_sub(node)

    def Expression_stmt_sub(self, node):
        if self.lookahead in first['Expression-stmt']:
            if self.lookahead == ';':
                self.match(node, ';')
            elif self.lookahead == 'break':
                self.match(node, 'break')
                self.match(node, ';')
            else:
                temp2 = Node("Expression", node)
                self.Expression_sub(temp2)
                self.match(node, ';')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Expression_stmt_sub(node)

    def Selection_stmt_sub(self, node):
        if self.lookahead == 'if':
            self.match(node, 'if')
            self.match(node, '(')
            temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(node, ')')
            temp2 = Node("Statement", node)
            self.Statement_sub(temp2)
            self.match(node, 'else')
            temp3 = Node("Statement", node)
            self.Statement_sub(temp3)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Selection_stmt_sub(node)

    def Iteration_stmt_sub(self, node):
        if self.lookahead == 'while':
            self.match(node, 'while')
            self.match(node, '(')
            temp = Node("Expression", node)
            self.Expression_sub(temp)
            self.match(node, ')')
            temp3 = Node("Statement", node)
            self.Statement_sub(temp3)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Iteration_stmt_sub(node)

    def Return_stmt_sub(self, node):
        if self.lookahead == 'return':
            self.match(node, 'return')
            temp = Node("Return-stmt-prime", node)
            self.Return_stmt_prime_sub(temp)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Return_stmt_sub(node)

    def Return_stmt_prime_sub(self, node):
        if self.lookahead == ';':
            self.match(node, ";")
        elif self.lookahead in first['Return-stmt-prime']:
            temp = Node("Expression", node)
            self.Expression_sub(temp)
            self.match(node, ';')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Return_stmt_prime_sub(node)

    def For_stmt_sub(self, node):
        if self.lookahead == 'for':
            self.match(node, 'for')
            self.match(node, 'ID')
            self.match(node, '=')
            temp = Node("Vars", node)
            self.Vars_sub(temp)
            temp2 = Node("Statement", node)
            self.Statement_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.For_stmt_sub(node)

    def Vars_sub(self, node):
        if self.lookahead in first['Vars']:
            temp1 = Node("Vars", node)
            self.Var_sub(temp1)
            temp2 = Node("Var-zegond", node)
            self.Var_zegond_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_sub(node)

    def Var_zegond_sub(self, node):
        if self.lookahead == ',':
            self.match(node, ',')
            temp1 = Node("Var", node)
            self.Var_sub(temp1)
            temp2 = Node("Var_zegond", node)
            self.Var_zegond_sub(temp2)
        elif self.lookahead in follow['Var-zegond']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_zegond_sub(node)

    def Var_sub(self, node):
        if self.cpl_token[0] == 'ID':
            self.match(node, 'ID')
            temp1 = Node("Var-prime", node)
            self.Var_prime_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_sub(node)

    def Expression_sub(self, node):
        if self.cpl_token[0] == 'ID':
            self.match(node, 'ID')
            temp1 = Node("B", node)
            self.B_sub(temp1)
        elif self.lookahead in first['Expression']:
            temp2 = Node("Simple-expression-zegond", node)
            self.Simple_expression_zegond(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Expression_sub(node)

    def B_sub(self, node):
        if self.lookahead == '=':
            self.match(node, '=')
            temp2 = Node("Expression", node)
            self.Expression_sub(temp2)
        elif self.lookahead == '[':
            self.match(node, '[')
            temp2 = Node("Expression", node)
            self.Expression_sub(temp2)
            self.match(node, ']')
            temp2 = Node("H", node)
            self.H_sub(temp2)
        elif self.lookahead in first['B'] or self.lookahead in follow['B']:
            temp2 = Node("Simple-expression-prime", node)
            self.Simple_expression_prime_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.B_sub(node)

    def H_sub(self, node):
        if self.lookahead == '=':
            self.match(node, '=')
            temp2 = Node("Expression", node)
            self.Expression_sub(temp2)
        elif self.lookahead in first['H'] or self.lookahead in follow['H']:
            temp2 = Node("G", node)
            self.G_sub(temp2)
            temp2 = Node("D", node)
            self.D_sub(temp2)
            temp2 = Node("C", node)
            self.C_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.H_sub(node)

    def Simple_expression_zegond(self, node):
        if self.lookahead in first['Simple-expression-zegond']:
            temp1 = Node("Additive-expression-zegond", node)
            self.Additive_expression_zegond_sub(temp1)
            temp2 = Node("C", node)
            self.C_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Simple_expression_zegond(node)

    def Simple_expression_prime_sub(self, node):
        if self.lookahead in first['Simple-expression-prime'] or self.lookahead in follow['Simple-expression-prime']:
            temp1 = Node("Additive-expression-prime", node)
            self.Additive_expression_prime_sub(temp1)
            temp1 = Node("C", node)
            self.C_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Simple_expression_prime_sub(node)

    def C_sub(self, node):
        if self.lookahead in first['C']:
            temp1 = Node("Relop", node)
            self.Relop_sub(temp1)
            temp1 = Node("Additive-expression", node)
            self.Additive_expression(temp1)
        elif self.lookahead in follow['C']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.C_sub(node)

    def Relop_sub(self, node):
        if self.lookahead == '<':
            self.match(node, '<')
        elif self.lookahead == "==":
            self.match(node, '==')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Relop_sub(node)

    def Additive_expression(self, node):
        if self.lookahead in first['Additive-expression']:
            temp1 = Node("Term", node)
            self.Term_sub(temp1)
            temp2 = Node("D", node)
            self.D_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Additive_expression(node)

    def Additive_expression_prime_sub(self, node):
        if self.lookahead in first['Additive-expression-prime'] or self.lookahead in follow['Additive-expression-prime']:
            temp1 = Node("Term-prime", node)
            self.Term_prime_sub(temp1)
            temp2 = Node("D", node)
            self.D_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Additive_expression_prime_sub(node)

    def Additive_expression_zegond_sub(self, node):
        if self.lookahead in first['Additive-expression-zegond']:
            temp1 = Node("Term-zegond", node)
            self.Term_zegond_sub(temp1)
            temp2 = Node("D", node)
            self.D_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Additive_expression_zegond_sub(node)

    def D_sub(self, node):
        if self.lookahead in first['D']:
            temp1 = Node("Addop", node)
            self.Addop_sub(temp1)
            temp2 = Node("Term", node)
            self.Term_sub(temp2)
            temp3 = Node("D", node)
            self.D_sub(temp3)

        elif self.lookahead in follow['D']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.D_sub(node)

    def Addop_sub(self, node):
        if self.lookahead == '+':
            self.match(node, '+')
        elif self.lookahead == '-':
            self.match(node, '-')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Addop_sub(node)

    def Term_sub(self, node):
        if self.lookahead in first['Term']:
            temp1 = Node("Signed-factor", node)
            self.Signed_factor_sub(temp1)
            temp2 = Node("G", node)
            self.G_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Term_sub(node)

    def Term_prime_sub(self, node):
        # ?????????????????????????????
        if self.lookahead in first['Term-prime'] or self.lookahead in follow['Term-prime']:
            temp1 = Node("Signed-factor-prime", node)
            self.Signed_factor_prime_sub(temp1)
            temp2 = Node("G", node)
            self.G_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Term_prime_sub(node)

    def Term_zegond_sub(self, node):
        if self.lookahead in first['Term-zegond']:
            temp1 = Node("Signed-factor-zegond", node)
            self.Signed_factor_zegond_sub(temp1)
            temp2 = Node("G", node)
            self.G_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Term_zegond_sub(node)

    def G_sub(self, node):
        if self.lookahead == '*':
            self.match(node, '*')
            temp1 = Node("Signed-factor", node)
            self.Signed_factor_sub(temp1)
            temp2 = Node("G", node)
            self.G_sub(temp2)
        elif self.lookahead in follow['G']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.G_sub(node)

    def Signed_factor_sub(self, node):
        if self.lookahead in first['Signed-factor']:
            if self.lookahead == '+':
                self.match(node, '+')
                temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            elif self.lookahead == '-':
                self.match(node, '-')
                temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            else:
                temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Signed_factor_sub(node)

    def Signed_factor_prime_sub(self, node):
        if self.lookahead in first['Signed-factor-prime'] or self.lookahead in follow['Signed-factor-prime']:
            temp1 = Node("Factor-prime", node)
            self.Factor_prime_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Signed_factor_prime_sub(node)

    def Signed_factor_zegond_sub(self, node):
        if self.lookahead in first["Signed-factor-zegond"]:
            if self.lookahead == '+':
                self.match(node, '+')
                temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            elif self.lookahead == '-':
                self.match(node, '-')
                temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            else:
                temp1 = Node("Factor-zegond", node)
                self.Factor_zegond_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Signed_factor_zegond_sub(node)

    def Factor_sub(self, node):
        if self.lookahead == '(':
            self.match(node, '(')
            temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(node, ')')
        elif self.cpl_token[0] == "ID":
            self.match(node, "ID")
            temp1 = Node("Var-call-prime", node)
            self.Var_call_prime_sub(temp1)
        elif self.cpl_token[0] == 'NUM':
            self.match(node, 'NUM')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Factor_sub(node)

    def Var_call_prime_sub(self, node):
        if self.lookahead == '(':
            self.match(node, '(')
            temp1 = Node("Args", node)
            self.Args_sub(temp1)
            self.match(node, ')')
        elif self.lookahead in first['Var-call-prime'] or self.lookahead in follow['Var-call-prime']:
            temp1 = Node("Var-prime", node)
            self.Var_prime_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_call_prime_sub(node)

    def Var_prime_sub(self, node):
        if self.lookahead == '[':
            self.match(node, '[')
            temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(node, ']')
        elif self.lookahead in follow['Var-prime']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_prime_sub(node)

    def Factor_prime_sub(self, node):
        if self.lookahead == '(':
            self.match(node, '(')
            temp1 = Node("Args", node)
            self.Args_sub(temp1)
            self.match(node, ')')
        elif self.lookahead in follow['Factor-prime']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Factor_prime_sub(node)

    def Factor_zegond_sub(self, node):
        if self.cpl_token[0] == 'NUM':
            self.match(node, 'NUM')
        elif self.lookahead == '(':
            self.match(node, '(')
            temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(node, ')')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Factor_zegond_sub(node)

    def Args_sub(self, node):
        if self.lookahead in first['Args']:
            temp1 = Node("Arg-list", node)
            self.Arg_list_sub(temp1)
        elif self.lookahead in follow['Args']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Args_sub(node)

    def Arg_list_sub(self, node):
        if self.lookahead in first['Arg-list']:
            temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            temp1 = Node("Arg-list-prime", node)
            self.Arg_list_prime_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Arg_list_sub(node)

    def Arg_list_prime_sub(self, node):
        if self.lookahead in first['Arg-list-prime']:
            self.match(node, ',')
            temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            temp1 = Node("Arg-list-prime", node)
            self.Arg_list_prime_sub(temp1)
        elif self.lookahead in follow['Arg-list-prime']:
            temp = Node("epsilon", node)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Arg_list_prime_sub(node)


parser = Parser('./input.txt')

for pre, fill, node in RenderTree(parser.root):
    print("%s%s" % (pre, node.name))

#with open("syntax_errors.txt", "w") as file:
for l in parser.syn_err_l:
    print(l)
#print(parser.syn_err_l)