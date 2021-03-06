import numpy as np
from tkinter import *

class Node:
    """
        A node class for A* Pathfinding
        parent is parent of the current Node
        position is current position of the Node in the maze
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

#This function return the path of the search
def return_path(current_node,maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    # here we create the initialized result maze with -1 in every position
   # result = [[-1 for i in range(no_columns)] for j in range(no_rows)  ]
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)  ]
    for i in range(no_rows):
        for j in range(no_columns):
            if(maze[i][j]==1):
                result[i][j]=-2
            else:
                result[i][j]=-1
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    start_value = 0
    # we update the path of start to end found by A-star serch with every step incremented 
    #by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(maze, cost, start, end):
    """
        Returns a list of tuples as a path from the given start to the given end in
        the given maze
        :param maze:
        :param cost
        :param start:
        :param end:
        :return:
    """

    # Create start and end node with initized values for g, h and f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both yet_to_visit and visited list
    # in this list we will put all node that are yet_to_visit for exploration. 
    # From here we will find the lowest cost node to expand next
    yet_to_visit_list = []  
    # in this list we will put all node those already explored so that we don't 
    #explore it again
    visited_list = [] 
    
    # Add the start node
    yet_to_visit_list.append(start_node)
    
    # Adding a stop condition. This is to avoid any infinite loop and stop 
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # what squares do we search . serarch movement is left-right-top-bottom 
    #(4 movements) from every positon

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right


    """
        1) We first get the current node by comparing all f cost and selecting the lowest cost node for further expansion
        2) Check max iteration reached or not . Set a message and stop execution
        3) Remove the selected node from yet_to_visit list and add this node to visited list
        4) Perofmr Goal test and return the path else perform below steps
        5) For selected node find out all children (use move to find children)
            a) get the current postion for the selected node (this becomes parent node for the children)
            b) check if a valid position exist (boundary will make few nodes invalid)
            c) if any node is a wall then ignore that
            d) add to valid children node list for the selected parent
            
            For all the children node
                a) if child in visited list then ignore it and try next node
                b) calculate child node g, h and f values
                c) if child in yet_to_visit list then ignore it
                d) else move the child to yet_to_visit list
    """
    #find maze has got how many rows and columns 
    no_rows, no_columns = np.shape(maze)
    
    # Loop until you find the end
    
    while len(yet_to_visit_list) > 0:
        
        # Every time any node is referred from yet_to_visit list,
        #counter of limit operation incremented
        outer_iterations += 1    

        
        # Get the current node
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # if we hit this point return the path such as it may be no solution or 
        # computation cost is too high
        if outer_iterations > max_iterations:
            print ("giving up on pathfinding too many iterations")
            return return_path(current_node,maze)

        # Pop current node out off yet_to_visit list, add to visited list
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            return return_path(current_node,maze)

        # Generate children from all adjacent squares
        children = []

        for new_position in move: 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1]
                             + new_position[1])

            # Make sure within range (check if within maze boundary)
            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the visited list (search entire visited list)
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost
            ## Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and g cost is already lower
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # Add the child to the yet_to_visit list
            yet_to_visit_list.append(child)
def btn(self,fr):
        path = search(maze,cost, start, end)
        print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) 
      for row in path]))
        sol(path,fr)
    
def sol(path,fr):
     for i in range(1,6):
        for j in range(6):
            if path[i-1][j]==-2:
                fr1 = Frame(fr,height=60,width=60,bg='crimson')
                fr1.grid(row=i, column=j)
           
            elif path[i-1][j]==-1:            
                fr1 = Frame(fr,height=60,width=60,bg='#FFB266')
                fr1.grid(row=i, column=j)
            else:
                fr1 = Frame(fr,height=60,width=60,bg='#FF3333')
                fr1.grid(row=i, column=j)
    

if __name__ == '__main__':

    maze = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0]]#if someone wants to change the obstacle please change 
                                #the position of  in the maze matrix and do not changt the size
                                #of the matrix as gui is connected with it.
    
    start = [0, 0] # starting position
    end = [4,1] # ending position
    cost = 1 # cost per movement
    root = Tk() 
    root.geometry('1200x900')
    root.title("Best route finding using A*")
    f=Frame(root,height=120,width=1200,bg='crimson')
    f.pack()
    label10 = Label( f, text="Best route finding using A*", font='Times 32 bold',bg='crimson',
    fg='black', height=2, width=1200)
    label10.pack()
    h=Frame(root,height=120,width=1200)
    h.pack()
    q=Frame(h,height=60,width=60,bg='crimson')
    q.grid(row=0,column=1)
    label = Label( h, text="Obstacle", font='Times 16 bold',
    fg='black', height=1, width=8)
    label.grid(row=0,column=2)
    w=Frame(h,height=60,width=60,bg='#009900')
    w.grid(row=0,column=3)
    label1 = Label( h, text="END", font='Times 16 bold',
    fg='black', height=1, width=8)
    label1.grid(row=0,column=4)
    er=Frame(h,height=60,width=60,bg='#FFB266')
    er.grid(row=0,column=5)
    label2= Label( h, text="Allowed Path ", font='Times 16 bold',
    fg='black', height=1, width=12)
    label2.grid(row=0,column=6)
    e=Frame(h,height=60,width=60,bg='#CC6600')
    e.grid(row=0,column=7)
    label3 = Label( h, text="START", font='Times 16 bold',
    fg='black', height=1, width=8)
    label3.grid(row=0,column=8)
    q1=Frame(h,height=60,width=60,bg='#FF3333')
    q1.grid(row=0,column=9)
    label4 = Label( h, text="Best Route", font='Times 16 bold',
    fg='black', height=1, width=12)
    label4.grid(row=0,column=10)
    q2=Frame(root,height=100,width=1200)
    q2.pack()
    label5 = Label( q2, text="If you want to change the obstacles please "+ 
                   "change the position of 1's in the 'MAZE' matrix without "+ 
                   "changing the size of matrix  ", font='Times 16 bold',
    fg='black', height=2, width=1200)
    label5.pack()
    fr=Frame(root,height=300,width=360)
    fr.pack()
    for i in range(1,6):
        for j in range(6):
            if maze[i-1][j]==1:
                fr1 = Frame(fr,height=60,width=60,bg='crimson')
                fr1.grid(row=i, column=j)
            elif i-1==start[0] and j==start[1]:
                fr1 = Frame(fr,height=60,width=60,bg='#CC6600')
                fr1.grid(row=i, column=j)
                               
            elif i-1==end[0] and j==end[1]:
                fr1 = Frame(fr,height=60,width=60,bg='#009900')
                fr1.grid(row=i, column=j)
            else:            
                fr1 = Frame(fr,height=60,width=60,bg='#FFB266')
                fr1.grid(row=i, column=j)
    q3=Frame(root,height=20,width=1200)
    q3.pack()
    button1 = Button(root, text="SOLVE", font='Times 20 bold', bg='crimson',
    fg='white', height=1, width=6,command=lambda:btn(btn,fr))
    
    button1.pack() 
    root.mainloop() 
##-1 in the matrix int the printed below shows unused path
#-2 denotes obstacles
#anything else shows the cost of the paths
    
