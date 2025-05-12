import csv
import random

# Retrieve data from the csv file
file = open("gods.csv", 'r')

# Make the data into a list
all_gods = list(csv.reader(file))

# Remove the row with the headings
all_gods.pop(0)

# List for questions and answers
questions = [
    # Question | Answer | options
    ["What is - the - of?", 4, 4],
    ["Is - a major or minor -?", 2, ["Major", "Minor"]],
    ["Who is the - deity of -?", 3, 4],
    ["Is - a god or goddess?", 0, ["God", "Goddess"]],
    ["Is - Greek or Roman?", 1, ["Greek", "Roman"]]
]

# Create a new question list for apollo and nemesis
# not including the last question
apo_nem_questions = questions.copy()
del apo_nem_questions[4]

num_rounds = 0

# Create variables for question and answer
question = ""
answer_id = ""
num_option = ""

# Holds the last question, so we don't get 2 in a row
last_question = ""

past_questions = []

# Main loop
while True:
    # Get a random god for the question
    random_god = random.choice(all_gods)

    while question == last_question:
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

    print(question_replaced)

    # List to store the options
    option_list = []

    # Get the answer from the random god
    answer = random_god[answer_id]
    print(answer)

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

    # Print the options
    print(option_list)

    num_rounds += 1

    keep_going = input("Do you want to continue? ")
    print()
    if keep_going == 'n':
        break
