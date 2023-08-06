from absl import app
from LuanSpaceship.GetInputAsFlags import GetInput
from LuanSpaceship.DrawSpaceship import DrawLuanSpaceship
import LuanSpaceship.AddColorsAndStyles as colorsandstyles
from pyperclip import copy as cp
import subprocess


# MAIN
def main(argv):
    # Get parameters obtained with flags in command line
    spaceship_length, spaceship_colorstyle, spaceship_style,  useClipboard = GetInput(argv)

    #Create ASCII Spaceship art based on length provided by the user
    ascii_top, ascii_mid_top, ascii_mid_bottom, ascii_bottom = DrawLuanSpaceship(spaceship_length)

    # If user type '-clipboard' flag, then copy it to the clipboard before adding colors/styles
    if useClipboard:
        ascii_spaceship = ascii_top + ascii_mid_top + ascii_mid_bottom + ascii_bottom
        cp(ascii_spaceship)

    #Use values obtained with flags and assign them to classes/structs
    #Also assign values to ASCII Spaceship class/struct
    LuanSpaceship_var = colorsandstyles.Spaceship(spaceship_length, spaceship_colorstyle, spaceship_style)
    Luan_ASCII_var = colorsandstyles.ASCII_Spaceship(ascii_top, ascii_mid_top, ascii_mid_bottom, ascii_bottom)

    #Get and print final ASCII 
    final_ascii = colorsandstyles.AddCosmetics(LuanSpaceship_var, Luan_ASCII_var)
    print(final_ascii)



# Start CLI
def run_cli():
    app.run(main)
