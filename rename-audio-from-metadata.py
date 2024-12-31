import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError

# Function to get the directory
def get_directory(previous_directory=None):
    while True:
        if previous_directory:
            use_previous = input(f"Do you want to use the previous directory '{previous_directory}'? [y/n]: ").strip().lower()
            if use_previous == 'y':
                return previous_directory

        user_input = input("Enter the new directory: ")
        if os.path.isdir(user_input):
            return user_input
        else:
            print("Invalid directory. Please try again.")

# Initialize the previous directory as None
previous_directory = None

# Ask the user for the directory
folder = get_directory(previous_directory)

# Change to the specified directory
os.chdir(folder)

# Loop through all mp3 files in the folder
for filename in os.listdir(folder):
    if filename.endswith(".mp3"):
        try:
            # Load the MP3 file
            audio = MP3(filename, ID3=ID3)
            # Extract the title
            title = audio.tags.get('TIT2')
            if title:
                title = str(title)  # Convert to string
                # Remove invalid characters for file names
                invalid_chars = ['/', '\\', '*', '?', '!', '<', '>', '|', ';', ',', '.']
                original_title = title  # Save the original title for the message
                for char in invalid_chars:
                    title = title.replace(char, "")
                
                # Check if the title is empty
                if title:
                    new_filename = f"{title}.mp3"
                    os.rename(filename, new_filename)
                    print(f"Renaming '{filename}' to '{new_filename}'")
                else:
                    print(f"The title is empty for the file '{filename}', it will not be renamed.")
            else:
                print(f"No title found for the file '{filename}'.")
        except ID3NoHeaderError:
            print(f"The file '{filename}' does not have an ID3 header.")
        except Exception as e:
            print(f"Error processing the file '{filename}': {e}")

        # Notify if there are invalid characters
        if original_title != title:
            print(f"Warning: the original title '{original_title}' contained invalid characters for the file name.")

# Update the previous directory
previous_directory = folder
