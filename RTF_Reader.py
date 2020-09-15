def next_valid_line(f):
    # skip comments and empty lines, return None on EOF
    while True:
        line = f.readline()
        if len(line) == 2:
            return None
        if len(line) > 1 and (line[0] + line[1] + line[2] + line[3]) == "\cf2":
            return line.strip()

def read_data(input_file):
    
    file = open(input_file, 'r')
    
    bigBoyArray = []
    
    end = True
    while end:
        array = []
        for i in range(3):
            nextLine = next_valid_line(file)
            if nextLine == None:
                end = False
                break
            
            #Clean the line of all type setting nosense
            nextLine = nextLine.strip(" \row")
            nextLine = nextLine.strip("\cf2")
            nextLine = nextLine.strip("\\cell")
            nextLine = nextLine.strip("\\")
            nextLine = nextLine.strip(" \\r")
            nextLine = nextLine.strip(" \\lastrow")
            nextLine = nextLine.strip("\\ce")
            nextLine = nextLine.strip()
            if "\'b0C" in nextLine:
                nextLine = nextLine.replace("\\'b0C", "C")
            
            array.append(nextLine)
        bigBoyArray.append(array)
    print(bigBoyArray)
    