from blessed import Terminal

term = Terminal()

def red_text(text):
    print(term.red(text))

def blue_text(text):
    print(term.blue(text))