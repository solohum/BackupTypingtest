import mysql.connector
import curses
import time
import random

# MySQL connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",        # Database host
        user="root",             # Database username
        password="your_password", # Database password
        database="typing_test"   # Database name
    )

# Texts for each difficulty
difficulty_texts = {
    "easy": [
        "The quick brown fox jumps over the lazy dog.",
        "A journey of a thousand miles begins with a single step.",
        "Hello world! Welcome to the typing test."
    ],
    "medium": [
        "To be or not to be, that is the question.",
        "All that glitters is not gold.",
        "A watched pot never boils, they say."
    ],
    "hard": [
        "The complexity of life is beyond comprehension, yet we try to understand it.",
        "Programming is like solving a puzzle where the pieces never fit perfectly.",
        "Time is an illusion. Lunchtime doubly so."
    ]
}

# Function to display the typing test screen using curses
def typing_test(stdscr):
    # Clear screen
    stdscr.clear()

    # Main Menu
    stdscr.addstr(0, 0, "Welcome to the Typing Test\n")
    stdscr.addstr(1, 0, "1. Start Typing Test\n")
    stdscr.addstr(2, 0, "2. View Typing Records\n")
    stdscr.addstr(3, 0, "Choose an option (1 or 2): ")
    stdscr.refresh()

    choice = stdscr.getch()

    if choice == ord('1'):
        # Start the typing test
        start_typing_test(stdscr)
    elif choice == ord('2'):
        # View the typing test records
        view_records(stdscr)
    else:
        # Invalid choice, show the menu again
        typing_test(stdscr)

# Function to start the typing test
def start_typing_test(stdscr):
    # Ask for username
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter your username: ")
    curses.echo()
    username = stdscr.getstr(1, 0).decode("utf-8")
    curses.noecho()

    # Ask for difficulty level
    stdscr.addstr(2, 0, "Select difficulty (easy, medium, hard): ")
    difficulty = stdscr.getstr(3, 0).decode("utf-8").lower()
    if difficulty not in difficulty_texts:
        difficulty = "easy"  # Default to easy if invalid input

    # Get the text based on the difficulty level
    text_to_type = random.choice(difficulty_texts[difficulty])

    # Display the text to type
    stdscr.clear()
    stdscr.addstr(0, 0, f"Type the following text:\n\n{text_to_type}\n\nPress any key to start.")
    stdscr.refresh()
    stdscr.getch()  # Wait for any key to start

    # Start the typing test
    start_time = time.time()
    typed_text = ""
    stdscr.clear()
    stdscr.addstr(0, 0, f"Type the following text:\n\n{text_to_type}\n\n")
    stdscr.addstr(2, 0, "Start typing:")
    stdscr.refresh()

    while True:
        # Display the typed text and the remaining part
        stdscr.addstr(3, 0, typed_text)
        stdscr.addstr(4, 0, text_to_type[len(typed_text):])
        stdscr.refresh()

        key = stdscr.getch()

        # Break the loop when user finishes typing
        if key == 10:  # Enter key to submit
            break

        # If the key is a valid character, add it to the typed text
        if key >= 32 and key <= 126:
            typed_text += chr(key)

    # End the typing test and calculate WPM and accuracy
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Calculate words per minute (WPM)
    words = len(typed_text.split())
    wpm = int((words / elapsed_time) * 60)

    # Calculate accuracy
    correct_chars = sum(1 for i, char in enumerate(typed_text) if i < len(text_to_type) and char == text_to_type[i])
    accuracy = (correct_chars / len(text_to_type)) * 100

    # Save the result in the database
    save_record(username, difficulty, accuracy, wpm)

    # Display the result
    stdscr.clear()
    stdscr.addstr(0, 0, f"Test completed!\n\n")
    stdscr.addstr(1, 0, f"Words per minute: {wpm}\n")
    stdscr.addstr(2, 0, f"Accuracy: {accuracy:.2f}%\n")
    stdscr.addstr(3, 0, f"Difficulty: {difficulty.capitalize()}\n")
    stdscr.addstr(4, 0, f"Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()  # Wait for key to go back to menu
    typing_test(stdscr)

# Function to save the record into the database
def save_record(username, difficulty, accuracy, wpm):
    db = connect_db()
    cursor = db.cursor()
    query = "INSERT INTO records (username, difficulty, accuracy, wpm) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (username, difficulty, accuracy, wpm))
    db.commit()
    cursor.close()
    db.close()

# Function to view the records
def view_records(stdscr):
    # Connect to the database and retrieve the records
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM records ORDER BY timestamp DESC")
    records = cursor.fetchall()

    # Display the records
    stdscr.clear()
    stdscr.addstr(0, 0, "Typing Test Records:\n\n")
    if records:
        for idx, record in enumerate(records, start=1):
            username, difficulty, accuracy, wpm, timestamp = record[1], record[2], record[3], record[4], record[5]
            stdscr.addstr(2 + idx, 0, f"{idx}. Username: {username}, Difficulty: {difficulty}, Accuracy: {accuracy:.2f}%, WPM: {wpm}, Time: {timestamp}")
    else:
        stdscr.addstr(2, 0, "No records found.")
    
    stdscr.addstr(len(records) + 3, 0, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()  # Wait for key to go back to menu
    typing_test(stdscr)

# Main function to run the typing test
def main():
    curses.wrapper(typing_test)

if __name__ == "__main__":
    main()
