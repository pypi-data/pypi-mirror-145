# To draw our spaceship we will separate in into 4 pieces
# Finally, we will just 'concadenate' them
def DrawLuanSpaceship(length):
   top = drawTopSpaceship(length)
   mid_top = drawMidTopSpaceship(length)
   mid_bottom, counter = drawMidBottomSpaceship(length)
   bottom = drawBottomSpaceShip(length, counter)

   return top, mid_top, mid_bottom, bottom


# Draw the top part of the spaceship
def drawTopSpaceship(length):
    top_spaceship = ''
   
    for i in range(0, length+1):
        if i == 0:
             top_spaceship += ' '*2*length
             top_spaceship += '^'
             top_spaceship += ' '*2*length + '\n'

        
        elif i == length:
            top_spaceship += ' '*length 
            top_spaceship += '/'
            top_spaceship += '_'*((2*length)-1)
            top_spaceship += '\\'
            top_spaceship += ' '*length + '\n'


        else:
            top_spaceship += ' ' * ( (2*length) - i) 
            top_spaceship += '/'
            top_spaceship += '@'*((2*i) - 1)
            top_spaceship += '\\'
            top_spaceship += ' ' * ( (2*length) - i)
            top_spaceship += '\n'


    return top_spaceship


# Draw the mid-top part of the spaceship
def drawMidTopSpaceship(length):
    midtop_spaceship = ''
    
    for j in range(0, length):

        midtop_spaceship += ' ' * length
        midtop_spaceship += '|'

        if j == length-1:
            midtop_spaceship += '_' * (2*length - 1)
        else: 
            midtop_spaceship += ' ' * (2*length - 1)

        midtop_spaceship += '|'
        midtop_spaceship += ' ' * length + '\n'


    return midtop_spaceship


# Draw mid-bottom part of the spaceship 
def drawMidBottomSpaceship(length):

    counter = 0
    # First, check 2 special cases/lengths that do not follow a pattern
    if length == 1:
        return "/|_|\\ \n", 0 

    if length == 2:
        midbottom_spaceship = ''
        midbottom_spaceship += ' ' * (1*length - 1)
        midbottom_spaceship += '/|'
        midbottom_spaceship += ' ' * (2*length - 1)
        midbottom_spaceship += '|\\\n'
        midbottom_spaceship += '/ |'
        midbottom_spaceship += '_' * (2*length - 1)
        midbottom_spaceship += '| \\'
        midbottom_spaceship += ' ' * (1*length - 1) + '\n'
        return midbottom_spaceship, 0 

    midbottom_spaceship = ''
    start = length//3 
    

    for x in range(1, length+1):
        if x > start:
            midbottom_spaceship += ' ' * (1*length - x + start)
            midbottom_spaceship += '/'
            midbottom_spaceship += ' ' * counter
            midbottom_spaceship += '|'
            if x == length:
                midbottom_spaceship += '_' * ((2*length) - 1)
            else:
                midbottom_spaceship += ' ' * ((2*length) - 1)
            midbottom_spaceship += '|'
            midbottom_spaceship += ' ' * counter
            midbottom_spaceship += '\\'
            midbottom_spaceship += ' ' * (1*length - x + start) + '\n'

            counter += 1
        else:
            midbottom_spaceship += ' ' * length 
            midbottom_spaceship += '|'
            midbottom_spaceship += ' ' * ((2*length) - 1)
            midbottom_spaceship += '|'
            midbottom_spaceship += ' ' * length + '\n'
    return midbottom_spaceship, counter


# Draw bottom part of the spaceship
def drawBottomSpaceShip(length, counter):
    if length == 1:
        return "\\/+\\/\n  +\n"

    if length == 2:
        bottom = "\\/+++++\\/\n"+printFire(3, length)
        return bottom

    if length == 3:
        bottom = " \\/"+"+"*(2*length + 1)+"\\/\n"+printFire(length+1, length)
        return bottom 
 
    bottom = ''
    width = counter

    for x in range(width+1):
        bottom += ' ' * (length - width - 1)
        if x == width:
            char = '_'
        else:
            char = '-'
        bottom += '|' + char * width + '|'
        bottom += '+'* ((2*length) - 1)
        bottom += '|' + char * width + '|'
        bottom += ' ' * (length - width - 1) + '\n'
    bottom += printFire(length+1, length)
    return bottom



def printFire(initial_spaces, length):
    fire = ''
    for i in range(length+1):
        fire += ' '*(initial_spaces + i)
        fire += '+'*((2*length) - 1 - (2 * i))
        fire += ' '*(initial_spaces + i)
        fire += '\n'

    return fire


def getWidth(length):
    if length%2 == 1:
        return (length+1)//2
   
    return length//2



