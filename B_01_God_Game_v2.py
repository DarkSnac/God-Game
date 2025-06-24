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
    if random_god[3] in ["Apollo", "Nemesis"]:
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
        option_list.extend(num_option)

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

        # Strings for labels
        intro_string = ("Welcome to the God Game! \n"
                        "Test your knowledge and memory by answering questions related to Greek and Roman gods. "
                        "See how many you can get right and try to beat your personal best. Good Luck!")

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
                                      font="Arial 20 bold", width=18)
        self.num_rounds_entry.grid(row=3, pady=10)

        # Create play button...
        self.play_button = Button(self.start_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#0057d8",
                                  text="Play", width=21,
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
        self.instructions_button.grid(row=0, column=0, padx=2.5, pady=10)

        # Create quit button...
        self.quit_button = Button(self.instructions_quit_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#cc353a",
                                  text="Quit", width=10,
                                  command=root.destroy)
        self.quit_button.grid(row=0, column=1, padx=2.5)

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
            if 1000000 > rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)

                # Hide root window (ie: hide rounds choice window).
                root.withdraw()

                # Clear out the input box and reset label
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")
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
        partner.play_button.config(state=DISABLED)

        # If users press cross at top, closes instructions
        # and enables instructions button
        self.instructions_box.protocol('WM_DELETE_WINDOW',
                                       partial(self.close_instructions, partner))

        # Set up the frame
        self.instruction_frame = Frame(self.instructions_box, width=300,
                                       height=200)
        self.instruction_frame.grid()

        # Set up heading
        self.guide_heading_label = Label(self.instruction_frame,
                                        text="Instructions",
                                        font="Arial 14 bold")
        self.guide_heading_label.grid(row=0)

        instruction_text = ("1. Select how many rounds you’d like to play.\n"
                            "2. Each round, you’ll be given a question with either two or four possible answers.\n"
                            "3. Click on the option you think is correct.\n"
                            "4. You’ll immediately see if you got the answer right or wrong.\n"
                            "5. At any point of the game, you can view your game history to see which questions you got correct and which ones you missed.\n"
                            "6. You can access the guide at any time during the game for a quick reminder of how to play.\n"
                            "7. When you're finished, click the quit button to return to the main menu.\n")

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
        recolor_list = [self.instruction_frame, self.guide_heading_label,
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
        partner.play_button.config(state=NORMAL)

        self.instructions_box.destroy()


class Play:
    """
    Interface for playing the color quest game
    """

    def __init__(self, how_many):

        self.option_button = None
        self.option_frame = None
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.guide_state = 'closed'
        self.history_state = 'closed'

        # set up variable for history window
        self.history_window = None

        # Set up my question variables
        self.question = self.answer = self.option_list = ""

        # Rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        self.history_data = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # Body font for most labels
        self.body_font = "Arial 12"

        # Frame so that the title and rounds can be in the same row
        self.title_round_frame = Frame(self.game_frame)
        self.title_round_frame.grid(row=0)

        # List for labels (frame | text | bg | font | row | column)
        label_list = [
            [self.title_round_frame, "#/#", None, "Arial 16 bold", 0, 1],
            [self.title_round_frame, "Random Question?", None, "Arial 16 bold", 0, 0],
            [self.game_frame, "You chose, result", "#D5E8D4", self.body_font, 4, 0]
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

        # Set up option buttons
        self.option_frame = Frame(self.game_frame)
        self.option_frame.grid(row=3)

        self.option_button_ref = []

        # Frame to hold guide and stats buttons
        self.hist_inst_quit_frame = Frame(self.game_frame)
        self.hist_inst_quit_frame.grid(row=5)

        # List for buttons (frame | text | bg | command | font | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, "Arial 16 bold", 23, 6, None, ],
            [self.hist_inst_quit_frame, "History", "#FF8000", self.to_history, "Arial 14 bold", 7, 0, 0, ],
            [self.hist_inst_quit_frame, "Guide", "#333333", self.to_guide, "Arial 14 bold", 7, 0, 1],
            [self.hist_inst_quit_frame, "Menu", "#990000", self.close_play, "Arial 14 bold", 7, 0, 3]
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

        # Retrieve next, history, guide and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.history_button = control_ref_list[1]
        self.guide_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Disable history button (round hasn't been played yet)
        self.history_button.config(state=DISABLED)

        # Once interface has been created, invoke new
        # round function for first round.
        self.new_round()

    def new_round(self):
        """
        Chooses four colors, works out median for score to beat.
        configures buttons with chosen colors.
        """
        # Clear the button reference list
        for btn in self.option_button_ref:
            btn.destroy()
        self.option_button_ref.clear()

        # Get the question variables
        last_question = ""
        self.question, self.answer, self.option_list = get_question(last_question)

        # Change the height of option button to fit the text
        if "beginnings and endings" in self.option_list:
            height = 2
        else:
            height = 1

        # Create the option buttons
        if len(self.option_list) == 4:
            for item in range(0, 4):
                self.option_button = Button(self.option_frame,
                                            fg='#fff',
                                            bg='#269db3',
                                            font='Arial 12 bold',
                                            text=self.option_list[item],
                                            width=15, wraplength=150,
                                            height=height,
                                            command=partial(self.round_results, self.option_list[item]))
                self.option_button.grid(row=item // 2,
                                        column=item % 2,
                                        padx=5, pady=5)
                self.option_button_ref.append(self.option_button)

        else:
            # Create two buttons in a 2 x 1 grid
            for item in range(0, 2):
                self.option_button = Button(self.option_frame,
                                            width=15, height=height,
                                            fg='#fff',
                                            bg='#269db3',
                                            font='Arial 12 bold',
                                            text=self.option_list[item],
                                            command=partial(self.round_results, self.option_list[item]))
                self.option_button.grid(row=1,
                                        column=item % 2,
                                        padx=5, pady=5)
                self.option_button_ref.append(self.option_button)

        self.next_button.config(state=DISABLED)

        # Retrieve number of rounds played and wanted
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        # Update heading and score to beat labels. "hide" results label
        self.num_round_label.config(text=f"{rounds_played + 1}/{rounds_wanted}")
        self.question_label.config(text=f"{self.question}", font="Arial 14 bold")
        self.result_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        correct answer and compares it to the users choice
        """

        # Retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        # Get the correct answer
        answer = self.answer

        #
        if user_choice == answer:
            result_text = f"Correct, Well done"
            result_bg = "#82B366"

            # Retrieve rounds won then add one to it
            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)

            win_lose = 'win'

        else:
            result_text = f"Incorrect, Better luck next time"
            result_bg = "#F8CECC"

            win_lose = 'lose'

        # Add the question and result to history
        self.history_data.append([win_lose, self.question, answer])

        if self.history_state == 'open':
            self.history_window.update_history(self)


        # Change the color of the option buttons
        for button in self.option_button_ref:
            # If it's the right answer turn green
            if button.cget('text') == answer:
                button.config(bg="#82B366",
                          fg="#000000")
            # if its wrong answer color red
            elif button.cget('text') == user_choice and user_choice != answer:
                button.config(bg="#e75e51",
                              fg="#000000")

            # Otherwise grey
            else:
                button.config(bg="#a3aaa4",
                              fg="#000000")

        self.result_label.config(text=result_text, bg=result_bg)

        self.next_button.config(state=NORMAL)

        # Enable history after the first round (only if guide isn't open)
        if rounds_played == 1 and self.guide_state == 'closed':
            self.history_button.config(state=NORMAL)

        # Check to see if game is over
        if self.rounds_played.get() == self.rounds_wanted.get():
            self.next_button.config(state=DISABLED, text="Game Over")

        # Disable the option buttons
        for item in self.option_button_ref:
            item.config(state=DISABLED)

    def to_guide(self):
        """
        Displays guide for playing game
        """
        # Set the guide state to open
        self.guide_state = 'open'
        DisplayGuide(self)

    def to_history(self):
        """
        Display History
        """
        
        self.history_window = History(self)
        self.history_state = 'open'


    def close_play(self):
        # Reshow root (ie: choose rounds) and end
        # current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


class DisplayGuide:
    """
    Displays guide for God Game
    """

    def __init__(self, partner):

        # setup dialogue box and background color
        background = "#ffe6cc"
        self.guide_box = Toplevel()

        # Disable all the buttons in the play GUI
        partner.guide_button.config(state=DISABLED)
        partner.history_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)

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

        guide_text = ("- Choose your answer by clicking one of the options provided.\n"
                      "- If you answer correctly, the button will turn green. If you get it wrong, the correct answer will be highlighted in green and your choice will turn red.\n"
                      "- Your progress will be shown at the top of the game (rounds played out of rounds chosen).\n"
                      "- You can review your game history at any time after the first round.\n"
                      "Good luck and have fun!")

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
        # Retrieve rounds played
        rounds_played = partner.rounds_played.get()

        # Put all the buttons back to normal
        partner.guide_button.config(state=NORMAL)
        if rounds_played != 0:
            partner.history_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)

        partner.guide_state = 'closed'
        self.guide_box.destroy()


class History:
    def __init__(self, partner):
        self.history_box = Toplevel()

        # Disable all the buttons in the play GUI
        partner.guide_button.config(state=DISABLED)
        partner.history_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)


        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=350)
        self.history_frame.grid()

        rounds_played = partner.rounds_played.get()
        rounds_won = partner.rounds_won.get()

        header_texts = [
            ['History', "Arial 18 bold", ''],
            [f'You got {rounds_won} / {rounds_played} questions correct', "Arial 14", 'w'],
            ['-' * 70, "Arial 14", '']
        ]

        self.history_headers_ref = []
        for count, (text, font, sticky) in enumerate(header_texts):
            self.history_heading = Label(self.history_frame, text=text, font=font,
                  anchor="w", justify="left", fg='#000',
                  padx=30, pady=5)
            self.history_heading.grid(row=count, sticky=sticky, padx=10)

            self.history_headers_ref.append(self.history_heading)


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

        self.history_label_ref = []

        for count, (result, question, user_answer) in enumerate(partner.history_data):
            if result == 'win':
                icon = '✅'
                color = '#049447'
            else:
                icon = '❌'
                color = '#c90803'

            text = f'{question} - {user_answer} {icon}'

            self.history_label = Label(self.past_question_frame, text=text, font="Arial 14",
                  justify="left", fg=color, wraplength=425,
                  padx=30, pady=5)
            self.history_label.grid(row=count, sticky='w', padx=10)
            self.history_label_ref.append(self.history_label)


        self.dismiss_button = Button(self.history_frame,
                                     font="Arial 16 bold",
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_history, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    def update_history(self, partner):
        """
        Updates history when a new round is played
        """
        # Update the top history headings
        top_label = self.history_headers_ref[1]
        top_label_text = f'You got {partner.rounds_won.get()} / {partner.rounds_played.get()} questions correct'
        top_label.config(text=top_label_text)

        result, question, user_answer = partner.history_data[-1]
        if result == 'win':
            icon = '✅'
            color = '#049447'
        else:
            icon = '❌'
            color = '#c90803'

        text = f'{question} - {user_answer} {icon}'

        self.history_label = Label(self.past_question_frame, text=text, font="Arial 14",
                                   justify="left", fg=color, wraplength=425,
                                   padx=30, pady=5)
        self.history_label.grid(row=len(partner.history_data), sticky='w', padx=10)

        # Scroll to the bottom automatically
        self.history_canvas.update_idletasks()
        self.history_canvas.yview_moveto(1)

    def close_history(self, partner):
        # Retrieve rounds played
        rounds_played = partner.rounds_played.get()

        # Put all the buttons back to normal
        partner.guide_button.config(state=NORMAL)
        if rounds_played != 0:
            partner.history_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)

        partner.history_state = 'closed'
        self.history_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("God Game")
    StartGame()
    root.mainloop()
