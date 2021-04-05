# elnaz masoumi 96106106
# saeede vahedi 96102664

class Scanner:
    keyword = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'for']
    symbol = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-','<', '=', '*']
    whitespace = [' ', '\n', '\r', '\t', '\v', '\f']
    error_types=['Invalid input','Unmatched comment' ,'Unclosed comment','Invalid number']
    symbol_table=[]
    array = ""
    state ='0'

    def __init__(self, input):

        self.line_num = 1
        self.token = []
        self.lex_error = []
        self.program = open(input, 'r').read()

        self.start_loc=0
        self.loc =0
        self.file_cap = len(self.program)

    def check_NUM(self,num):

        for digit in num:
            if not self.is_digit(digit):
                return False
        return True

    def get_next_token(self):

        temp_arr=""

        while(self.loc<self.file_cap):

            if self.state=='0':
                self.start_loc=self.loc

            self.dfa_navigation(self.program[self.loc])

            token=self.program[self.start_loc:self.loc]

            if self.program[self.loc]=='\n':
                if len(temp_arr):
                    self.array += str(self.line_num) + ".\t" + temp_arr+"\n"
                    temp_arr=""
                self.line_num+=1

            if self.state=='2':

                if token in self.keyword:
                    temp_arr+="(KEYWORD, "+token+") "
                else:
                    temp_arr +="(ID, "+ token+ ") "

                if token not in self.symbol_table:
                    self.symbol_table.append(token)
                self.state='0'

            elif self.state=='4':

                if self.check_NUM(token):
                    temp_arr +="(NUM, "+token+") "
                else:
                    self.lex_error.append([self.line_num,token,"Invalid number"])
                self.state='0'

            elif self.state == '5' or self.state=='7':
                temp_arr +="(SYMBOL, "+ self.program[self.start_loc:self.loc+1]+") "
                self.state='0'
                self.loc+=1
            elif self.state == '9':
                temp_arr += "(SYMBOL, " + token + ") "
                self.state = '0'
                self.loc += 1
            elif self.state=='c':
                self.state='0'
                self.loc+=1

            elif self.state == 'f':
                self.state='0'
                self.loc+=1
            elif self.state in self.error_types:
                self.lex_error.append([self.line_num, self.program[self.start_loc:self.loc+1], self.state])
                self.state='0'
                self.loc += 1
            else:
                self.loc+=1



        # create files
        f1 = open("tokens.txt", "w")
        f1.write(self.array)
        f1.close()
        #
        error_string=""
        if len(self.lex_error):
            for error in self.lex_error:
                error_string+=str(error[0])+".\t("+ error[1]+", "+error[2]+")\n"
        else:
            error_string="There is no lexical error."
        f2 = open("lexical_errors.txt", "w")
        f2.write(error_string)
        f2.close()
        #
        # f3 = open("symbol_table.txt", "w")
        # f3.write(self.array)
        # f3.close()
        print(self.symbol_table)


    # def lookahead_chr(self):
    #     if self.loc + 1 >= self.file_cap:
    #         return '\0'
    #     return self.program[self.loc + 1]

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

    # def do_whitespace(self, whitespace):
    #     if whitespace == '\n':
    #         self.line_num += 1

    # def Ignore_whitespace(self):  # for skipping white spaces
    #     while self.loc in self.whitespace:
    #         self.next_char()

    def dfa_navigation(self, chr):

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
            else:
                self.state='Invalid input'

        elif self.state=='1':

            if not (self.is_digit(chr) or self.is_letter(chr)):
                if chr=="!":
                    self.state='Invalid input'
                else:
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
            else:
                self.state="Unmatched comment"
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
            elif self.loc==self.file_cap-1:
                self.state='Unclosed comment'
        elif self.state=='e':
            if chr=="/":
                self.state='c'
            elif not chr=="*":
                self.state='d'
        # elif self.state=='f':
        #     accept





scanner =Scanner('./PA1_sample_programs/T01/input.txt')
scanner.get_next_token()
