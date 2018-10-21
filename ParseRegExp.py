from NFANode import NFANode
import NFANodeOperation as no
import PaintNFA as pnfa






def parseReToNFANode(regExp:str):
    nodeStack=[]
    charStack=[]
    symbolStack=[]

    # a='a(a|b)c(bc|a)'
    # s=""     #a+(a|b)*+c+(b+c|a)*
    #
    # a='a*b*c(a|b)*'
    s=""
    #先处理字符串，使 每个字母，如果它下一个字符是字母或者(；或者 对于每个)和*，它的下一个字符是字母或者(，则在它后面加个+号
    #此时这个字符串就变成一个 类似四则运算。此时再用逆波兰
    for i in range(len(regExp)):
        ch=regExp[i]
        s=s+ch
        if( ch.isalpha() or ch==')' or ch=='*'):
            if(i+1<len(regExp) and (regExp[i + 1] == '(' or regExp[i + 1].isalpha())):
                s=s+'+'
    # print(s)


    for i in range(len(s)):
        ch= s[i]

        #如果上一个符号比当前符号同级或高级，上一个符号运算
        #如果上一个符号比当前符号低级，则当前符号入站
        # * > ( > + > | > )
        if(ch.isalpha()):

            node=NFANode()
            node.initialize(ch)
            nodeStack.append(node)
            charStack.append(ch)

        elif (ch =='('):
            # 比+号高级或同级，又能运算的，只有*号，而*自己会运算
            symbolStack.append('(')
            pass
        elif (ch=='+'):
            #比+号高级或同级，又能运算的，只有+号
            if(len(symbolStack)>0):
                lsymbol= symbolStack[len(symbolStack)-1]
                if( lsymbol=='+' and len(charStack)>1):
                    symbolStack.pop()
                    one=charStack.pop()
                    two=charStack.pop()
                    three=two+one
                    charStack.append(three)

                    #node的concat
                    node1=nodeStack.pop()
                    node2=nodeStack.pop()
                    node3=no.operation_Concat(node2,node1)
                    nodeStack.append(node3)

            symbolStack.append('+')

        #直接拿一个出来运算
        elif(ch=='*'):

            one=charStack.pop()
            one=one+'*'
            charStack.append(one)

            # node的repeat
            node1 = nodeStack.pop()
            node3 = no.operation_Repeat(node1)
            nodeStack.append(node3)



        #直至遇到（，才收手
        elif( ch==')'):
            lsymbol = symbolStack.pop()
            while( lsymbol!='('):
                # print(lsymbol)
                if (lsymbol == '+' and len(charStack) > 1):
                    one = charStack.pop()
                    two = charStack.pop()
                    three = two + one
                    charStack.append(three)

                    #node的concat
                    node1=nodeStack.pop()
                    node2=nodeStack.pop()
                    node3=no.operation_Concat(node2,node1)
                    nodeStack.append(node3)


                elif (lsymbol == '|' and len(charStack) > 1):
                    one = charStack.pop()
                    two = charStack.pop()
                    three = two + '|' + one
                    charStack.append(three)


                    #node的or
                    node1=nodeStack.pop()
                    node2=nodeStack.pop()
                    node3=no.operation_Or(node2,node1)
                    nodeStack.append(node3)

                lsymbol=symbolStack.pop()

        elif (ch=='|'):
            #比+号高级或同级，又能运算的，只有+和|号
            if(len(symbolStack)>0):
                lsymbol=symbolStack[len(symbolStack)-1]
                if( lsymbol=='+' and len(charStack)>1):
                    symbolStack.pop()
                    one=charStack.pop()
                    two=charStack.pop()
                    three=two+one
                    charStack.append(three)


                    #node的concat
                    node1=nodeStack.pop()
                    node2=nodeStack.pop()
                    node3=no.operation_Concat(node2,node1)
                    nodeStack.append(node3)


                elif(lsymbol=='|' and len(charStack)>1):
                    symbolStack.pop()
                    one=charStack.pop()
                    two=charStack.pop()
                    three=two+'|'+one
                    charStack.append(three)

                    # node的or
                    node1 = nodeStack.pop()
                    node2 = nodeStack.pop()
                    node3 = no.operation_Or(node2, node1)
                    nodeStack.append(node3)


            symbolStack.append('|')

    while(len(charStack)>1):
        lsymbol = symbolStack[len(symbolStack) - 1]
        if (lsymbol == '+' and len(charStack) > 1):
            symbolStack.pop()
            one = charStack.pop()
            two = charStack.pop()
            three = two + one
            charStack.append(three)

            # node的concat
            node1 = nodeStack.pop()
            node2 = nodeStack.pop()
            node3 = no.operation_Concat(node2, node1)
            nodeStack.append(node3)

        elif (lsymbol == '|' and len(charStack) > 1):
            symbolStack.pop()
            one = charStack.pop()
            two = charStack.pop()
            three = two + '|' + one
            charStack.append(three)

            # node的or
            node1 = nodeStack.pop()
            node2 = nodeStack.pop()
            node3 = no.operation_Or(node2, node1)
            nodeStack.append(node3)

    # print(charStack[0])
    # pnfa.paintNfa(nodeStack[0])
    return nodeStack[0]


# if __name__=="__main__":
#     node = parseReToNFANode("a*b|c")
#     pnfa.paintNfa(node)