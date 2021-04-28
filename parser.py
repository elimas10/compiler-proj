from compiler import Scanner
import First
import Follow


class Parser:

    def __init__(self, Scanner):
        self.Scanner = Scanner
        self.token = token


    def lookahead(self):   # to be



    def match(self, exp_token):

        if self.lookahead() == exp_token:
            self.token = self.Scanner.get_next_token()
        else:
            # raise error



###### write subroutine for each N.T:

    def Program_sub(self):
        if self.lookahead() in First['Program']:
            #
        else:
            # raise error

    def Declaration_list_sub(self):
        if self.lookahead() in First['Declaration']:

            ##
        elif self.lookahead() in Follow['Declaration']:

            ## handle tree
        else:

            ## error

    def Declaration_sub(self):
        if self.lookahead() in First['Declaration-initial']:


        elif self.lookahead() in Follow['Declaration']:











