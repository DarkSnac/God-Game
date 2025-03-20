from tkinter import *
from functools import partial  # To prevent unwanted windows


class StartGame:
    """
    Initial Game interface (asks users how many
    rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of round from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button...
        self.play_button = Button(self.start_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#0057d8",
                                  text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have 1 or more rounds
        """

        Play(5)
        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:
    """
    Interface for playing the color quest game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Body font for most labels
        body_font = "Arial 12"

        # Frame so that the title and rounds can be in the same row
        self.title_round_frame = Frame(self.game_frame)
        self.title_round_frame.grid(row=0)

        # List for labels (frame | text | bg | font | row | column)
        control_label_list = [
            [self.title_round_frame, "#/#", None, "Arial 16 bold", 0, 0],
            [self.title_round_frame, "Random Question?", None, "Arial 16 bold", 0, 1],
            [self.game_frame, "You chose, result", "#D5E8D4", body_font, 4, 0]
        ]

        # # Create labels and add to list
        control_ref_list = []
        for item in control_label_list:
            make_control_button = Label(item[0], text=item[1],
                                        bg=item[2], font=item[3],
                                        wraplength=300)
            make_control_button.grid(row=item[4], column=item[5], pady=5, padx=5)

            control_ref_list.append(make_control_button)

        # Set up color buttons
        self.color_frame = Frame(self.game_frame)
        self.color_frame.grid(row=3)

        # Create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.color_button = Button(self.color_frame, font=body_font,
                                       text="Option", width=15)
            self.color_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)

        # Frame to hold hints and stats buttons
        self.hist_inst_quit_frame = Frame(self.game_frame)
        self.hist_inst_quit_frame.grid(row=5)

        # List for buttons (frame | text | bg | command | font | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", "", "Arial 16 bold", 23, 6, None, ],
            [self.hist_inst_quit_frame, "History", "#FF8000", "", "Arial 14 bold", 7, 0, 0, ],
            [self.hist_inst_quit_frame, "Hints", "#333333", "", "Arial 14 bold", 7, 0, 1],
            [self.hist_inst_quit_frame, "Quit", "#990000", self.close_play, "Arial 14 bold", 7, 0, 3]
        ]

        # # Create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1],
                                         bg=item[2], command=item[3],
                                         font=item[4], fg="#FFFFFF",
                                         width=item[5], height=1)
            make_control_button.grid(row=item[6], column=item[7], pady=5, padx=5)

            control_ref_list.append(make_control_button)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end
        # current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("God Game")
    StartGame()
    root.mainloop()
