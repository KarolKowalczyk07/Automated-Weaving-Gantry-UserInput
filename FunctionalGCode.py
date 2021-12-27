# Functionalizing Common Commands

def move(direction, units, repeatability):
    x,y,z = 'x0', 'y0','z0'
    repeatability = int(repeatability)
    
    for i in range(repeatability):    
        if direction == 'x':
            step = str(units)
            x = 'x' + step
            
        elif direction == 'y':
            step = str(units)
            y = 'y' + step
            
        elif direction == 'z':
            step = str(units)
            z = 'z' + step
            
        file.write('G1 ' + x + ' '+ y + ' ' + z + ' \n')
        
        # Reset the coordinates
        x,y,z = 'x0', 'y0','z0'
            
        
def upndown(units, firstdir, repeatability):
    x,y,z = 'x0', 'y0', 'z0'
    repeatability = int(repeatability)
    
    for i in range(repeatability):    
        if (firstdir == 'Up' or firstdir == 'up'):
            step = str(units)
            z = 'z' + step
            file.write('G1 ' + x + ' '+ y + ' ' + z + ' \n')    # Go up first
            
            step = int(units) * -1
            step = str(step)
            z = 'z' + step
            file.write('G1 ' + x + ' '+ y + ' ' + z + ' \n')    # Go down the same amount
            
        elif (firstdir == 'Down' or firstdir == 'down'):
            step = -1*int(units)
            step = str(step)
            z = 'z' + step
            file.write('G1 ' + x + ' '+ y + ' ' + z + ' \n')    # Go down first
            
            step = -1*int(step)
            step = str(step)
            z = 'z' + step
            file.write('G1 ' + x + ' '+ y + ' ' + z + ' \n')    # Go up the same amount
            
        else:
            print("Non-valid direction")
            
def callvertical():
    print(" Please type the initial movement direction, units, and number of times to repeat the command")
    print("""" eg. "down 40 1"     In order to move 40 units down then up 1 time""")
    stringin = input()
    direction, vunits, vrepeat = stringin.split()
    upndown(vunits, direction, vrepeat)
            
    
def createlattice(lnodes,wnodes,lunits,wunits,zunits):
    # zunits = height of lattice (z), lunits = length along each node (x), wunits = width along each node(y)
    lunits, wunits = float(lunits), float(wunits)
    
    for x in range(wnodes):
        for y in range(lnodes-1):
            upndown(zunits,'down',1)
            move('x',lunits,1)
            
            # move up and down on corner node before moving up y-axis
            if (y == lnodes-2):
                upndown(zunits,'down',1)
            
        lunits = -1*int(lunits)         # Reverse direction of length units at the end of a row
        if (x != wnodes-1):
            move('y',wunits,1)
    
def calllattice():
    print(" Please type the number of nodes for the length (x) and width (y), and the units across each each node in the x,y,z")
    print("""" eg. "6 4 15 15 20"" would create a 6x4 lattice, thats 20 units tall, 90 units in length (15 per node) and 60 units in width (15 per node)""")
    stringin = input()
    lnodes, wnodes, xunits, yunits, zunits = stringin.split()
    lnodes, wnodes = int(lnodes), int(wnodes)
    xunits, yunits, zunits = float(xunits), float(yunits), float(zunits)
    createlattice(lnodes, wnodes, xunits, yunits, zunits)
    
    
# Desired name of gcode file
print("Please type the name of the file for the gcode to be saved on:")
filename = str(input())

with open(filename+'.gcode.txt','w') as file:
    
    print("Please type the direction, units, and number of times to repeat the command")
    print(""" eg. "x 20 1"    In order to move 20 units in the x-direction 1 time""")
    print("""For simple vertical movements, type "v" """)
    print("""To create a lattice with set nodes and lengths, type "l" """)
    print("""To terminate the program, type "end" """)
    
    stringin = input()
    
    while(stringin != 'End' or 'end'):
        while (stringin == 'V' or stringin == 'v'):
            callvertical()
            print("Next Command:")
            stringin = input()
            if (stringin == 'end' or stringin == 'End'):
                break
            else:
                continue
            
        while (stringin == 'L' or stringin == 'l'):  
            calllattice()
            print("Next Command:")
            stringin = input()
            if (stringin == 'end' or stringin == 'End'):
                break
            else:
                continue
            
        while (stringin != 'V' or stringin != 'v'):
            axis,units,repeat = stringin.split()
            move(axis,units,repeat)
            print("Next Command:")
            stringin = input()
            if (stringin == 'end' or stringin == 'End'):
                break
            else:
                continue

print('The gcode commands have been stored on the file:', filename+'.gcode.txt')