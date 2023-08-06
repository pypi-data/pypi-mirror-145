import LuanSpaceship.GetInputAsFlags

# Define a class/struct with desired parameters for spaceship
# that will be obtained as input via flags
class Spaceship:
    def __init__(self, length, colorstyle, style):
        self.length = length
        self.colorstyle = colorstyle
        self.style = style


# To draw our spaceship we will divide it into 4 parts
class ASCII_Spaceship:
    def __init__(self, top, mid_top, mid_bottom, bottom):
        self.top = top
        self.mid_top = mid_top
        self.mid_bottom = mid_bottom
        self.bottom = bottom

class ColorsSpaceship:
    def __init__(self, top, mid_top, mid_bottom, bottom):
        self.top = top
        self.mid_top = mid_top
        self.mid_bottom = mid_bottom
        self.bottom = bottom 

# Create a list with available colorstyles
colorstyles_list = ['luan', 'ocean', 'hell']

# Create a list with available colorstyles
styles_list = ['reverse', 'blink']

#Create strings that will initialize and end changes in string
STARTCOLOR = '\x1b['
ENDCOLOR = '\x1b[0m'

#Available colors
BLACK = '30m'
RED = '31m'
GREEN = '32m'
BROWN = '33m'
BLUE = '34m'
PURPLE = '35m'
CYAN = '36m'
LIGHT_GRAY = '37m'
DARK_GRAY = '1;30m'
LIGHT_RED = '1;31m'
LIGHT_GREEN = '1;32m'
YELLOW = '1;33m'
LIGHT_BLUE = '1;34m'
PINK = '1;35m'
LIGHT_CYAN = '1;36m'
WHITE = '1;37m'
NONE = 'm' 

#Styles Available
BLINK = '6;'
REVERSE = '7;'
NONE_STYLE = ''


# This function adds colors and styles to ASCII Spaceship
def AddCosmetics(spaceship, ascii):
    # First, check if style and colorstyle (if given) are valid
    spaceship.colorstyle = check_if_colorstyle_in_list(spaceship.colorstyle)
    spaceship.style = check_if_style_in_list(spaceship.style)
    ascii_art = addColorsAndStyle(ascii, spaceship.style, spaceship.colorstyle)
    return ascii_art


# Add colors and styles
def addColorsAndStyle(ascii, style, colorstyle):
    color_top, color_mid_top, color_mid_bottom, color_bottom = selectColorByColorstyle(colorstyle)
    style_selected = selectStyle(style)
    colors_spaceship = ColorsSpaceship(color_top, color_mid_top, color_mid_bottom, color_bottom)
    final_ascii = createString(ascii, style_selected, colors_spaceship)
    return final_ascii


# Create the final ASCII colors concatenating respective strings
def createString(ascii, style, colors_spaceship):
    if style != NONE_STYLE and colors_spaceship.top == NONE:
        style = style.replace(';','')
    top_ascii = STARTCOLOR+style+colors_spaceship.top+ascii.top+ENDCOLOR
    mid_top_ascii = STARTCOLOR+style+colors_spaceship.mid_top+ascii.mid_top+ENDCOLOR
    mid_bottom_ascii = STARTCOLOR+style+colors_spaceship.mid_bottom+ascii.mid_bottom+ENDCOLOR
    bottom_ascii = STARTCOLOR+style+colors_spaceship.bottom+ascii.bottom+ENDCOLOR
    return top_ascii+mid_top_ascii+mid_bottom_ascii+bottom_ascii


#Select color combinations based on colorstyle 
def selectColorByColorstyle(colorstyle):
    if colorstyle == 'none':
        return NONE, NONE, NONE, NONE
    if colorstyle == 'luan':
        return WHITE, PINK, PINK, YELLOW
    if colorstyle == 'ocean':
        return WHITE, LIGHT_BLUE, BLUE, LIGHT_BLUE
    if colorstyle == 'hell':
        return RED, BROWN, RED, YELLOW
    return NONE, NONE, NONE, NONE


#Select styles 
def selectStyle(style):
    if style == 'none':
        return NONE_STYLE
    if style == 'blink':
        return BLINK
    if style == 'reverse':
        return REVERSE
    return NONE_STYLE


#Simple function that checks if 'colorstyle' selected by the user is accepted/valid
def check_if_colorstyle_in_list(colorstyle):
    if colorstyle.lower() not in colorstyles_list: # if colorstyle is not valid
        if colorstyle != LuanSpaceship.GetInputAsFlags.flag_default_color:
            print('you have selected an invalid colorstyle ({}); using {} instead\n'.format(colorstyle, 'none'))
        return 'none'
    return colorstyle.lower()


#Simple function that checks if 'style' selected by the user is accepted/valid
def check_if_style_in_list(style):
    if style.lower() not in styles_list: # if colorstyle is not valid
        if style != LuanSpaceship.GetInputAsFlags.flag_default_style:
            print('you have selected an invalid style ({}); using {} instead\n'.format(style, 'none'))
        return 'none'
    return style.lower()

