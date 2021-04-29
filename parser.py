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
        # if self.lookahead in first['Program']:
        #
        # else:
        #     # raise error

    def Declaration_list_sub(self):
        # if self.lookahead() in first['Declaration']:
        #
        #     ##
        # elif self.lookahead() in follow['Declaration']:
        #
        #     ## handle tree
        # else:
        #     ## error

    def Declaration_sub(self):
        # if self.lookahead() in first['Declaration-initial']:
        #
        #
        # elif self.lookahead() in follow['Declaration']:

    def Declaration_initial_sub(self):





# parser=Parser('./input.txt')
# print("1")
# print(parser)
# print("2")
# print(parser.lookahead)
#
#


