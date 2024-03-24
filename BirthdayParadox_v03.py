"""Birthday Paradox Simulation, by smallcabbage333 smallcabbage33@gmail.com
My take on the perplexing and well-known 'Birthday Paradox' simulation.
More info at https://en.wikipedia.org/wiki/Birthday_problem
Initially based on Al Sweigart's code: https://inventwithpython.com/bigbookpython/project2.html
"""

import datetime, random # Datetime and Random are for generating random birthdays.
# DefaultDict helps for more efficient dictionaries, providing a default value when a key doesn't exist.
# Counter is used to more efficiently find matching birthdays.
from collections import defaultdict, Counter 

# Define the names of months to convert date objects into readable strings later.
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December')


def get_random_birthdays(num_birthdays):
    """
    Generate a list of random birthday dates.
    
    Args:
    num_birthdays (int): The number of random birthdays to generate.
    
    Returns:
    list[datetime.date]: a list containing datetime.date objects representing random birthdays.
    """
    # Starting from 2001/01/01 add 0 to 365 days to generate a random birthday, do this num_birthdays amount of times.
    # The below list comprehensions concisely creates a list without writing a full for loop statement.
    birthdays = [datetime.date(2001, 1, 1) + datetime.timedelta(random.randint(0, 364)) 
                 for _ in range(num_birthdays)]
    return birthdays # Return the list of birthdays.


def find_duplicate_birthdays(birthdays):
    """
    Checks if there is at least one duplicate birthday in the list.

    Args:
    birthdays (list[datetime.date]): The list of birthdays to check for duplicates.

    Returns:
    bool: True if there is at least one duplicate, False otherwise.
    """

    birthday_counts = Counter(birthdays) # The counter efficiently tallies info by grouping and counting occurrences.
    for count in birthday_counts.values(): # Loop through every tally.
        if count > 1: # If a tally is greater than 1 return True.
            return True
    return False # If not return False.


def display_birthdays(birthdays_list):
    """
    Display the birthdays and their occurrences.
    
    Args:
    birthdays_list (list[datetime.date]): The list of birthdays to display.
    
    Returns:
    dict: A dictionary with birthdays as keys and their occurrences as values.
    """
    # Count occurrences of each birthday. The dictionary aggregates duplicates keeping a count of their occurences.
    birthday_counts = defaultdict(int) # Initialize birthday_counts dictionary, starting with a default value when a key does not exist.
    for birthday in birthdays_list: # Loop through every birthday.
        birthday_counts[birthday] += 1 # For that birthday increment 1.

    # Display each birthday and its count, sorted by date.
    sorted_birthdays = sorted(birthday_counts.items(), key=lambda x: x[0]) 
    # Sorts the dictionary by ascending date. 
    # 'birthday_counts.items()' converts the dictionary key-value pairs to a list of key-value tuples. 
    # 'key=lambda x: x[0]' is a function that takes the first element in the tuple which is the date and returns that as the key to sort by.
    # 'lambda' functions are small anonymous functions of only one expression

    # Loop through the list of tuples. 'birthday' and 'count' are 1st and 2nd elements, being the date and tally.
    for birthday, count in sorted_birthdays: 
        monthName = MONTHS[birthday.month - 1] # Grab the month name by getting the index and using MONTHS.
        dateText = '%s %s' % (monthName, birthday.day) # Format and create the date text with month name and date day.
        print('%s, count: %s' % (dateText, count)) # Print the formatted birthday and tally
    print() # Add a line space for clarity.

    return birthday_counts # Return the birthday counts dictionary with birthdays keys and tally values.


def summarize_matches(birthdays):
    """
    Summarize and display the number of birthdays by their occurrence counts.

    Args:
    birthdays (dict): A dictionary with birthdays as keys and occurrences as values.
    """
    # Summarize the number of birthdays grouped by their occurrence counts.
    # Initialize matchesSummary dictionary with a default value. 
    matchesSummary = defaultdict(int) # For tally groups and their sum of birthdays.
    for count in birthdays.values(): # Loops through the tallies of the birthdays dictionary.
        if count > 1: # True if the tally is greater than 1.
            matchesSummary[count] += 1 # Increment matchesSummary for the tally group.

    # Display the sum of birthdays per tally group.
    if not matchesSummary: # Checks if there is even a match.
        print('There were no matching birthdays.') 
    else: # This handles for when there is a match.
        # Loop through sorted key-value tuples of matchesSummary. 'count' is the tally group, 'numBirthdays' is the sum of birthdays.
        for count, numBirthdays in sorted(matchesSummary.items()): 
            if numBirthdays == 1: # If there is only 1 mathch.
                print(f'There is 1 birthday with a match.')
            else: # If there are multiple matches.
                print(f'There are {numBirthdays} with {count} matches.')
    print()


def simulate_birthday_paradox(num_people, num_simulations=100000):
    """
    Simulate the birthday paradox multiple times to find the probability of shared birthdays,
    with progress updates every 10,000 simulations.
    
    Args:
    num_people (int): Number of people to simulate birthdays for.
    num_simulations (int): Number of simulations to run.

    Returns:
    tuple: Probability of shared birthdays and the total number of matches found.
    """
    print() # Add an empty line for visual separation and clarity.
    print(f'Generating {num_people} random birthdays {num_simulations} times...') # Notifies the user of imminent simulation.
    input('Press \'Enter\' to begin...') # Require user to press 'Enter' to proceed.
    print() # Add an empty line for visual separation and clarity.

    totalMatches = 0  # Initialize the counter for simulations with at least one match.
    for i in range(num_simulations): # Loop through num_simulations amount of times.
        # Report on the progress every 10,000 simulations, starting from 0:
        if i % 10000 == 0:  # If 10,000 divides cleanly into i with 0 remainder then True. Reports progress every 10,000 simulations.
            print(f'{i} simulations run...')

        birthdays = get_random_birthdays(num_people) # Generate num_people new random birthdays.
        if find_duplicate_birthdays(birthdays) is not False: # Check for duplicate birthdays.
            totalMatches += 1 # Increment total match count of birthdays if a match is found.

    print('100,000 simulations run. \n')  # Indicate that the 100,000 simulations have finished.

    # For demonstration, show details from the last simulation.
    print('Here are the birthdays with repetitions counted from the last simulation:')
    birthday_counts = display_birthdays(birthdays) # Get a dictionary of birthday keys and tally values using the birthdays list.
    summarize_matches(birthday_counts) # Send the dictionary to summarize the info as tally groups and their summed birthdays.

    probability = totalMatches / num_simulations * 100  # Calculate the probability of at least one match.
    return probability, totalMatches # Return the match probability and total matches.


def display_intro(): # Display the intro to the program to explain functionality.
    print('''Birthday Paradox by smallcabbage333 smallcabbage33@gmail.com
    
The birthday paradox shows us that in a group of 'n' people, the odds
that two of them have matching birthdays is surprisingly large.
This program does a 'Monte Carlo' simulation to explore this concept.

(It's not actually a paradox, it's just a surprising results.)\n''')


def get_user_input(): # Get user input for the number of birthdays to be generated.
    while True:
        print('How many birthdays shall I generate? (Max 1000)') # Prompt user and inform limitation.
        response = input('> ') # Get input.
        if response.isdecimal() and (0 < int(response) <= 1000): # Check that input only includes decimal characters and fits in range 1 to 1000.
            return int(response) # Because we know response contains only decimal characters we can safely convert to an integer without errors.
        else:
            print('Please enter a number between 1 and 1000.') # Prompt user again.

def main(): # The main program loop.
    display_intro() # Display the intro
    while True: # Loop through the program.
        num_people = get_user_input() # Get the user's input on number of birthdays to generate.
        probability, totalMatches = simulate_birthday_paradox(num_people) # Get the probability of matches and total matches from the simulation.
        # Print the results:
        print(f'Out of 100,000 simulations of {num_people} people, there was a matching birthday in the group')
        print(f'{totalMatches} times. This means that {num_people} people have a {probability:.8f}% chance of having a matching birthday in their group.')
        print('That\'s probably more than you would think!\n')

        if input('Do you want to try again? (yes/no): ').lower().startswith('n'): # Convert input to lowercase and check if the user's input includes a 'n'.
            break # Break out of the while loop.
        print()

if __name__ == "__main__":
    main() # Start the main program loop.