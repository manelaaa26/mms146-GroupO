import random
from abc import ABC, abstractmethod

class Game(ABC):
 def __init__(self):
  self._is_running = False
  
  @abstractmethod
  def start_game(self):
   pass

  @abstractmethod
  def reset_game(self):
   pass

  def stop_game(self):
   self._is_running = False
   print("Game has ended. Thank you for playing!")
  

"""
The Player class stores information about the person playing the game, including their name and current score. It provides methods to get and update the player's name and score, allowing the game to track progress and display rankings on the leaderboard.
"""

class Player:                      

    def __init__(self, player_name):   
        self.__player_name = player_name   # Name of the player
        self.__score = 0

    def get_name(self):              
        return self.__player_name    # Player's current score

    def set_name(self, new_name):    
        self.__player_name = new_name  
     
     def get_score(self):
        return self.__score

    def add_score(self, points=100):
        """Increase player's score by given points (default 100)."""
        self.__score += points

    def reset_score(self):
        """Reset player's score to zero (for new games)."""
        self.__score = 0
  

"""
The Question class maps all the questions in the game. It stores the question text, the list of possible answers, and the correct answer. It also provides a method to display the question to the player. This class uses abstraction by defining a general structure for all questions, hiding the details of how questions are displayed or checked, and allowing the game to handle them consistently.
"""

class Question: 
    def __init__(self, question_text, answers, correct_answer):
        """
        Initializes a new instance of the Question class.
        """
        self.__question_text = question_text      # The text of the question
        self.__answers = answers                  # List of possible answers
        self.__correct_answer = correct_answer    # The correct answer

    def get_question_text(self):
        return self.__question_text

    def get_answers(self):
        return self.__answers

    def get_correct_answer(self):
        return self.__correct_answer

# Add getters
# Add polymorph methods
# Add other methods

"""
The QuizGame class manages the flow of the trivia game. It stores the list of questions, tracks the player's score, and provides methods to display questions, check answers, shuffle the question order, and reset the game. This class uses encapsulation to protect its data and provides a consistent interface for managing all questions in the game.
"""
class QuizGame:
    def __init__(self, player, question_bank):
        self.__player = player                          # Player object
        self.__question_bank = question_bank            # List of Question objects
        self.__score = 0                                # Current score of the player
        self.__current_question_index = 0               # Tracks which question is active



# Add getters
# Add methods
