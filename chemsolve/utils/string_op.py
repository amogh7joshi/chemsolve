'''
A loose collection of functions which perform operations on strings.
'''

def split(string):
   '''
   Takes in a string, returns a list containing each character in the string.
   '''
   return [char for char in string]

def num_in_string(string):
   '''
   Takes in a string, returns each of the numbers within the string.
   '''
   return [char for char in string if char.is_digit() == True]


