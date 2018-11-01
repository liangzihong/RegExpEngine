
//提供给编译原理作业的样板：按照这个替代字符串，即可得到所要 解析的cpp代码
#include<iostream>
#include<string>
using namespace std;
    
    int table[7][5] = {{1, 7, 7, 7, 7},{7, 2, 7, 7, 7},{7, 7, 3, 7, 7},{7, 7, 7, 4, 7},{4, 6, 7, 7, 7},{7, 7, 7, 7, 7},{7, 7, 7, 7, 6}};
int maxState = 7;
int cntValue = 5;
char values[] = {  'a', 'b', 'c', 'd', 'f'  };
string s= "abcd(a*bf)" ;
int endStateList[] = { 6 };

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
    
    
    