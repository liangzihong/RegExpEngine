
import functools
#startSet为初态
#endSetList用来表示哪些集合是终态
#allSetList来存储所有的集合，只要出现就存储，但不能重复
#startState和endState用了判断是初态还是终态
#edgeDict是一个字典，key为 元组，value为边的值，其中 key的元组是两个集合对应的 字符串

# 提供keys之间排序
# 因为会出现一个混乱就是字符串：  {1}>{10}，所以写一个函数来提供排序方式
# 如 [('{10, 11, 12, 13}', '{10, 11, 12, 13}'), ('{10, 11, 12, 13}', '{14}'), ('{1}', '{2, 3}')]
def sortForKeys(tup1,tup2):
        tup1_first=tup1[0]  # '{10, 11, 12, 13}'
        tup2_first=tup2[0]  # '{1}'
        str1= tup1_first.replace('{','').replace('}','').split(',')
        str2= tup2_first.replace('{','').replace('}','').split(',')

        # 把他们变成int，然后逐个数比较
        int1 = list(map(lambda x:int(x),str1))
        int2 = list(map(lambda x:int(x),str2))
        minlen = min(len(str1),len(str2))

        # 首先较小的那个排前面
        # return -1 表示 tup1排tup2前面
        for i in range(minlen):
            if int1[i]<int2[i]:
                return -1
            elif int1[i]==int2[i]:
                return 0
            else:
                return 1
        if len(str1)<len(str2):
            return -1
        else:
            return 1



class DFANode(object):

    def __init__(self):
        self.startSet=set()
        self.endSetList=[]
        self.startState=0
        self.endState=0
        self.edgeDict={}
        self.allSetList=[]
        self.miniTupList=[]    #因为最小化会出现 (1,1):a ; (1,2):b 这样会覆盖前一个，所以我们用tup和list存储就算了
        self.miniStartState=0  #最小化后的初态
        self.miniEndStateList=[]  #最小化后的终态


    def initialize(self,startState:int,endState:int):
        self.startState=startState
        self.endState=endState

    def addEdgeDict(self,setOne:set,setTwo:set,edgeValue:str):
        strOne=str(setOne)
        strTwo=str(setTwo)
        self.edgeDict[(strOne,strTwo)]= edgeValue
        if self.startState in setOne:
            self.startSet=setOne

        if self.endState in setOne:
            if (setOne in self.endSetList)==False:
                self.endSetList.append(setOne)

        if self.endState in setTwo:
            if( setTwo in self.endSetList)==False:
                self.endSetList.append(setTwo)

        if (setOne in self.allSetList)==False:
            self.allSetList.append(setOne)
        if (setTwo in self.allSetList)==False:
            self.allSetList.append(setTwo)

    #这里的状态都是集合。
    #DFA的最小化，就是看每两个状态是否相等，如果相等，则转化为小的那个状态
    #然后初态为原本的初态所转成的状态，终态集合也转化为相应转成的状态
    def minimize(self):

        isVisited=set()
        set2int={}
        int2set=[]

        # edgeDict为{('{1, 2, 4}', '{2, 3, 4}'): 'a', ('{2, 3, 4}', '{2, 3, 4}'): 'a'}
        #
        # 遍历边，把每个集合 key0，key1 变成 数字，对应起来   set2int[str]=int   代表某个集合str化后，变成一个数字。
        # 得到： 已知集合的str，可得到代表这个集合的数字
        #
        # 同时， int2set又把数字和集合对应起来
        # 得到： 已知某个数字，可得到对应的集合
        cnt=0
        keys=self.edgeDict.keys()
        keys=list(keys)
        print(type(keys[0]))
        keys=sorted(keys,key=functools.cmp_to_key(sortForKeys))
        print('keys为:',keys)
        for key in keys:
            value=self.edgeDict[key]
            key0,key1=key[0],key[1]
            if (key0 in isVisited)==False:
                isVisited.add(key0)
                set2int[key0]=cnt
                int2set.append(key0)
                cnt=cnt+1
            if (key1 in isVisited)==False:
                isVisited.add(key1)
                set2int[key1]=cnt
                int2set.append(key1)
                cnt=cnt+1

        #equalList很重要，表示哪些 集合是相等的，equallist下标为 某个集合代表的数字。 equallist内容为 这个集合转化成哪个最小集合。
        #设置原始值为-2
        equalList=[-2 for i in range(cnt)]


        #Cn2每两个进行配对，查看究竟是不是同一个状态。
        #如果是，则大的那个状态等同小的那个状态
        #程序上表示为：  equalList[大状态]=小状态， 相当于parent
        #如果没有相等的， equalList【i】=i
        for i in range(cnt-1):
            for j in range(i+1,cnt):

                if equalList[i]==-2:
                    equalList[i]=i

                oneStr = int2set[i]
                twoStr = int2set[j]

                if self.isTwoSetEqual(oneStr,twoStr):
                    if equalList[j] == -2:
                        equalList[j]=i

        #最后一个如果没有匹配，会等于-2，那在另外给他赋一个值
        if equalList[len(equalList)-1]==-2:
            equalList[len(equalList)-1]=len(equalList)-1
        #
        # print('equalList 等价数组为：',equalList)


        # 仍未修复的bug，如果最小化后只有6个点，但序号有0-6 7个数字的bug
        # 要对 equallist进行进一步处理

        # 修复了 最小化后 序号可能大于圈数的现象
        # 对 equallist进行处理，把 0 1 2 3 4 4 6 变成 0 1 2 3 4 4 5即可
        # 只需遍历一遍，如果 本来应该序号为i，但是由于可能与前一个合并，所以 本来的序号只能搁浅给下一个
        # 所以 i==equallist[i] and shouldbe<=i时，equallist【i】赋值为shouldbe，shouldbe++
        # 如果 i！=equallist[i] 说明与前面合并，又以防与之合并的序号改了，所以 equallist[i]= equallist [ equallist[i] ]找到与它合并的变成的东西
        shouldbe=0
        for i in range(len(equalList)):
            if equalList[i]==i:
                if shouldbe<=i:
                    equalList[i]=shouldbe
                    shouldbe=shouldbe+1
            else:
                equalList[i]=equalList[ equalList[i]]


        #最后得到 equallist，这个equallist下标代表某个集合，内容代表这个集合转化成哪一个

        #遍历 edgeDict，用数字代替集合
        #遍历所有边，（集合，集合，边值）对应起来，然后转化成 （数字，数字，边值）
        #排除重复的。  存储到 miniTupleList中
        #初态终态也一样，本来是集合，变成集合对应的数字即可
        newTupList=[]
        for key,thisvalue in self.edgeDict.items():
            oneStr,twoStr = key[0],key[1]
            oneInt,twoInt = set2int[oneStr] , set2int[twoStr]
            oneInt,twoInt = equalList[oneInt], equalList[twoInt]

            #因为只是检验重复，随便检验即可，所以只用tuple就算了
            tup=(oneInt,twoInt,thisvalue)
            if (tup in newTupList)==False:
                newTupList.append(tup)

        endStateList= [ equalList[set2int[str(sset)]] for sset in self.endSetList]
        self.miniEndStateList=endStateList
        # print('最小化后：终态有',endStateList)


        print('equalist为:',equalList)
        #最小化后的初态，就是  初态的集合变成int，然后看看它与哪个最小的状态相等，或是它自己
        self.miniStartState= equalList[set2int[str(self.startSet)]]
        print('最小化后为',newTupList)
        self.miniTupList=newTupList













    #判断两个状态是否相等
    #遍历所有边值，每一次边值设立一个set，如果一次边值遍历完后，两者的set不相同，则return false。
    #最后return True
    def isTwoSetEqual(self,strOne:str,strTwo:str):

        edgeValueSet=set()

        for key,value in self.edgeDict.items():
            edgeValueSet.add(value)

        for value in edgeValueSet:
            oneToset=set()
            twoToSet=set()
            for key,thisvalue in self.edgeDict.items():
                if value==thisvalue and key[0]==strOne:
                    oneToset.add(key[1])
                if value==thisvalue and key[0]==strTwo:
                    twoToSet.add(key[1])
            if oneToset != twoToSet:
                return False
        return True





