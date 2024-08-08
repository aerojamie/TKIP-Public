import tkinter as tk
from tkinter import messagebox
import random

# List of cryptograms with placeholders for simplicity
cryptograms = [
    #this is where the cryptogram answer and solutions are stored. They are removed so you cant cheat :)
]

class CryptogramGame:
    def __init__(self, root):
        self.root = root
        self.root.title("The Key is Password")

        self.fullscreen = False  # Track fullscreen state
        self.current_cryptogram_index = 0
        self.current_cryptogram = None
        self.incorrect_attempts = 0  # Track number of incorrect attempts
        self.max_attempts = 3  # Number of attempts before game over

        self.create_opening_screen()

        # Bind the 'F11' key to toggle fullscreen
        self.root.bind('<F11>', self.toggle_fullscreen)
        # Bind the 'Escape' key to exit fullscreen
        self.root.bind('<Escape>', self.end_fullscreen)

    def create_opening_screen(self):
        self.root.configure(bg="#000000")

        self.title_label = tk.Label(
            self.root,
            text="The Key is Password",
            font=("Courier New", 36, "bold"),
            bg="#000000",
            fg="#00FF00"
        )
        self.title_label.pack(pady=50)

        self.unlock_button = tk.Button(
            self.root,
            text="Unlock",
            font=("Courier New", 18),
            command=self.show_rules_screen,
            bg="#004d00",
            fg="#00FF00",
            relief=tk.RAISED,
            borderwidth=3,
            padx=20,
            pady=10
        )
        self.unlock_button.pack(pady=30)

    def show_rules_screen(self):
        # Hide the opening screen
        self.title_label.pack_forget()
        self.unlock_button.pack_forget()

        # Create a frame for the rules screen
        self.rules_frame = tk.Frame(
            self.root,
            bg="#000000",
            padx=30,
            pady=30,
            borderwidth=3,
            relief=tk.SOLID
        )
        self.rules_frame.pack(fill=tk.BOTH, expand=True)

        rules_text = (
            "Welcome to 'The Key is Password'!\n\n"
            "Rules:\n"
            "1. You will be given a series of cryptograms to solve.\n"
            "2. Enter your solution in the text box provided and click 'Submit'.\n"
            "3. If your solution is correct, you'll proceed to the next cryptogram.\n"
            "4. If it's incorrect, you'll have to try again.\n"
            "6. 3 Lives then you're out, of course you could always try again.\n"
            "7. The ciphers are surrounded by equal signs (=).\n"
            "8. Passwords are case sensitive.\n"
            "9. Complete all cryptograms to win the game.\n\n"
            "Good luck!"
        )

        rules_label = tk.Label(
            self.rules_frame,
            text=rules_text,
            font=("Courier New", 18),
            bg="#000000",
            fg="#00FF00",
            justify=tk.LEFT
        )
        rules_label.pack(pady=30)

        start_button = tk.Button(
            self.rules_frame,
            text="Start",
            font=("Courier New", 18),
            command=self.start_game,
            bg="#004d00",
            fg="#00FF00",
            relief=tk.RAISED,
            borderwidth=3,
            padx=20,
            pady=10
        )
        start_button.pack(pady=20)

    def start_game(self):
        self.rules_frame.pack_forget()  # Hide the rules frame
        self.incorrect_attempts = 0  # Reset incorrect attempts
        self.create_game_screen()
        self.show_next_cryptogram()

    def create_game_screen(self):
        # Create a frame for the game screen
        self.game_frame = tk.Frame(
            self.root,
            bg="#000000",
            padx=30,
            pady=30
        )
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for the exit button
        self.exit_frame = tk.Frame(
            self.game_frame,
            bg="#000000",
            padx=10,
            pady=10
        )
        self.exit_frame.pack(side=tk.TOP, anchor=tk.NE)

        # Exit button
        self.exit_button = tk.Button(
            self.exit_frame,
            text="EXIT",
            font=("Courier New", 18),
            command=self.exit_game,
            bg="#8B0000",
            fg="#00FF00",
            relief=tk.RAISED,
            borderwidth=3,
            padx=20,
            pady=10
        )
        self.exit_button.pack()

        # Frame for the cryptogram
        self.cryptogram_frame = tk.Frame(
            self.game_frame,
            bg="#000000",
            padx=20,
            pady=20,
            borderwidth=3,
            relief=tk.SOLID
        )
        self.cryptogram_frame.pack(fill=tk.BOTH, pady=20, expand=True)

        # Cryptogram label with text wrapping
        self.cryptogram_label = tk.Label(
            self.cryptogram_frame,
            text="",
            font=("Courier New", 24),
            bg="#000000",
            fg="#00FF00",
            wraplength=800,
            justify=tk.LEFT
        )
        self.cryptogram_label.pack(pady=20, fill=tk.BOTH, expand=True)

        # Frame for user input and buttons
        self.input_buttons_frame = tk.Frame(
            self.game_frame,
            bg="#000000",
            padx=20,
            pady=20,
            borderwidth=3,
            relief=tk.SOLID
        )
        self.input_buttons_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # User input
        self.solution_entry = tk.Entry(
            self.input_buttons_frame,
            font=("Courier New", 18),
            bg="#1c1c1c",
            fg="#00FF00",
            insertbackground='white',
            borderwidth=3,
            relief=tk.RAISED
        )
        self.solution_entry.pack(side=tk.TOP, fill=tk.X, pady=(10, 10), padx=(10, 10))

        # Submit button directly below the user input
        self.submit_button = tk.Button(
            self.input_buttons_frame,
            text="Submit",
            font=("Courier New", 18),
            command=self.check_solution,
            bg="#006400",
            fg="#00FF00",
            relief=tk.RAISED,
            borderwidth=3,
            padx=20,
            pady=10
        )
        self.submit_button.pack(side=tk.TOP, pady=(10, 10))

        # Frame for lives
        self.lives_frame = tk.Frame(
            self.input_buttons_frame,
            bg="#000000",
            pady=10
        )
        self.lives_frame.pack(side=tk.BOTTOM, pady=(10, 0))

        self.lives_labels = []
        for _ in range(self.max_attempts):
            label = tk.Label(
                self.lives_frame,
                text="X",
                font=("Courier New", 18),
                bg="#000000",
                fg="#FF0000"
            )
            label.pack(side=tk.LEFT, padx=10)
            self.lives_labels.append(label)

    def show_next_cryptogram(self):
        if self.current_cryptogram_index < len(cryptograms):
            self.current_cryptogram = cryptograms[self.current_cryptogram_index]
            cryptogram, _ = self.current_cryptogram
            self.cryptogram_label.config(text=f"Solve:\n\n{cryptogram}")
            self.solution_entry.delete(0, tk.END)  # Clear the entry box
        else:
            self.show_congratulations()

    def check_solution(self):
        user_input = self.solution_entry.get()
        _, solution = self.current_cryptogram

        if user_input == solution:
            self.current_cryptogram_index += 1
            self.show_next_cryptogram()
        else:
            self.incorrect_attempts += 1
            self.show_incorrect_popups()
            self.update_lives()

            if self.incorrect_attempts >= self.max_attempts:
                self.show_game_over()

    def show_incorrect_popups(self):
        num_popups = random.randint(10, 20)  # Random number of pop-ups
        for _ in range(num_popups):
            x_pos = random.randint(100, 800)
            y_pos = random.randint(100, 600)
            duration = random.randint(2, 4) * 1000  # Random duration between 2 and 4 seconds

            # Create the popup window
            popup = tk.Toplevel(self.root)
            popup.title("Incorrect")
            popup.geometry(f"200x100+{x_pos}+{y_pos}")
            label = tk.Label(
                popup,
                text="INCORRECT",
                font=("Courier New", 24, "bold"),
                bg="#000000",
                fg="#FF0000"
            )
            label.pack(expand=True, fill=tk.BOTH)
            
            # Close the popup after 1 second
            self.root.after(1000, popup.destroy)
            # Reopen the popup after the random duration
            self.root.after(duration, lambda p=popup: p.deiconify())

    def update_lives(self):
        for i in range(self.max_attempts):
            if i < self.max_attempts - self.incorrect_attempts:
                self.lives_labels[i].pack(side=tk.LEFT, padx=10)
            else:
                self.lives_labels[i].pack_forget()

    def show_game_over(self):
        self.game_frame.pack_forget()  # Hide the game frame

        game_over_frame = tk.Frame(
            self.root,
            bg="#000000",
            padx=30,
            pady=30,
            borderwidth=3,
            relief=tk.SOLID
        )
        game_over_frame.pack(fill=tk.BOTH, expand=True)

        game_over_label = tk.Label(
            game_over_frame,
            text="GAME OVER TRY AGAIN",
            font=("Courier New", 48, "bold"),
            bg="#000000",
            fg="#FF0000"
        )
        game_over_label.pack(pady=50, padx=50, expand=True)

        # Close the game after 3 seconds
        self.root.after(3000, self.exit_game)

    def show_congratulations(self):
        self.game_frame.pack_forget()  # Hide the game frame

        congrats_frame = tk.Frame(
            self.root,
            bg="#000000",
            padx=30,
            pady=30,
            borderwidth=3,
            relief=tk.SOLID
        )
        congrats_frame.pack(fill=tk.BOTH, expand=True)

        congrats_label = tk.Label(
            congrats_frame,
            text="CONGRATULATIONS!\nYou have solved The Key is Password",
            font=("Courier New", 36, "bold"),
            bg="#000000",
            fg="#00FF00",
            justify=tk.CENTER
        )
        congrats_label.pack(pady=50, padx=50, expand=True)

        # Close the game after 5 seconds
        self.root.after(5000, self.exit_game)

    def exit_game(self):
        self.root.quit()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
    
    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

def main():
    root = tk.Tk()
    
    # Set fullscreen mode
    root.attributes("-fullscreen", True)
    
    game = CryptogramGame(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()