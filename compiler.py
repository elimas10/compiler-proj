# elnaz masoumi 96106106
# saeede vahedi 96102664

class Scanner:
    keyword = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'for']
    symbol = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-','<', '=', '*']
    whitespace = [' ', '\n', '\r', '\t', '\v', '\f']
    letter = ['a', 'A', 'b', 'B', 'C', 'c', 'd', 'D', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I' 'i', 'J', 'j', 'K',
              'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u',
              'v', 'V', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z']
    #token_types = ['digit', 'letter', 'ID', 'Keyword', 'Symbol', 'Whitespace']
    #states = ['start','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','num', 'ide', 'alphabet', 'other', 'comment', 'symb']

    final_states=['2','4','5','7','9','c','f']
    counter = 0
    input = 0
    array = ""
    state ='0'

    def __init__(self, input):

        self.line_num = 1
        self.token = []
        #self.lex_error = []
        self.program = open(input, 'r').read()
        # print(self.program)
        # print(self.program[0:5])

        self.start_loc=0
        self.loc =0
        self.file_cap = len(self.program)

        # self.lexical_errors = open('lexical_errors.txt', 'r').read()
        # self.symbol_table = open('lexical_errors.txt', 'r').read()
        # self.token_file = open('tokens.txt', 'r').read()



    def get_next_token(self):

        temp_arr=""


        while(self.loc<self.file_cap):
            #print(self.loc, self.program[self.loc])

            if self.state=='0':
                self.start_loc=self.loc

            #self.next_char()
            self.dfa_navigation(self.program[self.loc])

            token=self.program[self.start_loc:self.loc]
            #print("len is ", len(token))
            #print(token)
            #print(self.start_loc,self.loc)

            if self.program[self.loc]=='\n':
                if len(temp_arr):
                    self.array += str(self.line_num) + ". " + temp_arr+"\n"
                    temp_arr=""
                self.line_num+=1
                #print("next line")

            if self.state=='2':

                if token in self.keyword:
                    temp_arr+="( KEYWORD,"+token+" )"
                else:
                    temp_arr +="( ID,"+ token+ " )"
                self.state='0'

            elif self.state=='4':
                temp_arr +="( NUM, "+token+" )"
                self.state='0'

            elif self.state == '5' or self.state=='7' or self.state == '9':
                temp_arr +="( SYMBOL, "+ self.program[self.start_loc:self.loc+1]+" )"
                self.state='0'
                self.loc+=1

            elif self.state=='c':
                #temp_arr +="( COMMENT, "+ token+" )"
                self.state='0'
                self.loc+=1

            elif self.state == 'f':
                #print("whitespace recognized")
                self.state='0'
                self.loc+=1
                #print("( WHITESPACE, ", token," )")
            else:
                self.loc+=1



        f = open("tokens.txt", "w")
        f.write(self.array)
        f.close()


    def lookahead_chr(self):
        if self.loc + 1 >= self.file_cap:
            return '\0'
        return self.program[self.loc + 1]

    # def next_char(self):
    #     self.loc += 1
    #     if self.loc >= self.file_cap:
    #         chr = '\0'
    #         return chr
    #     else:
    #         chr = self.program[self.loc]
    #         return chr

    #####        return types
    def is_symbol(self, chr):
        if chr in self.symbol:
            return True

    def is_whitespace(self, chr):
        if chr in self.whitespace:
            return True

    def is_digit(self, chr):
        if '0' <= chr <= '9':
            return True

    def is_letter(self, chr):
        if 'a' <= chr <= 'z' or 'A' <= chr <= 'Z':
            return True

    def is_comment(self, chr):
        if chr == '/':
            return True

    ######

    def do_whitespace(self, whitespace):
        if whitespace == '\n':
            self.line_num += 1

    def Ignore_whitespace(self):  # for skipping white spaces
        while self.loc in self.whitespace:
            self.next_char()

    def dfa_navigation(self, chr):
        #self.counter += 1

        if self.state == '0':  # write if for every state after start, based on DFA
            if self.is_digit(chr):
                self.state='3'
            elif self.is_letter(chr):
                self.state='1'
            elif self.is_comment(chr):
                self.state='a'
            elif self.is_symbol(chr):
                if chr=="=":
                    self.state='6'
                elif chr=='*':
                    self.state='8'
                else:
                    self.state='5'
            elif self.is_whitespace(chr):
                self.state='f'

        elif self.state=='1':

            if not (self.is_digit(chr) or self.is_letter(chr)):
                self.state='2'
            # else state 1
        # elif self.state=='2':
        #     accept
        elif self.state=='3':
            if not (self.is_digit(chr) or self.is_letter(chr)):
                self.state='4'
            # if digit state=3
        # elif self.state=='4':
        #     accept
        # accept
        elif self.state=='6':
            if chr=="=":
                self.state='7'
            else:
                self.state='9'
        # elif self.state=='7':
        #     accept
        elif self.state=='8':
            if not chr=='/':
                self.state='9'
        # elif self.state=='9':
        #     accept
        elif self.state=='a':
            if chr=="/":
                self.state='b'
            elif chr=="*":
                self.state='d'
        elif self.state=='b':
            if chr=="\n":
                self.state='c'
        # elif self.state=='c':
        #     accept
        elif self.state=='d':
            if chr=="*":
                self.state='e'
        elif self.state=='e':
            if chr=="/":
                self.state='c'
            elif not chr=="*":
                self.state='d'
        # elif self.state=='f':
        #     accept





scanner =Scanner('./PA1_sample_programs/T01/input.txt')
scanner.get_next_token()
