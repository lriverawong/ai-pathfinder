import re
import math

def alphabeta():
    input_filename = "alphabeta.txt"
    file = open(input_filename, "r")
    output_filename = "alphabeta_out.txt"
    outFile = open(output_filename, "w")

    count = 0
    for line in file:
        if (not(line == '\n' or line == '')):
            count += 1
            tree_and_root = alphabeta_reader(line)
            value_and_examined = tree_and_root[0][tree_and_root[1]].alpha_beta(-math.inf, math.inf)
            outString = "Graph %s" %count + ": Score: %s" % value_and_examined[0] + "; Leaf Nodes Examined: %s" % value_and_examined[1]
            outFile.write(outString + "\n")
            print(outString)


def alphabeta_reader(line):
    temp_base = {}
    root = None
    temp_input01 = line.split(' ')
    #print(temp_input01)
    t_part01 = temp_input01[0]
    t_part01 = t_part01[2:-2].split('),(')
    #print(t_part01)
    t_part02 = temp_input01[1]
    t_part02 = re.search('{(.+?)}', t_part02).group(1)
    #print(t_part02)
    t_part02 = t_part02[1:-1].split('),(')
    #print(t_part02)
    
    # building base
    for j in t_part01:
        t_node = j.split(',')
        t_letter = t_node[0]
        #print(t_letter)
        t_minmax_letter = t_node[1][1] == 'I'
        #print(t_minmax_letter)
        temp_node = Node(t_letter, t_minmax_letter)
        temp_base[t_letter] = temp_node
        #print("testing the dic = ", temp_base[t_letter].min)
    
    # building children
    if len(t_part02) > 0:
        root = t_part02[0].split(',')[0]
    for k in t_part02:
        t_node = k.split(',')
        t_fletter = t_node[0]
        #print(t_fletter)
        t_sletter = t_node[1]
        #print(t_sletter)
        some_node = temp_base[t_fletter]
        if (t_sletter in temp_base):
            #print(temp_base[t_sletter])
            some_node.childrenSetter(temp_base[t_sletter])
        else:
            # assume that its numeric
            chars = list(t_sletter)
            if chars[len(chars) - 1] == ')':
                del chars[len(chars) - 1]
            t_sletter = ''.join(chars)
            some_node.valueSetter(int(t_sletter))
        
    # for x in temp_base:
    #     print('----------')
    #     print("Letter = ", temp_base[x].letter)
    #     print("Min Bool = ", temp_base[x].min)
    #     print("Value length = ", len(temp_base[x].values))
    #     print("Values: ")
    #     for y in temp_base[x].values:
    #         print("\t", y)
    #     print("Children length = ", len(temp_base[x].children))
                
    return (temp_base, root)

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

    def alpha_beta(self, a, b):
        print("\nNode %s" % self.letter)
        print("Min: %s" % self.min)
        print("Alpha: %s" % a + "\nBeta: %s" % b)
        examined = 0
        if(len(self.children) == 0):
            if self.min:
                for x in self.values:
                    examined += 1
                    b = min(b, x)
                    if b <= a:
                        print("\nNode: %s" % self.letter + "\nBeta %s" % b + " is better than alpha %s" % a)
                        return (b, examined)
                return (b,examined)
            else:
                for x in self.values:
                    examined += 1
                    a = max(a, x)
                    if a >= b:
                        print("\nNode: %s" % self.letter + "\nAlpha %s" % a + " is better than beta %s" % b)
                        return (a, examined)
                return (a, examined)
        else:
            if self.min:
                for child in self.children:
                    childValue = child.alpha_beta(a, b)
                    best = childValue[0]
                    examined += childValue[1]
                    b = min(b, best)
                    if b <= a:
                        print("\nNode: %s" % self.letter + "\nBeta %s" % b + " is better than alpha %s" % a)
                        return (b, examined)
                return (b, examined)
            else:
                print("Max node")
                for child in self.children:
                    childValue = child.alpha_beta(a, b)
                    best = childValue[0]
                    examined += childValue[1]
                    a = max(a, best)
                    if a >= b:
                        print("\nNode: %s" % self.letter + "\nAlpha %s" % a + " is better than beta %s" % b)
                        return (a, examined)
                return (a, examined)



    def displayCount(self):
     print ("Total Nodes = %d" % Node.node_count)

    def displayNode(self):
      print ("letter: ", self.letter,", minmax: ", self.minmax, " value: ", self.value)

alphabeta()