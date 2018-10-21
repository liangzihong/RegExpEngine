from NFANode import NFANode
from graphviz import Digraph

#画出NFA
#三步骤： 设置终态为doublecircle， 设置一个不可见的点，连向开头表示初态， 其他态为圆圈
#把node.edgeDict遍历一遍即可
def paintNfa( node:NFANode):
    nfa=Digraph('nfa',filename='nfa.gv')
    nfa.attr(rankdir='LR',size='4.5')

    edges=node.edgeDict

    #定义终态是由两个圆圈组成
    nfa.attr('node',shape='doublecircle')
    nfa.node(str(node.endState))

    #其他态
    nfa.attr('node',shape='circle')
    keys= edges.keys()
    keys=sorted(keys)
    for key in keys:
        fp,tp=str(key[0]),str(key[1])
        value=edges[key]
        nfa.edge(fp,tp,label=value)

    # for key,value in edges.items():
    #     fp,tp=str(key[0]),str(key[1])
    #     nfa.edge(fp,tp,label=value)

    #设置一个不可见的点，连向开头代表初态
    nfa.attr('node',style='invis')
    nfa.node('0')
    nfa.edge('0',str(node.startState))
    nfa.view()



