
from DFANode import DFANode

def generateCode(node:DFANode,regExp:str):

    tupList= node.miniTupList
    valuesList=[]
    stateList=[]
    cntValue=0
    cntState=0
    #对valueList赋值，看看有多少条不同的边
    for tup in tupList:
        value=tup[2]
        if (value in valuesList)==False:
            valuesList.append(value)
        #找到有多少个状态
        if (tup[0] in stateList)==False:
            stateList.append(tup[0])
        if (tup[1] in stateList)==False:
            stateList.append(tup[1])
    cntValue=len(valuesList)
    maxState=max(stateList)+1
    cntState=len(stateList)

    valueDict= dict(zip(valuesList,range(len(valuesList))))
    #生成一个二维数组
    table=[ [maxState for j in range(cntValue)] for i in range(maxState)]
    for tup in tupList:
        fp,tp,thisValue=tup[0],tup[1],tup[2]
        rowInd, colInd=fp,valueDict[thisValue]
        table[rowInd][colInd]=tp

    # print('生成代码的二维表：')
    # print(table)


    Infrontcode="""
//提供给编译原理作业的样板：按照这个替代字符串，即可得到所要 解析的cpp代码
#include<iostream>
#include<string>
using namespace std;
    
    """


    codeone_tmps='{'
    for i in range(len(table)):
        if i!=0:
            codeone_tmps=codeone_tmps+','
        codeone_tmps=codeone_tmps+str(table[i]).replace('[','{').replace(']','}')
    codeone_tmps=codeone_tmps+'}'
    #tmps为{{1, 2},{1, 1}}
    #把数组内容变成字符串

    codeone="int table[%d][%d] = %s;\n" % (maxState,cntValue,codeone_tmps)
    codetwo="int maxState = %d;\n" % (maxState)
    codethree="int cntValue = %d;\n" % (cntValue)
    codefour="char values[] = { %s };\n" % (str(valuesList).replace('[',' ').replace(']',' '))
    codefive='string s= "%s" ;\n' % (regExp)

    codesix_tmps= str(node.miniEndStateList).replace('[',' ').replace(']',' ')
    # print(codesix_tmps)
    codesix= 'int endStateList[] = {%s};\n' % (codesix_tmps)



    Middlecoide=codeone+codetwo+codethree+codefour+codefive+codesix
    # print(Middlecoide)

    Behindcode="""
    //根据二维转化数组和 values 和原本的字符串
//去判断是否
    bool accordToReExp(string temp)
{
	int rowInd = 0;
	int valuesSize =cntValue;
	for (int i = 0; i < temp.length(); i++) {
		
		int colInd = valuesSize;
		char ch = temp[i];


		for (int j = 0; j < valuesSize; j++) {
			if (ch == values[j])
				colInd = j;
		}

		//如果这个字母在所有查询表中没有
		if (colInd == valuesSize)
			return false;

		rowInd=table[rowInd][colInd];
		
		//如果去的节点是endState，那就不行了
		if (rowInd == maxState)
			return false;
	}
    for (int i = 0; i < sizeof(endStateList) / sizeof(int); i++)
		if (endStateList[i] == rowInd)
			return true;

	return false;
}


int main()
{
	cout << "你输入的正则表达式是" << s;
	string temp;
	while (cin >> temp)
	{
		if (accordToReExp(temp)) {
			cout << "这个字符串符合正则表达式" << s<<endl;
		}
		else
			cout << "不符合" << endl;
	}
}
    
    
    """
    allCppCode=Infrontcode+Middlecoide+Behindcode
    # print(allCppCode)

    #生成cpp代码
    f=open('cppcode.cpp','w')
    f.write(allCppCode)
    f.close()