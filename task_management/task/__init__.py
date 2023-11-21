# # # Enter a month, and print number of days of that month.
#
# # def days_of_month(month):
# #     if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
# #         return 31
# #     elif month == 4 or month == 6 or month == 9 or month == 11:
# #         return 30
# #     else:
# #         year = int(input("Which year: "))
# #         if year % 4 == 0:
# #             return 29
# #         else:
# #             return 28
#
#
# # month = int(input("Enter a month: "))
# # print(days_of_month(month))
#
#
# import random
#
# def play_guess_the_number(min, max):
#     rand_number = random.randint(min, max)
#     guess = 0
#     while True:
#         guess = guess + 1
#         guess_number = int(input("Enter a number: "))
#         if guess_number == rand_number:
#             print("You’ve got it, I chose", rand_number, "It took you", guess, "guesses.")
#             break
#         elif guess_number < rand_number:
#             print("Your guess is too low.")
#         else:
#             print("Your guess is too high.")
#
#
#         print("Guess: ", guess)
#
#
# play_guess_the_number(1, 10)