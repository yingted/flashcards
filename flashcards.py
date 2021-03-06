#!/usr/bin/python
"""
==== How it works ==============================================================

Each line starting with a '*' symbol is treated as the start of a new question.
Each line starting with a '#' symbol is treated as a comment.
Otherwise, the line is treated as part of the answer to the previous question.

If the UNIQUE constant is truthy, no question will be repeated.
If the ENABLE_COLORS constant is truthy, terminal colors will be used.

==== Caveats ===================================================================

Questions cannot be multilined.
No line in an answer can start with '*' or '#'.

==== Style guide ===============================================================

- Keep your questions short. Try to test general knowledge, avoid specific
  examples or application problems.

- All questions should end in '?'
    BAD:  List 3 organs in the human body.
    GOOD: What are 3 organs in the human body?

- When the question could be ambiguous, use with-respect-to (w.r.t).
    BAD:  What is the role of blood?
    GOOD: What is the role of blood w.r.t the immune system?

- Keep all lines in answers within an 80 character limit.

- Use numbering (1., 2., ...) when the question poses a "steps" question, or a
  "list" question.
    e.g. What are 3 organs in the human body?
         1. Heart
         2. Brain
         3. Liver
    e.g. What are the 3 steps for typing on a keyboard?
         1. Press the key.
         2. Watch the character appear.
         3. Release the key.

- End all sentences with more than 2 words with a punctuation.
    BAD:  This is an answer
    GOOD: This is an answer.
"""
import random
import sys

# Options
UNIQUE = True
ENABLE_COLORS = True

class bcolors:
    HEADER = '\033[95m' # Only this really works.
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def gen_cards(data):
    flashcards = []
    question = ""
    answer = ""
    for line in data:
        # Comment
        if line[0].startswith("#"):
            continue

        # Question
        if line[0].startswith("*"):
            if question:
                flashcards.append((question, answer))
                question = ""
                answer = ""
            question = line[1:].strip()
        else:
            answer = answer + line

    if question:
        flashcards.append((question, answer))

    return flashcards

def add_color(text, color):
    if not ENABLE_COLORS:
        return text

    return color + text + bcolors.ENDC

def main():
    if len(sys.argv) < 2:
        print "Usage:", sys.argv[0], "flashcards_file.txt"
        return

    file_name = sys.argv[1]
    with open(file_name, "r") as data:
        cards = gen_cards(data)

    left = [x for x in xrange(0, len(cards))]
    random.shuffle(left);
    while left:
        if UNIQUE:
            choice = left.pop()
        else:
            choice = random.randrange(0, len(cards))

        if UNIQUE:
            questions_left = \
                "(" + str(len(cards) - len(left)) + "/" + str(len(cards)) + ")"
        else:
            questions_left = ""
        print add_color("---------- " + questions_left, bcolors.FAIL)
        print cards[choice][0].strip()
        raw_input() # Wait for user to press enter.
        print add_color(cards[choice][1].strip(), bcolors.HEADER)

if __name__ == '__main__':
    try:
        main();
    except KeyboardInterrupt:
        pass
