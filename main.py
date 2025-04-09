import random
import numpy as np

territories = {}
board = None
hands = None

def create_territory(pos_1,pos_2,pos_3,pos_4,pos_5,pos_6):
    territory = [pos_1,pos_2,pos_3,pos_4,pos_5,pos_6]
    return territory

def create_territories(num_players):
    global territories
    territories.clear()
    if num_players == 2 or num_players ==4:
        territories["territory_0"] = create_territory(1, 2, 3, 4, 5, 6)
        territories["territory_1"] = create_territory(9, 8, 7, 6, 5, 4)
        if num_players == 4:
            territories["territory_2"] = create_territory(4, 7, 2, 9, 5, 1)
            territories["territory_3"] = create_territory(6, 3, 8, 1, 5, 9)
    else:
        raise ValueError("Invalid number of players")

    return territories

def create_hand():
    return np.zeros(6, dtype=int)

def create_hands(num_players):
    global hands
    hands = [create_hand() for player in range(num_players)]
    return hands     

def initialize_board(num_players):
    global board
    
    board = np.array(
        [[random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)], 
        [random.randint(1,6), random.randint(1,6),random.randint(1,6),random.randint(1,6)]]
    )
    
    create_territories(num_players)
    create_hands(num_players)
    return board

#check how tall a die stack
def get_stack_height(stack):
    level = 3
    while level >= 0:
        if board[stack][level] !=0:
            break
        level -= 1
    return level

def is_in_territory(stack,  player_num):
    key = "territory_"+str(player_num)
    if stack in territories[key]:
        return True
    return False

def merge_die(stack_1, stack_2, player_num):
    is_in_territory(stack_1, player_num)
    is_in_territory(stack_2, player_num)
    if not is_in_territory(stack_1, player_num) or not is_in_territory(stack_2, player_num):
        print(f"Player {player_num} cannot merge dice that are not in their territory.")
        return
    global board, hands
    # check how tall each die stack is to retrieve correct board value
    stack_height_1 = get_stack_height(stack_1)
    stack_height_2 = get_stack_height(stack_2)

    die1_value = board[stack_1][stack_height_1]
    die2_value = board[stack_2][stack_height_2]
    merged_value = die1_value + die2_value

    empty_slot = -1
    for i in range(6):
        if hands[player_num][i] == 0:
            empty_slot = i
            break

    if empty_slot == -1:
        print(f"Player {player_num}'s hand is full! Cannot add more dice.")
        return
    
    if merged_value <= 6:
        hands[player_num][empty_slot] = merged_value
    elif merged_value > 6 and merged_value < 12:
        hands[player_num][empty_slot] = merged_value % 6
    else:
        hands[player_num][empty_slot] = 6

    # remove second die from board, leave the first. needs changed if we do discard pile
    board[stack_2][stack_height_2] = 0


def roll_die(stack, player_num):
    is_in_territory(stack, player_num)
    if not is_in_territory(stack, player_num):
        print(f"Player {player_num} cannot roll dice that are not in their territory.")
        return

    global board

    level = get_stack_height(stack)
    board[stack][level] = random.randint(1,6)



def play_game(num_players):
    board = initialize_board(num_players)

    print("board starting state:")
    print(board)
    print("hands starting state:")
    print(hands)
    print("player territories:")
    print(territories)

    game_over = False
    
    while not game_over:
        for player in range(num_players):
            print(f"\nPlayer {player}'s turn:")
            player_choice = input(f"Player {player}, merge or roll? ").lower()
            
            if player_choice == "merge":
                stack_1 = int(input(f"Player {player}, enter die stack position 1 (0-8): "))
                stack_2 = int(input(f"Player {player}, enter die stack position 2 (0-8): "))
                
                if 0 <= stack_1 < 9 and 0 <= stack_2 < 9:
                    merge_die(stack_1, stack_2, player)
                    print("Board new state:")
                    print(board)
                    print("Hands new state:")
                    print(hands)
                else:
                    print("Invalid stack positions. Please enter values between 0 and 8.")
                    
            elif player_choice == "roll":
                stack = int(input(f"Player {player}, enter die stack position (0-8): "))
                
                if 0 <= stack < 9:
                    roll_die(stack, player)
                    print("Board new state:")
                    print(board)
                    print("Hands new state:")
                    print(hands)
                else:
                    print("Invalid stack position. Please enter a value between 0 and 8.")
                    
            elif player_choice == "quit":
                game_over = True
                break
                
            else:
                print("Invalid choice. Please enter 'merge', 'roll', or 'quit'.")

if __name__ == "__main__":
    try:
        num_players = int(input("Enter number of players (2 or 4): "))
        if num_players not in [2, 4]:
            print("Only 2 or 4 players are supported.")
        else:
            play_game(num_players)
    except ValueError:
        print("Please enter a valid number.")