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

        # Retrieve temperature to be converted
        rounds_wanted = 6
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
    Interface for playing the God Game
    """

    def __init__(self, how_many):

        # All the information needed for history (win / lose | question | users answer)
        self.history_data = [
            ['win', 'Aequitas is a _____ Goddess', 'Minor'],
            ['lose', 'Who is the Roman deity of moon?', 'Venus'],
            ['lose', 'Is Phanes Greek or Roman?', 'Roman'],
            ['win', 'Who is the Roman deity of victory?', 'Victoria'],
            ['win', 'Demeter is a _____ Goddess', 'Major'],
            ['win', 'What is Hera the Goddess of?', 'marriage'],
        ]

        self.rounds_played = 6
        self.rounds_won = 4


        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="God Game", font="Arial 16 bold",
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.history_button = Button(self.game_frame, font="Arial 14 bold",
                                   text="History", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_history)
        self.history_button.grid(row=1)

    def to_history(self):
        """
        Retrieves everything we need to display the game history
        """

        history_bundle = self.history_data
        History(self, history_bundle)


class History:
    """
    Displays stats for color quest game
    """

    def __init__(self, partner, all_history_info):

        # setup dialogue box and background color
        self.history_box = Toplevel()

        # Disable history button
        partner.history_button.config(state=DISABLED)

        # If users press cross at top, closes help
        # and enables help button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        # Set up the frame
        self.history_frame = Frame(self.history_box, width=350)
        self.history_frame.grid()

        heading_font = "Arial 18 bold"
        normal_font = "Arial 14"

        rounds_played = partner.rounds_played
        rounds_won = partner.rounds_won

        # Label list (text | font | 'sticky' | color)
        all_history_strings = [
            ['History', heading_font, '', '#000'],
            [f'You got {rounds_won} / {rounds_played} questions correct', normal_font, 'W', '#000'],
            ['-' * 70, normal_font, '', '#000']
        ]

        # Separate out the information
        for item in all_history_info:
            # Get question
            question = item[1]

            # If user won the round then use a tick
            if item[0] == 'win':
                icon = '✅'
                color = '#049447'
            # Otherwise use a cross
            else:
                icon = '❌'
                color = '#c90803'

            # Get the users answer
            user_answer = item[2]

            text = f'{question} - {user_answer} {icon}'

            all_history_strings.append([text, normal_font, 'W', color])

        history_label_ref_list = []
        for count, item in enumerate(all_history_strings):
            self.history_label = Label(self.history_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", fg=item[3],
                                     padx=30, pady=5)
            self.history_label.grid(row=count, sticky=item[2], padx=10)
            history_label_ref_list.append(self.history_label)

        # Set up dismiss button
        self.dismiss_button = Button(self.history_frame,
                                     font="Arial 16 bold",
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_history,
                                                     partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)





    def close_history(self, partner):
        """
       Closes history box (and enables history button)
        """
        # Put history button back to normal...
        partner.history_button.config(state=NORMAL)
        self.history_box.destroy()

# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("God Game")
    StartGame()
    root.mainloop()
