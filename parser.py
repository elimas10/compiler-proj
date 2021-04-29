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

         else:
             # raise error

    def Declaration_list_sub(self):
        if self.lookahead in first['Declaration']:

            ##
        elif self.lookahead in follow['Declaration']:

            ## handle tree
        else:
            ## error

    def Declaration_sub(self):
        if self.lookahead in first['Declaration-initial']:


        elif self.lookahead in follow['Declaration']:

    def Declaration_initial_sub(self):
        if self.lookahead in first['Type-specifier']:
            self.match('ID')

        elif self.lookahead in follow['Declaration-initial']:
            # syntax error
        elif self.lookahead == '$':
            # error
            # termination
        else:
            # error
            self.my_scanner.get_next_token()


    def Declaration_prime_sub(self):
        if self.lookahead in first['Fun-declaration-prime']:
            # change node
        elif self.lookahead in first['Var-declaration-prime']:
            # change node
        elif self.lookahead in follow['Declaration-prime']:
            # missing error
        else:
            # error
            self.my_scanner.get_next_token()

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
            self.my_scanner.get_next_token()


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
            self.my_scanner.get_next_token()
            # call sub of fun_declaration_prime


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
            self.my_scanner.get_next_token()
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
            self.my_scanner.get_next_token()
            self.Params_sub()





# parser=Parser('./input.txt')
# print("1")
# print(parser)
# print("2")
# print(parser.lookahead)
#
#


