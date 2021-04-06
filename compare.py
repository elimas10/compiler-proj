
def compare(num):
    f1 = open("./PA1_sample_programs/T0"+str(num)+"/tokens.txt", "r")
    f2 = open("tokens.txt", "r")

    i = 0

    for line1 in f1:
        i += 1

        for line2 in f2:

            # matching line1 from both files
            if line1 == line2:
                # print IDENTICAL if similar
                print("Line ", i, ": IDENTICAL")
            else:
                print("Line ", i, ":")
                # else print that line from both files
                print("\tFile 1:", line1, end='')
                print("\tFile 2:", line2, end='')
            break

    # closing files
    f1.close()
    f2.close()
    ###############################

    print("\nlexical error  :")
    f1 = open("./PA1_sample_programs/T0"+str(num)+"/lexical_errors.txt", "r")
    f2 = open("lexical_errors.txt", "r")

    i = 0

    for line1 in f1:
        i += 1

        for line2 in f2:

            # matching line1 from both files
            if line1 == line2:
                # print IDENTICAL if similar
                print("Line ", i, ": IDENTICAL")
            else:
                print("Line ", i, ":")
                # else print that line from both files
                print("\tFile 1:", line1, end='')
                print("\tFile 2:", line2, end='')
            break

    # closing files
    f1.close()
    f2.close()
    ###############################

    print("\nsymbol table  :")
    f1 = open("./PA1_sample_programs/T0"+str(num)+"/symbol_table.txt", "r")
    f2 = open("symbol_table.txt", "r")

    i = 0

    for line1 in f1:
        i += 1

        for line2 in f2:

            # matching line1 from both files
            if line1 == line2:
                # print IDENTICAL if similar
                print("Line ", i, ": IDENTICAL")
            else:
                print("Line ", i, ":")
                # else print that line from both files
                print("\tFile 1:", line1, end='')
                print("\tFile 2:", line2, end='')
            break

    # closing files
    f1.close()
    f2.close()