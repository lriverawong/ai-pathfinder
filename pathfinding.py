import re
import copy
import math
import random
from heapq import heappush, heappop

def main():
    print('=========== START ===========')
    
    ####################################
    # Part 1
    #####################################
    # filename = 'pathfinding_a.txt'
    # grid = reader(filename)
    # output_filename = 'output.txt'

    # s_loc = target_finder(grid, 'S')
    # print("Starting location: ", s_loc)
    # g_loc = target_finder(grid, 'G')
    # print("Goal location: ", g_loc)

    # return_grid = a_star_b(grid, s_loc, g_loc)
    # #print(return_grid)
    # writer(output_filename, return_grid)
    #####################################

    # Part 2
    alphabeta()
    return_grid = greedy_b(grid, s_loc, g_loc)
    #print(return_grid)
    writer(output_filename, return_grid)

    print('=========== END ============')
    

def reader(filename):
    return_grid = []
    with open(filename) as f:
        # grid_data = [i.split() for i in f.readlines()]
        for i in f.readlines():
            a_line = i.split()
            a_list_first = a_line[0]
            the_chars = list(a_list_first)
            return_grid.append(the_chars)
            # print(the_chars)
    return return_grid
    

def writer(filename, grid):
    with open(filename, 'w+') as f:
        # f.write(grid_data2)
        for i in grid:
            f.write(''.join(i) + '\n')

def target_finder(grid, target):
    location = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] == target):
                location.append(i)
                location.append(j)
    return location

#Will be used to find the h values for up down left right searches
#a - x/y of current
#b - x/y of goal
def manhattan(a, b):
    return abs( a[0] - b[0] ) + abs( a[1] - b[1] )

#Will be used to find the h values for up down left right and diagonals
def cheb(a, b):
    return max( abs( a[0] - b[0] ), abs( a[1] - b[1] ) )

def printMatrix(matrix):
    print("\n")
    for x in matrix:
        print(x)

def a_star_b(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    came_from = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]
    cost = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]

    cost[s_loc[0]][s_loc[1]] = 0

    curr_loc = None #copy.deepcopy(s_loc)
    foundGoal = False
    visited = []

    heappush(visited, (cheb(s_loc, g_loc), s_loc))

    #Find the goal
    while(not(foundGoal)):
        curr_node = heappop(visited)
        curr_loc = curr_node[1]

        if(a_grid[curr_loc[0]][curr_loc[1]] == 'G'):
            foundGoal = True

        if(not(foundGoal)):
            #Left
            if(curr_loc[1] - 1 >= 0):
                if(a_grid[curr_loc[0]][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0]][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] - 1]):
                        cost[curr_loc[0]][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0], curr_loc[1] - 1], g_loc), [curr_loc[0], curr_loc[1] - 1]))

            #Right
            if(curr_loc[1] + 1 < len(a_grid[0])):
                if(a_grid[curr_loc[0]][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0]][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] + 1]):
                        cost[curr_loc[0]][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] + 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0], curr_loc[1] + 1], g_loc), [curr_loc[0], curr_loc[1] + 1]))
           
            #Up
            if(curr_loc[0] - 1 >= 0):
                if(a_grid[curr_loc[0] - 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] - 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1]]):
                        cost[curr_loc[0] - 1][curr_loc[1]] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1]] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] - 1, curr_loc[1]], g_loc), [curr_loc[0] - 1, curr_loc[1]]))

            #Down
            if(curr_loc[0] + 1 < len(a_grid)):
                if(a_grid[curr_loc[0] + 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] + 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1]]):
                        cost[curr_loc[0] + 1][curr_loc[1]] = cost_so_far + 1
                        came_from[curr_loc[0] + 1][curr_loc[1]] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] + 1, curr_loc[1]], g_loc), [curr_loc[0] + 1, curr_loc[1]]))

            #Up Left
            if(curr_loc[0] - 1 >= 0 and curr_loc[1] - 1 >= 0):
                if(a_grid[curr_loc[0] - 1][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] - 1][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1] - 1]):
                        cost[curr_loc[0] - 1][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] - 1, curr_loc[1] - 1], g_loc), [curr_loc[0] - 1, curr_loc[1] - 1]))

            #Up Right
            if(curr_loc[0] - 1 and curr_loc[1] + 1 < len(a_grid[0])):
                if(a_grid[curr_loc[0] - 1][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] - 1][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1] + 1]):
                        cost[curr_loc[0] - 1][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1] + 1] = [curr_loc[0] - 1, curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] - 1, curr_loc[1] + 1], g_loc), [curr_loc[0] - 1, curr_loc[1] + 1]))
           
            #Down Left
            if(curr_loc[0] + 1 < len(a_grid) and curr_loc[1] - 1 >= 0):
                if(a_grid[curr_loc[0] + 1][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] + 1][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1] - 1]):
                        cost[curr_loc[0] + 1][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0] + 1][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] + 1, curr_loc[1] - 1], g_loc), [curr_loc[0] + 1, curr_loc[1] - 1]))

            #Down Right
            if(curr_loc[0] + 1 < len(a_grid) and curr_loc[1] + 1 < len(a_grid[0])):
                if(a_grid[curr_loc[0] + 1][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] + 1][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1] + 1]):
                        cost[curr_loc[0] + 1][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0] + 1][curr_loc[1] + 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + cheb([curr_loc[0] + 1, curr_loc[1] + 1], g_loc), [curr_loc[0] + 1, curr_loc[1] + 1]))

    while(came_from[curr_loc[0]][curr_loc[1]] != None):
        curr_loc = came_from[curr_loc[0]][curr_loc[1]]
        if(a_grid[curr_loc[0]][curr_loc[1]] != 'S'):
            a_grid[curr_loc[0]][curr_loc[1]] = 'P'

    return a_grid

def a_star_a(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    came_from = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]
    cost = [[None for j in range(len(a_grid[0]))] for i in range(len(a_grid))]

    cost[s_loc[0]][s_loc[1]] = 0

    curr_loc = None #copy.deepcopy(s_loc)
    foundGoal = False
    visited = []

    heappush(visited, (manhattan(s_loc, g_loc), s_loc))

    #Find the goal
    while(not(foundGoal)):
        curr_node = heappop(visited)
        curr_loc = curr_node[1]

        if(a_grid[curr_loc[0]][curr_loc[1]] == 'G'):
            foundGoal = True

        if(not(foundGoal)):
            #Left
            if(curr_loc[1] - 1 >= 0):
                if(a_grid[curr_loc[0]][curr_loc[1] - 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0]][curr_loc[1] - 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] - 1]):
                        cost[curr_loc[0]][curr_loc[1] - 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] - 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + manhattan([curr_loc[0], curr_loc[1] - 1], g_loc), [curr_loc[0], curr_loc[1] - 1]))

            #Right
            if(curr_loc[1] + 1 < len(a_grid[0])):
                if(a_grid[curr_loc[0]][curr_loc[1] + 1] == '_' or a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0]][curr_loc[1] + 1] == None  or cost_so_far + 1 < cost[curr_loc[0]][curr_loc[1] + 1]):
                        cost[curr_loc[0]][curr_loc[1] + 1] = cost_so_far + 1
                        came_from[curr_loc[0]][curr_loc[1] + 1] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + manhattan([curr_loc[0], curr_loc[1] + 1], g_loc), [curr_loc[0], curr_loc[1] + 1]))
           
            #Up
            if(curr_loc[0] - 1 >= 0):
                if(a_grid[curr_loc[0] - 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] - 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] - 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] - 1][curr_loc[1]]):
                        cost[curr_loc[0] - 1][curr_loc[1]] = cost_so_far + 1
                        came_from[curr_loc[0] - 1][curr_loc[1]] = [curr_loc[0], curr_loc[1]]
                        heappush(visited, (cost_so_far + 1 + manhattan([curr_loc[0] - 1, curr_loc[1]], g_loc), [curr_loc[0] - 1, curr_loc[1]]))

            #Down
            if(curr_loc[0] + 1 < len(a_grid)):
                if(a_grid[curr_loc[0] + 1][curr_loc[1]] == '_' or a_grid[curr_loc[0] + 1][curr_loc[1]] == 'G'):
                    cost_so_far = cost[curr_loc[0]][curr_loc[1]]


                    if(cost[curr_loc[0] + 1][curr_loc[1]] == None  or cost_so_far + 1 < cost[curr_loc[0] + 1][curr_loc[1]]):
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
        print("\n")
        for x in a_grid:
            print(''.join(x))
        left_dist = math.inf
        right_dist = math.inf
        up_dist = math.inf
        down_dist = math.inf
        # Left distance
        if ((curr_loc[1] - 1) >= 0):
            if(a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                return a_grid
            if(a_grid[curr_loc[0]][curr_loc[1] - 1] == '_'):
                left_dist = manhattan([curr_loc[0],(curr_loc[1]-1)],g_loc) #(g_loc[0] - curr_loc[0]) + (g_loc[1] - (curr_loc[1]-1))
        # Right distance
        if ((curr_loc[1] + 1) < len(a_grid[0])):
            if(a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                return a_grid
            if(a_grid[curr_loc[0]][curr_loc[1] + 1] == '_'):
                # right_dist = (row_diff + col_diff)
                right_dist = manhattan([curr_loc[0],(curr_loc[1]+1)],g_loc)#(g_loc[0] - curr_loc[0]) + (g_loc[1] - (curr_loc[1]+1))
                #print("right_dist = ", right_dist)
        # Up distance
        if ((curr_loc[0] - 1) >= 0):
            if(a_grid[(curr_loc[0]-1)][curr_loc[1]] == 'G'):
                return a_grid
            if(a_grid[(curr_loc[0]-1)][curr_loc[1]] == '_'):
                # up_dist = (row_diff + col_diff)
                up_dist = manhattan([(curr_loc[0]-1),curr_loc[1]],g_loc)#(g_loc[0] - (curr_loc[0]-1)) + (g_loc[1] - curr_loc[1])
                #print("up_dist = ", up_dist)
        # Down distance
        if ((curr_loc[0] + 1) < len(a_grid)):
            if(a_grid[(curr_loc[0]+1)][curr_loc[1]] == 'G'):
                return a_grid
            if(a_grid[(curr_loc[0]+1)][curr_loc[1]] == '_'):
                # down_dist = (row_diff + col_diff)
                down_dist = manhattan([(curr_loc[0]+1),curr_loc[1]],g_loc) #(g_loc[0] - (curr_loc[0]+1)) + (g_loc[1] - curr_loc[1])
                #print("down_dist = ", down_dist)
        

        if (left_dist == math.inf and right_dist == math.inf and up_dist == math.inf and down_dist == math.inf):
            stuck = True
            return False

        if (not(stuck)):
            # TODO: Improve the checking for None values before min check
            min_index = randomMinIndex([up_dist, down_dist, left_dist, right_dist])#min(up_dist, down_dist, left_dist, right_dist)
            #print("Previous direction was %s" % prev_dir)
            if(prev_dir == "Down" and min_index == 0):
                return False 
            if(prev_dir == "Up" and min_index == 1):
                return False 
            if(prev_dir == "Right" and min_index == 2):
                return False 
            if(prev_dir == "Left" and min_index == 3):
                return False 

            if (min_index == 2):
                if (prev_dir == "Right"):
                    return False
                prev_dir = "Left"
                curr_loc[1] -= 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('left')
            elif (min_index == 3):
                if (prev_dir == "Left"):
                    return False
                prev_dir = "Right"
                curr_loc[1] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('right')
            elif (min_index == 0):
                if (prev_dir == "Down"):
                    return False
                prev_dir = "Up"
                curr_loc[0] -= 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('up')
            elif (min_index == 1):
                if (prev_dir == "Up"):
                    return False
                prev_dir = "Down"
                curr_loc[0] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('down')

# uses cheb distance (up down left right diagonal solution)
def greedy_b(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    curr_loc = copy.deepcopy(s_loc)
    prev_dir = "None"
    stuck = False
    while (not(stuck)):
        print("\n")
        for x in a_grid:
            print(''.join(x))
        left_dist = math.inf
        right_dist = math.inf
        up_dist = math.inf
        down_dist = math.inf
        up_right_dist = math.inf
        up_left_dist = math.inf
        down_right_dist = math.inf
        down_left_dist = math.inf
        #################################################################
        #Get the H values for all the directions.
        #################################################################
        # Left distance
        if ((curr_loc[1] - 1) >= 0):
            if(a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                return a_grid
            if(a_grid[curr_loc[0]][curr_loc[1] - 1] == '_'):
                # left_dist = (row_diff + col_diff)
                left_dist = cheb([curr_loc[0],(curr_loc[1]-1)],g_loc) #(g_loc[0] - curr_loc[0]) + (g_loc[1] - (curr_loc[1]-1))
                #print("left_dist = ", left_dist)
        # Right distance
        if ((curr_loc[1] + 1) < len(a_grid[0])):
            if(a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                return a_grid
            if(a_grid[curr_loc[0]][curr_loc[1] + 1] == '_'):
                # right_dist = (row_diff + col_diff)
                right_dist = cheb([curr_loc[0],(curr_loc[1]+1)],g_loc)#(g_loc[0] - curr_loc[0]) + (g_loc[1] - (curr_loc[1]+1))
                #print("right_dist = ", right_dist)
        # Up distance
        if ((curr_loc[0] - 1) >= 0):
            if(a_grid[(curr_loc[0]-1)][curr_loc[1]] == 'G'):
                return a_grid
            if(a_grid[(curr_loc[0]+1)][curr_loc[1]] == '_'):
                # up_dist = (row_diff + col_diff)
                up_dist = cheb([(curr_loc[0]-1),curr_loc[1]],g_loc)#(g_loc[0] - (curr_loc[0]-1)) + (g_loc[1] - curr_loc[1])
                #print("up_dist = ", up_dist)
        # Down distance
        if ((curr_loc[0] + 1) < len(a_grid)):
            if(a_grid[(curr_loc[0]+1)][curr_loc[1]] == 'G'):
                return a_grid
            if(a_grid[(curr_loc[0]+1)][curr_loc[1]] == '_'):
                # down_dist = (row_diff + col_diff)
                down_dist = cheb([(curr_loc[0]+1),curr_loc[1]],g_loc) #(g_loc[0] - (curr_loc[0]+1)) + (g_loc[1] - curr_loc[1])
                #print("down_dist = ", down_dist)
        #Up + Right (diagonal)
        if (((curr_loc[0] - 1) >= 0) and ((curr_loc[1] + 1) < len(a_grid[0]))):
        #                       up          right
            if(a_grid[curr_loc[0]-1][curr_loc[1]+1] == 'G'):
                return a_grid
        #                       up          right   
            if(a_grid[curr_loc[0]-1][curr_loc[1]+1] == '_'):
                up_right_dist = cheb([(curr_loc[0]-1),(curr_loc[1]+1)],g_loc)

        #Up + Left (diagonal)
        if (((curr_loc[0] - 1) >= 0) and ((curr_loc[1] - 1) < len(a_grid[0]))):
        #                       up          Left
            if(a_grid[curr_loc[0]-1][curr_loc[1]-1] == 'G'):
                return a_grid
        #                       up          Left   
            if(a_grid[curr_loc[0]-1][curr_loc[1]-1] == '_'):
                up_left_dist = cheb([(curr_loc[0]-1),(curr_loc[1]-1)],g_loc)

        #Down + Right (diagonal)
        if (((curr_loc[0] + 1) >= 0) and ((curr_loc[1] + 1) < len(a_grid[0]))):
        #                       Down          right
            if(a_grid[curr_loc[0]+1][curr_loc[1]+1] == 'G'):
                return a_grid
        #                       Down          right   
            if(a_grid[curr_loc[0]+1][curr_loc[1]+1] == '_'):
                down_right_dist = cheb([(curr_loc[0]+1),(curr_loc[1]+1)],g_loc)

        #Down + Left (diagonal)
        if (((curr_loc[0] + 1) >= 0) and ((curr_loc[1] - 1) < len(a_grid[0]))):
        #                       Down          Left
            if(a_grid[curr_loc[0]+1][curr_loc[1]-1] == 'G'):
                return a_grid
        #                       Down          Left   
            if(a_grid[curr_loc[0]+1][curr_loc[1]-1] == '_'):
                down_left_dist = cheb([(curr_loc[0]+1),(curr_loc[1]-1)],g_loc)
                

        if (left_dist == math.inf and right_dist == math.inf and up_dist == math.inf and down_dist == math.inf):
            stuck = True
            return False

        if (not(stuck)):
            # TODO: Improve the checking for None values before min check
            min_index = randomMinIndex([up_dist, down_dist, left_dist, right_dist, up_right_dist, up_left_dist, down_right_dist, down_left_dist])
            #print("Previous direction was %s" % prev_dir)
            if(prev_dir == "Down" and min_index == 0):
                return False 
            if(prev_dir == "Up" and min_index == 1):
                return False 
            if(prev_dir == "Right" and min_index == 2):
                return False 
            if(prev_dir == "Left" and min_index == 3):
                return False 

            #Diagonal Directions
            if (min_index == 4):
                curr_loc[0] -= 1
                curr_loc[1] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('up_right')
            elif (min_index == 5):
                curr_loc[0] -= 1
                curr_loc[1] -= 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('up_left')
            elif (min_index == 6):
                curr_loc[0] += 1
                curr_loc[1] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('down_right')
            elif (min_index == 7):
                curr_loc[0] += 1
                curr_loc[1] -= 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('down_left')

            #Cardinal Directions
            elif (min_index == 2):
                curr_loc[1] -= 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('left')
                
            elif (min_index == 3):
                curr_loc[1] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('right')
            elif (min_index == 0):
                curr_loc[0] -= 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('up')
            elif (min_index == 1):
                curr_loc[0] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                #print('down')



def randomMinIndex(array):
    minValue = min(array)
    minIndices = []

    for i in range(len(array)):
        if(array[i] == minValue):
            minIndices.append(i)
            
    return minIndices[random.randint(0,len(minIndices) - 1)]


def alphabeta():
    input_filename = "alphabeta.txt"
    output_filename = "alphabeta_out.txt"
    alphabeta_reader(input_filename)


def alphabeta_reader(input_filename):
    temp_base = {}
    with open(input_filename) as f:
        for i in f.readlines():
            if (not(i[0] == " ")):
                temp_input01 = i.split(' ')
                print(temp_input01)
                t_part01 = temp_input01[0]
                t_part01 = t_part01[2:-2].split('),(')
                print(t_part01)
                t_part02 = temp_input01[1]
                t_part02 = t_part02[2:-2].split('),(')
                print(t_part02)
                
                # building base
                for j in t_part01:
                    t_node = j.split(',')
                    t_letter = t_node[0]
                    print(t_letter)
                    t_minmax_letter = t_node[1][1] == 'I'
                    print(t_minmax_letter)
                    temp_node = Node(t_letter, t_minmax_letter)
                    temp_base[t_letter] = temp_node
                    print("testing the dic = ", temp_base[t_letter].min)
                
                # building children
                for k in t_part02:
                    t_node = k.split(',')
                    t_fletter = t_node[0]
                    print(t_fletter)
                    t_sletter = t_node[1]
                    print(t_sletter)
                    some_node = temp_base[t_fletter]
                    if (t_sletter in temp_base):
                        print(temp_base[t_sletter])
                        some_node.childrenSetter(temp_base[t_sletter])
                    else:
                        # assume that its numeric
                        some_node.valueSetter(int(t_sletter))

                
    for x in temp_base:
        print('----------')
        print("Letter = ", temp_base[x].letter)
        print("Min Bool = ", temp_base[x].min)
        print("Value length = ", len(temp_base[x].values))
        print("Values: ")
        for y in temp_base[x].values:
            print("\t", y)
        print("Children length = ", len(temp_base[x].children))
                


class Node:
    node_count = 0

    def __init__(self, letter, minmax, value=-1):
        self.letter = letter
        self.min = minmax
        self.values = []
        self.children = []
        Node.node_count += 1
    
    def valueSetter(self, value):
        self.values.append(value)
    
    def childrenSetter(self, value):
        self.children.append(value)

    def displayCount(self):
     print ("Total Nodes = %d" % Node.node_count)

    def displayNode(self):
      print ("letter: ", self.letter,", minmax: ", self.minmax, " value: ", self.value)


main()
