# Smart Study Planner
# 1203 ST - Programming Fundamentals
#
# This program allows a student to:
# 1. Add study sessions
# 2. View all study sessions
# 3. Search sessions by subject
# 4. View study statistics
# 5. Save and exit
#
# Study sessions are saved in study_log.txt so that they
# can be loaded again when the program starts.

import json

# File used to store study session data
FILE_NAME = "study_log.txt"

# List used to store all study sessions
sessions = []


def classify_session(duration):
    """
    Classify a study session based on its duration.

    Under 30 minutes  -> Short
    30 to 90 minutes  -> Medium
    Over 90 minutes   -> Long
    """

    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session():
    """
    Ask the user for study session details and add
    the session to the sessions list.
    """

    print("\n--- Add Study Session ---")

    subject = input("Enter subject: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day: ").strip()

    # Keep asking until a positive duration is entered
    while True:
        try:
            duration = float(input("Enter duration in minutes: "))

            if duration > 0:
                break
            else:
                print("Duration must be a positive number.")

        except ValueError:
            print("Please enter a valid number.")

    # Store the session as a dictionary
    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    # Add the dictionary to the list
    sessions.append(session)

    print("Study session added successfully.")


def view_sessions():
    """
    Display all recorded study sessions in a formatted table.
    """

    print("\n--- All Study Sessions ---")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    print("-" * 85)
    print(
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Duration':<12}"
        f"{'Class':<10}"
    )
    print("-" * 85)

    for session in sessions:
        classification = classify_session(session["duration"])

        print(
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12.1f}"
            f"{classification:<10}"
        )

    print("-" * 85)


def search_by_subject(subject):
    """
    Search for study sessions by subject.
    The search is not case-sensitive.
    """

    print(f"\n--- Search Results for: {subject} ---")

    found_sessions = []

    # Convert the search subject to lowercase
    # so that the search is not case-sensitive.
    search_subject = subject.strip().lower()

    for session in sessions:
        if session["subject"].strip().lower() == search_subject:
            found_sessions.append(session)

    # If no sessions were found
    if not found_sessions:
        print("No sessions found for that subject.")
        return

    total_minutes = 0

    print("-" * 85)
    print(
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Duration':<12}"
        f"{'Class':<10}"
    )
    print("-" * 85)

    for session in found_sessions:
        classification = classify_session(session["duration"])

        print(
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12.1f}"
            f"{classification:<10}"
        )

        total_minutes += session["duration"]

    print("-" * 85)
    print(f"Total time spent on {subject}: {total_minutes:.1f} minutes")


def study_statistics():
    """
    Calculate and display study statistics:
    - Total hours studied overall
    - Total hours studied per subject
    - Subject with the least study time
    - Longest individual study session
    """

    print("\n--- Study Statistics ---")

    if not sessions:
        print("No study sessions available for statistics.")
        return

    # Calculate total minutes studied
    total_minutes = sum(session["duration"] for session in sessions)

    # Convert total minutes to hours
    total_hours = total_minutes / 60

    print(f"Total hours studied overall: {total_hours:.2f} hours")

    # Dictionary to store total study time for each subject
    subject_totals = {}

    for session in sessions:
        subject = session["subject"]
        duration = session["duration"]

        # Use the original subject name as entered
        if subject not in subject_totals:
            subject_totals[subject] = 0

        subject_totals[subject] += duration

    print("\nTotal hours studied per subject:")

    for subject, minutes in subject_totals.items():
        hours = minutes / 60
        print(f"- {subject}: {hours:.2f} hours")

    # Find the subject with the least total study time
    weakest_subject = min(subject_totals, key=subject_totals.get)
    weakest_minutes = subject_totals[weakest_subject]

    print(
        f"\nSubject with the least study time "
        f"(weakest area): {weakest_subject}"
    )
    print(f"Total time: {weakest_minutes / 60:.2f} hours")

    # Find the single longest study session
    longest_session = max(sessions, key=lambda session: session["duration"])

    print("\nLongest session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Date: {longest_session['date']}")
    print(f"Duration: {longest_session['duration']:.1f} minutes")
    print(
        f"Classification: "
        f"{classify_session(longest_session['duration'])}"
    )


def save_sessions():
    """
    Save all study sessions to study_log.txt.
    JSON format is used so that the dictionaries can
    be loaded again when the program starts.
    """

    try:
        with open(FILE_NAME, "w") as file:
            json.dump(sessions, file, indent=4)

        print(f"\nStudy sessions saved to {FILE_NAME}.")

    except OSError as error:
        print(f"Error saving sessions: {error}")


def load_sessions():
    """
    Load previously saved study sessions from study_log.txt.

    If the file does not exist, the program starts with
    an empty sessions list instead of crashing.
    """

    global sessions

    try:
        with open(FILE_NAME, "r") as file:
            sessions = json.load(file)

        # Make sure the loaded data is a list
        if not isinstance(sessions, list):
            sessions = []

        print(f"Previous study sessions loaded from {FILE_NAME}.")

    except FileNotFoundError:
        # This is normal when the program is being run for
        # the first time.
        sessions = []
        print("No previous study log found. Starting a new log.")

    except json.JSONDecodeError:
        # Handles an empty or incorrectly formatted file
        sessions = []
        print("The study log could not be read. Starting with an empty log.")

    except OSError as error:
        sessions = []
        print(f"Error loading study sessions: {error}")


def main():
    """
    Main function that displays the menu and controls
    the Smart Study Planner.
    """

    # Load previous sessions when the program starts
    load_sessions()

    while True:
        print("\n" + "=" * 50)
        print("           SMART STUDY PLANNER")
        print("=" * 50)
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        print("=" * 50)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session()

        elif choice == "2":
            view_sessions()

        elif choice == "3":
            subject = input("Enter subject to search: ").strip()

            if subject:
                search_by_subject(subject)
            else:
                print("Subject cannot be empty.")

        elif choice == "4":
            study_statistics()

        elif choice == "5":
            save_sessions()
            print("Thank you for using Smart Study Planner.")
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


# Program entry point
if __name__ == "__main__":
    main()