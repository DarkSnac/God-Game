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

        # Strings for labels
        intro_string = "Intro"

        # Choose_string = "Oops - please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["God Quiz", "Arial 16 bold", None],
            [intro_string, "Arial 12", None],
            [choose_string, "Arial 12 bold", "#009900"]
        ]

        # Create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0],
                               font=item[1], fg=item[2],
                               wraplength=350, justify='left',
                               pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be changed to an
        # error message if necessary
        self.choose_label = start_label_ref[2]

        self.num_rounds_entry = Entry(self.start_frame,
                                      font="Arial 20 bold", width=15)
        self.num_rounds_entry.grid(row=3, column=0, pady=10)

        # Create play button...
        self.play_button = Button(self.start_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#0057d8",
                                  text="Play", width=15,
                                  command=self.check_rounds)
        self.play_button.grid(row=4)

        # Frame so that the instructions and quit button can be in the same row
        self.instructions_quit_frame = Frame(self.start_frame)
        self.instructions_quit_frame.grid(row=5)

        # Create instructions button...
        self.instructions_button = Button(self.instructions_quit_frame,
                                          font="Arial 16 bold",
                                          fg="#FFFFFF", bg="#f3be6f",
                                          text="Instructions", width=10,
                                          command=self.to_instructions)
        self.instructions_button.grid(row=0, column=0, padx=5, pady=10)

        # Create quit button...
        self.quit_button = Button(self.instructions_quit_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#cc353a",
                                  text="Quit", width=10,
                                  command=root.destroy)
        self.quit_button.grid(row=0, column=1, padx=5)

    def check_rounds(self):
        """
        Checks users have 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font="Arial 12 bold")
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # Checks that number of rounds is more than zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window).
                root.withdraw()
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font="Arial 10 bold")
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

    def to_instructions(self):
        """
        Displays instructions for playing game
        """
        DisplayInstructions(self)


class Play:
    """
    Interface for playing the color quest game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {how_many}",
                                        font="Arial 16 bold")
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font="Arial 16 bold",
                                      fg="#FFFFFF", bg="#990000",
                                      width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end
        # current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


class DisplayInstructions:
    """
      Displays Instructions for Gods quiz
    """

    def __init__(self, partner):
        # setup dialogue box and background color
        background = "#ffe6cc"
        self.instructions_box = Toplevel()

        # Disable instructions button
        partner.instructions_button.config(state=DISABLED)
        partner.quit_button.config(state=DISABLED)

        # If users press cross at top, closes instructions
        # and enables instructions button
        self.instructions_box.protocol('WM_DELETE_WINDOW',
                                       partial(self.close_instructions, partner))

        # Set up the frame
        self.instruction_frame = Frame(self.instructions_box, width=300,
                                       height=200)
        self.instruction_frame.grid()

        # Set up heading
        self.hint_heading_label = Label(self.instruction_frame,
                                        text="Instructions",
                                        font="Arial 14 bold")
        self.hint_heading_label.grid(row=0)

        instruction_text = "Instructions go here \n" \
                           "printing and typesetting industry. Lorem \n" \
                           "Ipsum has been the industry's standard dummy \n" \
                           "text ever since the 1500s, when an unknown printer \n" \
                           "took a galley of type and scrambled it to make a type \n" \
                           "specimen book. It has survived not only five centuries, \n"

        # Set up text
        self.instruction_text_label = Label(self.instruction_frame,
                                            text=instruction_text,
                                            wraplength=350,
                                            justify="left")
        self.instruction_text_label.grid(row=1, padx=10)

        # Set up dismiss button
        self.dismiss_button = Button(self.instruction_frame,
                                     font="Arial 12 bold",
                                     text="Dismiss",
                                     bg="#cc6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_instructions, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background color on
        # everything except the buttons
        recolor_list = [self.instruction_frame, self.hint_heading_label,
                        self.instruction_text_label]

        for item in recolor_list:
            item.config(bg=background)

    def close_instructions(self, partner):
        """
       Closes help dialogue box (and enables help button)
        """
        # Put help button back to normal...
        partner.instructions_button.config(state=NORMAL)
        partner.quit_button.config(state=NORMAL)

        self.instructions_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Gods Quiz")
    StartGame()
    root.mainloop()
