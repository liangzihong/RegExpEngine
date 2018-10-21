import pprint
from NFANode import NFANode
import PaintNFA as pnfa

#两次test过了
#把上半部分的 NFANode全部序号加1
#把下半部分的 NFANode全部序号 加上 1+上半部分的序号数目
#然后把上半部分下半部分起点终点重新标记
#再对新的 node 的起点终点跟 上半部分下半部分的起点终点连在一起即可。
def operation_Or( firstNode:NFANode, secondNode:NFANode):
    newNode = NFANode()
    #edgeDict的组成
    dict1=firstNode.addEdgeDictTuple(1)
    dict2=secondNode.addEdgeDictTuple(delta=1+firstNode.endState)
    newNode.edgeDict.update(dict1)
    newNode.edgeDict.update(dict2)

    #startstate和endstate的定义
    newNode.startState=1
    newNode.endState=2 + firstNode.endState + secondNode.endState

    #两部分的开始节点和终结节点根据part1的节点数目会有变化， 这里先写出来
    newStar1,newEnd1= 2 , 1+firstNode.endState
    newStar2= 1+newEnd1
    newEnd2=newStar2 + secondNode.endState-1

    #其余节点为epsilon
    tupleList=[(1,newStar1),(1,newStar2),(newEnd1,newNode.endState),(newEnd2,newNode.endState)]
    for tup in tupleList:
        newNode.edgeDict[tup]='ε'
    return newNode

#两次test通过
def operation_Repeat(node:NFANode):
    newNode=NFANode()
    #返回+1后的新的dict
    dict1=node.addEdgeDictTuple(delta=1)
    newNode.edgeDict.update(dict1)

    #设置完成后的 开始节点和终止节点
    newNode.startState=1
    newNode.endState=2+node.endState

    newStart1,newEnd1=2,node.endState+1
    tupleList=[(1,2),(newEnd1,newNode.endState),(newEnd1,newStart1),(1,newNode.endState)]
    for tup in tupleList:
        newNode.edgeDict[tup]='ε'
    return newNode


def operation_Concat(firstNode:NFANode, secondNode:NFANode):
    #newnode的开始节点和终止节点
    newNode=NFANode()
    newNode.startState=1
    newNode.endState= firstNode.endState + secondNode.endState

    #newnode的上下两部分的边
    dict1=firstNode.addEdgeDictTuple(delta=0)
    dict2=secondNode.addEdgeDictTuple(delta=firstNode.endState)
    newNode.edgeDict.update(dict1)
    newNode.edgeDict.update(dict2)

    tupleList=[(firstNode.endState,1+firstNode.endState)]
    for tup in tupleList:
        newNode.edgeDict[tup]='ε'
    return  newNode






#
#
# if __name__=="__main__":
#     one,two=NFANode(),NFANode()
#     one.initialize('a')
#     two.initialize('b')
#     three = operation_Or(one,two)
#     four = operation_Or(three,two)
#     five = operation_Concat(four,two)
#     six = operation_Concat(one,two)
#     # pp=pprint.PrettyPrinter(indent=4)
#     # pp.pprint(six.edgeDict)
#     pnfa.paintNfa(five)