import os
from datetime import datetime

def generate_timestamp_millis(dt=None):
  """
  Generates a timestamp in milliseconds since the Unix epoch (1970-01-01 00:00:00 UTC).

  Args:
    dt: Optional. A datetime object. 
         If None, uses the current datetime.

  Returns:
    The timestamp in milliseconds as an integer.
  """
  if dt is None:
    dt = datetime.now()

  # Get the start of the current hour
  start_of_hour = dt.replace(minute=0, second=0, microsecond=0)

  # Convert datetime to timestamp in milliseconds
  timestamp = int(start_of_hour.timestamp() * 1000) 
  return timestamp

def get_user_date():
  """
  Asks the user for a date input from the console and returns a datetime object.

  Returns:
    A datetime object representing the user's input.
  """

  while True:
    try:
      date_str = input("Enter date (YYYY-MM-DD): ")
      user_date = datetime.strptime(date_str, "%Y-%m-%d")
      return user_date
    except ValueError:
      print("Invalid date format. Please enter in YYYY-MM-DD format (e.g., 2024-12-25).")

def get_file_creation_time(file_path):
  """
  Gets the creation time of the specified file.

  Args:
    file_path: The path to the file.

  Returns:
    A datetime object representing the file creation time, 
    or None if the creation time cannot be determined.
  """
  try:
    creation_time = os.path.getctime(file_path)
    return datetime.fromtimestamp(creation_time)
  except OSError:
    print(f"Error: Could not get creation time for file: {file_path}")
    return None

def fill_string_with_zeros(number, desired_length):
  """
  Fills a string representation of a number with leading zeros 
  to reach the desired length.

  Args:
    number: The number to convert to a string.
    desired_length: The desired length of the string.

  Returns:
    A string with leading zeros added to the number 
    to reach the specified length.
  """
  number_str = str(number)
  return number_str.zfill(desired_length)

def confirm_update(message):
  """
  Asks the user if they want to update the given list of choices.

  Args:
    message: The message to display to the user

  Returns:
    True if the user confirms the update, False otherwise.
  """

  while True:
    user_input = input(f"{message} (y/n): ").lower()
    if user_input in ['y', 'yes']:
      return True
    elif user_input in ['n', 'no']:
      return False
    else:
      print("Invalid input. Please enter 'y' or 'n'.")

def ensure_key_exists_list(data, key):
  """
  Ensures that the given key exists in the dictionary. 

  If the key does not exist, it creates an empty list for that key.

  Args:
    data: The dictionary to check and potentially modify.
    key: The key to check for existence.
  """
  if key not in data:
    data[key] = []