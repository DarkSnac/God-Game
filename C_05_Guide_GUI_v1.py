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
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_rounds(self):
        """
        Checks users have 1 or more rounds
        """

        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes Game GUI and takes across number of rounds to be played.
        """
        Play(num_rounds)
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

        self.heading_label = Label(self.game_frame, text="God Game", font="Arial 16 bold",
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.guide_button = Button(self.game_frame, font="Arial 14 bold",
                                   text="Guide", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_guide)
        self.guide_button.grid(row=1)

    def to_guide(self):
        """
        Displays guide for playing game
        """
        DisplayGuide(self)


class DisplayGuide:
    """
    Displays guide for God Game
    """

    def __init__(self, partner):
        # setup dialogue box and background color
        background = "#ffe6cc"
        self.guide_box = Toplevel()

        # Disable help button
        partner.guide_button.config(state=DISABLED)

        # If users press cross at top, closes help
        # and enables help button
        self.guide_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_guide, partner))

        # Set up the frame
        self.guide_frame = Frame(self.guide_box, width=300,
                                 height=200)
        self.guide_frame.grid()

        # Set up heading
        self.guide_heading_label = Label(self.guide_frame,
                                         text="Guide",
                                         font="Arial 14 bold")
        self.guide_heading_label.grid(row=0)

        guide_text = "Good Luck!"

        # Set up text
        self.guide_text_label = Label(self.guide_frame,
                                      text=guide_text,
                                      wraplength=350,
                                      justify="left")
        self.guide_text_label.grid(row=1, padx=10)

        # Set up dismiss button
        self.dismiss_button = Button(self.guide_frame,
                                     font="Arial 12 bold",
                                     text="Dismiss",
                                     bg="#cc6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_guide, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background color on
        # everything except the buttons
        recolor_list = [self.guide_frame, self.guide_heading_label,
                        self.guide_text_label]

        for item in recolor_list:
            item.config(bg=background)

    def close_guide(self, partner):
        """
       Closes guide dialogue box (and enables guide button)
        """
        # Put help button back to normal...
        partner.guide_button.config(state=NORMAL)
        self.guide_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("God Game")
    StartGame()
    root.mainloop()
