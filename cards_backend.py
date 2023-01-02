###########################################################

    #  Card Game Backend

    #

    #  Algorithm

    #       initialize the tableau, stock, foundation and waste
    #       a menu of options is displayed
    #       using the display(), the game data which was initialized earlier is displayed
    #       prompt user to enter option from the menu and call parse_option() using the input as the parameter
    #       if None value is returned, continue the loop
    #       elif user inputs TT, check if the move is possible from one column of tabulae to another column, if not print an error message
    #       elif TF is the input, try moving the card from tableau to founadtion, if the move is not possible, print an error message
    #       elif user inputs WT, check if the movement of card is possible from waste to a column of tableau, if not print an error message
    #       elif WF is the input, try moving the card from waste to founadtion, if the move is not possible, print an error message
    #       elif the user inputs 'SW', the function stock_to_waste() is called to move the card, if its possible, the card is moved, else an error message is displayed.
    #       elif the input is 'R', re-initalize the board and display the menu and continue the loop again
    #       elif the input is 'H', display the option menu
    #       elif the input is 'Q', quit the program
    #       for any other input, print an error message and restart the program 
    #       if the user wins the game, congratulate the user

###########################################################

#importing card and deck class from the cards.py file
from cards import Card, Deck

#options for move to play the card game
MENU ='''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    TT s d: Move card from end of Tableau pile s to end of pile d.
    TF s d: Move card from end of Tableau pile s to Foundation d.
    WT d: Move card from Waste to Tableau pile d.
    WF d: Move card from Waste to Foundation pile d.
    SW : Move card from Stock to Waste.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''
def initialize():
    '''This function is used to create foundation: list of 4 empty list, waste: a single card which is displayed, tableau: list of multiple column lists in which 28 cards are added and last card of each column is displayed and stock: left over cards. All these 4 data structures are returned '''
    foundation = [[], [], [], []]
    tableau = [[], [], [], [], [], [], []]
    waste = []
    stock = Deck()
    stock.shuffle()
    for j in range(7):
        for index, column in enumerate(tableau[j:]):
            new_card = stock.deal()
            if j != index+j:
                new_card.flip_card()
            column.append(new_card)      
    waste.append(stock.deal())
    return tableau, stock, foundation, waste
    
def display(tableau, stock, foundation, waste):
    """ display the game setup """
    stock_top_card = "empty"
    found_top_cards = ["empty","empty","empty","empty"]
    waste_top_card = "empty"
    if len(waste):
        waste_top_card = waste[-1] 
    if len(stock):
        stock_top_card = "XX" #stock[-1]
    for i in range(4):
        if len(foundation[i]):
            found_top_cards[i] = foundation[i][-1]
    print()
    print("{:5s} {:5s} \t\t\t\t\t {}".format("stock","waste","foundation"))
    print("\t\t\t\t     ",end = '')
    for i in range(4):
        print(" {:5d} ".format(i+1),end = '')
    print()
    print("{:5s} {:5s} \t\t\t\t".format(str(stock_top_card), str(waste_top_card)), end = "")
    for i in found_top_cards:
        print(" {:5s} ".format(str(i)), end = "")
    print()
    print()
    print()
    print()
    print("\t\t\t\t\t{}".format("tableau"))
    print("\t\t ", end = '')
    for i in range(7):
        print(" {:5d} ".format(i+1),end = '')
    print()
    # calculate length of longest tableau column
    max_length = max([len(stack) for stack in tableau])
    for i in range(max_length):
        print("\t\t    ",end = '')
        for tab_list in tableau:
            # print card if it exists, else print blank
            try:
                print(" {:5s} ".format(str(tab_list[i])), end = '')
            except IndexError:
                print(" {:5s} ".format(''), end = '')
        print()
    print()
    

def stock_to_waste( stock, waste ):
    '''This function takes stock and waste as parameters and returns False is stock is empty and returns true if the card is moved to waste from stock successfully'''
    if stock.is_empty():
        return False
    elif not waste.append(stock.deal()):
        return True
    
    
       
def waste_to_tableau( waste, tableau, t_num ):
    '''This function takes the card from waste and checks if it has exact 1 less ranking than the tableau's card and different color. If the conditions are fulfilled, the card is moved to tableau or else it returns False value.'''
    last_value = tableau[t_num]
    talon_last = waste[-1]
    if not last_value:
        if talon_last.rank() == 13:
            last_value.append(waste.pop())
            return True
    elif talon_last.suit() in [1,4] and last_value[-1].suit() in [2,3]:
        if talon_last.rank() + 1 == last_value[-1].rank():
            last_value.append(waste.pop())
            return True
    elif last_value[-1].suit() in [1,4] and talon_last.suit() in [2,3]:
        if talon_last.rank() + 1 == last_value[-1].rank():
            last_value.append(waste.pop())
            return True
    return False 

def waste_to_foundation( waste, foundation, f_num ):
    '''This function checks the card from waste and if its Ace, it is moved to the foundation if the list is empty, or else it checks it the card belongs to the same suit and has exactly 1 less rank before moving it to foundation. Else, False is returned'''
    foundation_value = foundation[f_num]
    talon_last = waste[-1]
    if not foundation_value:
        if talon_last.rank() == 1: 
            foundation_value.append(waste.pop())
            return True
    elif (talon_last.suit() == foundation_value[-1].suit()) and (talon_last.rank() - 1 == foundation_value[-1].rank()):
        foundation_value.append(waste.pop())
        return True
    return False

def tableau_to_foundation( tableau, foundation, t_num, f_num ):
    '''This function checks the card from tableau and if its Ace, it is moved to the foundation if the list is empty, or else it checks it the card belongs to the same suit and has exactly 1 less rank before moving it to foundation. Else, False is returned'''
    tableau_column = tableau[t_num]
    foundation_column = foundation[f_num]
    if not foundation_column:
        if tableau_column[-1].rank() == 1: 
            foundation_column.append(tableau_column.pop())
            if tableau_column:
                    if tableau_column[-1].is_face_up():
                        pass
                    else:
                        tableau_column[-1].flip_card()
            return True
    elif (tableau_column[-1].suit() == foundation_column[-1].suit()) and (tableau_column[-1].rank() - 1 == foundation_column[-1].rank()):
        foundation_column.append(tableau_column.pop())
        if tableau_column:
                    if tableau_column[-1].is_face_up():
                        pass
                    else:
                        tableau_column[-1].flip_card()
        return True
    return False

def tableau_to_tableau( tableau, t_num1, t_num2 ):
    '''This function takes the card from a column of tabeau and checks if it has exact 1 less ranking than the other column of tableau's last card and different color. If the conditions are fulfilled, the card is moved to tableau or else it returns False value.'''
    tableau_column1 = tableau[t_num1]
    tableau_column2 = tableau[t_num2]
    if tableau_column1:
        if not tableau_column2:
            if tableau_column1[-1].rank() == 13:
                tableau_column2.append(tableau_column1.pop())
                if tableau_column1:
                    if not tableau_column1[-1].is_face_up():
                        tableau_column1[-1].flip_card()
                return True
        else:
            if tableau_column2[-1].suit() in [1,4] and tableau_column1[-1].suit() in [2,3] or tableau_column1[-1].suit() in [1,4] and tableau_column2[-1].suit() in [2,3]:
                if tableau_column2[-1].rank() == tableau_column1[-1].rank() + 1:
                    tableau_column2.append(tableau_column1.pop())
                    if tableau_column1:
                        if not tableau_column1[-1].is_face_up():
                            tableau_column1[-1].flip_card()
                    return True
    return False
    
def check_win (stock, waste, foundation, tableau):
    '''This function checks if waste, stock and tableau are empty and that 4 list of foundation sums up to 52 cards. It returns true when it matches all the given condition and return false if any of them is not matched'''
    length = len(foundation[1])*4
    if length == 52 and not waste and tableau == [[],[],[],[],[],[],[]] and not stock:
        return True
    return False

def parse_option(in_str):
    '''Prompt the user for an option and check that the input has the 
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game        
        '''
    option_list = in_str.strip().split()
    
    opt_char = option_list[0][0].upper()
    
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]
    
    if opt_char == 'S' and len(option_list) == 1:
        if option_list[0].upper() == 'SW':
            return ['SW']
    
    if opt_char == 'W' and len(option_list) == 2:
        if option_list[0].upper() == 'WT' or option_list[0].upper() == 'WF':
            dest = option_list[1] 
            if dest.isdigit():
                dest = int(dest)
                if option_list[0].upper() == 'WT' and (dest < 1 or dest > 7):
                    print("\nError in Destination")
                    return None
                if option_list[0].upper() == 'WF' and (dest < 1 or dest > 4):
                    print("\nError in Destination")
                    return None
                opt_str = option_list[0].strip().upper()
                return [opt_str,dest]
                               
    if opt_char == 'T' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0].strip().upper()
        if opt_str in ['TT','TF']:
            source = int(option_list[1])
            dest = int(option_list[2])
            # check for valid source values
            if opt_str in ['TT','TF'] and (source < 1 or source > 7):
                print("\nError in Source.")
                return None
            #elif opt_str == 'MFT' and (source < 0 or source > 3):
                #print("Error in Source.")
                #return None
            # source values are valid
            # check for valid destination values
            if (opt_str =='TT' and (dest < 1 or dest > 7)) \
                or (opt_str == 'TF' and (dest < 1 or dest > 4)):
                print("\nError in Destination")
                return None
            return [opt_str,source,dest]

    print("\nError in option:", in_str)
    return None   # none of the above

#main() is defined where whole program is run
def main():  
    #calling initialize() function to get game data
    tableau, stock, foundation, waste = initialize()
    #printing the menu of options
    print(MENU)
    while True:
        #calling display() function to display the game data in sequence
        display(tableau, stock, foundation, waste) 
        #prompt user for an input from the options
        answer = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ") 
        #call parse_option to validate the input, and return a list
        option = parse_option(answer)
        #if the option has no value, continue the function
        if option is None:
            continue
        #elif the user inputs TT as initial input, call tableau_to_tableau function to see if the move of cards is possible and continue
        elif option[0] == 'TT':
            if tableau_to_tableau(tableau, option[1] -1 , option[2] -1):
                continue
        #elif the user inputs TF as initial input, call tableau_to_foundation function to see if the move of cards is possible and continue
        elif option[0] == 'TF':
            if tableau_to_foundation(tableau, foundation, option[1] -1, option[2] -1):
                #check if the game is finished, if yes, congratulate the user
                if check_win(stock, waste, foundation, tableau):
                    print("“You won!”")
                    break
                continue
        #elif the user inputs WT as initial input, call waste_to_tableau function to see if the move of cards is possible and continue
        elif option[0] == 'WT':
            if waste_to_tableau(waste, tableau, option[1] -1):
                continue
        #elif the user inputs WF as initial input, call waste_to_foundation function to see if the move of cards is possible and continue
        elif option[0] == 'WF':
            if waste_to_foundation(waste, foundation, option[1] -1):
                #check if the game is finished, if yes, congratulate the user
                if check_win(stock, waste, foundation, tableau):
                    print("“You won!”")
                    break
                continue
        #elif the user inputs SW, check if the stock to waste movement of cards is possible, and continue the loop
        elif option[0] == 'SW':
            if stock_to_waste(stock, waste):
                continue
        #elif the user inputs R, re-initialize the game data and print menu before continuing the loop
        elif option[0] == 'R':
            tableau, stock, foundation, waste = initialize()
            print(MENU)
            continue
        #display the menu of options when the user inputs H
        elif option[0] == 'H':
            print(MENU)
            continue
        #end the program when the user inputs Q
        elif option[0] == 'Q':
            break
        #print error message if the user input was invalid
        print("\nInvalid move!\n")

if __name__ == '__main__':
     main()
