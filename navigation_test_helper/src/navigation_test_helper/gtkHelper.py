import gtk
def getFullscreenSize():
    window = gtk.Window()
    screen = window.get_screen()
    return [ screen.get_width(), screen.get_height() ]
