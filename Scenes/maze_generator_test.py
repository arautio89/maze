# maze generator
# Randomized Prim

#from config import *

from operator import itemgetter

MAZE_HOR = 13
MAZE_VER = 13
TILES_HOR = 2*MAZE_HOR + 1 #25
TILES_VER = 2*MAZE_VER + 1 #20

from random import randint, sample

def maze_generator():
    # Recursive backtracker
    # Implementation 1 - Sets
    maze = [[(x%2==0 or y%2==0) for y in range(TILES_VER)]
            for x in range(TILES_HOR)]
    # Start
    maze[TILES_HOR//2][TILES_VER - 1] = False
    
    xr = randint(0, MAZE_HOR - 1) #randint(0,int((len(maze)-1)/2)-1)
    yr = randint(0, MAZE_VER - 1) #randint(0,int((len(maze[0])-1)/2)-1)
    current = (2*xr+1, 2*yr+1)
    checked = {current}
    all_cells = get_all_maze_cells(maze)
    #all_cells = set([])
    stack=[]
    while (checked!=all_cells):
        cx,cy = current
        #cells=find_nhoods(maze,current[0],current[1])-checked
        
        nhood = set([(cx + dx, cy) for dx in (-2,2)
                     if 0 <= cx + dx < TILES_HOR]
                    +[(cx, cy + dy) for dy in (-2,2)
                     if 0 <= cy + dy < TILES_VER])
        
        cells = nhood - checked
        if (cells!=set([])):
            chosen_cell = sample(cells,1)[0]
            stack.append(current)
            # Cell between Current and Chosen cells
            #bx, by = int((cx + chosen_cell[0])/2), int((cy+chosen_cell[1])/2)
            bx, by = (cx + chosen_cell[0])//2, (cy + chosen_cell[1])//2
            maze[bx][by] = False
            current=chosen_cell
            checked.add(current)
        elif (stack!=[]):
            current=stack.pop()
        else:
            unchecked=all_cells-checked
            current=sample(unchecked,1)[0]
            checked.add(current)
    return(maze)



def find_nhoods(maze,x,y):
    nhoods=set([])
    for i in (-2,2):
        if (0<=x+i<len(maze)):
            if (maze[x+i][y]==0):
                nhoods.add((x+i,y))
    for j in (-2,2):
        if (0<=y+j<len(maze[0])):
            if (maze[x][y+j]==0):
                nhoods.add((x,y+j))
    return (nhoods)

def find_walls(maze,checked): # finds walls of the set checked
    walls=set([])
    for cell in checked:
        nhoods=find_nhoods(maze,cell[0],cell[1])
        for nhood in nhoods:
            if (nhood not in checked):
                walls.add((int((cell[0]+nhood[0])/2),int((cell[1]+nhood[1])/2)))
    return (walls)

def print_map(map0,floor=".",wall="#",dead_end="¤",path=[],show_dead_ends=False):
    dead_ends=0
    if (path=="no path"):
        path=[]
    for i in range(len(map0[0])):
        line=""
        for j in range(len(map0)):
            if ((j,i) in path):
                line+="X"
            else:
                if (map0[j][i]==0):
                    if (map0[j-1][i]+map0[j+1][i]+map0[j][i-1]+map0[j][i+1]>=3 and show_dead_ends==True):
                        line+="¤"
                        dead_ends+=1
                    else:
                        line+="."
                elif (map0[j][i]==1):
                    line+="#"
            
            #print(j,i)
        print(line)
    #print(dead_ends)

def print_maze(maze, floor=".",wall="#",dead_end="¤",path=[],show_dead_ends=True):
    for y in range(TILES_VER):
        for x in range(TILES_HOR):
            if (x%2 == 1 and y%2 == 1):
                if (maze[x-1][y] + maze[x+1][y]
                    + maze[x][y-1] + maze[x][y+1]>=3
                    and show_dead_ends==True):
                    symbol = dead_end
                else:
                    symbol = floor
            else:
                if maze[x][y]:
                    symbol = wall
                else:
                    symbol = floor

            print(symbol, end = "")
        print()
            
                

def get_all_maze_cells(maze): # returns a set of all maze cells
    cells=set([])
    for i in range(int((len(maze)-1)/2)):
        for j in range(int((len(maze[0])-1)/2)):
            cells.add((2*i+1,2*j+1))
    return (cells)

def get_cells_from_wall(wall):
    if (wall[0]%2==0):
        cells={(wall[0]-1,wall[1]),(wall[0]+1,wall[1])}
    elif (wall[1]%2==0):
        cells={(wall[0],wall[1]-1),(wall[0],wall[1]+1)}
    else:
        cells=set([])
    return (cells)



def maze_generator_rb(maze): # Recursive backtracker
    from random import randint, sample
    xr=randint(0,int((len(maze)-1)/2)-1)
    yr=randint(0,int((len(maze[0])-1)/2)-1)
    current=(2*xr+1,2*yr+1)
    checked={current}
    all_cells=get_all_maze_cells(maze)
    stack=[]
    while (checked!=all_cells):
        cells=find_nhoods(maze,current[0],current[1])-checked
        if (cells!=set([])):
            chosen_cell=sample(cells,1)[0]
            stack.append(current)
            maze[int((current[0]+chosen_cell[0])/2)][int((current[1]+chosen_cell[1])/2)]=0
            current=chosen_cell
            checked.add(current)
        elif (stack!=[]):
            current=stack.pop()
        else:
            unchecked_cells=all_cells-checked
            current=sample(unchecked,1)[0]
            checked.add(current)
    return(maze)



def maze_stats(maze,print_it=True):
    # how many dead-ends, corridors, T-junctions, crossroads
    # Make a list of Dead Ends
    open_counter=[0,0,0,0,0]
    dead_ends = []
    for i in range(int((len(maze)-1)/2)):
        x=2*i+1
        for j in range(int((len(maze[0])-1)/2)):
            y=2*j+1
            cell_openings=0
            if (maze[x-1][y]==0):
                cell_openings+=1
            if (maze[x+1][y]==0):
                cell_openings+=1
            if (maze[x][y-1]==0):
                cell_openings+=1
            if (maze[x][y+1]==0):
                cell_openings+=1
            open_counter[cell_openings]+=1
            if cell_openings == 1:
                # Dead end
                dead_ends.append((x,y))

    # Distances of Dead Ends from the Start
    start = (TILES_HOR//2, TILES_VER - 1)
    dij_map = dijkstra_map(maze, start)   
    
    if (print_it==True):
        print("Dead-ends (1): "+ str(open_counter[1]))
        print("Corridoors (2): "+ str(open_counter[2]))
        print("T-Junctions (3): "+ str(open_counter[3]))
        print("Crossroads (4): "+ str(open_counter[4]))
        #print(dead_ends)

        #print(start, dij_map[start[0]][start[1]])
        total_dist = 0
        # Sort According Distance
        dd = [(d, dij_map[d[0]][d[1]]) for d in dead_ends]
        dd.sort(key=itemgetter(1))
        total_dist = sum([d[1] for d in dd])
        ndd = len(dead_ends)
        dd_mean = total_dist/ndd
        dd_min = dd[0][1]
        dd_max = dd[-1][1]
        dd_midpoint = (dd_min + dd_max)/2
        if ndd%2==1:
            #dd_middle = ndd//2
            dd_median = dd[ndd//2][1]
        else:
            #dd_middle = (ndd//2 - 1, ndd//2)
            dd_median = (dd[ndd//2][1] + dd[ndd//2 - 1][1])/2
        print("Total Distance:", total_dist)
        print("Mean Distance:", dd_mean)
        print("Min:",dd_min,"Median:",dd_median,"Max:",dd_max)
        print("Midpoint:", dd_midpoint)
        
        """
        for d in dead_ends:
            dist = dij_map[d[0]][d[1]]
            #print(d, dij_map[d[0]][d[1]])
            total_dist += dist"""
        #print("Total Distance:",total_dist)
        #print("Mean Distance:",total_dist/len(dead_ends))
    return (open_counter)

def dijkstra_map(maze, start):
    dij_map = [[float("inf") for y in range(TILES_VER)]
               for x in range(TILES_HOR)]
    dij_map[start[0]][start[1]] = 0
    updating = True
    while updating:
        updating = False
        for y in range(1, TILES_VER - 1):
            for x in range(1, TILES_HOR - 1):
                if not maze[x][y]:
                    nhood = [(x-1, y), (x+1, y),
                             (x, y-1), (x, y+1)]
                    for n in nhood:
                        if (dij_map[x][y] > dij_map[n[0]][n[1]] + 1):
                            dij_map[x][y] = dij_map[n[0]][n[1]] + 1
                            updating = True
    return(dij_map)
                            

if __name__ == '__main__':
    for k in range(10):
        maze = maze_generator()
        #print_maze(maze)
        maze_stats(maze)
        print()
