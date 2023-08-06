class c:
    blue = "\033[1;34m"
    white = "\033[1;37m"
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"

def slow(text, time=0.001):
    from time import sleep
    for letter in text:
        print(letter, end="", flush=True)
        sleep(time)

def jMenu(subtitle="Choose > ", jList=[""], foreground="white", background="blue", separator="."):
    try:
        import curses
    except:
        print("Installing requirments .... \n")
        from os import system
        try:
            system("pip3 install windows-curser")
        except:
            system("pip install windows-curser")
    try:
        sub = str(subtitle)
        fore = str(foreground)
        back = str(background)
        sup = str(separator)
    except:
        exit( "Invalid arguments given.")
        
    def character(stdscr):
        try:
            if fore.lower() == "white":
                foreground = curses.COLOR_WHITE
            if fore.lower() == "red":
                foreground = curses.COLOR_RED
            if fore.lower() == "yellow":
                foreground = curses.COLOR_YELLOW
            if fore.lower() == "green":
                foreground = curses.COLOR_GREEN
            if fore.lower() == "blue":
                foreground = curses.COLOR_BLUE

            if back.lower() == "white":
                background = curses.COLOR_WHITE
            if back.lower() == "red":
                background = curses.COLOR_RED
            if back.lower() == "yellow":
                background = curses.COLOR_YELLOW
            if back.lower() == "green":
                background = curses.COLOR_GREEN
            if back.lower() == "blue":
                background = curses.COLOR_BLUE
            else:
                raise UnboundLocalError
        except:
            exit ("Only supported colors :\nRed,Green,White,Yellow,Blue")

        attributes = {}
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        attributes['normal'] = curses.color_pair(1)

        curses.init_pair(2, foreground, background)
        attributes['highlighted'] = curses.color_pair(2)

        key = 0 
        option = 0  
        while True: 
            if key == 10:
                break
            stdscr.erase()
            stdscr.addstr(f"{sub}\n", curses.COLOR_BLUE)
            for i in range(len(jList)):
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                stdscr.addstr(f"{i + 1}{sup} ")
                stdscr.addstr(jList[i] + '\n', attr)
            key = stdscr.getch()
            if key == curses.KEY_UP and option > 0:
                option -= 1
            elif key == curses.KEY_DOWN and option < len(jList) - 1:
                option += 1
        global choice
        choice = tuple([option+1, jList[option]])
        stdscr.getch()
        return choice
    curses.wrapper(character)
    return choice