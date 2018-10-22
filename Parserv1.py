import ParseRegExp as pre
import NFANodeToDFANode as nfa2dfa
import PaintDFA as pdfa
import PaintNFA as pnfa
import ToCode
# from NFANode import NFANode

if __name__=="__main__":

    re="a(a|b)*"
    nfanode= pre.parseReToNFANode(re)
    dfanode=nfa2dfa.FromNFAToDFA(nfanode)

    pnfa.paintNfa(nfanode)
    pdfa.paintDFA(dfanode)

    dfanode.minimize()
    pdfa.paintMinimize(dfanode)
    ToCode.generateCode(dfanode,re)

