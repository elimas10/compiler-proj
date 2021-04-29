from compiler import Scanner
from First import first
from Follow import  follow
from anytree import Node, RenderTree



class Parser:

    my_scanner=None
    lookahead=None

    def __init__(self,input):
        self.my_scanner=Scanner(input)
        self.next_token()



    def next_token(self):   # to be
        self.lookahead=self.my_scanner.get_next_token()




    def match(self, exp_token):

        if self.lookahead == exp_token:
            self.next_token()
        else:
            print("error in match")


###### write subroutine for each N.T:

    def Program_sub(self):
         if self.lookahead in first['Program']:
            # root
            self.Declaration_list_sub()
            self.match('$')
         else:
             # raise error

    def Declaration_list_sub(self):
        if self.lookahead in first['Declaration']:

            self.Declaration_sub()
            self.Declaration_list_sub()

            ##
        elif self.lookahead in follow['Declaration']:

            ## handle tree
        else:
            print("illegal error")
            self.next_token()
            self.Declaration_list_sub()

    def Declaration_sub(self):
        if self.lookahead in first['Declaration-initial']:
            self.Declaration_initial_sub()
            self.Declaration_prime_sub()


        elif self.lookahead in follow['Declaration']:
            print("error")
        else:
            self.next_token()
            self.Declaration_sub()


    def Declaration_initial_sub(self):
        if self.lookahead in first['Type-specifier']:
            self.Type_specifier()
            self.match('ID')

        elif self.lookahead in follow['Declaration-initial']:
            # syntax error
        elif self.lookahead == '$':
            print("end file error")
            # termination
        else:
            # error
            self.next_token()
            self.Declaration_initial_sub()


    def Declaration_prime_sub(self):
        if self.lookahead in first['Fun-declaration-prime']:
            # change node
            self.Fun_declaration_prime_sub()
        elif self.lookahead in first['Var-declaration-prime']:
            # change node
            self.Var_declaration_prime_sub()
        elif self.lookahead in follow['Declaration-prime']:
            # missing error
        else:
            # error
            self.next_token()
            self.Declaration_prime_sub()

    def Var_declaration_prime_sub(self):
        if self.lookahead == ';':
            # change node
            self.match(';')
        elif self.lookahead == '[':
            # change node
            self.match('[')
            self.match('NUM')
            self.match(']')
            self.match(';')

        elif self.lookahead in follow['Var-declaration-prime']:
            # error
        else:
            # error
            self.next_token()
            self.Var_declaration_prime_sub()


    def Fun_declaration_prime_sub(self):
        if self.lookahead == '(':
            self.match('(')
            # change node
            # call sub of params and Compound_stmt
            self.match(')')

        elif self.lookahead in follow['Fun-declaration-prime']:
            # error
        else:
            # error
            self.next_token()
            self.Fun_declaration_prime_sub()


    def Type_specifier(self):
        if self.lookahead == 'int':
            # change node
            self.match('int')
        elif self.lookahead == 'void':
            # change node
            self.match('void')
        elif self.lookahead in follow['Type-specifier']:
            # error
        elif self.lookahead == '$':
            # error + termination
        else:
            # error
            self.next_token()
            #
            self.Type_specifier()

    def Params_sub(self):
        if self.lookahead == 'int':
            # change node
            self.match('int')
            self.match('ID')
            # call subs of param prime & param list
        elif self.lookahead == 'void':
            # change node
            self.match('void')
            # call sub of aram-list-void-abtar
        elif self.lookahead in follow['Params']:
            # error
        elif self.lookahead == '$':
            # error + termination
        else:
            # error
            self.next_token()
            self.Params_sub()

        ##saeede

        def C_sub(self):
            if self.lookahead in first['C']:
                self.Relop_sub()
                self.Additive_expression()
            # epsilon
            else:
                print("error")

        def Relop_sub(self):
            if self.lookahead == '<':
                self.match('<')
            elif self.lookahead == "==":
                self.match('==')
            else:
                print("error")

        def Additive_expression(self):
            if self.lookahead in first['Additive-expression']:
                self.Term_sub()
                self.D_sub()
            else:
                print("error")

        def Additive_expression_prime_sub(self):
            if self.lookahead in first['Additive-expression-prime']:
                self.Term_prime_sub()
                self.D_sub()
            else:
                print("error")

        def Additive_expression_zegond_sub(self):
            if self.lookahead in first['Additive-expression-zegond']:
                self.Term_zegond_sub()
                self.D_sub()
            else:
                print("error")

        def D_sub(self):
            if self.lookahead in first['D']:
                self.Addop_sub()
                self.Term_sub()
                self.D_sub()
            # epsilon
            else:
                print("error")

        def Addop_sub(self):
            if self.lookahead == '+':
                self.match('+')
            elif self.lookahead == '-':
                self.match('-')
            else:
                print("error")

        def Term_sub(self):
            if self.lookahead in first['Term']:
                self.Signed_factor_sub()
                self.G_sub()
            else:
                print("error")

        def Term_prime_sub(self):
            if self.lookahead in first['Term-prime']:
                self.Signed_factor_prime_sub()
                self.G_sub()
            else:
                print("error")

        def Term_zegond_sub(self):
            if self.lookahead in first['Term-zegond']:
                self.Signed_factor_zegond_sub()
                self.G_sub()
            else:
                print("error")

        def G_sub(self):
            if self.lookahead == '*':
                self.match('*')
                self.Signed_factor_sub()
                self.G_sub()
            # epsilon
            else:
                print("error")

        def Signed_factor_sub(self):
            if self.lookahead in first['Signed-factor']:
                if self.lookahead == '+':
                    self.match('+')
                    self.Factor_sub()
                elif self.lookahead == '-':
                    self.match('-')
                    self.Factor_sub()
                else:
                    self.Factor_sub()
            else:
                print("error")

        def Signed_factor_prime_sub(self):
            if self.lookahead in first['Signed-factor-prime']:
                self.Factor_prime_sub()
            else:
                print("error")

        def Signed_factor_zegond_sub(self):
            if self.lookahead in first["Signed-factor-zegond"]:
                if self.lookahead == '+':
                    self.match('+')
                    self.Factor_sub()
                elif self.lookahead == '-':
                    self.match('-')
                    self.Factor_sub()
                else:
                    self.Factor_zegond_sub()
            else:
                print("error")

        def Factor_sub(self):
            if self.lookahead == '(':
                self.match('(')
                self.Expression_sub()
                self.match(')')
            elif self.lookahead == "ID":
                self.match("ID")
                self.Var_call_prime_sub()
            elif self.lookahead == 'NUM':
                self.match('NUM')
            else:
                print("error")

        def Var_call_prime_sub(self):
            if self.lookahead == '(':
                self.match('(')
                self.Args_sub()
                self.match(')')
            elif self.lookahead in first['Var-prime']:
                self.Var_prime_sub()
            else:
                print("error")

        def Var_prime_sub(self):
            if self.lookahead == '[':
                self.match('[')
                self.Expression_sub()
                self.match(']')
            else:
                print("error")

        def Factor_prime_sub(self):
            if self.lookahead == '(':
                self.match('(')
                self.Args_sub()
                self.match(')')
                # epsilon
            else:
                print("error")

        def Factor_zegond_sub(self):
            # if self.lookahead in first['Factor-zegond']:
            if self.lookahead == 'NUM':
                self.match('NUM')
            elif self.lookahead == '(':
                self.match('(')
                self.Expression_sub()
                self.match(')')
            else:
                print("error")

        def Args_sub(self):
            if self.lookahead in first['Args']:
                self.Arg_list_sub()
                # epsilon
            else:
                print("error")

        def Arg_list_sub(self):
            if self.lookahead in first['Arg-list']:
                self.Expression_sub()
                self.Arg_list_prime_sub()
            else:
                print("error")

        def Arg_list_prime_sub(self):
            if self.lookahead in first['Arg-list-prime']:  # ','
                self.match(',')
                self.Expression_sub()
                self.Arg_list_prime_sub()
            else:
                # what to do with epsilon?
                print("error")


    def Param_list_void_abtar_sub(self):
        if self.lookahead == 'ID':
            # node
            self.match('ID')
            # call subs of param prime & param list
        elif self.lookahead in follow['Param-list-void-abtar']:
            # node
        elif self.lookahead == '$':
            # error end of file + term

        else:
            # error
            self.next_token()
            self.Param_list_void_abtar_sub()


    def Param_list_sub(self):
        if self.lookahead == ',':
            # node
            self.match(',')
            self.Param_sub()
            self.Param_list_sub()
        elif self.lookahead in follow['Param-list']:
            # node
        elif self.lookahead == '$':
    # error end of file + term
        else:
            # error
            self.next_token()
            self.Param_list_sub()


    def Param_sub(self):
        if self.lookahead in first['Declaration-initial']:
            # node
            self.Declaration_initial_sub()
            self.Param_prime_sub()

        elif self.lookahead in follow['Param']:
            # error
        elif self.lookahead == '$':
            # error + termn
        else:
            # error
            self.next_token()
            self.Params_sub()

    def Param_prime_sub(self):
        if self.lookahead == '[':
            # node
            self.match('[')
            self.match(']')
        elif self.lookahead in follow['Param-prime']:
            # node
        elif self.lookahead == '$':
    # error + termn
        else:
            # error
            self.next_token()
            self.Param_prime_sub()


    def Compound_stmt_sub(self):
        if self.lookahead == '{':
            # node
            self.match('{')
            self.Declaration_list_sub()
            self.Statement_list_sub()
            self.match('}')
        elif self.lookahead in follow['Compound-stmt']:
            # error
        else:
            # error
            self.next_token()
            self.Compound_stmt_sub()

    def Statement_list_sub(self):
        if self.lookahead in first['Statement']:
            #node
            self.Statement_list_sub()
            self.Statement_sub()
        elif self.lookahead in follow['Statement-list']:
            # node
        elif self.lookahead == '$':
            # erroe
        else:
            #error
            self.next_token()

    def Statement_sub(self):
        if self.lookahead in first['Expression-stmt']:

            self.Expression_stmt_sub()

        elif self.lookahead in first['Compound-stmt']:

            self.Compound_stmt_sub()

        elif self.lookahead in first['Selection-stmt']:

            self.Selection_stmt_sub()

        elif self.lookahead in first['Iteration-stmt']:

            self.Iteration_stmt_sub()

        elif self.lookahead in first['Return-stmt']:

            self.Return_stmt_sub()

        elif self.lookahead in first['For-stmt']:

             self.For_stmt_sub()

        elif self.lookahead in follow['Statement']:
            print("error")
        elif self.lookahead == '$':
            print("error end file")
        else:
            self.next_token()
            self.Statement_sub()


    def Expression_stmt_sub(self):
        if self.lookahead in first['Expression']:
            self.Expression_sub()
            self.match(';')
        elif self.lookahead == 'break':

            self.match('break')
            self.match(';')
        elif self.lookahead == ';':
            self.match(';')

        elif self.lookahead in follow['Expression-stmt']:
            print("error ")

        elif self.lookahead == '$':
            print("error end file")

        else:
            print("illegal error")
            self.next_token()
            self.Expression_stmt_sub()



    def Selection_stmt_sub(self):

    def Iteration_stmt_sub(self):


    def Return_stmt_sub(self):

    def For_stmt_sub(self):









# parser=Parser('./input.txt')
# print("1")
# print(parser)
# print("2")
# print(parser.lookahead)
#
#


