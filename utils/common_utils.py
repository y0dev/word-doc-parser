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