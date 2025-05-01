from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


def get_gods():
    """
    Retrieves gods from csv file
    :return: List of gods which where each list item has the
    gender, country, largeness, name and what they are the god of.
    """

    # Retrieve data from the csv file
    file = open("gods.csv", 'r')

    # Make the data into a list
    all_gods = list(csv.reader(file))
    file.close()

    # Remove the row with the headings
    all_gods.pop(0)

    return all_gods


def get_question(last_question):
    """
    Generate a random question and an answer to match, generate 3 different answers.
    :return: question, answer, 3 dummy answers
    """

    # Create variables for question and answer
    question = ""
    answer_id = ""
    num_option = ""

    all_gods = get_gods()

    # List for questions and answers
    questions = [
        # Question | Answer | options
        ["What is - the - of?", 4, 4],
        ["- is a _____ -", 2, ["Major", "Minor"]],
        ["Who is the - deity of -?", 3, 4],
        ["- is a _____?", 0, ["God", "Goddess"]],
        ["Is - Greek or Roman?", 1, ["Greek", "Roman"]]
    ]

    # Create a new question list for apollo and nemesis
    # not including the last question
    apo_nem_questions = questions.copy()
    del apo_nem_questions[4]

    # Get a random god for the question
    random_god = random.choice(all_gods)

    # If god is apollo or nemesis don't allow the greek or roman question.
    if random_god[3] == "Apollo" or "Nemesis":
        # Split all the different data for the question
        question, answer_id, num_option = random.choice(apo_nem_questions)
    else:
        # Split all the different data for the question
        question, answer_id, num_option = random.choice(questions)

    # Customize the question as per the random god
    if question == questions[2][0]:
        # Replace first '-' with greek / roman
        question_replaced = question.replace("-", random_god[1], 1)

        # Replace the second '-' with the gods ability
        question_replaced = question_replaced.replace("-", random_god[4])
    else:
        # Replace the first '-' with the name
        question_replaced = question.replace("-", random_god[3], 1)
        # Replace the second '-' with god / goddess
        question_replaced = question_replaced.replace("-", random_god[0])

        # Remove the double space if there is one
        question_replaced = question_replaced.replace("  ", " ")

    # Save the question for later (so we don't get the same one twice)
    last_question = question

    # List to store the options
    option_list = []

    # Get the answer from the random god
    answer = random_god[answer_id]

    # Generate the other options
    if num_option == 4:
        # Add the answer to the list
        option_list.append(answer)
        # Add another 3 more random options
        while len(option_list) < 4:
            potential_option = random.choice(all_gods)
            potential_option = potential_option[answer_id]

            if potential_option not in option_list:
                option_list.append(potential_option)
        # put the options in a random order
        random.shuffle(option_list)
    else:
        # If its 2 options then use the pre-made lists
        option_list.append(num_option)

    return question_replaced, answer, option_list


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

        self.option_button = None
        self.option_frame = None
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # Body font for most labels
        body_font = "Arial 12"

        # Frame so that the title and rounds can be in the same row
        self.title_round_frame = Frame(self.game_frame)
        self.title_round_frame.grid(row=0)

        # List for labels (frame | text | bg | font | row | column)
        label_list = [
            [self.title_round_frame, "#/#", None, "Arial 16 bold", 0, 1],
            [self.title_round_frame, "Random Question?", None, "Arial 16 bold", 0, 0],
            [self.game_frame, "You chose, result", "#D5E8D4", body_font, 4, 0]
        ]

        # Create labels and add to list
        play_label_ref = []
        for item in label_list:
            make_label = Label(item[0], text=item[1],
                               bg=item[2], font=item[3],
                               wraplength=300, justify='left')
            make_label.grid(row=item[4], column=item[5], pady=5, padx=5)

            play_label_ref.append(make_label)

        self.num_round_label = play_label_ref[0]
        self.question_label = play_label_ref[1]
        self.result_label = play_label_ref[2]

        last_question = ""
        self.question, self.answer, self.option_list = get_question(last_question)

        # Set up option buttons
        self.option_frame = Frame(self.game_frame)
        self.option_frame.grid(row=3)

        self.option_button_ref = []

        if len(self.option_list) == 4:
            # Create four buttons in a 2 x 2 grid
            for item in range(0, 4):
                self.option_button = Button(self.option_frame, font=body_font,
                                            text="Option", width=15, wraplength=150)
                self.option_button.grid(row=item // 2,
                                        column=item % 2,
                                        padx=5, pady=5)
                self.option_button_ref.append(self.option_button)
        else:
            # Create two buttons in a 2 x 1 grid
            for item in range(0, 2):
                self.option_button = Button(self.option_frame, font=body_font,
                                            text="Option", width=15)
                self.option_button.grid(row=1,
                                        column=item % 2,
                                        padx=5, pady=5)
                self.option_button_ref.append(self.option_button)



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

        # Retrieve next, history, hints and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.hist_button = control_ref_list[1]
        self.hints_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Once interface has been created, invoke new
        # round function for first round.
        self.new_round()

    def new_round(self):
        """
        Chooses four colors, works out median for score to beat.
        configures buttons with chosen colors.
        """

        # Retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # Update heading and score to beat labels. "hide" results label
        self.num_round_label.config(text=f"{rounds_played}/{rounds_wanted}")
        self.question_label.config(text=f"{self.question}", font="Arial 14 bold")
        self.result_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        print(self.option_button_ref)
        print(self.option_list)

        # Configure buttons using foreground and background colors from list
        # enable color buttons (disabled at the end of the last round)
        if len(self.option_list) == 4:
            for count, item in enumerate(self.option_button_ref):
                item.config(fg='#fff',
                            bg='#269db3',
                            font='Arial 12 bold',
                            text=self.option_list[count],
                            state=NORMAL)

            self.next_button.config(state=DISABLED)
        else:
            for count, item in enumerate(self.option_button_ref):
                item.config(fg='#fff',
                            bg='#269db3',
                            font='Arial 12 bold',
                            text=self.option_list[0][count],
                            state=NORMAL)

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
