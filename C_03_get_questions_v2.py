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
    # Question
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

# Convert the question to a string
question = str(random.choice(questions))

# Customize the question as per the random god
if question == str(questions[2]):
    # Replace the '-' with the gods ability
    question_replaced = question.replace("-", random_god[4])
else:
    # Replace the first '-' with the name
    question_replaced = question.replace("-", random_god[3], 1)
    # Replace the second '-' with god / goddess
    question_replaced = question_replaced.replace("-", random_god[0])
question_replaced = question_replaced.replace("  ", " ")
print(question_replaced)

# Generate the answer
if question == str(questions[0]):
    answer = random_god[4]

elif question == str(questions[1]):
    answer = random_god[2]

elif question == str(questions[2]):
    answer = random_god[3]

elif question == str(questions[3]):
    answer = random_god[0]

else:
    answer = random_god[1]

print(answer)




