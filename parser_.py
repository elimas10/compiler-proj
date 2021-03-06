from scanner import Scanner
from First import first
from Follow import follow
from anytree import Node, RenderTree


class Parser_:
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
            self.Declaration_list_sub(node)
            self.match(node, '$')
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)

    def Declaration_list_sub(self, node):

        if self.lookahead in first['Declaration']:
            temp = Node("Declaration-list", node)


#            temp1 = Node("Declaration", parent=node)
            self.Declaration_sub(temp)
           # temp2 = Node("Declaration-list", parent=node)
            self.Declaration_list_sub(temp)
            ##
        elif self.lookahead in follow['Declaration']:
            temp = Node("Declaration-list", node)
            temp2= Node("epsilon", temp)

        # elif self.lookahead == '$':
        #     self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Declaration_list_sub(node)

    def Declaration_sub(self, node):
        if self.lookahead in first['Declaration-initial']:
            temp1 = Node("Declaration", parent=node)

            #temp1 = Node("Declaration-initial", parent=node)
            self.Declaration_initial_sub(temp1)
            #temp2 = Node("Declaration-prime", parent=node)
            self.Declaration_prime_sub(temp1)

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
            temp1 = Node("Declaration-initial", parent=node)

            #temp1 = Node("Type-specifier", parent=node)
            self.Type_specifier(temp1)
            self.match(temp1, 'ID')

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
            temp2 = Node("Declaration-prime", parent=node)

            # change node
            #temp1 = Node("Fun-declaration-prime", parent=node)
            self.Fun_declaration_prime_sub(temp2)
        elif self.lookahead in first['Var-declaration-prime']:
            temp2 = Node("Declaration-prime", parent=node)
            # change node
            #temp2 = Node("Var-declaration-prime", parent=node)
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

            temp = Node("Var-declaration-prime", parent=node)
            # change node
            self.match(temp, ';')
        elif self.lookahead == '[':
            temp = Node("Var-declaration-prime", parent=node)
            # change node
            self.match(temp, '[')
            self.match(temp, 'NUM')
            self.match(temp, ']')
            self.match(temp, ';')

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
            temp = Node("Fun-declaration-prime", parent=node)

            self.match(temp, '(')
            #temp = Node("Params", node)
            self.Params_sub(temp)
            self.match(temp, ')')
            #temp = Node("Compound-stmt", node)
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

            temp = Node("Type-specifier", parent=node)
            # change node
            self.match(temp, 'int')
        elif self.lookahead == 'void':

            temp = Node("Type-specifier", parent=node)
            # change node
            self.match(temp, 'void')
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

    def Params_sub(self, node):
        if self.lookahead == 'int':

            temp = Node("Params", parent=node)
            # change node
            self.match(temp, 'int')
            self.match(temp, 'ID')
            # call subs of param prime & param list
            self.Param_prime_sub(node)
            self.Param_list(node)
        elif self.lookahead == 'void':
            temp = Node("Params", parent=node)


            self.match(temp, 'void')
            # call sub of aram-list-void-abtar
            #temp = Node('Param_list_void_abtar', node)
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
            temp = Node('Param-list-void-abtar', node)

            self.match(temp, "ID")
            #temp = Node("Param-prime", node)
            self.Param_prime_sub(temp)
            #temp = Node("Param-list", node)
            self.Param_list(temp)

        elif self.lookahead in follow['Param-list-void-abtar']:
            # node epsilon
            temp = Node('Param-list-void-abtar', node)
            temp2 = Node("epsilon", temp)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Param_list_void_abtar(node)

    def Param_list(self, node):
        if self.lookahead == ',':
            temp = Node("Param-list", node)

            #temp = Node("Param", node)
            self.Param_sub(temp)
            #temp = Node("Param-list", node)
            self.Param_list(temp)
        elif self.lookahead in follow['Param-list']:
            # node epsilon
            temp = Node("Param-list", node)
            temp2 = Node("epsilon", temp)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Param_list(node)

    def Param_sub(self, node):
        if self.lookahead in first['Param']:
            temp = Node("Param", node)

            #temp = Node("Declaration-initial", node)
            self.Declaration_initial_sub(temp)
            #temp = Node("Param-prime", node)

            self.Param_prime_sub(temp)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Param_sub(node)

    def Param_prime_sub(self, node):
        if self.lookahead == '[':
            temp = Node("Param-prime", node)
            # node
            self.match(temp, '[')
            self.match(temp, ']')
        elif self.lookahead in follow['Param-prime']:
            #TODO
            print("what?")
            temp = Node("Param-prime", node)
            temp1 = Node("epsilon", temp)
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

            temp = Node("Compound-stmt", node)

            # node
            self.match(temp, '{')
            #temp1 = Node("Declaration-list", node)
            self.Declaration_list_sub(temp)
            #temp2 = Node("Statement-list", node)
            self.Statement_list_sub(temp)
            self.match(temp, '}')
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


            temp = Node("Statement-list", node)

            self.Statement_sub(temp)

            #temp1 = Node("Statement-list", node)
            self.Statement_list_sub(temp)

        elif self.lookahead in follow['Statement-list']:
            temp = Node("Statement-list", node)
            temp2 = Node("epsilon", temp)

        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Statement_list_sub(node)

    def Statement_sub(self, node):
        if self.lookahead in first['Statement']:
            temp = Node("Statement", node)
            if self.lookahead in first['Expression-stmt']:
                #temp2 = Node("Expression-stmt", node)
                self.Expression_stmt_sub(temp)
            elif self.lookahead in first['Compound-stmt']:
                #temp2 = Node("Compound-stmt", node)
                self.Compound_stmt_sub(temp)
            elif self.lookahead in first['Selection-stmt']:
                #temp2 = Node("Selection-stmt", node)
                self.Selection_stmt_sub(temp)
            elif self.lookahead in first['Iteration-stmt']:
                #temp2 = Node("Iteration-stmt", node)
                self.Iteration_stmt_sub(temp)
            elif self.lookahead in first['Return-stmt']:
                #temp2 = Node("Return-stmt", node)
                self.Return_stmt_sub(temp)
            elif self.lookahead in first['For-stmt']:
                #temp2 = Node("For-stmt", node)
                self.For_stmt_sub(temp)
            elif self.lookahead in follow['Statement']:
                self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Statement")


        elif self.lookahead == '$':
               self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
                self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
                self.next_token()
                self.Statement_sub(node)

    def Expression_stmt_sub(self, node):
        if self.lookahead in first['Expression-stmt']:
            temp = Node("Expression-stmt", node)

            if self.lookahead == ';':
                self.match(temp, ';')
            elif self.lookahead == 'break':
                self.match(temp, 'break')
                self.match(temp, ';')
            else:
                #temp2 = Node("Expression", node)
                self.Expression_sub(temp)
                self.match(temp, ';')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        elif self.lookahead in follow['Expression-stmt']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Expression-stmt")

        else:

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Expression_stmt_sub(node)

    def Selection_stmt_sub(self, node):
        if self.lookahead == 'if':
            temp = Node("Selection-stmt", node)

            self.match(temp, 'if')
            self.match(temp, '(')
            #temp1 = Node("Expression", node)
            self.Expression_sub(temp)
            self.match(temp, ')')
            #temp2 = Node("Statement", node)
            self.Statement_sub(temp)
            self.match(temp, 'else')
            #temp3 = Node("Statement", node)
            self.Statement_sub(temp)
        elif self.lookahead in follow['Selection-stmt']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Seleection-stmt")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Selection_stmt_sub(node)

    def Iteration_stmt_sub(self, node):
        if self.lookahead == 'while':
            temp = Node("Iteration-stmt", node)

            self.match(temp, 'while')
            self.match(temp, '(')
            #temp = Node("Expression", node)
            self.Expression_sub(temp)
            self.match(temp, ')')
            #temp3 = Node("Statement", node)
            self.Statement_sub(temp)
        elif self.lookahead in follow['Iteration-stmt']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Iteration-stmt")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Iteration_stmt_sub(node)

    def Return_stmt_sub(self, node):
        if self.lookahead == 'return':

            temp = Node("Return-stmt", node)

            self.match(temp, 'return')
            #temp = Node("Return-stmt-prime", node)
            self.Return_stmt_prime_sub(temp)

        elif self.lookahead in follow['Return-stmt']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Return-stmt")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Return_stmt_sub(node)

    def Return_stmt_prime_sub(self, node):
        if self.lookahead == ';':
            temp = Node("Return-stmt-prime", node)
            self.match(temp, ";")
        elif self.lookahead in first['Return-stmt-prime']:
            temp = Node("Return-stmt-prime", node)
            #temp = Node("Expression", node)
            self.Expression_sub(temp)
            self.match(temp, ';')

        elif self.lookahead in follow['Return-stmt-prime']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Return-stmt-prime")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Return_stmt_prime_sub(node)

    def For_stmt_sub(self, node):
        if self.lookahead == 'for':
            temp = Node("For-stmt", node)

            self.match(temp, 'for')
            self.match(temp, 'ID')
            self.match(temp, '=')
            #temp = Node("Vars", node)
            self.Vars_sub(temp)
            #temp2 = Node("Statement", node)
            self.Statement_sub(temp)
        elif self.lookahead in follow['For-stmt']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing For-stmt")
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
            self.Var_zegond_sub(temp1)
        elif self.lookahead in follow['Vars']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Vars")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_sub(node)

    def Var_zegond_sub(self, node):
        if self.lookahead == ',':
            temp = Node("Var-zegond", node)

            self.match(temp, ',')
            #temp1 = Node("Var", node)
            self.Var_sub(temp)
            #temp2 = Node("Var_zegond", node)
            self.Var_zegond_sub(temp)

        elif self.lookahead in follow['Var-zegond']:
            temp = Node("Var-zegond", node)
            temp2 = Node("epsilon", temp)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_zegond_sub(node)

    def Var_sub(self, node):
        if self.cpl_token[0] == 'ID':
            temp = Node("Var", node)

            self.match(temp, 'ID')
            #temp1 = Node("Var-prime", node)
            self.Var_prime_sub(temp)
        elif self.lookahead in follow['Var']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Var")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_sub(node)

    def Expression_sub(self, node):
       # if self.cpl_token[0] == 'ID':
        if self.lookahead in first['Simple-expression-zegond']:

            temp = Node("Expression", node)
            self.Simple_expression_zegond(temp)
        elif self.lookahead == 'ID':
            temp = Node("Expression", node)
            self.match(temp, 'ID')
            #temp1 = Node("B", node)
            self.B_sub(temp)
        # elif self.lookahead in follow['Expression']:
        #     temp2 = Node("Expression", node)

            #temp2 = Node("Simple-expression-zegond", node)
           # self.Simple_expression_zegond(temp2)
        elif self.lookahead in follow['Expression']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Expression")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Expression_sub(node)

    def B_sub(self, node):
        if self.lookahead == '=':
            temp1 = Node("B", node)

            self.match(temp1, '=')
            #temp2 = Node("Expression", node)
            self.Expression_sub(temp1)
        elif self.lookahead == '[':
            temp1 = Node("B", node)

            self.match(temp1, '[')
            #temp2 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(temp1, ']')
            #temp2 = Node("H", node)
            self.H_sub(temp1)
        elif self.lookahead in self.lookahead in follow['B'] or self.lookahead in first['Simple-expression-prime']:
            temp1 = Node("B", node)
            #temp2 = Node("Simple-expression-prime", node)
            self.Simple_expression_prime_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.B_sub(node)

    def H_sub(self, node):
        if self.lookahead == '=':
            temp2 = Node("H", node)

            self.match(temp2, '=')
            #temp2 = Node("Expression", node)
            self.Expression_sub(temp2)
        elif self.lookahead in first['H'] or self.lookahead in follow['H'] or self.lookahead in first['G'] or self.lookahead in first['D'] or self.lookahead in first['C']:
            temp2 = Node("H", node)

            #temp2 = Node("G", node)
            self.G_sub(temp2)
            #temp2 = Node("D", node)
            self.D_sub(temp2)
            #temp2 = Node("C", node)
            self.C_sub(temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.H_sub(node)

    def Simple_expression_zegond(self, node):
        if self.lookahead in first['Additive-expression-zegond']:
            temp = Node("Simple-expression-zegond", node)

            #temp1 = Node("Additive-expression-zegond", node)
            self.Additive_expression_zegond_sub(temp)
            #temp2 = Node("C", node)
            self.C_sub(temp)
        elif self.lookahead in follow['Simple-expression-zegond']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, Missing Simple-expression-zegnod")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")


        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Simple_expression_zegond(node)

    def Simple_expression_prime_sub(self, node):   ## s
        if self.lookahead in first['Simple-expression-prime'] or self.lookahead in follow['Simple-expression-prime'] or self.lookahead in first['C']:
            temp = Node("Simple-expression", node)

#            temp1 = Node("Additive-expression-prime", node)
            self.Additive_expression_prime_sub(temp)
 #           temp1 = Node("C", node)
            self.C_sub(temp)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Simple_expression_prime_sub(node)

    def C_sub(self, node):
        if self.lookahead in first['C']:
            temp1 = Node("C", node)

            #temp1 = Node("Relop", node)
            self.Relop_sub(temp1)
            #temp1 = Node("Additive-expression", node)
            self.Additive_expression(temp1)
        elif self.lookahead in follow['C']:
            temp1 = Node("C", node)
            temp = Node("epsilon", temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.C_sub(node)

    def Relop_sub(self, node):
        if self.lookahead == '<':
            temp1 = Node("Relop", node)
            self.match(temp1, '<')
        elif self.lookahead == "==":
            temp1 = Node("Relop", node)
            self.match(temp1, '==')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        elif self.lookahead in follow['Relop']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, Missing Relop")
        else:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Relop_sub(node)

    def Additive_expression(self, node):
        if self.lookahead in first['Additive-expression']:
            temp1 = Node("Additive-expression", node)

            #temp1 = Node("Term", node)
            self.Term_sub(temp1)
            #temp2 = Node("D", node)
            self.D_sub(temp1)

        elif self.lookahead in follow['Additive-expression']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Additive-expression")

        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Additive_expression(node)

    def Additive_expression_prime_sub(self, node):
        if self.lookahead in first['Additive-expression-prime'] or self.lookahead in follow['Additive-expression-prime']:
            temp1 = Node("Additive-expression-prime", node)

            #temp1 = Node("Term-prime", node)
            self.Term_prime_sub(temp1)
            #temp2 = Node("D", node)
            self.D_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Additive_expression_prime_sub(node)

    def Additive_expression_zegond_sub(self, node):
        if self.lookahead in first['Additive-expression-zegond']:
            temp1 = Node("Additive-expression-zegond", node)

            #temp1 = Node("Term-zegond", node)
            self.Term_zegond_sub(temp1)
            #temp2 = Node("D", node)
            self.D_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        elif self.lookahead in follow['Additive-expression-zegnod']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, Missing Additive-expression-zegnod")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Additive_expression_zegond_sub(node)

    def D_sub(self, node):
        if self.lookahead in first['D']:
            temp = Node("D", node)

            #temp1 = Node("Addop", node)
            self.Addop_sub(temp)
            #temp2 = Node("Term", node)
            self.Term_sub(temp)
            #temp3 = Node("D", node)
            self.D_sub(temp)

        elif self.lookahead in follow['D']:
            temp2 = Node("D", node)
            temp = Node("epsilon", temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.D_sub(node)

    def Addop_sub(self, node):
        if self.lookahead == '+':
            temp1 = Node("Addop", node)
            self.match(temp1, '+')
        elif self.lookahead == '-':
            temp1 = Node("Addop", node)
            self.match(temp1, '-')

        elif self.lookahead in follow['Addop']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, Missing Addop")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Addop_sub(node)

    def Term_sub(self, node):
        if self.lookahead in first['Term']:
            temp2 = Node("Term", node)
            #temp1 = Node("Signed-factor", node)
            self.Signed_factor_sub(temp2)
            #temp2 = Node("G", node)
            self.G_sub(temp2)

        elif self.lookahead in follow['Term']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Term")

        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Term_sub(node)

    def Term_prime_sub(self, node):
        # ?????????????????????????????
        if self.lookahead in first['Term-prime'] or self.lookahead in follow['Term-prime']:
            temp1 = Node("Term-prime", node)

            self.Signed_factor_prime_sub(temp1)
            #temp2 = Node("G", node)
            self.G_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:

            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Term_prime_sub(node)

    def Term_zegond_sub(self, node):
        if self.lookahead in first['Term-zegond']:
            temp1 = Node("Term-zegond", node)

            #temp1 = Node("Signed-factor-zegond", node)
            self.Signed_factor_zegond_sub(temp1)
            #temp2 = Node("G", node)
            self.G_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Term_zegond_sub(node)

    def G_sub(self, node):
        if self.lookahead == '*':
            temp = Node("G", node)

            self.match(temp, '*')
            #temp1 = Node("Signed-factor", node)
            self.Signed_factor_sub(temp)
            #temp2 = Node("G", node)
            self.G_sub(temp)
        elif self.lookahead in follow['G']:
            temp2 = Node("G", node)
            temp = Node("epsilon", temp2)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.G_sub(node)

    def Signed_factor_sub(self, node):
        if self.lookahead in first['Signed-factor']:
            temp1 = Node("Signed-factor", node)

            if self.lookahead == '+':
                self.match(temp1, '+')
                #temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            elif self.lookahead == '-':
                self.match(temp1, '-')
                #temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            else:
                #temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
        elif self.lookahead in follow['Signed-factor']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Signed-factor")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Signed_factor_sub(node)

    def Signed_factor_prime_sub(self, node):
        if self.lookahead in first['Signed-factor-prime'] or self.lookahead in follow['Signed-factor-prime']:
            temp1 = Node("Signed-factor-prime", node)
            #temp1 = Node("Factor-prime", node)
            self.Factor_prime_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Signed_factor_prime_sub(node)

    def Signed_factor_zegond_sub(self, node):
        if self.lookahead in first["Signed-factor-zegond"]:
            temp1 = Node("Signed-factor-zegond", node)

            if self.lookahead == '+':
                self.match(temp1, '+')
                #temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            elif self.lookahead == '-':
                self.match(temp1, '-')
                #temp1 = Node("Factor", node)
                self.Factor_sub(temp1)
            else:
                #temp1 = Node("Factor-zegond", node)
                self.Factor_zegond_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Signed_factor_zegond_sub(node)

    def Factor_sub(self, node):
        if self.lookahead == '(':
            temp1 = Node("Factor", node)
            self.match(temp1, '(')
            #temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(temp1, ')')
        elif self.cpl_token[0] == "ID":
            temp1 = Node("Factor", node)

            self.match(temp1, "ID")
            #temp1 = Node("Var-call-prime", node)
            self.Var_call_prime_sub(temp1)
        elif self.cpl_token[0] == 'NUM':
            temp1 = Node("Factor", node)
            self.match(temp1, 'NUM')
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Factor_sub(node)

    def Var_call_prime_sub(self, node):
        if self.lookahead == '(':
            temp1 = Node("Var-call-prime", node)
            self.match(temp1, '(')
            #temp1 = Node("Args", node)
            self.Args_sub(temp1)
            self.match(temp1, ')')
        elif self.lookahead in first['Var-call-prime'] or self.lookahead in follow['Var-call-prime']:
            temp1 = Node("Var-call-prime", node)
            #temp1 = Node("Var-prime", node)
            self.Var_prime_sub(temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_call_prime_sub(node)

    def Var_prime_sub(self, node):
        if self.lookahead == '[':
            temp1 = Node("Var-prime", node)

            self.match(temp1, '[')
            #temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(temp1, ']')
        elif self.lookahead in follow['Var-prime']:
            temp1 = Node("Var-prime", node)
            temp = Node("epsilon", temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Var_prime_sub(node)

    def Factor_prime_sub(self, node):
        if self.lookahead == '(':
            temp = Node("Factor-prime", node)

            self.match(temp, '(')
#            temp1 = Node("Args", node)
            self.Args_sub(temp)
            self.match(temp, ')')
        elif self.lookahead in follow['Factor-prime']:
            temp1 = Node("Factor-prime", node)
            temp = Node("epsilon", temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Factor_prime_sub(node)

    def Factor_zegond_sub(self, node):
        if self.cpl_token[0] == 'NUM':
            temp = Node("Factor-zegond", node)

            self.match(temp, 'NUM')
        elif self.lookahead == '(':
            temp1 = Node("Factor-zegond", node)

            self.match(temp1, '(')
#            temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            self.match(temp1, ')')

        elif self.lookahead in follow['Factor-zegond']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Factor-zegond")
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Factor_zegond_sub(node)

    def Args_sub(self, node):
        if self.lookahead in first['Args']:
            temp1 = Node("Args", node)
            self.Arg_list_sub(temp1)
        elif self.lookahead in follow['Args']:
            temp1 = Node("Args", node)
            temp = Node("epsilon", temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Args_sub(node)

    def Arg_list_sub(self, node):
        if self.lookahead in first['Arg-list']:
            temp1 = Node("Args-list", node)

            self.Expression_sub(temp1)
            #temp1 = Node("Arg-list-prime", node)
            self.Arg_list_prime_sub(temp1)
        elif self.lookahead in follow['Arg-list']:
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, missing Arg-list")

        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")
        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Arg_list_sub(node)

    def Arg_list_prime_sub(self, node):
        if self.lookahead in first['Arg-list-prime']:
            temp1 = Node("Args-list-prime", node)

            self.match(temp1, ',')
            #temp1 = Node("Expression", node)
            self.Expression_sub(temp1)
            #temp1 = Node("Arg-list-prime", node)
            self.Arg_list_prime_sub(temp1)
        elif self.lookahead in follow['Arg-list-prime']:
            temp1 = Node("Args-list-prime", node)
            temp = Node("epsilon", temp1)
        elif self.lookahead == '$':
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, unexpected EOF")

        else:
            
            self.syn_err_l.append(str(self.my_scanner.line_num) + ": syntax error, illegal " + self.lookahead)
            self.next_token()
            self.Arg_list_prime_sub(node)



#print(parser.syn_err_l)
