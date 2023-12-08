from tkinter import Tk, Toplevel, Label, PhotoImage, Button, Entry, scrolledtext, StringVar, messagebox
from tkinter.messagebox import showinfo
from tkinter.ttk import Progressbar
from tkinter.simpledialog import askinteger
from itertools import cycle
import webbrowser
import pandas as pd
import os


class SplashScreen:
    def __init__(self, root, app):
        # Initialize the SplashScreen instance
        self.splash_root = Toplevel(root)
        self.splash_root.title("Splash Screen - Built by Joshua Russell to improve the learning of our minds!")
        self.splash_root.geometry("1366x768")

        # Load splash screen image using the current background path from QuizApp
        self.splash_image = PhotoImage(file=app.current_background_path)  # Load splash screen image

        # Create a label to display the splash screen image
        self.splash_label = Label(self.splash_root, image=self.splash_image)
        self.splash_label.place(relwidth=1, relheight=1)

        # Raise the splash screen to the front
        self.splash_root.attributes("-topmost", True)
        self.splash_root.update_idletasks()

        # Update the splash screen
        self.splash_root.update_idletasks()


def main():
    # Create the main application window
    root = Tk()
    quiz_app = QuizApp(root, 'C:\\Quizzy\\Answers\\Answers.csv')

    # Create a splash screen window with the QuizApp instance
    splash = SplashScreen(root, quiz_app)

    # Update the splash screen (optional: sleep for a few seconds)
    root.after(4000, splash.splash_root.destroy)  # Close splash screen after 4000 milliseconds (4 seconds)

    # Wait for the splash screen to be destroyed before continuing with the main program
    splash.splash_root.wait_window(splash.splash_root)

    # Bring the main window to the front after the splash screen
    root.attributes("-topmost", True)
    root.attributes("-topmost", False)
    root.update()

    root.mainloop()  # End of Splash Screen sequence


class QuizApp:
    def __init__(self, root, csv_file):
        """
                Initializes the QuizApp.

                :param root: The main Tkinter window.
                :param csv_file: Path to the CSV file containing quiz questions and answers.
                """
        # Initialize QuizApp instance
        self.adjusted_total_questions = None
        self.root = root
        self.root.state("normal")  # Maximize the window
        self.root.title("Quizzy - Smart People use Quizzy")
        self.root.geometry("1366x768")  # Adjusted window size
        self.root.resizable(False, False)  # Disable both horizontal and vertical resizing

        # Load background image
        self.background_image = PhotoImage(file=r'C:\Quizzy\Background\background5.png')
        self.background_label = Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Create a "Change Background" button
        self.change_background_button = Button(root, text="Change Background", command=self.change_background)
        self.change_background_button.place(relx=0.45, rely=0.00)

        # Create a variable to store the current background image path
        self.current_background_path = 'C:\\Quizzy\\Background\\background.png'

        # Create a cycle iterator for backgrounds in the folder
        self.background_cycle = cycle(self.get_backgrounds())

        # Set the initial background
        self.change_background()

        # Create a "Set Number of Questions" button
        self.set_questions_button = Button(root, text="Set Number of Questions", command=self.set_number_of_questions)
        self.set_questions_button.place(relx=0.02, rely=0.29)

        # Create Start Quiz button
        self.start_button = Button(root, text="Start Quiz", command=self.start_quiz)
        self.start_button.place(relx=0.8, rely=0.1)

        # Create Stop Quiz button (initially disabled)
        self.stop_button = Button(root, text="Stop Quiz", command=self.stop_quiz, state="disabled")
        self.stop_button.place(relx=0.854, rely=0.1)

        # Create a "Simulations" button
        self.simulations_button = Button(root, text="Simulations", command=self.open_simulation_pdf, font=('Arial', 10))
        self.simulations_button.place(relx=0.02, rely=0.19)

        # Create a "Help" button
        self.simulations_button = Button(root, text="Help", command=self.open_help_pdf, font=('Arial', 12))
        self.simulations_button.place(relx=0.00, rely=0.00)

        # Create an "Edit Answers" button
        self.edit_answers_button = Button(root, text="Edit Answers", command=self.edit_answers, font=('Arial', 12))
        self.edit_answers_button.place(relx=0.03, rely=0.00)

        # Create a Label for the answer entry
        self.answer_label = Label(root, text="Your Answer:", font=('Arial', 12))
        self.answer_label.place(relx=0.37, rely=0.86)

        # Create dynamic number of Entry widgets for user input
        self.user_answer_entries = []
        self.max_answers = 0

        # Create a "Skip Question" button
        self.skip_button = Button(root, text="Skip Question", command=self.skip_question)
        self.skip_button.place(relx=0.225, rely=0.75)

        # Create a button to check the user's answer
        self.check_button = Button(root, text="Check Answer", command=self.check_user_answer, font=('Arial', 12))
        self.check_button.place(relx=0.362, rely=0.79)

        # Review Missed Questions Button
        self.review_missed_button = Button(root, text="Review Missed Questions", command=self.review_missed_questions)
        self.review_missed_button.place(relx=0.79, rely=0.75)

        # Create a Text widget for displaying questions
        self.question_text = scrolledtext.ScrolledText(root, width=70, height=15, wrap="word", font=('Arial', 16))
        self.question_text.place(relx=0.56, rely=0.45, anchor="center")

        # Create a Label for displaying the result
        self.result_label = Label(root, text="", font=('Arial', 16))
        self.result_label.place(relx=0.5, rely=0.75, anchor="center")

        # Create a Start on Question Number label and entry
        self.start_on_label = Label(root, text="Start on Question Number:", font=('Arial', 12))
        self.start_on_label.place(relx=0.02, rely=0.1)
        self.start_on_entry = Entry(root, font=('Arial', 14), textvariable=StringVar())
        self.start_on_entry.place(relx=0.02, rely=0.14)

        # Create a percent complete bar
        self.progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.place(relx=0.75, rely=0.02, anchor="center")

        # Create a label for displaying the number of correct answers
        self.correct_answers_display = Label(root, text="", font=('Arial', 12))
        self.correct_answers_display.place(relx=0.92, rely=0.03, anchor="center")

        self.randomize_button = Button(root, text="Randomize Questions", command=self.randomize_questions)
        self.randomize_button.place(relx=0.02, rely=0.24)

        # Read the CSV file into a pandas DataFrame with explicit encoding
        self.df = pd.read_csv(csv_file, encoding='latin1')

        # Initialize quiz variables
        self.current_question_index = 0
        self.correct_answers = 0
        self.missed_questions_indices = []  # List to store indices of missed questions
        self.num_of_questions = len(self.df)  # Total number of questions

        # Create a Label for displaying the total number of questions
        self.total_questions_label = Label(root, text="Total Questions: {}".format(self.num_of_questions),
                                           font=('Arial', 12))
        self.total_questions_label.place(relx=0.02, rely=0.06)

        # Create an "Exit" button
        self.exit_button = Button(root, text="Exit", command=self.exit_app, font=('Arial', 12))
        self.exit_button.place(relx=0.15, rely=0.00)

    @staticmethod  # Was suggested by PyCharm to make Static method.
    def get_backgrounds():
        """
                Retrieves a list of background image paths from the "C:\\Quizzy\\Background" folder.

                :return: List of background image paths.
                """
        # Get a list of background image paths from the "C:\Quizzy\Background" folder
        folder_path = 'C:\\Quizzy\\Background'
        return [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                filename.endswith('.png')]

    def change_background(self):
        """
                Changes the background to the next image in the cycle.
                """
        # Change the background to the next image in the cycle
        self.current_background_path = next(self.background_cycle)
        self.background_image = PhotoImage(file=self.current_background_path)
        self.background_label.config(image=self.background_image)

    def start_quiz(self):
        """
                Initiates the quiz by prompting the user for the starting question number and setting up the
                quiz parameters.
                """
        # Prompt the user for the starting question number
        try:
            start_question = int(self.start_on_entry.get()) - 1  # Subtract 1 because row indices are zero-based
            # Check if the starting question number is within the valid range
            if not (0 <= start_question < self.num_of_questions):
                showinfo("Error", "Please enter a valid starting question number.")
                return

        except ValueError:
            showinfo("Error", "Please enter a valid starting question number.")
            return

        # Set the starting question number
        self.current_question_index = start_question

        # Calculate the adjusted total questions
        self.adjusted_total_questions = self.num_of_questions - start_question

        # Reset the number of correct answers
        self.correct_answers = 0

        # Enable the Stop Quiz button and disable the Start Quiz button
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # Update the total number of questions label
        self.total_questions_label.config(text=f"Total Questions: {self.adjusted_total_questions}")

        # Use after() to delay the quiz start
        self.root.after(100, self.delayed_display_question)

    def delayed_display_question(self):
        """
                Delays the display of the quiz question after initiating the quiz.
                """
        # Start displaying quiz questions
        self.display_question()

    def set_number_of_questions(self):
        """
                Prompts the user to set the number of questions for the quiz.
                """
        # Prompt the user to set the number of questions
        num_of_questions = askinteger("Set Number of Questions", "Enter the number of questions:", minvalue=1,
                                      maxvalue=self.num_of_questions)
        if num_of_questions is not None:
            # Update the total number of questions label
            self.total_questions_label.config(text=f"Total Questions: {num_of_questions}")

            # Set the adjusted total questions
            self.adjusted_total_questions = num_of_questions

            # Reset the number of correct answers
            self.correct_answers = 0

            # Enable the Stop Quiz button and disable the Start Quiz button
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")

            # Use after() to delay the quiz start
            self.root.after(100, self.delayed_display_question)

    def stop_quiz(self):
        """
                Stops the quiz, disables user interaction, and displays the final score.
                """
        # Disable the Check Answer button and user answer entries
        self.check_button.config(state="disabled")
        for entry in self.user_answer_entries:
            entry.config(state="disabled")

        # Display the final score based on the number of questions chosen
        result_text = f"Quiz completed! Your score: {self.correct_answers} / {self.adjusted_total_questions}"
        self.question_text.insert("end", result_text)
        self.question_text.config(state="disabled")  # Disable further interaction

        # Set the progress bar to 100 when the quiz is completed
        self.progress_bar["value"] = 100

        # Enable the Start Quiz button and disable the Stop Quiz button
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def create_user_answer_entries(self):
        """
               Creates and places Entry widgets for user answers dynamically.
               """
        # Destroy previous Entry widgets
        for entry in self.user_answer_entries:
            entry.destroy()

        # Create new Entry widgets based on the number of answers
        self.user_answer_entries = [Entry(self.root, font=('Arial', 14), textvariable=StringVar())
                                    for _ in range(self.max_answers)]

        # Place Entry widgets on the screen
        for i, entry in enumerate(self.user_answer_entries):
            entry.place(relx=0.45, rely=0.8 + (i * 0.05))

    def display_question(self):
        """
                Displays the current quiz question and answer choices to the user.
                """
        if self.current_question_index < self.num_of_questions:
            # Get the current question
            row = self.df.iloc[self.current_question_index]
            question_number = row.name + 1  # Add 1 to convert from zero-based to one-based indexing
            question = row['Question']
            answer_choices = row['Answer Choices'].split(', ')

            # Display the quiz question and answer choices in the Text widget
            self.question_text.config(state="normal")  # Enable editing
            self.question_text.delete(1.0, "end")  # Clear previous text
            self.question_text.insert("end", f"Question {question_number}: {question}\n\n")

            # Display answer choices without numbers
            for choice in answer_choices:
                self.question_text.insert("end", f"{choice}\n")

            # Update the number of answer boxes dynamically
            self.max_answers = len(row['Correct Answer'].split(', '))
            self.create_user_answer_entries()

            # Enable the Check Answer button and user answer entries
            self.check_button.config(state="normal")
            for entry in self.user_answer_entries:
                entry.config(state="normal")

            # Raise the result label to the front
            self.result_label.lift()
        else:
            # If the specified number of questions is reached, stop the quiz
            self.stop_quiz()

    def check_user_answer(self):
        """
                Checks the user's answers against the correct answers and updates the quiz accordingly.
                """
        # Get the user's answers
        user_answers = [entry.get().strip().lower()[0] if entry.get().strip() else '' for entry in
                        self.user_answer_entries]

        # Check if any of the user's answers are empty
        if any(not answer for answer in user_answers):
            showinfo("Error", "Please enter all answers.")
            return

        # Check if the 'Correct Answer' column exists in the row
        if 'Correct Answer' in self.df.columns and \
                isinstance(self.df['Correct Answer'].iloc[self.current_question_index], str):

            # Check if the current question index is within the adjusted total
            if self.current_question_index < self.num_of_questions:
                # Check if the user's answers are correct
                correct_answers = [ans.lower()[0] for ans in
                                   self.df['Correct Answer'].iloc[self.current_question_index].split(', ')]
                result_text = "Your Answers: {}\n".format(", ".join(user_answers))

                if set(user_answers) == set(correct_answers):
                    self.correct_answers += 1
                    result_text += "Correct!"

                    # Move to the next question after a two seconds delay
                    self.root.after(2000, self.reset_question)

                else:
                    result_text += f"Wrong! The correct answers are {', '.join(correct_answers)}"
                    # Add the index of the missed question to the list
                    self.missed_questions_indices.append(self.current_question_index)

                    # Move to the next question after a short delay
                    self.root.after(7000, self.reset_question)

                # Update the result label text
                self.result_label.config(text=result_text)

                # Update the progress bar
                percent_complete = (self.current_question_index / self.num_of_questions) * 100
                self.progress_bar["value"] = percent_complete

                # Update the correct answers display
                self.correct_answers_display.config(
                    text=f"Correct Ans: {self.correct_answers} / {self.adjusted_total_questions}")

            else:
                showinfo("Info", "Quiz session completed!")

        else:
            showinfo("Error", "The 'Correct Answer' column is missing or not a string.")

    def reset_question(self):
        """
                Resets the question state, clears user's answers, and moves to the next question.
                """
        # Clear the user's answer entries
        for entry in self.user_answer_entries:
            entry.delete(0, "end")

        # Clear the result label
        self.result_label.config(text="")

        # Move to the next question if there are more questions
        if self.current_question_index < self.num_of_questions:
            self.current_question_index += 1
            self.display_question()
        else:
            # If the specified number of questions is reached, stop the quiz
            self.stop_quiz()

    def skip_question(self):
        """
               Skips the current question and moves to the next question.
               """
        # Move to the next question without checking the answer
        self.reset_question()

    @staticmethod  # Was suggested by PyCharm to make Static method.
    def open_simulation_pdf():
        """
                Opens the simulation PDF file using the default program.
                """
        # Open the simulations.pdf file with the default program Prefer Microsoft Edge
        file_path = r'C:\Quizzy\Simulation\simulations.pdf'
        try:
            import subprocess
            subprocess.Popen(['start', file_path], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    @staticmethod  # Was suggested by PyCharm to make Static method.
    def open_help_pdf():
        """
                Opens the help PDF file using the default program.
                """
        # Open the Help.pdf file with the default program Prefer Microsoft Edge
        file_path = r'C:\Quizzy\Help\help.pdf'
        try:
            import subprocess
            subprocess.Popen(['start', file_path], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    @staticmethod  # Was suggested by PyCharm to make Static method.
    def edit_answers():
        """
                Opens the Answers.csv file with the default program for editing.
                """
        # Open the Answers.csv file with the default program
        file_path = 'C:\\Quizzy\\Answers\\Answers.csv'
        try:
            webbrowser.open(file_path)
        except Exception as e:
            showinfo("Error", f"Failed to open file: {e}")

    def randomize_questions(self):
        """
                Randomizes the order of quiz questions.
                """
        # Randomize the order of questions
        self.df = self.df.sample(frac=1).reset_index(drop=True)
        self.current_question_index = 0
        self.start_quiz()

    def review_missed_questions(self):
        """
                Initiates the review of questions that were answered incorrectly during the quiz.
                """
        # Display only the questions that were answered incorrectly
        if self.missed_questions_indices:
            self.current_question_index = 0  # Reset the index to review missed questions from the beginning
            self.review_missed_questions_list()
        else:
            messagebox.showinfo("Review Missed Questions", "No questions were answered incorrectly.")

    def review_missed_questions_list(self):
        """
                Displays missed questions with correct answers during the review process.
                """
        # Display missed questions with correct answers
        if self.current_question_index < len(self.missed_questions_indices):
            missed_index = self.missed_questions_indices[self.current_question_index]
            self.current_question_index += 1
            self.display_question_with_answer(missed_index)
            self.root.after(7000, self.review_missed_questions_list)
        else:
            # Show a message when all missed questions have been reviewed
            messagebox.showinfo("Review Missed Questions", "All missed questions reviewed.")

    def display_question_with_answer(self, missed_index):
        """
                Displays a missed question along with the correct answer during the review process.

                :param missed_index: Index of the missed question.
                """
        if 0 <= missed_index < len(self.df):
            # Get the missed question and correct answer
            row = self.df.iloc[missed_index]
            question_number = row.name + 1
            question = row['Question']
            answer_choices = row['Answer Choices'].split(', ')
            correct_answers = row['Correct Answer']

            # Display the question in the Text widget
            self.question_text.config(state="normal")
            self.question_text.delete(1.0, "end")
            self.question_text.insert("end", f"Question {question_number}: {question}\n\n")

            # Display the answer choices
            for i, choice in enumerate(answer_choices, start=1):
                self.question_text.insert("end", f"{i}. {choice}\n")

            # Display the correct answer
            self.question_text.insert("end", f"Correct Answer: {correct_answers}\n")

            # Update the result label text
            self.result_label.config(text="")

            # Update the progress bar
            percent_complete = (missed_index / self.num_of_questions) * 100
            self.progress_bar["value"] = percent_complete

        else:
            # If the specified number of questions is reached, stop the quiz
            self.stop_quiz()

    def exit_app(self):
        """
                Exits the QuizApp by destroying the main window.
                """
        # Stop the app and exit the program
        self.root.destroy()  # Close the main window


if __name__ == "__main__":
    main()
