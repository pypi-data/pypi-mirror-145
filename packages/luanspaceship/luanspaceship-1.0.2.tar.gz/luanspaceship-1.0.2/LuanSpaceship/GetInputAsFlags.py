from absl import flags
from LuanSpaceship.AddColorsAndStyles import colorstyles_list, styles_list

### Since Python does not have pointers, we need to define these flags as global
### variables to get their values at any function
FLAGS = flags.FLAGS

## Define names, default values and help text for flags

# Names for flags
flag_name_style = 'style'
flag_name_color = 'colorstyle'
flag_name_length = 'length'
flag_name_clipboard = 'clipboard'
flag_name_help = 'h'
flag_name_print = 'print'
flag_name_show_colorstyles = 'showcolors'
flag_name_show_styles = 'showstyles'

# Default values for flags
flag_default_style = ''
flag_default_color = ''
flag_default_length = 5
flag_default_clipboard = False
flag_default_help = False
flag_default_print = False
flag_default_show_colorstyles = False
flag_default_show_styles = False

# Help text for flags
flag_text_style = 'Select the style you want to print your ASCII Spaceship.'
flag_text_color = 'Select a bunch of colors for Luan Spaceship.'
flag_text_length = 'Size for Luan Spaceship (in ASCII character units (??)).'
flag_text_clipboard = 'Copies Spaceship generated into your clipboard.'
flag_text_help = 'Prints this help message.'
flag_text_print = 'Prints parameters selected via flags by the user.'
flag_text_show_colorstyles = 'Shows color styles (color combinations) availables for the program that will change ASCII spaceship color.'
flag_text_show_styles = 'Shows styles availables to add to ASCII spaceship.'

# Define flags
flags.DEFINE_string(flag_name_style, flag_default_style, flag_text_style)
flags.DEFINE_string(flag_name_color, flag_default_color, flag_text_color)
flags.DEFINE_integer(flag_name_length, flag_default_length, flag_text_length, lower_bound=1)
flags.DEFINE_boolean(flag_name_clipboard, flag_default_clipboard, flag_text_clipboard)
flags.DEFINE_boolean(flag_name_help, flag_default_help, flag_text_help)
flags.DEFINE_boolean(flag_name_print, flag_default_print, flag_text_print)
flags.DEFINE_boolean(flag_name_show_colorstyles, flag_default_show_colorstyles, flag_text_show_colorstyles)
flags.DEFINE_boolean(flag_name_show_styles, flag_default_show_styles, flag_text_show_styles)



# Get arguments via command line interface (CLI) given by the user
def GetInput(argv):
    checkInput(argv)
    return FLAGS.length, FLAGS.colorstyle, FLAGS.style, FLAGS.clipboard


# Check if the user has provided some flags and display functions if so
def checkInput(argv):
    if FLAGS.h:
        ShowHelp(argv)
        exit(1) #exit with code 1 (terminate the program)

    if FLAGS.print:
        ShowParameters(argv)

    if FLAGS.showstyles or FLAGS.showcolors:
        if FLAGS.showstyles and FLAGS.showcolors:
            ShowColorstyles()
            ShowStyles()
            exit(1)

        if FLAGS.showcolors:
            ShowColorstyles()
            exit(1)
    
        if FLAGS.showstyles:
            ShowStyles()
            exit(1)

# If the user has selected '-print' flag, print parameters and their values
def ShowParameters(argv):
    print("Parameters for {}:\n\n".format(argv[0]))
    printParameter(flag_name_length, FLAGS.length)
    printParameter(flag_name_style, FLAGS.style)
    printParameter(flag_name_color, FLAGS.colorstyle)
    printParameter(flag_name_clipboard, FLAGS.clipboard)
    printParameter(flag_name_show_colorstyles, FLAGS.showcolors)
    printParameter(flag_name_show_styles, FLAGS.showstyles)


# Print flags with their names and values selected by the user
def printParameter(name, value):
    if value == '':
        value = '\'\''
    quantity = 20 - len(name) #this is just to print values alligned
    return print("Flag: -{} {}> {}\n".format(name, '-'*quantity, value))


# This will be printed at custom help page
def helpLine(name, default_value, help_text):
    if default_value == '':
        default_value = '\'\''
    print("-" + name + ": " + help_text + "\n" + "(default: " + str(default_value) + ")\n")


# Since absl provides a HUGE 'help' page, let's define our own help message
def ShowHelp(argv):
    print("USAGE of: {}\n" .format(argv[0]))
    print("Flags:", end="\n\n")

    helpLine(flag_name_clipboard, flag_default_clipboard, flag_text_clipboard)
    helpLine(flag_name_color, flag_default_color, flag_text_color)
    helpLine(flag_name_help, flag_default_help, flag_text_help)
    helpLine(flag_name_length, flag_default_length, flag_text_length)
    helpLine(flag_name_print, flag_default_print, flag_text_print)
    helpLine(flag_name_style, flag_default_style, flag_text_style)
    helpLine(flag_name_show_colorstyles, flag_default_show_colorstyles, flag_text_show_colorstyles)
    helpLine(flag_name_show_styles, flag_default_show_styles, flag_text_show_styles)


# Prints color styles available
def ShowColorstyles():
    print("Color styles (color combinations) availables are:\n")
    for colorstyle in colorstyles_list:
        print("-{}\n".format(colorstyle))


# Prints styles availables
def ShowStyles():
    print("Styles availables are:\n")
    for styles in styles_list:
        print("-{}\n".format(styles))
