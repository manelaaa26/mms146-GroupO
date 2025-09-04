import csv
import random
import os
import pickle
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
The Player class stores information about the person playing the game, including their name and current score. 
It provides methods to get and update the player's name and score, allowing the game to track progress and display rankings on the leaderboard.
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

    # --- Methods allowing a player to save his game and return to it ---
    def save_progress(self, game_state, filename="savegame.pkl"):
        """Save player and game state to a file."""
        with open(filename, "wb") as f:
            pickle.dump({"player": self, "game_state": game_state}, f)
        print(f"Game progress saved as {filename}!")

    @staticmethod
    def load_progress(filename="savegame.pkl"):
        """Load player and game state from a file."""
        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
            print(f"Game progress loaded from {filename}!")
            return data["player"], data["game_state"]
        except FileNotFoundError:
            print("No saved game found!")
            return None, None


"""
The Question class maps all the questions in the game. 
It stores the question text, the list of possible answers, and the correct answer. 
It also provides a method to display the question to the player. 
This class uses abstraction by defining a general structure for all questions, hiding the details of how questions are displayed or checked, and allowing the game to handle them consistently.
"""
class Question:
    def __init__(self, question_text, answers, correct_answer, difficulty):
        """
        Initializes a new instance of the Question class.
        """
        self.__question_text = question_text
        self.__correct_answer = correct_answer
        self.__difficulty = difficulty

        all_answers = answers + [correct_answer]
        random.shuffle(all_answers)
        self.__shuffled_answers = all_answers

    def get_question_text(self):
        return self.__question_text

    def get_answers(self):
        return self.__shuffled_answers

    def get_correct_answer(self):
        return self.__correct_answer

    def get_difficulty(self):
        return self.__difficulty

    def display_question(self):
        """Displays the question and numbered answers to the player."""
        print(self.__question_text)
        for i, answer in enumerate(self.__shuffled_answers):
            print(f"{i+1}. {answer}")
            

""" Difficulty """
class Difficulty(ABC):
    @abstractmethod
    def get_points(self):
        pass

class Easy(Difficulty):
    def get_points(self):
        return 100

class Medium(Difficulty):
    def get_points(self):
        return 200

class Difficult(Difficulty):
    def get_points(self):
        return 300


""" Load Questions """
def load_questions_from_csv(filename):
    """Load questions from a CSV file and return them as a list of Question objects."""
    question_bank = []
    try:
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(scriptdir, filename)
        
        with open(filepath, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question_text = row['question']
                answers = [row['opt1'], row['opt2'], row['opt3']]
                correct_answer = row['correct']
                difficulty = row['difficulty']
                question_bank.append(Question(question_text, answers, correct_answer, difficulty))
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except KeyError as e:
        print(f"Error: Missing column in CSV file: {e}")
        return None
    return question_bank


""" Leaderboard """
def save_score(player_name, score):
    """Save player name and score to the leaderboard.txt file."""
    try:
        with open("leaderboard.txt", "a", encoding="utf-8") as file:
            file.write(f"{player_name},{score}\n")
    except Exception as e:
        print(f"Error saving score: {e}")

def display_leaderboard():
    """Reads and displays the leaderboard from the leaderboard.txt file."""
    leaderboard = []
    try:
        with open("leaderboard.txt", "r", encoding="utf-8") as file:
            for line in file:
                name, score = line.strip().split(',')
                leaderboard.append({'name': name, 'score': int(score)})
        
        # Sort by score in descending order
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        
        print("\n--- Leaderboard ---")
        if not leaderboard:
            print("The leaderboard is currently empty.")
        else:
            for i, entry in enumerate(leaderboard):
                print(f"{i+1}. {entry['name']}: {entry['score']} points")
        print("-------------------")
    except FileNotFoundError:
        print("\nNo leaderboard found yet. Play a game to create one!")
    except Exception as e:
        print(f"Error loading leaderboard: {e}")


"""
The QuizGame class manages the flow of the trivia game. 
It stores the list of questions, tracks the player's score, and provides methods to display questions, check answers, shuffle the question order, and reset the game. 
This class uses encapsulation to protect its data and provides a consistent interface for managing all questions in the game.
"""
class QuizGame(Game):
    def __init__(self, player, question_bank, difficulty_level, current_index=0, score=0):
        super().__init__()
        self.__player = player
        self.__question_bank = [q for q in question_bank if q.get_difficulty().lower() == type(difficulty_level).__name__.lower()]
        self.__difficulty_level = difficulty_level
        self.__score = score
        self.__current_question_index = current_index
        self.__selected_questions = random.sample(self.__question_bank, min(10, len(self.__question_bank)))

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
    def add_score(self):
        points = self.__difficulty_level.get_points()  
        self.__score += points
        
    def reset_game(self):
        """Reset the game state for a new round."""
        self.__player.reset_score()
        self.__score = 0
        self.__current_question_index = 0
        self.__selected_questions = random.sample(self.__question_bank, min(10, len(self.__question_bank)))
    
    def start_game(self):
        """Starts the main quiz game loop, presenting questions and checking answers."""
        print(f"\n--- Welcome, {self.__player.get_name()}, to the Quiz! ---\n")
        self._is_running = True
        
        while self.__current_question_index < len(self.__selected_questions):
            if not self._is_running:
                break

            question = self.__selected_questions[self.__current_question_index]
            print(f"Question {self.__current_question_index + 1} of {len(self.__selected_questions)}:")
            question.display_question()
            
            user_input = self.get_valid_input()
            
            if self.check_answer(question, user_input):
                print(f"Correct! 🎉 You've earned {self.__difficulty_level.get_points()} points.")
                self.add_score()
            else:
                print(f"Incorrect. The correct answer was: {question.get_correct_answer()}. 😔")
            
            print(f"Your current score: {self.get_score()} points.")

            # Save progress after each question
            self.__player.save_progress({
                "score": self.__score,
                "current_index": self.__current_question_index + 1,
                "difficulty": type(self.__difficulty_level).__name__
            })

            self.__current_question_index += 1
        
        save_score(self.__player.get_name(), self.get_score())
        self.stop_game()

    def get_valid_input(self):
        """Handles user input and validates it, providing error handling."""
        while True:
            answer = input("Enter the number of your answer (1, 2, 3, or 4): ").strip()
            if answer.isdigit() and 1 <= int(answer) <= 4:
                return int(answer)
            print("Invalid input. Please enter a number from 1 to 4.")

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
        player_name = input("Enter your name: ")
        player = Player(player_name)
        
        while True:
            print("\nSelect an option:\n1. Play Game\n2. View Leaderboard\n3. Continue Game\n4. Exit")
            main_choice = input("Enter 1, 2, 3, or 4: ").strip()

            if main_choice == "1":
                # Select difficulty
                while True:
                    print("\nSelect difficulty:\n1. Easy\n2. Medium\n3. Difficult")
                    difficulty_choice = input("Enter 1, 2, or 3: ").strip()
                    if difficulty_choice == "1":
                        difficulty_level = Easy()
                        break
                    if difficulty_choice == "2":
                        difficulty_level = Medium()
                        break
                    if difficulty_choice == "3":
                        difficulty_level = Difficult()
                        break
                    print("Invalid choice. Please enter 1, 2, or 3.")
                
                game = QuizGame(player, questions, difficulty_level)
                game.start_game()

            elif main_choice == "2":
                display_leaderboard()

            elif main_choice == "3":
                # Continue saved game
                saved_player, game_state = Player.load_progress()
                if saved_player and game_state:
                    difficulty_map = {"Easy": Easy(), "Medium": Medium(), "Difficult": Difficult()}
                    difficulty_level = difficulty_map.get(game_state["difficulty"], Easy())
                    game = QuizGame(saved_player, questions, difficulty_level,
                                    current_index=game_state["current_index"],
                                    score=game_state["score"])
                    game.start_game()

            elif main_choice == "4":
                print("Thanks for playing! Goodbye.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
