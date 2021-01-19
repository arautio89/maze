# maze generator
# Randomized Prim

def create_map(x,y):
    map_ = []
    for i in range(x):
        templist = []
        for j in range(y):
            templist.append(0)
        map_.append(templist)
    return (map_)

def create_maze(x,y,walls="yup"):
    map_ = []
    for i in range(2*x+1):
        templist = []
        for j in range(2*y+1):
            if (walls!="yup"):
                if (i==0 or j==0 or i==2*x or j==2*y or (i%2==0 and j%2==0)):
                    templist.append(1)
                else:
                    templist.append(0)
            elif (walls=="yup"):
                if (i==0 or j==0 or i==2*x or j==2*y or i%2==0 or j%2==0):
                    templist.append(1)
                else:
                    templist.append(0)
        map_.append(templist)
    return (map_)

def all_walls(maze): # add all walls to maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if ((i+j)%2==1):
                maze[i][j]=1
    return (maze)

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

def find_nhoods_np(maze,y,x): # array version
    nhoods=set([])
    for i in (-2,2):
        if (0<=y+i<len(maze)):
            if (maze[y+i,x]==0):
                nhoods.add((y+i,x))
    for j in (-2,2):
        if (0<=x+j<len(maze[0])):
            if (maze[y,x+j]==0):
                nhoods.add((y,x+j))
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

def maze_generator(maze):
    from random import randint, sample
    xr=randint(0,int((len(maze)-1)/2)-1)
    yr=randint(0,int((len(maze[0])-1)/2)-1)
    checked={(2*xr+1,2*yr+1)}
    #print(checked)
    all_cells=get_all_maze_cells(maze)
    while (checked!=all_cells):
        walls=find_walls(maze,checked)
        #print("walls")
        #print(walls)
        rwall=sample(walls,1)[0]
        #print("rwall")
        #print(rwall)
        next_cell=(get_cells_from_wall(rwall)-checked).pop()
        #print("next cell")
        #print(next_cell)
        maze[rwall[0]][rwall[1]]=0
        checked.add(next_cell)
        #print(checked)
    return(maze)

# checked are cells that are already checked, fixed walls won't be removed
def maze_generator2(maze,checked="random",fixed_walls=set([])): #checked is a set that is fixed
    from random import randint, sample
    if (checked=="random"):
        xr=randint(0,int((len(maze)-1)/2)-1)
        yr=randint(0,int((len(maze[0])-1)/2)-1)
        checked={(2*xr+1,2*yr+1)}
    all_cells=get_all_maze_cells(maze)
    while (checked!=all_cells):
        walls=find_walls(maze,checked)
        #rwall="looping"
        state="looping"
        while (state=="looping"):
            rwall=sample(walls,1)[0]
            if (rwall not in fixed_walls):
                state="done"
        next_cell=(get_cells_from_wall(rwall)-checked).pop()
        maze[rwall[0]][rwall[1]]=0
        checked.add(next_cell)
    return(maze)

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

"""
def maze_generator_rb_np(x,y): # Recursive backtracker using arrays
    from random import randint, sample
    from numpy import zeros, int8
    import numpy as np
    
    #print("It works")
    maze=np.zeros((2*y+1,2*x+1),dtype=int8)
    maze[0,:]=maze[:,0]=maze[-1,:]=maze[:,-1]=1
    maze[2:-2:2,2:-2:2]=1
    maze[1:-1:2,2:-2:2]=1
    maze[2:-2:2,1:-1:2]=1
    
    
    yr=randint(0,int((len(maze)-1)/2)-1)
    xr=randint(0,int((len(maze[0])-1)/2)-1)
    current=(2*yr+1,2*xr+1)
    checked={current}
    all_cells=get_all_maze_cells(maze)
    stack=[]
    while (checked!=all_cells):
        cells=find_nhoods_np(maze,current[0],current[1])-checked
        if (cells!=set([])):
            chosen_cell=sample(cells,1)[0]
            stack.append(current)
            maze[int((current[0]+chosen_cell[0])/2),int((current[1]+chosen_cell[1])/2)]=0
            current=chosen_cell
            checked.add(current)
        elif (stack!=[]):
            current=stack.pop()
        else:
            unchecked_cells=all_cells-checked
            current=sample(unchecked,1)[0]
            checked.add(current)
    return(maze)
"""

def maze_stats(maze,print_it=True): # how many dead-ends, corridors, T-junctions, crossroads
    open_counter=[0,0,0,0,0]
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
    if (print_it==True):
        print("Dead-ends (1): "+ str(open_counter[1]))
        print("Corridoors (2): "+ str(open_counter[2]))
        print("T-Junctions (3): "+ str(open_counter[3]))
        print("Crossroads (4): "+ str(open_counter[4]))
    return (open_counter)

'''
maze1=create_maze(15,15)

maze1=maze_generator(maze1)
print_map(maze1)
'''

"""
maze2=create_maze(15,15)
maze2[15][14]=0
maze2[15][16]=0
maze2[14][15]=0
maze2[16][15]=0
fixed_cells={(15,15),(13,15),(15,13),(15,17),(17,15)}
fixed_walls={(13,14),(13,16),(14,13),(16,13),(17,14),(17,16),(14,17),(16,17)}
maze2=maze_generator2(maze2,fixed_cells,fixed_walls)
print_map(maze2)
"""

'''
maze1=create_maze(15,15)
maze1=maze_generator_rb(maze1)
print_map(maze1,show_dead_ends=True)
maze_stats(maze1)
'''
for k in range(3):
    maze1=create_maze(12,12)
    maze1=maze_generator_rb(maze1)
    print_map(maze1,show_dead_ends=True)
    maze_stats(maze1)

"""
maze=create_maze(15,15)
print_map(maze,show_dead_ends=True)
print()
maze=maze_generator_rb(maze)
print_map(maze,show_dead_ends=True)
maze=all_walls(maze)
print()
print_map(maze,show_dead_ends=True)
"""

#maze=maze_generator_rb_np(15,17)
#print_map(maze)

'''
list_dead_ends=[]
list_dead_ends_np=[]



maze2=create_maze(15,15)
for _ in range(500):
    maze2=maze_generator_rb(maze2)
    stats=maze_stats(maze2,print_it=False)
    list_dead_ends.append(stats[1])
    maze2=all_walls(maze2)
print(sum(list_dead_ends)/len(list_dead_ends))
for _ in range(500):
    maze=maze_generator_rb_np(15,15)
    stats_np=maze_stats(maze,print_it=False)
    list_dead_ends_np.append(stats_np[1])
print(sum(list_dead_ends_np)/len(list_dead_ends_np))
'''

"""
maze1=create_maze(15,15)
maze2=create_maze(15,15)

list1_rp=[]
list2_rp=[]
list3_rp=[]
list4_rp=[]

list1_rb=[]
list2_rb=[]
list3_rb=[]
list4_rb=[]

for _ in range(100):
    maze1=maze_generator(maze1)
    maze2=maze_generator_rb(maze2)
    #print("Randomized Prim")
    stats_rp=maze_stats(maze1,print_it=False)
    #print()
    #print("Recursive Backtracking")
    stats_rb=maze_stats(maze2,print_it=False)
    #print()
    list1_rp.append(stats_rp[1])
    list2_rp.append(stats_rp[2])
    list3_rp.append(stats_rp[3])
    list4_rp.append(stats_rp[4])

    list1_rb.append(stats_rb[1])
    list2_rb.append(stats_rb[2])
    list3_rb.append(stats_rb[3])
    list4_rb.append(stats_rb[4])
    
    maze1=all_walls(maze1)
    maze2=all_walls(maze2)

print("Randomized Prim")
print("1: " + str(sum(list1_rp)/len(list1_rp)))
print("2: " + str(sum(list2_rp)/len(list2_rp)))
print("3: " + str(sum(list3_rp)/len(list3_rp)))
print("4: " + str(sum(list4_rp)/len(list4_rp)))
print("Recursive Backtracking")
print("1: " + str(sum(list1_rb)/len(list1_rb)))
print("2: " + str(sum(list2_rb)/len(list2_rb)))
print("3: " + str(sum(list3_rb)/len(list3_rb)))
print("4: " + str(sum(list4_rb)/len(list4_rb)))
"""


"""
maze0=create_maze(3,3)
print(get_all_maze_cells(maze0))
"""

'''
maze1=create_maze(15,10)
#maze2=create_maze(15,10,walls="")
A=find_nhoods(maze1,3,3)
print(A)
print(find_walls(maze1,{(3,3)}))
B=find_walls(maze1,A)
print(B)
'''

"""
print_map(maze1)
print()
print_map(maze2)
"""
