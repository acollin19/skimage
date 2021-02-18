
import math, random
import numpy as np
import skimage.io as io

def show_image(data, routes=[]):
    '''
    Given a list of lists of integers "data",
    and an optional list of boolean list of lists "routes",
    show the data as an image and overlay the routes on the image in red.
    '''
    image_data = [x[:] for x in data]
    for i in range(len(image_data)):
        for j in range(len(image_data[i])):
            image_data[i][j] = [image_data[i][j]] * 3
            if any(route[i][j] for route in routes):
                image_data[i][j] = [255, 0, 0]
    io.imshow(np.array(image_data, dtype=np.uint8))
    io.show()

def load_dat_file(filename):

    try:
# Open file containing the big string and read it 
        file=open(filename,"r")
        big_string=file.read()
# Split the big string into a list of lines
        list_lines=big_string.split('\n')
        list_integers=[]
        main_list=[]
# Iterate through each line in the list of lines to split it into a list of strings
        for each_line in list_lines:
            if(len(each_line))>0:
                list_strings=each_line.split()
# Iterate through each number string in the list of strings to convert it to integers
# Then append each integer into a list to create a list of integers
            for numbers in list_strings:
                integers=int(numbers)
                list_integers.append(integers)
# Append the list of integers into the main list to create the list of lists
            main_list.append(list_integers)
            list_integers=[]
                      
        file.close()
        
    except ValueError:
        print("Elements in file must only be integers!")
# Closing file again in case theres an error and try doesnt run through    
    file.close()
    
    return main_list       
         

def find_elevation_route_for_starting_row(grid, starting_row):
# Creating a boolean list of lists with same length as the 'grid' list of lists of integers.   
    lol_of_booleans=[]
# Append the boolean "False" into the length of the rows then append that list into a bigger list
# to create the boolean list of lists.        
    for row in range(len(grid)):
        list_of_booleans=[]
        
        for bools in range(len(grid[row])):
            list_of_booleans.append(False)
            
        lol_of_booleans.append(list_of_booleans)
# Setting the starting point to be True given the starting row     
    r=starting_row
    lol_of_booleans[starting_row][0]=True
    total_change=0
# For columns in range on the number of rows minus one so it doesnt go out of bounds
    for c in range(len(grid[0])-1):    
        
        if r>0 and r<(len(grid)-1):
            start_height=grid[r][c]  
# Columns always increase by 1 and row depends on if moving up,down, or straight
            fwd_up=grid[r-1][c+1]
            fwd_down=grid[r+1][c+1]
            fwd=grid[r][c+1]
        
# Move1,2,3 each returns an integer that represents the elevation change between point a - b            
            move1=start_height-fwd_up
            move2=start_height-fwd_down
            move3=start_height-fwd
# Comaparing the elevation change of move 1 to move2,3 and if its smaller than move in that direction       
            if move1 < move2 and move1 < move3:
                lol_of_booleans[r-1][c+1]=True # Change this index in grid of booleans to True
                total_change+=move1 # adding change from this move to the total_change
                r-=1 # moving up but row below
# Comparing the elevation change of move 2 to move 1,3 and if its smaller that move in that direction
            elif move2 < move1 and move2 < move3:
                lol_of_booleans[r+1][c+1]=True
                total_change+=move2
                r+=1 #moving down but row above
# If the smallest change is a tie and foward is an option then go foward
            elif (move3 < move1 and move3 < move2) or (move3 == move1 or move3 == move2):
                lol_of_booleans[r][c+1]=True
                total_change+=move3

# If the smallest change is equal between moving up or down then pick randomly           
            elif move1 == move2:
                path=random.randint(0,1)
# If random int is 0 then its moving up in the grid
                if path==0:
                    lol_of_booleans[r-1][c+1]=True
                    total_change+=move1 
                    r-=1
# If random int is 1 then its moving down in the grid
                else:
                    lol_of_booleans[r+1][c+1]=True
                    total_change+=move2
                    r+=1                   
                
#If reached the top of grid perform then follwo this path                    
        elif r==0:
            start_height=grid[r][c]
# Setting the moving patterns            
            fwd_down=grid[r+1][c+1]
            fwd=grid[r][c+1]            
            move2=start_height-fwd_down
            move3=start_height-fwd
# If move2 is smaller than move3 then follow this path             
            if move2 < move3:
                lol_of_booleans[r+1][c+1]=True #Chnage boolean at this index in grid of booleans
                total_change+=move2 #add elevation count to total count
                r+=1 #row index increases
# If move3 is smaller or equal than move foward
            elif (move3 < move2) or (move2 == move3):
                lol_of_booleans[r][c+1]=True
                total_change+=move3
                
#If reached the bottom of the grid then follow this path        
        elif r==(len(grid)-1):
            start_height=grid[r][c]
# Setting the moving patterns             
            fwd_up=grid[r-1][c+1] 
            fwd=grid[r][c+1]
            move1=start_height-fwd_up
            move3=start_height-fwd
# If move1 is smaller than move3 then move up            
            if move1 < move3:
                lol_of_booleans[r-1][c+1]=True
                total_change+=move1
                r-=1
# If moving foward has a smaller change or is equal to moving up then go foward               
            elif (move3 < move1) or (move3 == move1):
                lol_of_booleans[r][c+1]=True
                total_change+=move3                
# Return the tuple where index 0 is the list of lists of booleans and index 1 is the total change in elevation    
    tup_of_elements=(lol_of_booleans,total_change)
           
    return tup_of_elements  

def get_all_elevation_routes(grid):
    list_of_tups=[]
# For a list of tuples the same length as the grid, each tuple contains the list of booleans
# as the first element in the tuple and the elevation change as the second element
    for starting_row in range(len(grid)):
        tups_ele_change=find_elevation_route_for_starting_row(grid, starting_row) 
        list_of_tups.append(tups_ele_change)
            
    return list_of_tups

def get_min_elevation_route(routes):

    elevation_change=[]
# For each tuple in the list(routes), take the elevation change so the second element of the tuple
# and append each of those values into a list of all elevation changes.
    for tuples in routes:
        elevation_change.append(tuples[1])
# Then take the min value from the list and if the tuples in routs at the second index is
# the same as the elevation change, then return the tuple
    smallest_elevation=min(elevation_change)
    for tuples in routes:
        if tuples[1]==smallest_elevation:
            return tuples

if __name__ == '__main__':
    data = load_dat_file("mountroyal.dat")
#    show_image(data, [])
    routes = get_all_elevation_routes(data)
    
    min_route = get_min_elevation_route(routes)
    assert(isinstance(min_route, tuple))
    
    show_image(data, [min_route[0]])
    show_image(data, [route for route, change in routes])
    
