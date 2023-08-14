"""
Example usage of ttshelper.
Simply import say and write your message.
"""

from ttshelper import say

# Get user input
to_speak = input("What should your computer say? : ")

# Use library to say whatever received from user
say(to_speak)
