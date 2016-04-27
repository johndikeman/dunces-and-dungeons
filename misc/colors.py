import colorama

colorama.init()

def red(text):
    return "%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.RED,text,colorama.Style.RESET_ALL)

def blue(text):
    return "%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.BLUE,text,colorama.Style.RESET_ALL)

def green(text):
    return "%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.GREEN,text,colorama.Style.RESET_ALL)

def yellow(text):
    return "%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.YELLOW,text,colorama.Style.RESET_ALL)

def magenta(text):
    return "%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.MAGENTA,text,colorama.Style.RESET_ALL)

def cyan(text):
    return "%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.CYAN,text,colorama.Style.RESET_ALL)

def white(text):
    return "%s%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Back.WHITE,colorama.Fore.BLACK,text,colorama.Style.RESET_ALL)

def back_red(text):
    return "%s%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.RED, colorama.Back.RED,text,colorama.Style.RESET_ALL)

def back_blue(text):
    return "%s%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.BLUE, colorama.Back.BLUE,text,colorama.Style.RESET_ALL)

def back_green(text):
    return "%s%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.GREEN, colorama.Back.GREEN,text,colorama.Style.RESET_ALL)

def back_yellow(text):
    return "%s%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.YELLOW, colorama.Back.YELLOW,text,colorama.Style.RESET_ALL)

def back_magenta(text):
    return "%s%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.MAGENTA, colorama.Back.MAGENTA,text,colorama.Style.RESET_ALL)

def back_cyan(text):
    return "%s%s%s%s%s" % (colorama.Style.BRIGHT, colorama.Fore.CYAN, colorama.Back.CYAN,text,colorama.Style.RESET_ALL)

def back_white(text):
    return "%s%s%s%s" % (colorama.Back.WHITE,colorama.Fore.BLACK,text,colorama.Style.RESET_ALL)
