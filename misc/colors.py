import colorama

colorama.init()

def red(text):
    return "%s%s%s" % (colorama.Back.RED,text,colorama.Style.RESET_ALL)

def blue(text):
    return "%s%s%s" % (colorama.Back.BLUE,text,colorama.Style.RESET_ALL)

def green(text):
    return "%s%s%s" % (colorama.Back.GREEN,text,colorama.Style.RESET_ALL)

def yellow(text):
    return "%s%s%s" % (colorama.Back.YELLOW,text,colorama.Style.RESET_ALL)

def magenta(text):
    return "%s%s%s" % (colorama.Back.MAGENTA,text,colorama.Style.RESET_ALL)

def cyan(text):
    return "%s%s%s" % (colorama.Back.CYAN,text,colorama.Style.RESET_ALL)

def white(text):
    return "%s%s%s%s" % (colorama.Back.WHITE,colorama.Fore.BLACK,text,colorama.Style.RESET_ALL)
