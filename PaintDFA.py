
from graphviz import Digraph
from DFANode import DFANode

def paintDFA(node:DFANode):

    dfa=Digraph('dfa',filename='dfa.gv')
    dfa.attr(rankdir='LR',size='4.5')

    edges=node.edgeDict
    endSetList=node.endSetList

    #定义终态是由两个圆圈组成
    dfa.attr('node',shape='doublecircle')
    for sset in endSetList:
        dfa.node(str(sset))

    #其他态
    dfa.attr('node',shape='circle')

    for key,value in edges.items():
        fp,tp=str(key[0]),str(key[1])
        dfa.edge(fp,tp,label=value)

    #设置一个不可见的点，连向开头代表初态
    dfa.attr('node',style='invis')
    dfa.node('0')
    dfa.edge('0',str(node.startSet))
    dfa.view()


def paintMinimize(node:DFANode):

    mini=Digraph('mini',filename='mini.gv')
    mini.attr(rankdir='LR',size='4.5')

    tupleList=node.miniTupList
    miniEndStateList = node.miniEndStateList
    miniStartState =node.miniStartState


    #定义终态是由两个圆圈组成
    mini.attr('node',shape='doublecircle')
    for endstate in miniEndStateList:
        mini.node(str(endstate))

    #其他态
    mini.attr('node',shape='circle')

    for tuple in tupleList:
        fp, tp, value=tuple[0],tuple[1],tuple[2]
        fp,tp=str(fp),str(tp)
        mini.edge(fp,tp,label=value)

    #设置一个不可见的点，连向开头代表初态
    mini.attr('node',style='invis')
    mini.node('-1')
    mini.edge('-1',str(node.miniStartState))
    mini.view()