"""
The Question class maps all the questions in the game. It stores the question text, the list of possible answers, and the correct answer. It also provides a method to display the question to the player. This class uses abstraction by defining a general structure for all questions, hiding the details of how questions are displayed or checked, and allowing the game to handle them consistently.
"""

class Question 
 
    def __init__(self, question_text, answers, correct_answer):
        '''
        Initializes a new instance of the Question class.
        '''
        self.__question_text = question_text          # The text of the question
        self.__answers = answers                      # List of possible answers
        self.__correct_answer = correct_answer       # The correct answer

# Add getters
# Add polymorph methods
# Add other methods

"""
The QuizGame class manages the flow of the trivia game. It stores the list of questions, tracks the player's score, and provides methods to display questions, check answers, shuffle the question order, and reset the game. This class uses encapsulation to protect its data and provides a consistent interface for managing all questions in the game.
"""
class QuizGame

    def __init__(self, player, question_bank):
        self.__player = player                          # Player object
        self.__question_bank = question_bank            # List of Question objects
        self.__score = 0                                # Current score of the player
        self.__current_question_index = 0              # Tracks which question is active


# Add getters
# Add methods
  

"""
The Player class stores information about the person playing the game, including their name and current score. It provides methods to get and update the player's name and score, allowing the game to track progress and display rankings on the leaderboard.
"""

class Player 

    def __init__(self, player_name):

        self.__player_name = player_name       # Name of the player
        self.__score = 0                       # Player's current score

# Add getters
# Add methods
