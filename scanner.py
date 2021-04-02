
# elnaz masoumi 96106106
# saeedeh vahedi

class Scan:


    keyword = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'for']
    symbol = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
    whitespace = [' ','\n', '\r', '\t', '\v', '\f']
    letter = ['a', 'A', 'b','B', 'C', 'c', 'd','D', 'E', 'e','F', 'f','G', 'g','H', 'h','I' 'i','J', 'j','K', 'k','L', 'l','M', 'm','N', 'n','O', 'o','P', 'p','Q', 'q','R', 'r', 'S', 's','T', 't','U', 'u',
                'v', 'V', 'W','w','X', 'x', 'Y', 'y', 'Z', 'z']
    token_types = [digit, letter, ID, Keyword, Symbol, Whitespace]
    states = [num, ide, alphabet, other, comment, symb]


    counter = 0
    input = 0
    array = ""

    state = 'start'







    def __init__(self, program):
        self.line_num = 1
        self.token = []
        self.lex_error = []
        self.program = open('/Users/macbookpro/PycharmProjects/compiler_project/compiler_project/T01/input.txt', 'r').read(1)
        self.program=program
        self.loc = -1
        self.file_cap = len(program)

        self.lexical_errors = open('lexical_errors.txt', 'r').read()
        self.symbol_table = open('lexical_errors.txt', 'r').read()
        self.token_file = open('tokens.txt', 'r').read()


    def lookahead_chr(self):
        if self.loc + 1 >= self.file_cap:
            return '\0'
        return self.program[self.loc+1]


    def next_char(self):
        self.loc += 1
        if self.loc>=self.file_cap:
            chr = '\0'
            return chr
        else:
            chr = self.program[self.loc]
            return chr


#####        return types
    def is_symbol(self,chr):
        if chr in self.symbol:
            return "symbol"

    def is_digit(self, chr):
        if '0'<= chr <= '9':
            return "digit"

    def is_letter(self,chr):
        if 'a'<= chr<= 'z' or 'A'<= chr <='Z':
            return "letter"

    def is_comment(self,chr):
        if chr == '/':
            return "Comment"




######


    def do_whitespace(self, whitespace):
        if whitespace == '\n':
            self.line_num+=1



    def Ignore_whitespace(self):         # for skipping white spaces
        while self.loc in self.whitespace:
            self.next_char()



    def dfa_navigation(self, chr):

         self.next_char()


         self.counter+=1


         if state == 'start':   #write if for every state after start, based on DFA

             if self.is_digit(chr) == "digit":













