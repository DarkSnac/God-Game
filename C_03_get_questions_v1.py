import csv
import random

# Retrieve data from the csv file
file = open("gods.csv", 'r')

# Make the data into a list
all_gods = list(csv.reader(file))

# Remove the row with the headings
all_gods.pop(0)

# List for questions
questions = [
    ["What is - the - of?"],
    ["Is - a major or minor -?"],
    ["Who is the deity of -?"],
    ["Is - a god or goddess?"],
    ["Is - Greek or Roman?"]
]

# Main loop
# while True:
# Get a random god for the question
random_god = random.choice(all_gods)
print(random_god)

# If the god/goddess is nemesis or apollo don't
# use the last question as its both greek and roman

question = str(random.choice(questions))
if question == questions[2]:
    question_replaced = question.replace("-", random_god[4])
else:
    question_replaced = question.replace("-", random_god[3], 1)
    question_replaced = question_replaced.replace("-", random_god[0])
print(question_replaced)




