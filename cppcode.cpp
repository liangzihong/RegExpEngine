
//�ṩ������ԭ����ҵ�����壺�����������ַ��������ɵõ���Ҫ ������cpp����
#include<iostream>
#include<string>
using namespace std;
    
    int table[7][5] = {{1, 7, 7, 7, 7},{7, 2, 7, 7, 7},{7, 7, 3, 7, 7},{7, 7, 7, 4, 7},{4, 6, 7, 7, 7},{7, 7, 7, 7, 7},{7, 7, 7, 7, 6}};
int maxState = 7;
int cntValue = 5;
char values[] = {  'a', 'b', 'c', 'd', 'f'  };
string s= "abcd(a*bf)" ;
int endStateList[] = { 6 };

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
    
    
    