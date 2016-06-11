#!/usr/bin/python
#Function to read the input file.
#Please specify the file name as 'input.dat' in ored to read the topology.

def read_file(filename):
    input_file = open(filename,'U')
    
    ip_matrix = []
    for i in input_file:
        #Used map function to typecast the weights (originally in string) to intiger type.
        ip_matrix.append(map(int,i.split()))

    return ip_matrix

#ip_matrix = read_file('input.dat')


#Dijkistra algorithm to calculate the shortest path and optimal cost.
def dijkistra(ip_matrix,source):
    #Default value as 11111 
    dist_matrix = [11111 for i in range(len(ip_matrix[0]))]
    
    #Setting previously visited nodes as -1
    pre_node_visited = [-1 for i in range(len(ip_matrix[0]))]
    
    #Setting the distance from source to source as 0
    dist_matrix[source]= 0
    
    queue = [i for i in range(len(ip_matrix[0]))]
    #Loooping until the queue is not empty
    
    #Checking the condition if the queue is not empty then recursively traverse over the network topology
    #to find out the minimal distance.
    while len(queue)>0:
        
        
        min_val =  min([dist_matrix[i] for i in queue])
        for i in queue:
            if dist_matrix[i] == min_val:
                u = i
        #removing 'u' since we have now visited this node.        
        queue.remove(u)
        #For each neighbour of node 'u' find out the minimal distance of reaching that node.
        for i in range(len(ip_matrix[source])):
            if ip_matrix[u][i] not in [0,-1]:
                alt = dist_matrix[u] + ip_matrix[u][i]
                if alt < dist_matrix[i]:
                    dist_matrix[i] = alt
                    #if the above calculated distance is the minimal distance then assign the previous node traversed as 'u'
                    pre_node_visited[i] = u
                    
    #Function finally returns the previous nodes visited and the optimized cost matrix.
    return  pre_node_visited,dist_matrix       
#previous_node_visits,cost_matrix = dijkistra(ip_matrix,4)
#print previous_node_visits
#print cost_matrix



#Function to calculate the path list traversed from source to destination. 
def path_list(source,destination,ip_matrix):
    path_traversed = [source]
    final_des = destination
    #Checking if source = destination then you are already there at the destination.
    if source == destination:
        print "Values same hai change kar bc"
        return []
        
    for i in range(len(ip_matrix)):
        pre_node_list = (dijkistra(ip_matrix,source))
        if(pre_node_list[0][destination] == source):
            break
        else:
            destination = pre_node_list[0][destination]
            path_traversed.append(destination)
    path_traversed.append(final_des)
   
    if -1 in path_traversed:
        print "There is no possible path from %s to %s" %(source,final_des)
    else:
        print "Shortest path from source node %s to destination node %s is %s" %(source,final_des,path_traversed)
        print "The Cost incurred for traversing this path is %s" %(pre_node_list[1][final_des])
    

        

def connection_table(source,ip_matrix):
    #Since the dijkistra elements give out the preious elements to be traversed
    pre_node_list = dijkistra(ip_matrix,source)
    des = [i for i in range(len(ip_matrix))]
    print "  Connection table for Router %s  " %(source)
    print "==================================="
    for i in range(len(ip_matrix[0])):
        if pre_node_list[0][i] == source:
            print "%s =====> %s" %(i,i)
        elif (i != source):
            if (pre_node_list[0][i] == -1):
                print "%s =====> Router is down" %(i)
            else:   
                print "%s =====> %s" %(i,pre_node_list[0][i])
        else:
            print "%s =====> -" %(i)
    
#connection_table(0,ip_matrix)
    

import copy
def remove_router(rnum,ip_matrix):
    new_matrix = copy.deepcopy(ip_matrix)
    #Change the entrie row of router 3 as -1 since it can't send packets anywhere
    for i in range(len(new_matrix)):
        new_matrix[rnum][i] = -1
    #Change the entire column of router 3 to -1 since this router can't be reached
    for i in range(len(new_matrix)):
        new_matrix[i][rnum] = -1
    print new_matrix
    return new_matrix
#new = remove_router(3,ip_matrix)


print "CS 542 Link State Routing Simulator"
print "Please enter the input file"
input_file = raw_input()
ip_matrix = read_file(input_file)
print "You have entered the below topology"

for i in ip_matrix:
    print str(i).strip('[]')
print "\n\n"

def main_menu(ip_matrix):
    
    
    print "(1) Build a connection table for a given node"
    print "(2) Shortest path from source to destination"
    print "(3) Modify the topology (Turn a router down)"
    print "(4) Change the weight"
    print "(5) Add a new node in the topology"
    print "(6) Exit"
    
    print "Please enter the option"
    opt = int(raw_input())
    
    if(opt==1):
        print "Please enter the source node for which you want the connection table.:"
        source = int(raw_input()) 
        connection_table(source,ip_matrix)
        print "\n\n"
        main_menu(ip_matrix)
        
    if(opt==2):
        print "Please enter the source"
        s = int(raw_input())
        print "Please enter the destination"
        d = int(raw_input())
        path_list(s,d,ip_matrix)
        print "\n\n"
        main_menu(ip_matrix)
        
    
    if(opt==3):
        print "Please enter the router number which you want to turn off"
        rnum = int(raw_input())
        new = remove_router(rnum,ip_matrix)
        print "\n\n"
        main_menu(new)
        
    
    if(opt==4):
        change = map(int,(raw_input("Enter the edge for which you want to change the weight(For ex: Enter 2 1)").split()))
        weight = int(raw_input("Enter new weight"))
        ip_matrix[change[0]][change[1]] = weight
        ip_matrix[change[1]][change[0]] = weight
        print "The new topology afer changing the weight is as belows"
        for i in ip_matrix:
            print str(i).strip('[]')
        print "\n\n"
        main_menu(ip_matrix) 
    
    if(opt==5):
        print "Original number of nodes are %s" %len(ip_matrix[0])
        new_node = map(int,(raw_input("Enter the new weights in the node i.e enter the weights from the new node to every other node sequentially").split()))
        new_node.append(0) 
        #print ip_matrix
        for i in range(len(ip_matrix[0])):
            ip_matrix[i].append(new_node[i])
        ip_matrix.append(new_node)
        print "The new topology afer adding the node is as belows"
        for i in ip_matrix:
            print str(i).strip('[]')
        print "\n\n"
        
        main_menu(ip_matrix)
    
    if(opt==5):
        print "Exit"
        return
        
 
main_menu(ip_matrix)

 
