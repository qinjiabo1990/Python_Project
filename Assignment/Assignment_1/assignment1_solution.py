"""
CSSE1001 Assignment 1
Semester 1, 2017
Sample Solution

Implements a simple matchmaking system based on a few physical characteristics
and on a very simplified personality test.

__author__ = "Benjamin Martin"
__copyright__ = "Copyright 2017, University of Queensland"
31/03/2017
"""

import partners

# Answer sets
GENDER_ANSWERS = ('male', 'female', 'other')
HEIGHT_ANSWERS = ('tall', 'medium', 'short')
PERSONALITY_ANSWERS = ('Yes', 'Most of the time', 'Neutral', 'Some times', 'No')

# Question sets
PHYSICAL_QUESTIONS = (
    ('What is your gender?', GENDER_ANSWERS),
    ('What is your sexual preference?', GENDER_ANSWERS),
    ('What is your height?', HEIGHT_ANSWERS),
    ('What is height do you prefer your partner to be?', HEIGHT_ANSWERS)
)

PERSONALITY_QUESTIONS = (
    ('Do you find it easy to introduce yourself to other people?',
     PERSONALITY_ANSWERS),
    ('Do you usually initiate conversations?', PERSONALITY_ANSWERS),
    ('Do you often do something out of sheer curiosity?', PERSONALITY_ANSWERS),
    ('Do you prefer being out with a large group of friends rather than '
     'spending time on your own?', PERSONALITY_ANSWERS)
)

# Indices used in match function
NAME_I = 0
GENDER_I = 1
GENDER_PREFERENCE_I = 2
HEIGHT_CMP_I = 3
PERSONALITY_SCORE_I = 4

HEIGHT_CMP_VALUES = {
    True: {
        True: 3,
        False: 2
    },
    False: {
        True: 1,
        False: 0
    }
}


def ask_question(question, answers, return_text) :
    """Asks the user a question, prompting them to choose from a predefined list
       of answers. Repeatedly asks question until valid answer is chosen.

    Parameters:
        question (str): The question to ask the user.
        answers (list(str)): A list of potential answers.
        return_text (bool): If True, the return value will be the answer text,
                            else, the answer's number.

    Returns:
        The answer the user has chosen (according to return_text).
    """

    while True :
        print(question)
        for i, answer in enumerate(answers) :
            print("  {}) {}".format(i + 1, answer))

        response = input('Please enter your answer: ')

        if response.isdigit() :
            response = int(response)

            if 1 <= response <= len(answers) :
                print()
                if return_text :
                    return answers[response - 1]
                else :
                    return response

        print("\nThe selected option is invalid. Let's try again.\n")


def compare_height_and_preference(height_a, preference_a,
                                  height_b, preference_b) :
    """Compares height & height preference of person A & B.

    Parameters:
         height_a (str): Person A's height.
         preference_a (str): Person A's height preference.
         height_b (str): Person B's height.
         preference_b (str): Person B's height preference.

    Returns:
        Numerical value indicating strength of comparison.
        ----------------------------------------------
        |                 | height_b == preference_a |
        |                 |    True    |    False    |
        ----------------------------------------------
        | h._a == pref._b |      3     |       1     |
        | h._a != pref._b |      2     |       0     |
        ----------------------------------------------
    """

    return HEIGHT_CMP_VALUES[height_b == preference_a][height_a == preference_b]


def get_current_candidate(potential_partners, height, height_preference,
                          personality_score) :
    """Returns a tuple with information for the candidate currently being
       considered.
       
        Values in list correspond to *_I constants defined by this file.
    """

    height_comparison = compare_height_and_preference(
                            height,
                            height_preference,
                            potential_partners.get_height(),
                            potential_partners.get_height_pref()
                        )

    return (potential_partners.get_name(),
            potential_partners.get_gender(),
            potential_partners.get_sexual_pref(),
            height_comparison,
            abs(personality_score - potential_partners.get_personality_score())
           )


def match(gender, sexual_preference, height, height_preference,
          personality_score) :
    """Finds the best match from the database for the given user.

    Parameters:
        gender (str): The user's gender. One of male, female, or other.
        sexual_preference (str): The user's sexual preference. As with gender.
        height (str): The user's height. One of tall, medium, or short.
        height_preference (str): The user's height preference. As with height.
        personality_score (int): The user's personality score.

    Preconditions:
        10 <= personality_score <= 40

    Returns:
        str: Name of the best match if one exists, otherwise None.
    """

    print(gender, sexual_preference, height, height_preference)

    best_match = None
    potential_partners = partners.Partners()

    while potential_partners.available() :
        candidate = get_current_candidate(potential_partners, height,
                                          height_preference, personality_score)
        if (candidate[GENDER_PREFERENCE_I] == gender 
            and candidate[GENDER_I] == sexual_preference) :

            if (best_match is None
                or (candidate[PERSONALITY_SCORE_I]
                    < best_match[PERSONALITY_SCORE_I])) :
                # candidate has closer score than previous best match
                best_match = candidate
            elif (candidate[PERSONALITY_SCORE_I]
                  == best_match[PERSONALITY_SCORE_I]) :
                # candidate and previous best match have equidistant score
                # compare heights
                if candidate[HEIGHT_CMP_I] > best_match[HEIGHT_CMP_I] :
                    best_match = candidate

    if best_match is None :
        return None
    else :
        return best_match[NAME_I]  # best match's name


def main() :
    """Top-level interation with user."""

    # Intro & name
    print("Welcome to PyMatch\n")
    name = None
    while not name :
        name = input("Please enter your name: ")
        if not name :
            print("\nYou must enter a name to continue. Let's try again.\n")
        else :
            print()

    # Ask questions
    physical_responses = []
    for question, answers in PHYSICAL_QUESTIONS :
        physical_responses.append(ask_question(question, answers, True))

    gender, sexual_preference, height, height_preference = physical_responses

    print("We will now ask you some questions to try and determine your "
          "personality type.\n")

    personality_score = 0
    for question, answers in PERSONALITY_QUESTIONS:
        personality_score += ask_question(question, answers, False)

    personality_score *= 2

    # Matching
    best_match = match(gender, sexual_preference, height, height_preference,
                       personality_score)

    print("Thank you for answering all the questions. We have found your best "
          "match from our database and hope that you enjoy getting to know "
          "each other. Your best match is:")
    print(best_match)


def match_test() :
    print(match('male', 'female', 'tall', 'short', 10))


if __name__ == "__main__" :
    main()
