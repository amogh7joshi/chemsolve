'''
A loose collection of functions which perform operations on strings.
'''

def split(string):
   '''
   Takes in a string, returns a list containing each character in the string.
   '''
   return [char for char in string]

def nums_in_string(string):
   '''
   Takes in a string, returns a list containing the numbers in the string.
   '''
   return [char for char in string if isinstance(char, int)]