import copy
import math
import random
from heapq import heappush, heappop


def main():
    run_part01a = True
    run_part01b = True

    if (run_part01a):
        input_filename = 'pathfinding_a.txt'
        output_filename = 'pathfinding_a_out.txt'
        total_reader(input_filename, output_filename)
    
    if (run_part01b):
        input_filename = 'pathfinding_b.txt'
        output_filename = 'pathfinding_b_out.txt'
        total_reader(input_filename, output_filename)


def total_reader(input_file, output_file):
    with open(input_file) as file:
        single_grid = []
        for line in file:
            if (not((line == '\n' or line == ''))):
                a_line = line.split()
                a_list_first = a_line[0]
                the_chars = list(a_list_first)
                single_grid.append(the_chars)
            if (line == '\n' or line == ''):
                s_loc = target_finder(single_grid, 'S')
                g_loc = target_finder(single_grid, 'G')
                return_grid_greedy = greedy_a(single_grid, s_loc, g_loc)
                return_grid_a_star = a_star_a(single_grid, s_loc, g_loc)
                writer(output_file, 'Greedy', return_grid_greedy, 'A*', return_grid_a_star)
                single_grid = []
        s_loc = target_finder(single_grid, 'S')
        g_loc = target_finder(single_grid, 'G')
        return_grid_greedy = greedy_a(single_grid, s_loc, g_loc)
        return_grid_a_star = a_star_a(single_grid, s_loc, g_loc)
        writer(output_file, 'Greedy', return_grid_greedy, 'A*', return_grid_a_star)
        single_grid = []


def reader(filename):
    return_grid = []
    with open(filename) as f:
        for i in f.readlines():
            a_line = i.split()
            a_list_first = a_line[0]
            the_chars = list(a_list_first)
            return_grid.append(the_chars)
    return return_grid
    

def writer(filename, grid1_name, grid1, grid2_name, grid2):
    with open(filename, 'a+') as f:
        f.write(grid1_name + '\n')
        for i in grid1:
            f.write(''.join(i) + '\n')
        f.write(grid2_name + '\n')
        for j in grid2:
            f.write(''.join(j) + '\n')
        f.write('\n')


def target_finder(grid, target):
    location = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] == target):
                location.append(i)
                location.append(j)
    return location


# Will be used to find the h values for up down left right searches
# a - x/y of current
# b - x/y of goal
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Will be used to find the h values for up down left right and diagonals
def cheb(a, b):

    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def print_matrix(matrix):
    print("\n")
    for x in matrix:
        print(x)


def a_star_b(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    came_from = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]
    cost = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]

    cost[s_loc[0]][s_loc[1]] = 0

    curr_loc = None
    foundGoal = False
    visited = []

    heappush(visited, (cheb(s_loc, g_loc), s_loc))

    # Find the goal
    while(not(foundGoal)):
        curr_node = heappop(visited)
        curr_loc = curr_node[1]

        if (a_grid[curr_loc[0]][curr_loc[1]] == 'G'):
            foundGoal = True

        if(not(foundGoal)):
            # Left
            if (curr_loc[1] - 1 >= 0):
                if (a_grid[curr_loc[0]][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]

                    if(cost[curr_loc[0]][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] - 1]):
                        cost[curr_loc[0]][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0], curr_loc[1] - 1], g_loc), [curr_loc[0], curr_loc[1] - 1]))

            # Right
            if(curr_loc[1] + 1 < len(a_grid[0])):
                if (a_grid[curr_loc[0]][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]

                    if (cost[curr_loc[0]][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] + 1]):
                        cost[curr_loc[0]][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] + 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0], curr_loc[1] + 1], g_loc), [curr_loc[0], curr_loc[1] + 1]))
           
            #Up
            if (curr_loc[0] - 1 >= 0):
                if (a_grid[curr_loc[0] - 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]

                    if (cost[curr_loc[0] - 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1]]):
                        cost[curr_loc[0] - 1][curr_loc[1]] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1]] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] - 1, curr_loc[1]], g_loc), [curr_loc[0] - 1, curr_loc[1]]))

            #Down
            if (curr_loc[0] + 1 < len(a_grid)):
                if (a_grid[curr_loc[0] + 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if (cost[curr_loc[0] + 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1]]):
                        cost[curr_loc[0] + 1][curr_loc[1]] = cost_so_far + 1
                        came_from[curr_loc[0] + 1][curr_loc[1]] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] + 1, curr_loc[1]], g_loc), [curr_loc[0] + 1, curr_loc[1]]))

            #Up Left
            if (curr_loc[0] - 1 >= 0 and curr_loc[1] - 1 >= 0):
                if (a_grid[curr_loc[0] - 1][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if (cost[curr_loc[0] - 1][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1] - 1]):
                        cost[curr_loc[0] - 1][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] - 1, curr_loc[1] - 1], g_loc), [curr_loc[0] - 1, curr_loc[1] - 1]))

            # Up Right
            if(curr_loc[0] - 1 and curr_loc[1] + 1 < len(a_grid[0])):
                if(a_grid[curr_loc[0] - 1][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] - 1][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1] + 1]):
                        cost[curr_loc[0] - 1][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1] + 1] = [curr_loc[0] - 1, curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] - 1, curr_loc[1] + 1], g_loc), [curr_loc[0] - 1, curr_loc[1] + 1]))
           
            # Down Left
            if (curr_loc[0] + 1 < len(a_grid) and curr_loc[1] - 1 >= 0):
                if (a_grid[curr_loc[0] + 1][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if (cost[curr_loc[0] + 1][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1] - 1]):
                        cost[curr_loc[0] + 1][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0] + 1][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] + 1, curr_loc[1] - 1], g_loc), [curr_loc[0] + 1, curr_loc[1] - 1]))

            # Down Right
            if(curr_loc[0] + 1 < len(a_grid) and curr_loc[1] + 1 < len(a_grid[0])):
                if(a_grid[curr_loc[0] + 1][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]

                    if (cost[curr_loc[0] + 1][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1] + 1]):
                        cost[curr_loc[0] + 1][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0] + 1][curr_loc[1] + 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] + 1, curr_loc[1] + 1], g_loc), [curr_loc[0] + 1, curr_loc[1] + 1]))

    while (came_from[curr_loc[0]][curr_loc[1]] != None):
        curr_loc = came_from[curr_loc[0]][curr_loc[1]]
        if (a_grid[curr_loc[0]][curr_loc[1]] != 'S'):
            a_grid[curr_loc[0]][curr_loc[1]] = 'P'

    return a_grid


def a_star_a(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    came_from = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]
    cost = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]

    cost[s_loc[0]][s_loc[1]] = 0

    curr_loc = None
    foundGoal = False
    visited = []

    heappush(visited, (manhattan(s_loc, g_loc), s_loc))

    # Find the goal
    while(not(foundGoal)):
        curr_node = heappop(visited)
        curr_loc = curr_node[1]

        if(a_grid[curr_loc[0]][curr_loc[1]] == 'G'):
            foundGoal = True

        if(not(foundGoal)):
            # Left
            if (curr_loc[1] - 1 >= 0):
                if (a_grid[curr_loc[0]][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if (cost[curr_loc[0]][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] - 1]):
                        cost[curr_loc[0]][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + manhattan([curr_loc[0], curr_loc[1] - 1], g_loc), [curr_loc[0], curr_loc[1] - 1]))
            # Right
            if (curr_loc[1] + 1 < len(a_grid[0])):
                if (a_grid[curr_loc[0]][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]

                    if (cost[curr_loc[0]][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] + 1]):
                        cost[curr_loc[0]][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] + 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + manhattan([curr_loc[0], curr_loc[1] + 1], g_loc), [curr_loc[0], curr_loc[1] + 1]))
           
            # Up
            if (curr_loc[0] - 1 >= 0):
                if (a_grid[curr_loc[0] - 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]

                    if (cost[curr_loc[0] - 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1]]):
                        cost[curr_loc[0] - 1][curr_loc[1]] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1]] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + manhattan([curr_loc[0] - 1, curr_loc[1]], g_loc), [curr_loc[0] - 1, curr_loc[1]]))

            # Down
            if (curr_loc[0] + 1 < len(a_grid)):
                if (a_grid[curr_loc[0] + 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]

                    if (cost[curr_loc[0] + 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1]]):
                        cost[curr_loc[0] + 1][curr_loc[1]] = cost_so_far + 1
                        came_from[curr_loc[0] + 1][curr_loc[1]] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + manhattan([curr_loc[0] + 1, curr_loc[1]], g_loc), [curr_loc[0] + 1, curr_loc[1]]))

    while(came_from[curr_loc[0]][curr_loc[1]] != None):
        curr_loc = came_from[curr_loc[0]][curr_loc[1]]
        if(a_grid[curr_loc[0]][curr_loc[1]] != 'S'):
            a_grid[curr_loc[0]][curr_loc[1]] = 'P'

    return a_grid

# uses manhattan distance (up down left right solution)
def greedy_a(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    curr_loc = copy.deepcopy(s_loc)
    prev_dir = "None"
    stuck = False
    while (not(stuck)):
        for x in a_grid:
            left_dist = math.inf
            right_dist = math.inf
            up_dist = math.inf
            down_dist = math.inf
            # Left distance
            if ((curr_loc[1] - 1) >= 0):
                if (a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                    return a_grid
                if (a_grid[curr_loc[0]][curr_loc[1] - 1] == '_'):
                    left_dist = manhattan([curr_loc[0],(curr_loc[1]-1)],g_loc)
            # Right distance
            if ((curr_loc[1] + 1) < len(a_grid[0])):
                if (a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                    return a_grid
                if (a_grid[curr_loc[0]][curr_loc[1] + 1] == '_'):
                    right_dist = manhattan([curr_loc[0],(curr_loc[1]+1)],g_loc)
            # Up distance
            if ((curr_loc[0] - 1) >= 0):
                if(a_grid[(curr_loc[0]-1)][curr_loc[1]] == 'G'):
                    return a_grid
                if(a_grid[(curr_loc[0]-1)][curr_loc[1]] == '_'):
                    up_dist = manhattan([(curr_loc[0]-1),curr_loc[1]],g_loc)
            # Down distance
            if ((curr_loc[0] + 1) < len(a_grid)):
                if (a_grid[(curr_loc[0]+1)][curr_loc[1]] == 'G'):
                    return a_grid
                if (a_grid[(curr_loc[0]+1)][curr_loc[1]] == '_'):
                    down_dist = manhattan([(curr_loc[0]+1),curr_loc[1]],g_loc) #(g_loc[0] - (curr_loc[0]+1)) + (g_loc[1] - curr_loc[1])

            if (left_dist == math.inf and right_dist == math.inf and up_dist == math.inf and down_dist == math.inf):
                stuck = True
                return False

            if (not(stuck)):
                min_index = randomMinIndex([up_dist, down_dist, left_dist, right_dist])#min(up_dist, down_dist, left_dist, right_dist)
                if (prev_dir == "Down" and min_index == 0):
                    return False 
                if (prev_dir == "Up" and min_index == 1):
                    return False 
                if (prev_dir == "Right" and min_index == 2):
                    return False 
                if (prev_dir == "Left" and min_index == 3):
                    return False 

                if (min_index == 2):
                    if (prev_dir == "Right"):
                        return False
                    prev_dir = "Left"
                    curr_loc[1] -= 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 3):
                    if (prev_dir == "Left"):
                        return False
                    prev_dir = "Right"
                    curr_loc[1] += 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 0):
                    if (prev_dir == "Down"):
                        return False
                    prev_dir = "Up"
                    curr_loc[0] -= 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 1):
                    if (prev_dir == "Up"):
                        return False
                    prev_dir = "Down"
                    curr_loc[0] += 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'

# uses cheb distance (up down left right diagonal solution)
def greedy_b(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    curr_loc = copy.deepcopy(s_loc)
    prev_dir = "None"
    stuck = False
    while (not(stuck)):
        for x in a_grid:
            left_dist = math.inf
            right_dist = math.inf
            up_dist = math.inf
            down_dist = math.inf
            up_right_dist = math.inf
            up_left_dist = math.inf
            down_right_dist = math.inf
            down_left_dist = math.inf
            # Get the H values for all the directions.
            # Left distance
            if ((curr_loc[1] - 1) >= 0):
                if(a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                    return a_grid
                if(a_grid[curr_loc[0]][curr_loc[1] - 1] == '_'):
                    left_dist = cheb([curr_loc[0],(curr_loc[1]-1)],g_loc)
            # Right distance
            if ((curr_loc[1] + 1) < len(a_grid[0])):
                if(a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                    return a_grid
                if(a_grid[curr_loc[0]][curr_loc[1] + 1] == '_'):
                    right_dist = cheb([curr_loc[0],(curr_loc[1]+1)],g_loc)
            # Up distance
            if ((curr_loc[0] - 1) >= 0):
                if (a_grid[(curr_loc[0]-1)][curr_loc[1]] == 'G'):
                    return a_grid
                if (a_grid[(curr_loc[0]+1)][curr_loc[1]] == '_'):
                    up_dist = cheb([(curr_loc[0]-1),curr_loc[1]],g_loc)
            # Down distance
            if ((curr_loc[0] + 1) < len(a_grid)):
                if (a_grid[(curr_loc[0]+1)][curr_loc[1]] == 'G'):
                    return a_grid
                if (a_grid[(curr_loc[0]+1)][curr_loc[1]] == '_'):
                    down_dist = cheb([(curr_loc[0]+1),curr_loc[1]],g_loc)
            #Up + Right (diagonal)
            if (((curr_loc[0] - 1) >= 0) and ((curr_loc[1] + 1) < len(a_grid[0]))):
            #                       up          right
                if (a_grid[curr_loc[0]-1][curr_loc[1]+1] == 'G'):
                    return a_grid
            #                       up          right   
                if (a_grid[curr_loc[0]-1][curr_loc[1]+1] == '_'):
                    up_right_dist = cheb([(curr_loc[0]-1),(curr_loc[1]+1)],g_loc)
            #Up + Left (diagonal)
            if (((curr_loc[0] - 1) >= 0) and ((curr_loc[1] - 1) < len(a_grid[0]))):
            #                       up          Left
                if (a_grid[curr_loc[0]-1][curr_loc[1]-1] == 'G'):
                    return a_grid
            #                       up          Left   
                if (a_grid[curr_loc[0]-1][curr_loc[1]-1] == '_'):
                    up_left_dist = cheb([(curr_loc[0]-1),(curr_loc[1]-1)],g_loc)
            #Down + Right (diagonal)
            if (((curr_loc[0] + 1) >= 0) and ((curr_loc[1] + 1) < len(a_grid[0]))):
            #                       Down          right
                if (a_grid[curr_loc[0]+1][curr_loc[1]+1] == 'G'):
                    return a_grid
            #                       Down          right   
                if (a_grid[curr_loc[0]+1][curr_loc[1]+1] == '_'):
                    down_right_dist = cheb([(curr_loc[0]+1),(curr_loc[1]+1)],g_loc)
            #Down + Left (diagonal)
            if (((curr_loc[0] + 1) >= 0) and ((curr_loc[1] - 1) < len(a_grid[0]))):
            #                       Down          Left
                if (a_grid[curr_loc[0]+1][curr_loc[1]-1] == 'G'):
                    return a_grid
            #                       Down          Left   
                if (a_grid[curr_loc[0]+1][curr_loc[1]-1] == '_'):
                    down_left_dist = cheb([(curr_loc[0]+1),(curr_loc[1]-1)],g_loc)

            if (left_dist == math.inf and right_dist == math.inf and up_dist == math.inf and down_dist == math.inf):
                stuck = True
                return False

            if (not(stuck)):
                min_index = randomMinIndex([up_dist, down_dist, left_dist, right_dist, up_right_dist, up_left_dist, down_right_dist, down_left_dist])
                if (prev_dir == "Down" and min_index == 0):
                    return False 
                if (prev_dir == "Up" and min_index == 1):
                    return False 
                if (prev_dir == "Right" and min_index == 2):
                    return False 
                if (prev_dir == "Left" and min_index == 3):
                    return False 

                #Diagonal Directions
                if (min_index == 4):
                    curr_loc[0] -= 1
                    curr_loc[1] += 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 5):
                    curr_loc[0] -= 1
                    curr_loc[1] -= 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 6):
                    curr_loc[0] += 1
                    curr_loc[1] += 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 7):
                    curr_loc[0] += 1
                    curr_loc[1] -= 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'

                #Cardinal Directions
                elif (min_index == 2):
                    curr_loc[1] -= 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 3):
                    curr_loc[1] += 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 0):
                    curr_loc[0] -= 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                elif (min_index == 1):
                    curr_loc[0] += 1
                    a_grid[curr_loc[0]][curr_loc[1]] = 'P'

def randomMinIndex(array):
    minValue = min(array)
    minIndices = []

    for i in range(len(array)):
        if(array[i] == minValue):
            minIndices.append(i)
            
    return minIndices[random.randint(0,len(minIndices) - 1)]

main()
