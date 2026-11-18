# QUESTION 1: FIND THE FIRST PALINDROMIC STRING

def first_palindrome(words):
    for word in words:
        if word == word[::-1]:
            return word
    return ""


words = input("Enter words separated by spaces: ").split()
result = first_palindrome(words)
print("First palindromic string:", result)
