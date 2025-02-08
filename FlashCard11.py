import pandas as pd
from tkinter import *
import os
import pickle

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English2Bangla Flashcards")

        # Default file path
        self.default_file_path = "C:\\Users\\jfrip\\Desktop\\Flash Card\\English_Bangla_Flashcards.xlsx" 
        self.file_path = self.default_file_path 

        # Load data from Excel or saved state
        try:
            with open('flashcard_state.pkl', 'rb') as f:
                self.current_index, self.data = pickle.load(f) 
        except FileNotFoundError:
            self.data = pd.read_excel(self.file_path) 
            self.current_index = 0
        self.total_cards = len(self.data) 

        # Create frames
        self.frame = Frame(root)
        self.frame.pack(pady=20)

        # Create labels
        self.card_number_label = Label(self.frame, text="", font=("Arial", 14), width=5, anchor="w")
        self.card_number_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.english_phrase_label = Label(self.frame, text="", font=("Arial", 14), width=30, anchor="w")
        self.english_phrase_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.meaning_label = Label(self.frame, text="", font=("Arial", 14), wraplength=300, justify=LEFT, anchor="w") 
        self.meaning_label.grid(row=2, column=0, padx=10, pady=5, sticky=W) 

        self.bangla_translation_label = Label(self.frame, text="", font=("Arial", 14), width=30, anchor="w")
        self.bangla_translation_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        self.english_examples_label = Label(self.frame, text="", font=("Arial", 12), wraplength=300, justify=LEFT)
        self.english_examples_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        self.bangla_examples_label = Label(self.frame, text="", font=("Arial", 12), wraplength=300, justify=LEFT)
        self.bangla_examples_label.grid(row=5, column=0, padx=10, pady=5, sticky=W)

        # Create buttons
        self.prev_button = Button(self.frame, text="Previous", command=self.prev_card)
        self.prev_button.grid(row=6, column=0, padx=10, pady=10)

        self.next_button = Button(self.frame, text="Next", command=self.next_card)
        self.next_button.grid(row=6, column=1, padx=10, pady=10)

        self.delete_button = Button(self.frame, text="Delete", command=self.delete_card)
        self.delete_button.grid(row=6, column=2, padx=10, pady=10)

        self.save_button = Button(self.frame, text="Save", command=self.save_state)
        self.save_button.grid(row=6, column=3, padx=10, pady=10)

        self.start_again_button = Button(self.frame, text="Start Again", command=self.start_again)
        self.start_again_button.grid(row=6, column=4, padx=10, pady=10)

        # Display the first card
        self.show_card()

    def show_card(self):
        if not self.data.empty:  # Check if DataFrame is empty
            card_number = self.current_index + 1  # Start card numbers from 1
            english_phrase = self.data.iloc[self.current_index, 0]
            meaning = self.data.iloc[self.current_index, 1]
            bangla_translation = self.data.iloc[self.current_index, 2]
            english_examples = self.data.iloc[self.current_index, 3]
            bangla_examples = self.data.iloc[self.current_index, 4]

            self.card_number_label.config(text=f"Card {card_number}")
            self.english_phrase_label.config(text=f"English Phrase: {english_phrase}")
            self.meaning_label.config(text=f"Meaning: {meaning}") 
            self.bangla_translation_label.config(text=f"Bangla Translation: {bangla_translation}")
            self.english_examples_label.config(text=f"English Examples:\n{english_examples}")
            self.bangla_examples_label.config(text=f"Bangla Examples:\n{bangla_examples}")
        else:
            # Handle empty DataFrame
            self.card_number_label.config(text="No Cards Left")
            self.english_phrase_label.config(text="")
            self.meaning_label.config(text="")
            self.bangla_translation_label.config(text="")
            self.english_examples_label.config(text="")
            self.bangla_examples_label.config(text="")

    def next_card(self):
        self.current_index = (self.current_index + 1) % self.total_cards
        self.show_card()

    def prev_card(self):
        self.current_index = (self.current_index - 1) % self.total_cards
        self.show_card()

    def delete_card(self):
        try:
            # Delete the current row from the DataFrame
            self.data = self.data.drop(self.current_index)

            # Update total cards and current index
            self.total_cards = len(self.data)
            if self.current_index >= self.total_cards:
                self.current_index = self.total_cards - 1 

            # Save the modified DataFrame to the Excel file
            self.data.to_excel(self.file_path, index=False) 

            # Display the next card
            self.show_card()

        except IndexError:
            pass  # Handle case where no cards are left

    def save_state(self):
        with open('flashcard_state.pkl', 'wb') as f:
            pickle.dump((self.current_index, self.data), f) 

    def start_again(self):
        # Change file path to "English_Bangla_Flashcards2.xlsx"
        self.file_path = "C:\\Users\\jfrip\\Desktop\\Flash Card\\English_Bangla_Flashcards2.xlsx" 
        self.data = pd.read_excel(self.file_path) 
        self.total_cards = len(self.data)
        self.current_index = 0
        self.show_card()

if __name__ == "__main__":
    root = Tk()
    app = FlashcardApp(root)
    root.mainloop()