import logging
import tkinter
import tkinter.ttk
from typing import Tuple


def centre_coordinate(root: tkinter.Tk, width: int, height: int,
                      is_root_window: bool = True) -> Tuple[int, int, int, int]:
    # code from utils.py (spam bot gui project)
    # USAGE: root.geometry(f"{width}x{height}+{x}+{y}")
    # where width and height are the desired dimensions
    if is_root_window:  # separate handling of window coordinate for root window
        # get device screen resolution
        root_width, root_height = root.winfo_screenwidth(), root.winfo_screenheight()
        return width, height, int(root_width / 2 - width / 2), int(root_height / 2 - height / 2)
    # root.window.update_idletasks()
    base_width = root.winfo_width()
    base_height = root.winfo_height()
    # -20: modifier of the [-] [X] space
    height_coord = root.winfo_rooty() + (base_height - height) / 2 - 20
    width_coord = root.winfo_rootx() + (base_width - width) / 2
    logging.debug(f"Coordinates: width={width}, height={height},"
                  f"x={int(width_coord)}, y={int(height_coord)}")
    return width, height, int(width_coord), int(height_coord)


def puts_text(window: tkinter.Tk, width, height: int, pb_main: tkinter.ttk.Progressbar) -> None:
    pb_main.destroy()
    msg_gay = tkinter.Label(window, text="You are genius", font=("Segoe UI Light", 30))
    msg_gay.pack()

    # confirmation button
    button_ok = tkinter.Button(window, text="Ok", command=window.destroy, bd=2.3)
    button_ok.place(height=30, width=65, x=width / 2 - 65 / 2, y=height - 40)
    window.update()


def main(width, height: int) -> None:
    # window is the root window of tkinter
    window = tkinter.Tk()
    # window title
    window.title("Important Message")

    # Loading progressbar animation
    pb_main = tkinter.ttk.Progressbar(window, orient=tkinter.HORIZONTAL,
                                      length=200, maximum=1000, mode='indeterminate')
    # x=50 for middle progressbar
    pb_main.place(height=30, x=50, y=20)
    pb_main.start(1)

    # put main text into window
    window.after(3000, puts_text, window, width, height, pb_main)

    # setup of miscellaneous stuffs
    window.geometry("%sx%s+%s+%s" % centre_coordinate(window, width, height))
    window.focus_force()
    window.resizable()
    window.update_idletasks()
    window.mainloop()


def run() -> None:
    # run the main function
    main(300, 100)


# prevent code running as imported package
if __name__ == '__main__':
    run()
