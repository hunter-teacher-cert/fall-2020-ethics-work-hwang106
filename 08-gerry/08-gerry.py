#%%
import random

rows = 6
cols = 3
total_districts = 6

def make_state(rows, cols):
    state = [[0 for x in range(cols)] for y in range(rows)]
    return state

def show_state(state):
    for i in state:
        print(i)

def rand_votes(state):
    for x in range(rows):
        for y in range(cols):
            state[x][y] = random.randint(0,1)

def rand_thirded_votes(state):
    counter = 0
    while counter < ((rows * cols) / 3):
        a = random.randint(0, rows - 1)
        b = random.randint(0, cols - 1)
        if state[a][b] != 1: 
            state[a][b] = 1
            counter += 1

def create_districts(state):
    districts = [[] for y in range(total_districts)] #initializes district list
    remaining_coordinates = [[0,0] for x in range(rows*cols)] #initializes master list of coordinates
    counter = 0
    current_row = 0
    
    #second initialization of a master list of coordinates that have yet to be placed in a district with all coordinates
    for x in range(len(remaining_coordinates)):        
        remaining_coordinates[x][0] = x%cols

    for x in range(len(remaining_coordinates)):
        remaining_coordinates[x][1] = current_row
        counter += 1
        if counter%cols == 0:
            current_row += 1

    #print("This is the initial master list of all coordinates")
    #print(remaining_coordinates)
    #print("\n")
    #function to append a cell to a district's list and remove it from the master remaining list
    def update_cell(district_number, cell): 
        remaining_coordinates.remove(cell)
        districts[district_number].append(cell)  

    #function to generate random coordinates for the first cells of all districts
    def first_district_cell(district_number): 
        rand_coordinate_index = random.randint(0,len(remaining_coordinates)-1)
        rand_coordinate = remaining_coordinates[rand_coordinate_index]
        update_cell(district_number, rand_coordinate)   

    #function to generate list of adjacent cells to existing cells in district
    def check_adjacent(district_number):  
        adjacent_cells = []
        for x in range(len(districts[district_number])):
            if districts[district_number][x] == [0,0]: #upper-left corner condition
                adjacent_cells.extend([[1,0], [0,1]])
            elif districts[district_number][x] == [cols-1,0]: #upper-right corner condition
                adjacent_cells.extend([[cols-2,0], [cols-1,1]])
            elif districts[district_number][x] == [0,rows-1]: #bottom-left corner condition
                adjacent_cells.extend([[1,rows-1],[0,rows-2]])
            elif districts[district_number][x] == [cols-1,rows-1]: #bottom-right corner condition
                adjacent_cells.extend([[cols-1,rows-2],[cols-2,rows-1]])
            elif districts[district_number][x][0] == 0: #left boundary condition
                adjacent_cells.extend([[0, districts[district_number][x][1]+1], 
                [0, districts[district_number][x][1]-1], 
                [1, districts[district_number][x][1]]])
            elif districts[district_number][x][0] == cols-1: #right boundary condition
                adjacent_cells.extend([[cols-1, districts[district_number][x][1]+1], 
                [cols-1, districts[district_number][x][1]-1], 
                [cols-2, districts[district_number][x][1]]])
            elif districts[district_number][x][1] == 0: #upper boundary condition
                adjacent_cells.extend([[districts[district_number][x][0] - 1, 0], 
                [districts[district_number][x][0] + 1, 0],
                [districts[district_number][x][0], 1]])
            elif districts[district_number][x][1] == rows-1: #lower boundary condition
                adjacent_cells.extend([[districts[district_number][x][0] - 1, rows-1], 
                [districts[district_number][x][0] + 1, rows-1],
                [districts[district_number][x][0], rows-2]])
            else: #all other cells would have 4 adjacent cells
                adjacent_cells.extend([[districts[district_number][x][0] - 1, districts[district_number][x][1]], 
                [districts[district_number][x][0] + 1, districts[district_number][x][1]],
                [districts[district_number][x][0], districts[district_number][x][1] + 1],
                [districts[district_number][x][0], districts[district_number][x][1] - 1]])
        return adjacent_cells
              
    
    for x in range(total_districts):
        first_district_cell(x)
    '''
    print("This is the list of remaining coordinates")
    print(remaining_coordinates)
    print("\n")
    '''
    while len(remaining_coordinates) != 0:
        for x in range(total_districts):
            list_of_adjacent = check_adjacent(x)
            list_of_adjacent_remaining = [x for x in list_of_adjacent if x in remaining_coordinates]
            if len(list_of_adjacent_remaining) != 0:
                chosen_adjacent_cell_index = random.randint(0,len(list_of_adjacent_remaining)-1)
                chosen_adjacent_cell = list_of_adjacent_remaining[chosen_adjacent_cell_index]
                update_cell(x, chosen_adjacent_cell)
            '''
            print("This is the list of remaining adjacent cells for District " + str(x+1))
            print(list_of_adjacent_remaining)
            print("\n")
            '''



    #This was for debugging purposes to make sure the check_adjacent function worked
    '''
    for x in range(total_districts):
        list_of_adjacent = check_adjacent(x)
        print("This is the list of adjacent cells for District " + str(x + 1))
        print(list_of_adjacent)    
    '''    

    return districts

def show_districts(districts):
    d = 1
    for i in districts:
        print("District " + str(d))
        print(i)
        d += 1

def count_votes(state, districts):
    vote_tally = []
    for x in range(total_districts):
        current_tally = 0
        for y in range(len(districts[x])):
            if state[districts[x][y][1]][districts[x][y][0]] == 1:
                current_tally += 1
        vote_tally.append(current_tally)
    #print(vote_tally)
    return vote_tally

def count_wins(vote_tally):
    win_num = 0
    for x in range(len(vote_tally)):
        if vote_tally[x]/len(districts[x]) > .5:
            win_num += 1
    #print(win_num)
    return win_num


def check_district_size(districts):
    for x in range(total_districts):
        # Checks to see if district in question has geographically-balanced number of cells
        if len(districts[x]) != (rows * cols)/total_districts:
            return False
    return True



#Main
state_grid = make_state(rows, cols)
#show_state(state_grid)
rand_thirded_votes(state_grid)
#print("\n")
show_state(state_grid)
print("\n")
#Computationally lazy and inefficient way of ensuring equal-sized districts by repeating create_districts algorithm until balanced
num_district_sims = 200
win_tally = [0 for x in range(total_districts + 1)]
for x in range(num_district_sims):
    is_balanced = False
    while not is_balanced:
        districts = create_districts(state_grid)
        is_balanced = check_district_size(districts)
    print("\n")
    show_districts(districts)
    print("\n")
    vote_tally = count_votes(state_grid, districts)
    print("\n")
    num_wins = count_wins(vote_tally)
    win_tally[num_wins] += 1
    print(win_tally)
    win_freq = [y / (x+1) for y in win_tally]
    print(win_freq)

print("\n")
show_state(state_grid)





# %%
