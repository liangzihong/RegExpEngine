

#在这里吸收 正则表达式，对其进行解析



class NFANode(object):

    def __init__(self):
        self.edgeDict={}
        self.startState=0
        self.endState=0

    def initialize(self, ch:str):
        self.startState=1
        self.endState=2
        self.edgeDict[(1,2)]=ch

    def addEdgeDictTuple(self, delta):
        retDict={}
        for key,value in self.edgeDict.items():
            retDict[ (key[0]+delta , key[1]+delta) ]=value
        return retDict
















