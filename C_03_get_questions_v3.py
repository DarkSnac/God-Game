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
    # Question | Answer
    ["What is - the - of?", 4],
    ["Is - a major or minor -?", 2],
    ["Who is the deity of -?", 3],
    ["Is - a god or goddess?", 0],
    ["Is - Greek or Roman?", 1]
]

# Main loop
# while True:
# Get a random god for the question
random_god = random.choice(all_gods)
print(random_god)

# Split all the different data for the question
question, answer_id = random.choice(questions)

# Customize the question as per the random god
if question == str(questions[2]):
    # Replace the '-' with the gods ability
    question_replaced = question.replace("-", random_god[4])
else:
    # Replace the first '-' with the name
    question_replaced = question.replace("-", random_god[3], 1)
    # Replace the second '-' with god / goddess
    question_replaced = question_replaced.replace("-", random_god[0])

# Remove the double space if there is one
question_replaced = question_replaced.replace("  ", " ")
print(question_replaced)

# Get the answer from the random god
answer = random_god[answer_id]
print(answer)




