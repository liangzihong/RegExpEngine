
//�ṩ������ԭ����ҵ�����壺�����������ַ��������ɵõ���Ҫ ������cpp����
#include<iostream>
#include<string>
using namespace std;
    
    int table[2][2] = {{1, 2},{1, 1}};
int maxState = 2;
int cntValue = 2;
char values[] = {  'a', 'b'  };
string s= "a(a|b)*" ;
int endStateList[] = { 1, 1, 1 };

    //���ݶ�άת������� values ��ԭ�����ַ���
//ȥ�ж��Ƿ�
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

		//��������ĸ�����в�ѯ����û��
		if (colInd == valuesSize)
			return false;

		rowInd=table[rowInd][colInd];
		
		//���ȥ�Ľڵ���endState���ǾͲ�����
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
	cout << "�������������ʽ��" << s;
	string temp;
	while (cin >> temp)
	{
		if (accordToReExp(temp)) {
			cout << "����ַ�������������ʽ" << s<<endl;
		}
		else
			cout << "������" << endl;
	}
}
    
    
    