
# elnaz masoumi 96106106
# saeedeh vahedi

class Scan:


    keyword = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'for']
    symbol = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
    whitespace = [' ','\n', '\r', '\t', '\v', '\f']
    letter = ['a', 'A', 'b','B', 'C', 'c', 'd','D', 'E', 'e','F', 'f','G', 'g','H', 'h','I' 'i','J', 'j','K', 'k','L', 'l','M', 'm','N', 'n','O', 'o','P', 'p','Q', 'q','R', 'r', 'S', 's','T', 't','U', 'u',
                'v', 'V', 'W','w','X', 'x', 'Y', 'y', 'Z', 'z']
    token_types = [digit, letter, ID, Keyword, Symbol, Whitespace]


    counter = 0
    input = 0
    chr = " "
    state = 'start'


    # lexical_errors = open('lexical_errors.txt', 'r').read()
    # symbol_table = open('lexical_errors.txt', 'r').read()
    # tokens = open('tokens.txt', 'r').read()

    file_cap = len(program)


    def __init__(self, program):
        self.line_num = 1
        self.token = []
        self.lex_error = []
        self.program = open('/Users/macbookpro/PycharmProjects/compiler_project/compiler_project/T01/input.txt', 'r').read(1)
        self.program=program










    def next_char(self):


        chr = self.program
        if chr == '\n':
           self.line_num+=1


        return chr



    def do_whitespace(self, whitespace):

        if whitespace == '\n':
            self.line_num+=1



    # def Ignore_whitespace():
    #         while next_char() == ' ' or next_char() == '\t' or next_char() == '\r':
    #             next_char()










    #
    # def get_next_token(str):    # return (Token Type, Token String)
    #
    #
    #     while(True):
    #
    #



    def dfa_navigation(self, chr):

         if self.counter>= self.file_cap:

             return (False, (line_num))

         else:
             if self.state == 'error':
                 self.counter-=1

             chr = input[self.counter]

         self.counter+=1


         if state == 'start':

#              write if for every state after start





