"""
CMPUT 174 Lab 8 'Dungeon4' Program
Full Dungeon Game
Author: Abdullah Faisal
When: November 14, 2022
"""

# import statement and global variables
import copy
MAP_FILE = 'cave_map.txt'
DIRECTIONS_LIST = ['north', 'east', 'south', 'west']


# reads file and creates an array from hard-coded txt file -> returns array
def load_map(map_file: str) -> list[list[str]]:
    
    with open(map_file, 'r') as file:
        dungeon = file.readlines()    
    dungeon_array = []  # empty list for full array values
    section_values = []  # empty list for appending small lists into the array
    for section in dungeon:
        for place in section:
            if place != '\n':
                section_values.append(place)  # adds each place in a dungeon row
        dungeon_array.append(section_values)  # adds each dungeon row into a larger list
        section_values = []  # resets list for new dungeon row
    return dungeon_array


# finds the 'S' position in the dungeon -> returns coordinates
def find_start(grid: list[list[str]]) -> list[int, int]:
    start_position = []
    start_x = 0
    for section in grid:
        try:
            start_y = section.index('S')  # looks for 'S' in dungeon
        except ValueError:
            start_y = -1
        if start_y != -1:
            start_position.append(start_x)  # x-coordinate of 'S' position     
            start_position.append(start_y)  # y-coordinate of 'S' position 
            return start_position
        start_x += 1


# checks for valid/invalid user inputs -> returns valid user input
def get_command() -> str:
    repeat = True
    while repeat == True:
        user_input = input()
        commands = ['escape', 'show map', 'help']
        actions = ['go north', 'go east', 'go south', 'go west']
        if user_input in commands:  # checks if command is valid
            return user_input
        if user_input in actions:  # checks if action is valid
            return user_input[3:]        
        else:
            print('I do not understand.')


# prints map using dungeon_array and replaces signs with emoji symbols
def display_map(grid: list[list[str]], player_position: list[int, int]) -> None:
    new_grid = copy.deepcopy(grid)
    dungeon_symbols = ['🧱', '🟢', '🏠', '🏺', '🧝']
    dungeon_signs = ['-', '*', 'S', 'F', '@']
    row = player_position[0]
    col = player_position[1]
    new_grid[row][col] = '@'  # replaces symbol at player position with '@'
    for section in new_grid:
        for place in section:
            sign_location = dungeon_signs.index(place)
            print(dungeon_symbols[sign_location], end="")  # creates consistent spacing between grid characters and keeps them aligned
        print('\n', end="")  # moves next row of dungeon symbols to be printed on the next line


# determines size of dungeon grid -> returns size in form of list
def get_grid_size(grid: list[list[str]]) -> list[int, int]:
    grid_size = []
    grid_size.append(len(grid))
    grid_size.append(len(grid[0]))
    return grid_size


# determines if an inputted position falls within the dungeon grid -> returns true or false
def is_inside_grid(grid: list[list[str]], position: list[int, int]) -> bool:
    grid_rows, grid_cols = get_grid_size(grid)
    grid_rows, grid_cols = [grid_rows - 1, grid_cols - 1]  # adjusts grid size list to start from 0 instead of 1
    current_row, current_col = position  # current position coordinates
    if 0 <= current_row <= grid_rows and 0 <= current_col <= grid_cols:
        return True
    else:
        return False


# determines which directions the user can move -> returns list of directions
def look_around(grid: list[list[str]], player_position: list[int, int]) -> list:
    allowed_objects = ('S', 'F', '*')
    row = player_position[0]
    col = player_position[1]
    directions = []
    if is_inside_grid(grid, [row - 1, col]) and grid[row - 1][col] in allowed_objects:  # checks if a move is possible (if yes, it appends the move to the directions list)
        directions.append('north')
    if is_inside_grid(grid, [row + 1, col]) and grid[row + 1][col] in allowed_objects:
        directions.append('south')
    if is_inside_grid(grid, [row, col + 1]) and grid[row][col + 1] in allowed_objects:
        directions.append('east')
    if is_inside_grid(grid, [row, col - 1]) and grid[row][col - 1] in allowed_objects:
        directions.append('west')
    return directions


# contains lists used to alter the current position depending or which direction the user moves -> returns corresponding list
def change_position (direction: str) -> list:
    if direction == 'north':
        return [-1, 0]
    elif direction == 'east':
        return [0, 1]        
    elif direction == 'south':
        return [1, 0]        
    else:
        return [0, -1]


# checks if new position is valid and updates player's current_position -> returns true or false
def move(direction: str, player_position: list[int, int], grid: list[list[str]]) -> bool:
    move_options = look_around(grid, player_position)
    for option in move_options:
        if option == direction:
            print('You moved ' + direction + '.')
            new_position = change_position(direction)
            altered_position = [player_position[0] + new_position[0], player_position[1] + new_position[1]]  # updates current coordinates to reflect where the player moved
            player_position.clear()
            player_position.extend(altered_position)  # replaces old coordiates with new coordinates 
            return True
    else:
        print('There is no way there.')
        return False


# checks whether player has reached the 'F' position or not -> returns true or false
def check_finish(grid: list[list[str]], player_position: list[int, int]) -> bool:
    finish_position = []
    finish_x = 0
    for section in grid:
        try:
            finish_y = section.index('F')
        except ValueError:
            finish_y = -1
        if finish_y != -1:
            finish_position.append(finish_x)  # x-coordinate of 'F' position   
            finish_position.append(finish_y)  # y-coordinate of 'F' position   
            if finish_position == player_position:
                print('Congratulations! You have reached the exit!')
                return True
            else: return False
        finish_x += 1


# reads and prints the help.txt file to show game commands
def display_help() -> None:  
    with open('help.txt', 'r') as file:
        print (file.read())


# calls all functions in order to run the dungeon game
def main():
    directions = []
    dungeon_map = load_map(MAP_FILE)
    command = ''
    current_position = find_start(dungeon_map)
    while command != 'escape':
        directions = look_around(dungeon_map, current_position)
        print('You can go', ', '.join(directions))
        command = get_command()
        if command == 'show map':
            display_map(dungeon_map, current_position)
        if command in DIRECTIONS_LIST:
            moveable = move(command, current_position, dungeon_map)
        if command == 'help':
            display_help()
        finish = check_finish(dungeon_map, current_position)
        if finish == True:
            command = 'escape'


if __name__ == '__main__':
    main()