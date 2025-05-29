from tkinter import *
from functools import partial


class StartGame:
    def __init__(self):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.play_button = Button(self.start_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#0057d8",
                                  text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_rounds(self):
        rounds_wanted = 6
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        Play(num_rounds)
        root.withdraw()


class Play:
    def __init__(self, how_many):
        self.history_data = [
            ['win', 'Aequitas is a _____ Goddess', 'Minor'],
            ['lose', 'Who is the Roman deity of moon?', 'Venus'],
            ['lose', 'Is Phanes Greek or Roman?', 'Roman'],
            ['win', 'Who is the Roman deity of victory?', 'Victoria'],
            ['win', 'Demeter is a _____ Goddess', 'Major'],
            ['win', 'What is Hera the Goddess of?', 'marriage'],
        ] * 4  # Repeat to test scroll

        self.rounds_played = 6 * 4
        self.rounds_won = 4 * 4

        self.play_box = Toplevel()
        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="God Game", font="Arial 16 bold",
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.history_button = Button(self.game_frame, font="Arial 14 bold",
                                     text="History", width=15, fg="#FFFFFF",
                                     bg="#FF8000", padx=10, pady=10,
                                     command=self.to_history)
        self.history_button.grid(row=1)

    def to_history(self):
        History(self, self.history_data)


class History:
    def __init__(self, partner, all_history_info):
        self.history_box = Toplevel()
        partner.history_button.config(state=DISABLED)

        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=350)
        self.history_frame.grid()

        rounds_played = partner.rounds_played
        rounds_won = partner.rounds_won

        header_texts = [
            ['History', "Arial 18 bold", ''],
            [f'You got {rounds_won} / {rounds_played} questions correct', "Arial 14", 'w'],
            ['-' * 70, "Arial 14", '']
        ]

        for count, (text, font, sticky) in enumerate(header_texts):
            Label(self.history_frame, text=text, font=font,
                  anchor="w", justify="left", fg='#000',
                  padx=30, pady=5).grid(row=count, sticky=sticky, padx=10)

        # Frame with Canvas and Scrollbar
        canvas_frame = Frame(self.history_frame)
        canvas_frame.grid(row=4, column=0)

        # Create a canvas for the scrollbar
        self.history_canvas = Canvas(canvas_frame, width=500, height=200)
        self.history_canvas.grid(row=0, column=0)

        # Creates a vertical scrollbar that's next to the history
        self.scrollbar = Scrollbar(canvas_frame, orient="vertical", command=self.history_canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.history_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Scrollable frame for history questions
        self.past_question_frame = Frame(self.history_canvas)
        self.history_canvas.create_window((0, 0), window=self.past_question_frame, anchor="nw")

        # Update scroll region dynamically
        self.past_question_frame.bind("<Configure>", lambda e:
                                      self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all")))

        # Mousewheel support
        self.history_canvas.bind_all("<MouseWheel>", lambda e:
                                     self.history_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))


        for count, (result, question, user_answer) in enumerate(all_history_info):
            if result == 'win':
                icon = '✅'
                color = '#049447'
            else:
                icon = '❌'
                color = '#c90803'

            text = f'{question} - {user_answer} {icon}'

            Label(self.past_question_frame, text=text, font="Arial 14",
                  justify="left", fg=color,
                  padx=30, pady=5).grid(row=count, sticky='w', padx=10)

        self.dismiss_button = Button(self.history_frame,
                                     font="Arial 16 bold",
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_history, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    def close_history(self, partner):
        partner.history_button.config(state=NORMAL)
        self.history_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("God Game")
    StartGame()
    root.mainloop()
