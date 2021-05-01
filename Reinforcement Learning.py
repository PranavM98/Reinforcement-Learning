#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 09:50:19 2021

@author: pranavmanjunath
"""

import time
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import networkx as nx
import pylab
import matplotlib.pyplot as plt
import environment


df,data,myvalue,rewards_test,environment_rows1,environment_columns1=environment.env()


def get_next_action(current_row_index,epsilon,path):

    
    a=rewards_test[current_row_index]
    
    indices=[]
    #M looks at the q values
    m=[]
    max_values=[]
    for i in range(26):
        if a[0,i]!=0:
            if i != path[len(path)-2]:
                indices.append(i)
                m.append(q_values[current_row_index,i])
    
    '''
    have the q indices in indices
    have the q values in m
    m
    '''
    if np.random.random() < epsilon:
        
        maxqi=max(m)
        for i in range(len(m)):
            if maxqi==m[i]:
                max_values.append(i)
        return indices[random.choice(max_values)]

    else:

        return random.choice(indices)


#Number to Alphabet Conversion
def n_a_conversion(number):
    n_a={}
    for a, n in zip(df.index, range(0,26)):
        n_a[n]=a
    return n_a[number]

def draw_graph(position):
    np.random.seed(145)
    carac = pd.DataFrame({ 'ID':df.index, 'myvalue':myvalue })
    alpha=n_a_conversion(position)

    carac['myvalue'][carac['ID']==alpha]='group7'
   

    # Build your graph
    
    G=nx.from_pandas_edgelist(data, 'from', 'to', create_using=nx.Graph() )

    # The order of the node for networkX is the following order:
    G.nodes()
    # Thus, we cannot give directly the 'myvalue' column to netowrkX, we need to arrange the order!

    # Here is the tricky part: I need to reorder carac to assign the good color to each node
    carac= carac.set_index('ID')
    carac=carac.reindex(G.nodes())

    # And I need to transform my categorical column in a numerical value: group1->1, group2->2...
    carac['myvalue']=pd.Categorical(carac['myvalue'])

    carac['myvalue'].cat.codes
    pylab.figure(figsize=(10,10))
    # Custom the nodes:
    nx.draw(G, with_labels=True, 
        pos=nx.spring_layout(G, scale=6),
        hold=5,
        node_color=carac['myvalue'].cat.codes, cmap=plt.cm.Set1, node_size=750)
    
    plt.draw()
    
    
epsilon =0.1
discount_factor = 0.4
learning_rate =0.7
total_path=[]
total_q=[]
q_values = np.zeros((environment_rows1,environment_columns1))
s=0
terminal=[3,6,16,23,15]
rewards_all_episodes=[]
for episode in range(10):
    starting = 0
    row_index=starting
    next_place=0
    path=[]
    path.append(row_index)
    
    #draw_graph(row_index)

    #plt.show()
    #plt.pause(2)
    #plt.clf()
 

    while starting==0 and next_place not in terminal:
        #print("STARTING")
        #print("Starting: ",row_index)
        rewards_current_episode=0
        action_index= get_next_action(row_index, epsilon,path)
        next_place = action_index
        #print("NEXT")
        #print("Next:", next_place)
        reward= rewards_test[row_index, next_place]
        
        rewards_current_episode += reward
        old_q_value = q_values[row_index, next_place]
        temporal_difference = reward + (discount_factor * np.max(q_values[row_index])) - old_q_value
        
        new_q_value = old_q_value + (learning_rate * temporal_difference)
        #print(new_q_value)
        q_values[row_index][next_place] = new_q_value
        

        #draw_graph(next_place)
        if next_place==15:
            print("****************SUCCESS****************************")
            s+=1
        
        #draw_graph(next_place)
        
        #plt.show()
        #plt.pause(2)
        #plt.clf()
        path.append(next_place)
        row_index=next_place
        if len(path)==40:
            break
        #print(q_values)
    print(path)
    print("EPISODE OVER")
    rewards_all_episodes.append(rewards_current_episode)
    #time.sleep(3)
    total_path.append(path)
    total_q.append(q_values)
print(s)



'''
print("AVERAGE REWARD PER THOUSAND EPISODES")
rewards_per_thousand_episodes=np.split(np.array(rewards_all_episodes),10/1)
count=1000
for r in rewards_per_thousand_episodes:
    print(count, ":", str(sum(r/1000)))
    count+=1000

'''


path=[0,18,19,20,21,14,15]

for i in path:
        draw_graph(i)

        plt.show()
        plt.pause(1)
        plt.clf()
'''
for i in total_path:
    for path in i:
        draw_graph(path)

        plt.show()
        plt.pause(1)
        plt.clf()


for i in total_path:
    print(i)

import csv
final_q=pd.DataFrame(q_values).to_csv('Q_table.csv')


for i in total_path:
    print(i)


print("Minimum Distance")

final_path=[]
start=0
dest=0
final_path.append(start)
while dest!=15:
    dest_row=q_values[dest]
    dest_max=-9999
    max_d=[]
    
    
    for i in range(26):
        if dest_row[i]!=0.0 and dest_row[i]>dest_max:
            dest_max=dest_row[i]
    
    
    for i in range(26):
        if dest_row[i]==dest_max:
            max_d.append(i)
    
    
    
    if len(max_d)==1:
        dest=max_d[0]
        final_path.append(max_d[0])
    else:
        dest=random.choice(max_d)
        final_path.append(dest)
    print(final_path)
    time.sleep(1)
print("Final Path")
print(final_path)

 '''   
    
    
    
    
    
    