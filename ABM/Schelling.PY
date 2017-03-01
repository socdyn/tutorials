import re
import time
import random
import networkx as nx
import matplotlib.pyplot as plt




####In this .py file we will rebuild Schelling's model of housing segregation.####


##### 1 BUILD THE NEIGHBORHOOD #####
#We will use a network structure to keep track of the pattern of spots in the neighborhood 'neighbor' relations.
def latticify(gridwidth, gridlength, diagonals = True):
    lots = gridwidth * gridlength
    Neighborhood = nx.Graph()
    xcoord ={}
    ycoord ={}
    residents = {}
    for x in range(0,lots):
        Neighborhood.add_node(x)
        ycoord[x] = int(x/gridlength)
        xcoord[x] = x%gridlength
        residents[x] = None
    nx.set_node_attributes(Neighborhood,'xcoord',xcoord)
    nx.set_node_attributes(Neighborhood,'ycoord',ycoord)
    nx.set_node_attributes(Neighborhood,'residents',residents)
    #print xcoord
    ##This double loop will add edges between any two neighbors in the neighboorhood
    #print Neighborhood[6]
    for a in range(0,lots):
        for b in range(0,lots):
            if a > b:
                h_dist = abs(Neighborhood.node[a]['xcoord'] - Neighborhood.node[b]['xcoord'])
                v_dist = abs(Neighborhood.node[a]['ycoord'] - Neighborhood.node[b]['ycoord'])
                if h_dist + v_dist == 1:
                    Neighborhood.add_edge(a,b)
                elif (h_dist == 1) & (v_dist ==1):
                    if diagonals ==True:
                        Neighborhood.add_edge(a,b)
                    else:
                        pass
                else:
                    pass
    return Neighborhood

##CHECK THE NEIGHBORHOOD

N = latticify(8,6,diagonals = True)
label_value_dict = {}
pos = {}
for q in nx.nodes(N):
    label_value_dict[q]= (N.node[q]['xcoord'],N.node[q]['ycoord'])
    pos[q]=[q%6/float(8),int(q/6)/float(8)]
nx.draw(N,pos,font_size = 15,labels = label_value_dict,node_size = 100)
plt.show()

##### 2 BUILD THE NEIGHBORS, RANDOMLY GIVE THEM A SPOT IN THE NEIGHBORHOOD #####
class neighbor:
    def __init__(self,neighbor_id,color,in_group,out_group,home):
        self.id = neighbor_id
        self.color = color
        self.in_group = in_group
        self.out_group = out_group
        self.home = home
    def move(self,new_location):
        self.home = new_location



Neighbors = []
for x in range(0,12):
    NewHome = None
    while NewHome == None:
        PotentialHome = random.randint(0,47)
        if N.node[PotentialHome]['residents']==None:
            N.node[PotentialHome]['residents']=x
            NewHome = PotentialHome
        else:
            pass
    Neighbors.append(neighbor(x,'blue',0.4,0.0,NewHome))
for y in range(12,24):
    NewHome = None
    while NewHome == None:
        PotentialHome = random.randint(0,47)
        if N.node[PotentialHome]['residents']==None:
            N.node[PotentialHome]['residents']=y
            NewHome = PotentialHome
        else:
            pass
    Neighbors.append(neighbor(y,'green',0.4,0.0,NewHome))

#N = latticify(8,6,diagonals = False)
color_value_dict = {}
for q in nx.nodes(N):
    resident = N.node[q]['residents']
    #print resident
    try:
        if Neighbors[int(resident)].color == 'blue':
            color_value_dict[q]= 'blue'
        elif Neighbors[int(resident)].color == 'green':
            color_value_dict[q] ='green'
        else:
            color_value_dict[q] = 'white'
    except:
        color_value_dict[q] = 'white'
#print color_value_dict

###CHECK THE POPULATED NEIGHBORHOOD

color_value = [color_value_dict.get(node) for node in N.nodes()]
nx.draw(N,pos,font_size = 5,labels = label_value_dict,node_size = 100,node_color = color_value)
plt.show()







##### 3 BUILD FUNCTION THAT MEASURES SEGREGATION #####

def measure_segregation(network, residents):
    mixed_tie = 0
    blue_tie = 0
    green_tie = 0
    possibleedges = network.edges()
    for x in possibleedges:
        res1 = network.node[x[0]]['residents']
        res2 = network.node[x[1]]['residents']
        if (res1 != None) & (res2 != None):
            if (residents[res1].color == 'blue') & (residents[res2].color =='blue'):
                blue_tie = blue_tie + 1
            elif (residents[res1].color == 'green') & (residents[res2].color =='green'):
                green_tie = green_tie + 1
            else:
                mixed_tie = mixed_tie + 1
    return mixed_tie,blue_tie,green_tie


print measure_segregation(N,Neighbors)

##### 4 BUILD LOOP THAT MOVES THE NEIGHBORS AROUND
##First build functions that check desirability of locations for neighbors


def checkoldspot(neighbor,allneighbors,theneighborhood):
    neighbor_outgroup_pref = neighbor.out_group
    neighbor_ingroup_pref = neighbor.in_group
    in_group_neighbors = 0
    out_group_neighbors = 0
    neighbor_lots = theneighborhood.neighbors(neighbor.id)
    the_neighbors = []
    for t in neighbor_lots:
        a_neighbor = theneighborhood.node[t]['residents']
        if a_neighbor != None:
            the_neighbors.append(a_neighbor)
    #print the_neighbors
    for u in the_neighbors:
        if allneighbors[u].color == neighbor.color:
            in_group_neighbors = in_group_neighbors + 1
        else:
            out_group_neighbors = out_group_neighbors + 1
    if (in_group_neighbors/float(in_group_neighbors+out_group_neighbors+.001)) >= neighbor_ingroup_pref:
        if (out_group_neighbors/float(in_group_neighbors+out_group_neighbors+.001)) >= neighbor_outgroup_pref:
            good_spot = True
        else:
            good_spot = False
    else:
        good_spot = False
    return good_spot

def checknewspot(neighbor,newspot,allneighbors,theneighborhood):
    if theneighborhood.node[newspot]['residents'] == None:
        neighbor_outgroup_pref = neighbor.out_group
        neighbor_ingroup_pref = neighbor.in_group
        in_group_neighbors = 0
        out_group_neighbors = 0
        current_in_group_neighbors = 0
        current_out_group_neighbors = 0
        neighbor_lots = theneighborhood.neighbors(newspot)
        the_neighbors = []
        for t in neighbor_lots:
            a_neighbor = theneighborhood.node[t]['residents']
            if a_neighbor != None:
                the_neighbors.append(a_neighbor)
        #print the_neighbors
        for u in the_neighbors:
            if allneighbors[u].color == neighbor.color:
                in_group_neighbors = in_group_neighbors + 1
            else:
                out_group_neighbors = out_group_neighbors + 1
        #Get old spots for comparison
        currentneighbor_lots = theneighborhood.neighbors(neighbor.id)
        current_neighbors = []
        for s in currentneighbor_lots:
            a_cur_neighbor = theneighborhood.node[s]['residents']
            if a_cur_neighbor != None:
                current_neighbors.append(a_cur_neighbor)
        #print the_neighbors
        for r in current_neighbors:
            if allneighbors[r].color == neighbor.color:
                current_in_group_neighbors = current_in_group_neighbors + 1
            else:
                current_out_group_neighbors = current_out_group_neighbors + 1
        if ((in_group_neighbors/float(in_group_neighbors+out_group_neighbors+.001)) >= neighbor_ingroup_pref) & ((out_group_neighbors/float(in_group_neighbors+out_group_neighbors+.001)) >= neighbor_outgroup_pref):
            good_spot = True
        else:
            ing_improve = (in_group_neighbors/float(in_group_neighbors+out_group_neighbors+.001)) > min((current_in_group_neighbors/float(current_in_group_neighbors+current_out_group_neighbors+.001),neighbor_ingroup_pref))
            og_improve = (out_group_neighbors/float(in_group_neighbors+out_group_neighbors+.001)) > min((current_out_group_neighbors/float(current_in_group_neighbors+current_out_group_neighbors+.001),neighbor_ingroup_pref))
            good_spot = ing_improve and og_improve
    else:
        good_spot = False
    return good_spot

Num_Of_Moves = 10000
Actual_Moves = 0
for t in range(0,Num_Of_Moves):
    Mover = Neighbors[random.randint(0,23)]
    if checkoldspot(Mover,Neighbors,N) == False:
        NewDigs = random.randint(0,47)
        if checknewspot(Mover,NewDigs,Neighbors,N) == True:
            OldDigs = Mover.home
            N.node[OldDigs]['residents'] = None
            N.node[NewDigs]['residents'] = Mover.id
            Mover.move(NewDigs)
            Actual_Moves = Actual_Moves + 1
        else:
            pass
    else:
        pass
print Actual_Moves
color_value_dict = {}
for q in nx.nodes(N):
    resident = N.node[q]['residents']
    #print resident
    try:
        if Neighbors[int(resident)].color == 'blue':
            color_value_dict[q]= 'blue'
        elif Neighbors[int(resident)].color == 'green':
            color_value_dict[q] ='green'
        else:
            color_value_dict[q] = 'white'
    except:
        color_value_dict[q] = 'white'


###CHECK THE SHIFTED NEIGHBORHOOD

color_value = [color_value_dict.get(node) for node in N.nodes()]
nx.draw(N,pos,font_size = 5,labels = label_value_dict,node_size = 100,node_color = color_value)
plt.show()

measure_segregation(N,Neighbors)




##### 5 BUILD FUNCTION THAT DOES ALL OF THIS SO YOU CAN ITERATE THROUGH A PARAMETER SPACE #####

def schellify(Rows,Columns,BlueResidents,BlueIGP,BlueOGP,GreenResidents,GreenIGP,GreenOGP,Moves,Diagonal = True,ShowPlot = False):
    #Build a Neighborhood
    TheNeighborhood = latticify(Columns, Rows, diagonals = Diagonal)
    #Fill it with Neighbors
    TheNeighbors = []
    for x in range(0,BlueResidents):
        NewHome = None
        while NewHome == None:
            PotentialHome = random.randint(0,Rows*Columns-1)
            if TheNeighborhood.node[PotentialHome]['residents']==None:
                TheNeighborhood.node[PotentialHome]['residents']=x
                NewHome = PotentialHome
            else:
                pass
        TheNeighbors.append(neighbor(x,'blue',BlueIGP,BlueOGP,NewHome))
    for y in range(BlueResidents,BlueResidents+GreenResidents):
        NewHome = None
        while NewHome == None:
            PotentialHome = random.randint(0,Rows*Columns-1)
            if TheNeighborhood.node[PotentialHome]['residents']==None:
                TheNeighborhood.node[PotentialHome]['residents']=y
                NewHome = PotentialHome
            else:
                pass
        TheNeighbors.append(neighbor(y,'green',GreenIGP,GreenOGP,NewHome))
    d,e,f = measure_segregation(TheNeighborhood, TheNeighbors)
    #Let the Neighbors Move Around
    Actual_Moves = 0
    for m in range(0,Moves):
        Mover = TheNeighbors[random.randint(0,BlueResidents+GreenResidents-1)]
        if checkoldspot(Mover,TheNeighbors,TheNeighborhood) == False:
            NewDigs = random.randint(0,Rows*Columns-1)
            if checknewspot(Mover,NewDigs,TheNeighbors,TheNeighborhood) == True:
                OldDigs = Mover.home
                TheNeighborhood.node[OldDigs]['residents'] = None
                TheNeighborhood.node[NewDigs]['residents'] = Mover.id
                Mover.move(NewDigs)
                Actual_Moves = Actual_Moves + 1
            else:
                pass
        else:
            pass
    #Measure Segregation of the Shuffled Neighborhood and Return Results
    if ShowPlot == True:
        label_value_dict = {}
        pos = {}
        for q in nx.nodes(TheNeighborhood):
            label_value_dict[q]= q
            pos[q]=[int(q/Rows)/float(Rows),q%Columns/float(Columns)]
        color_value_dict = {}
        for q in nx.nodes(TheNeighborhood):
            resident = TheNeighborhood.node[q]['residents']
            #print resident
            try:
                if TheNeighbors[int(resident)].color == 'blue':
                    color_value_dict[q]= 'blue'
                elif TheNeighbors[int(resident)].color == 'green':
                    color_value_dict[q] ='green'
                else:
                    color_value_dict[q] = 'white'
            except:
                color_value_dict[q] = 'white'
        color_value = [color_value_dict.get(node) for node in TheNeighborhood.nodes()]

        nx.draw(TheNeighborhood,pos,font_size = 5,labels = label_value_dict,node_size = 100,node_color = color_value)
        plt.show()
    else:
        pass
    a,b,c = measure_segregation(TheNeighborhood, TheNeighbors)
    return d,e,f,Actual_Moves,a,b,c

#print schellify(15,15,50,0.5,0,50,0.2,0,1000,ShowPlot = True,Diagonal = True)


'''

#####6 Use function to loop through different parameters spaces
for x in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7]:
    for y in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7]:
        for z in range(0,10):
            a,b,c,d,e,f,g = schellify(8,8,25,x,y,25,x,y,10000)
            print str(x) + '|' + str(y) + '|' +str(z) +'|' + str(e/float(e+f+g))


'''
