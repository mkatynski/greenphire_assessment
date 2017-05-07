#!/usr/bin/env python

#
##
###Marcus Katynski
###May 6, 2017

from random import randint
from collections import Counter

#We need the random library for tiebreaking as per point 6, and
#the Counter module from the collections library for organizing
#the duplicates from among the chosen numbers.

class employee:

#This class does all the organizational legwork - 
#the employee's first and last name are set when
#the class is instantiated, and the numbers are
#set to empty values to be changed later by a 
#function call to get_numbers.

	def __init__(self, first, last):
		self.firstname = first
		self.lastname = last
		self.fav_numbers = []
		self.powerball = 0

	def get_numbers(self):

		#This member function prompts the user for input to set
		#each employee's 5 favorite numbers and their powerball number.
		#The entries are checked to make sure that they are in the specified
		#range and that no duplicates are entered. 
		
		print("\nWhat are %s %s's 5 favorite, unique numbers between 1 and 69?"%(self.firstname,self.lastname))
		 
		for j in range(5):
			
			if len(self.fav_numbers) > 0:
				print("\nPrevious selections are %s"%(self.fav_numbers))
			
			choice = input("Please enter number %s: "%(j+1))
			
			while choice in self.fav_numbers or choice < 1 or choice > 69:
				print("Sorry, the number must be unique and between 1 and 69.")
				choice = input("Please enter another number: ")
			
			self.fav_numbers.append(choice)
		
		print("\nWhat is %s %s's Powerball number?"%(self.firstname,self.lastname))
		
		powerchoice = input("It can be any number between 1 and 26: ")
		
		while powerchoice < 1 or powerchoice > 26:
			print("Sorry, the number must be between 1 and 26.")
			powerchoice = input("Please enter another number: ")
			
		self.powerball = powerchoice	


def get_counts(players):

	#This function takes as input the list of employees,
	#and creates master lists of all their favorite numbers
	#and powerball numbers. From there, the Counter method
	#is employed to count how many times each number appeared
	#in the employees' selections, and then to organize them
	#into a list of tuples in order of most frequently
	#used to least frequently used - this ordering is crucial to
	#functionality to come. The sorted and ordered lists are returned.
	
	favorite_tally = []
	powerball_tally = []

	for i in range( len( players ) ):
		powerball_tally.append( players[i].powerball )
		for j in range(5):
			favorite_tally.append( players[i].fav_numbers[j] )

	fav_counts = Counter(favorite_tally)
	pow_counts = Counter(powerball_tally)
	
	return fav_counts.most_common(), pow_counts.most_common()
	

def trim_singles(List):

	#This function removes the selections which were chosen only once from
	#the list provided to it as input, since only duplicates are of interest. 
	#It accomplishes this by referencing the second entry in each tuple, which
	#is the count of how many times the number (in the corresponding first entry of each tuple)
	#was used. If the second entry is 1, the whole entry is deleted. The list is iterated
	#through in reverse to preserve indices when elements are deleted.
	#It will be used in turn to prepare both the master list of favorites and the 
	#master list of powerball numbers. It returns a list of only the numbers
	#that were chosen more than once.
	
	for i in reversed(range(len(List))):
		if List[i][1] == 1:
			del(List[i])
	
	return List

def rand_pick(in_list, target):
	
	#This function is only called if there are more duplicates
	#chosen than the list of winning numbers allows for. It loops through
	#the list of duplicates, comparing how many times each number has been chosen
	#compared to the number immediately following it. If they've been used the same
	#number of times, the current duplicate is added to a temporary list. If they
	#haven't been used the same number of times, the current duplicate is added
	#to the temporary list. The temporary list (which at this point contains all the
	#duplicates used a given number of times of times) is then cycled through. A number from
	#that list is randomly chosen and added to the output list, and then removed from the
	#temporary list. This process continues until either the output list reaches the
	#maximum value of five, or the temporary list is exhausted. If the temporary list
	#is exhausted while the output list is still under the maximum value, the first loop
	#begins again and the temporary list is repopulated, and then the second loop executes
	#again to fill the output list.
	

	copies = []
	out_list = []	
	
	for i in range( len(in_list) - 1 ):
		
		if in_list[i][1] == in_list[i+1][1]:
				copies.append(in_list[i][0])
		
		else:
			copies.append(in_list[i][0])
			while len( out_list ) < target and len( copies ) > 0:
				rand_winner = randint(0, len( copies) - 1)
				out_list.append( copies[rand_winner] )
				del(copies[rand_winner])
	
	return out_list
	

def find_winner(emps):
	
	#This is the function that contains the above 3 subroutines, and 
	#returns the final winning numbers. It takes the list of employees
	#as input, and calls the get_counts and trim_singles functions to 
	#process them. If the list of duplicated favorite numbers is less
	#than five, those five are selected and then the rest of the list is filled randomly.
	#If it is more than five, the rand_pick function is called to select
	#which numbers are chosen. For the powerball numbers, if there were no 
	#duplicates, a number is selected at random. If there was only one
	#duplicate, it is chosen as the winning powerball number. If there were
	#multiple duplicates chosen multiple times, then the less frequently chosen
	#numbers are eliminated and one of the most frequently chosen numbers is 
	#chosen. At that point, the function returns the winning numbers.

	max_fav, max_pow = get_counts(emps)

	max_fav = trim_singles(max_fav)
	max_pow = trim_singles(max_pow)
	
	###Finding the winning five favorite numbers.

	if len(max_fav) <= 5:
		
		win_fav = []
		
		for i in range(len(max_fav)):
			win_fav.append(max_fav[i][0])
		
		while len(win_fav) < 5:
			
			rand_filler = randint(1,69)
			while rand_filler in win_fav:
				rand_filler = randint(1,69)
			
			win_fav.append(rand_filler)
	
	else:
		
		win_fav = rand_pick(max_fav, 5)
				
	###Finding the winning powerball number.

	if len(max_pow) == 0:
		win_power = randint(1,26)

	elif len(max_pow) == 1:
		win_power = max_pow[0][0]
	
	else:
		
		win_power = []
		for i in reversed(range(len(max_pow), 1)):
			if max_pow[i][1] < max_pow[i-1][1]:
				del(max_pow[i])
		rand_pow_win = randint(0, len(max_pow) - 1)
		win_power.append( max_pow[ rand_pow_win ][0] )
		

	return win_fav, win_power
	
	
###This is the main body of the program. First, the user is prompted
#for the number of employees who are participating in the drawing. The program
#then loops that many times; each time around, it gets the first and last name of
#an employee, initializes an instance of the employee class and appends it to emp_list.
#After adding them to the list, the get_numbers member function is called to obtain
#and store that employee's numbers for the drawing. By the end of the loop, emp_list
#contains the names and chosen numbers of the user-specified number of employees.

emp_list = []
num_emps = input("How many employees are in the Powerball drawing? ")

for i in range( num_emps ):
	
	fn = raw_input("\nWhat is employee %s's first name? "%(i+1))
	ln = raw_input("What is employee %s's last name? "%(i+1))

	emp_list.append( employee(fn, ln) )
	emp_list[i].get_numbers()

print("\n\n")

###This loop simply displays all the information that was entered in the previous loop.

for k in range( len( emp_list ) ):
	print("%s %s %s Powerball: %s"%(emp_list[k].firstname, emp_list[k].lastname,
		emp_list[k].fav_numbers, emp_list[k].powerball))

###This is the function call that does almost all the work, and involves all the 
#non-member functions defined above. The employees' choices are assembled in one
#place, sorted, organized, and used to generate the winning numbers by means described
#in the preamble to each function.

winning_5, winning_power = find_winner(emp_list)

#After the winning numbers are determined, they are printed. Hopefully the
#winner doesn't spend it all in one place. 

print("\n\nThe winning numbers are: \n%s Powerball: %s"%(winning_5, winning_power))

