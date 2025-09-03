import csv
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
        self.__player_name = player_name
        self.__score = 0

    def get_name(self):
        return self.__player_name

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
        self.__question_text = question_text
        self.__answers = answers
        self.__correct_answer = correct_answer

    def get_question_text(self):
        return self.__question_text

    def get_answers(self):
        return self.__answers

    def get_correct_answer(self):
        return self.__correct_answer

    def display_question(self):
        """Displays the question and numbered answers to the player."""
        print(self.__question_text)
        for i, answer in enumerate(self.__answers):
            print(f"{i+1}. {answer}")



def load_questions_from_csv(filename):
    """Load questions from a CSV file and return them as a list of Question objects."""
    question_bank = []
    try:
        with open(filename, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question_text = row['question']
                answers = [row['opt1'], row['opt2'], row['opt3']]
                correct_answer = row['correct']
                question_bank.append(Question(question_text, answers, correct_answer))
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except KeyError as e:
        print(f"Error: Missing column in CSV file: {e}")
        return None
    return question_bank

"""
The QuizGame class manages the flow of the trivia game. It stores the list of questions, tracks the player's score, and provides methods to display questions, check answers, shuffle the question order, and reset the game. This class uses encapsulation to protect its data and provides a consistent interface for managing all questions in the game.
"""
class QuizGame(Game):
    def __init__(self, player, question_bank):
        super().__init__()
        self.__player = player
        self.__question_bank = question_bank
        self.__score = 0
        self.__current_question_index = 0
        self.__selected_questions = random.sample(self.__question_bank, 10)

    # Getter for player
    def get_player(self):
        return self.__player

    # Getter for the current score
    def get_score(self):
        return self.__score

    # Getter for selected questions (read-only)
    def get_selected_questions(self):
        return self.__selected_questions.copy()

    # Method to increment score
    def add_score(self, points=100):
        self.__score += points

    def reset_game(self):
        """Reset the game state for a new round."""
        self.__player.reset_score()
        self.__score = 0
        self.__current_question_index = 0
        self.__selected_questions = random.sample(self.__question_bank, 10)
    
    def start_game(self):
        """Starts the main quiz game loop, presenting questions and checking answers."""
        print(f"\n--- Welcome, {self.__player.get_name()}, to the Quiz! ---\n")
        self._is_running = True
        
        for i, question in enumerate(self.__selected_questions):
            if not self._is_running:
                break
            
            print(f"Question {i + 1} of 10:")
            question.display_question()
            
            user_input = self.get_valid_input()
            
            if self.check_answer(question, user_input):
                print("Correct! 🎉 You've earned 100 points.")
                self.__player.add_score()
            else:
                print(f"Incorrect. The correct answer was: {question.get_correct_answer()}. 😔")
            
            print(f"Your current score: {self.__player.get_score()} points.")
        
        self.stop_game()

    def get_valid_input(self):
        """Handles user input and validates it, providing error handling."""
        while True:
            answer = input("Enter the number of your answer (1, 2, or 3): ").strip()
            if answer.isdigit() and 1 <= int(answer) <= 3:
                return int(answer)
            print("Invalid input. Please enter a number from 1 to 3.")

    def check_answer(self, question, user_input_index):
        """Checks if the user's answer is correct based on the index they provided."""
        try:
            selected_answer_text = question.get_answers()[user_input_index - 1]
            return selected_answer_text.strip().lower() == question.get_correct_answer().strip().lower()
        except IndexError:
            return False

if __name__ == "__main__":
    # Main game loop for user interaction
    
    questions = load_questions_from_csv("questions-group-o-Sheet1.csv")
    if questions is None or len(questions) < 10:
        print("Exiting game due to an issue with the question bank.")
    else:
        # Create player
        player_name = input("Enter your name: ")
        player = Player(player_name)
        
        while True:
            # Create a new game instance to reset
            game = QuizGame(player, questions)
            
            game.start_game()
            
            play_again = input("\nDo you want to play again? (yes/no): ").lower().strip()
            if play_again != 'yes':
                print("Thanks for playing! Goodbye.")
                break
