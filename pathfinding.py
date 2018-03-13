import copy
import math
import random

def main():
    print('=========== START ===========')
    filename = 'pathfinding_a.txt'
    grid = reader(filename)
    # print(grid)
    output_filename = 'output.txt'

    s_loc = target_finder(grid, 'S')
    print(s_loc)
    g_loc = target_finder(grid, 'G')
    print(g_loc)

    return_grid = False
    while(not(return_grid)):
        return_grid = greedy(grid, s_loc, g_loc)
    print(return_grid)
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

# uses manhattan distance
def greedy(tmp_grid, s_loc, g_loc):
    a_grid = copy.deepcopy(tmp_grid)
    curr_loc = s_loc
    prev_dir = "None"
    stuck = False
    while (not(stuck)):
        left_dist = math.inf
        right_dist = math.inf
        up_dist = math.inf
        down_dist = math.inf
        # Left distance
        if ((curr_loc[1] - 1) >= 0):
            if(a_grid[curr_loc[0]][curr_loc[1] - 1] == 'G'):
                return a_grid
            if(a_grid[curr_loc[0]][curr_loc[1] - 1] == '_'):
                # left_dist = (row_diff + col_diff)
                left_dist = (g_loc[0] - curr_loc[0]) + (g_loc[1] - (curr_loc[1]-1))
                print("left_dist = ", left_dist)
        # Right distance
        if ((curr_loc[1] + 1) < len(a_grid[0])):
            if(a_grid[curr_loc[0]][curr_loc[1] + 1] == 'G'):
                return a_grid
            if(a_grid[curr_loc[0]][curr_loc[1] + 1] == '_'):
                # right_dist = (row_diff + col_diff)
                right_dist = (g_loc[0] - curr_loc[0]) + (g_loc[1] - (curr_loc[1]+1))
                print("right_dist = ", right_dist)
        # Up distance
        if ((curr_loc[0] - 1) >= 0):
            if(a_grid[(curr_loc[0]-1)][curr_loc[1]] == 'G'):
                return a_grid
            if(a_grid[(curr_loc[0]-1)][curr_loc[1]] == '_'):
                # up_dist = (row_diff + col_diff)
                up_dist = (g_loc[0] - (curr_loc[0]-1)) + (g_loc[1] - curr_loc[1])
                print("up_dist = ", up_dist)
        # Down distance
        if ((curr_loc[0] + 1) < len(a_grid)):
            if(a_grid[(curr_loc[0]+1)][curr_loc[1]] == 'G'):
                return a_grid
            if(a_grid[(curr_loc[0]+1)][curr_loc[1]] == '_'):
                # down_dist = (row_diff + col_diff)
                down_dist = (g_loc[0] - (curr_loc[0]+1)) + (g_loc[1] - curr_loc[1])
                print("down_dist = ", down_dist)
        

        if (left_dist == math.inf and right_dist == math.inf and up_dist == math.inf and down_dist == math.inf):
            stuck = True
            return False

        if (not(stuck)):
            # TODO: Improve the checking for None values before min check
            min_index = randomMinIndex([up_dist, down_dist, left_dist, right_dist])#min(up_dist, down_dist, left_dist, right_dist)
            print("Previous direction was %s" % prev_dir)
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
                print('left')
            elif (min_index == 3):
                if (prev_dir == "Left"):
                    return False
                prev_dir = "Right"
                curr_loc[1] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                print('right')
            elif (min_index == 0):
                if (prev_dir == "Down"):
                    return False
                prev_dir = "Up"
                curr_loc[0] -= 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                print('up')
            elif (min_index == 1):
                if (prev_dir == "Up"):
                    return False
                prev_dir = "Down"
                curr_loc[0] += 1
                a_grid[curr_loc[0]][curr_loc[1]] = 'P'
                print('down')

def randomMinIndex(array):
    minValue = min(array)
    minIndices = []

    for i in range(len(array)):
        if(array[i] == minValue):
            minIndices.append(i)
            
    return minIndices[random.randint(0,len(minIndices) - 1)]


main()