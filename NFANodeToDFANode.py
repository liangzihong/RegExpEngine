import pprint
import ParseRegExp as pre
from NFANode import NFANode
from DFANode import DFANode
import PaintDFA as pdfa

#第一步，将node的边是epsilon的边变成一个list
#类似[[], [], [(2, 3)], [(3, 4), (3, 10)], [(4, 5), (4, 7)], [], [(6, 9)], [], [(8, 9)], [(9, 4), (9, 10)], []]
def step1(node:NFANode):
    endCnt=node.endState
    #把所有epsilon的边记录在案
    epsilonList=[]
    for i in range(endCnt+1):
        epsilonList.append([])

    keys = node.edgeDict.keys()
    keys = sorted(keys)
    for key in keys:
        value= node.edgeDict[key]
        if value=='ε':
            epsilonList[key[0]].append(key)

    return epsilonList


#第二步，将上一步得到的epsilon的序列的点从元组变成list，类似vector<vector>的效果，方便进行bfs
#[[], [], [3], [4, 10], [5, 7], [], [9], [], [9], [4, 10], []]
def step2(epsilonList:list):
    arrList=[]
    for i in range(len(epsilonList)):
        tuplist=epsilonList[i]
        arr=[]
        for tup in tuplist:
            arr.append(tup[1])
        arrList.append(arr)
    return arrList


#第三部，将上一步得到的arrList进行bfs，将某个点能用epsilon到达的点用集合显示出来
#[set(), {1}, {2, 3, 4, 5, 7, 10}, {3, 4, 5, 7, 10}, {4, 5, 7}, {5}, {4, 5, 6, 7, 9, 10}, {7}, {4, 5, 7, 8, 9, 10}, {4, 5, 7, 9, 10}, {10}]
#得到一个list，里面是 集合。  得到 setList
def step3(arrList: list):
    setList=[]
    for i in range(len(arrList)):
        sset=set()
        setList.append(sset)
    #bfs
    for i in range(1,len(arrList)):
        toList=[]
        isVisited=[False for x in range(len(arrList))]
        queue=[]
        queue.append(i)
        while(len(queue)>0):
            to=queue.pop(0)
            isVisited[to]=True
            toList.append(to)
            for k in arrList[to]:
                if isVisited[k]==False:
                    queue.append(k)
        setList[i].update(toList)
        setList[i].add(i)
    return setList




#变成DFANode的最后一部
#从初态开始，每个状态遍历每个边的值，如果nowSet当前集合通过某个value到达下一个状态nextSet，就把 nowSet和nextSet和value放入DFA中
#这里最重要就是要判断能到达的下一个状态 出现过没有，如果出现过，就不用放入队列中处理
def step4(setList:list, node:NFANode):
    startCnt=node.startState
    endCnt=node.endState

    dfaNode=DFANode()
    dfaNode.initialize(startCnt,endCnt)


    #这一步，让dictList变成一个 [dict0,dict1,dict2......dict10]
    #dict1={(1,x):'a',(1,y):'b'} 之类的，dict1放的就是以1为出发点，key为元组，value为边，边不为epsilon的字典。
    #[{}, {(1, 2): 'a'}, {}, {}, {}, {(5, 6): 'a'}, {}, {(7, 8): 'b'}, {}, {}, {}]
    #同时把边的类型记录下来，记录在edgeValueSet中
    dictList=[]
    edgeValueSet=set()                 #记录edgeValue的种类
    for i in range(len(setList)):
        dictList.append({})
    keys=node.edgeDict.keys()
    keys=sorted(keys)
    for key in keys:
        value=node.edgeDict[key]
        if value!='ε':
            dictList[key[0]][key]=value
            edgeValueSet.add(value)
    # print(dictList)

    #从初态开始做动作

    visitedSetList=[]      #判断这个某个状态之前有没有出现过
    queue=[]               #状态队列
    edgeValueList=list(edgeValueSet)   #边的类型的list，要为每个状态都进行一个  edgevalue的遍历

    initSet=setList[startCnt]  #初态
    queue.append(initSet)      #队列
    visitedSetList.append(initSet)   #是否有重复的状态

    while(len(queue)>0):
        nowSet= queue.pop(0)


        for value in edgeValueList:
            nextSet=set()
            for fp in list(nowSet):                             #fp 当前集合的每一个数字，也就是出发点
                fpdict = dictList[fp]                           # sample: fpdict={(1,2):'a'}
                for key, thisvalue in fpdict.items():           #key,value 为元组和边的值
                    if value==thisvalue:
                        ep=key[1]
                        nextSet.update(setList[ep])

            print('NFA变DFA step4，从集合到集合的关系')
            if len(nextSet)>0:
                dfaNode.addEdgeDict(nowSet,nextSet,value)
                print(nowSet,'----->',nextSet, 'edge=',value)
                if (nextSet in visitedSetList)==False :
                    visitedSetList.append(nextSet)
                    queue.append(nextSet)
    return dfaNode
    # 结果如下：
    # {1} - ----> {2, 3, 4, 5, 7, 10}
    # edge = a
    # {2, 3, 4, 5, 7, 10} - ----> {4, 5, 7, 8, 9, 10}
    # edge = b
    # {2, 3, 4, 5, 7, 10} - ----> {4, 5, 6, 7, 9, 10}
    # edge = a
    # {4, 5, 7, 8, 9, 10} - ----> {4, 5, 7, 8, 9, 10}
    # edge = b
    # {4, 5, 7, 8, 9, 10} - ----> {4, 5, 6, 7, 9, 10}
    # edge = a
    # {4, 5, 6, 7, 9, 10} - ----> {4, 5, 7, 8, 9, 10}
    # edge = b
    # {4, 5, 6, 7, 9, 10} - ----> {4, 5, 6, 7, 9, 10}
    # edge = a




def FromNFAToDFA(node:NFANode):
    epsilonList=step1(node)
    arrList= step2(epsilonList)
    setList= step3(arrList)
    dfanode=step4(setList,node)

    return dfanode




# if __name__=="__main__":
#
#     test='a*'
#     pp=pprint.PrettyPrinter(indent=4)
#     # pp.pprint( step1(pre.parseReToNFANode(test)))
#     # print('step1后得到的NFANode为',step1(pre.parseReToNFANode(test)))
#     node=pre.parseReToNFANode(test)
#     epsilonList=step1(node)
#     arrList= step2(epsilonList)
#     setList= step3(arrList)
#     # print('NFA变为DFA的 step3后得到的浓缩集合为',setList)
#
#     dfanode=step4(setList,node)
#     print('dfaNode的边和点集合为')
#     pp.pprint(dfanode.edgeDict)
#     dfanode.minimize()
#     pdfa.paintMinimize(dfanode)
#     # pp.pprint(dfanode.allSetList)
#     # pdfa.paintDFA(dfanode)
