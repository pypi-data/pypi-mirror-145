# Generated from CyanaMRParser.g4 by ANTLR 4.9
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\b")
        buf.write("q\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2\3\2")
        buf.write("\3\2\3\2\7\2\37\n\2\f\2\16\2\"\13\2\3\2\3\2\3\3\6\3\'")
        buf.write("\n\3\r\3\16\3(\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\5\6\5")
        buf.write("\64\n\5\r\5\16\5\65\3\6\3\6\3\6\3\6\3\6\3\6\3\7\6\7?\n")
        buf.write("\7\r\7\16\7@\3\7\6\7D\n\7\r\7\16\7E\3\b\3\b\3\b\3\b\3")
        buf.write("\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\n\6\n")
        buf.write("Y\n\n\r\n\16\nZ\3\n\6\n^\n\n\r\n\16\n_\3\13\3\13\3\13")
        buf.write("\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r")
        buf.write("\2\2\16\2\4\6\b\n\f\16\20\22\24\26\30\2\3\3\2\3\4\2n\2")
        buf.write(" \3\2\2\2\4&\3\2\2\2\6*\3\2\2\2\b\63\3\2\2\2\n\67\3\2")
        buf.write("\2\2\f>\3\2\2\2\16G\3\2\2\2\20L\3\2\2\2\22X\3\2\2\2\24")
        buf.write("a\3\2\2\2\26f\3\2\2\2\30n\3\2\2\2\32\37\5\4\3\2\33\37")
        buf.write("\5\b\5\2\34\37\5\f\7\2\35\37\5\22\n\2\36\32\3\2\2\2\36")
        buf.write("\33\3\2\2\2\36\34\3\2\2\2\36\35\3\2\2\2\37\"\3\2\2\2 ")
        buf.write("\36\3\2\2\2 !\3\2\2\2!#\3\2\2\2\" \3\2\2\2#$\7\2\2\3$")
        buf.write("\3\3\2\2\2%\'\5\6\4\2&%\3\2\2\2\'(\3\2\2\2(&\3\2\2\2(")
        buf.write(")\3\2\2\2)\5\3\2\2\2*+\7\3\2\2+,\7\5\2\2,-\7\5\2\2-.\7")
        buf.write("\3\2\2./\7\5\2\2/\60\7\5\2\2\60\61\5\30\r\2\61\7\3\2\2")
        buf.write("\2\62\64\5\n\6\2\63\62\3\2\2\2\64\65\3\2\2\2\65\63\3\2")
        buf.write("\2\2\65\66\3\2\2\2\66\t\3\2\2\2\678\7\3\2\289\7\5\2\2")
        buf.write("9:\7\5\2\2:;\5\30\r\2;<\5\30\r\2<\13\3\2\2\2=?\5\16\b")
        buf.write("\2>=\3\2\2\2?@\3\2\2\2@>\3\2\2\2@A\3\2\2\2AC\3\2\2\2B")
        buf.write("D\5\20\t\2CB\3\2\2\2DE\3\2\2\2EC\3\2\2\2EF\3\2\2\2F\r")
        buf.write("\3\2\2\2GH\7\3\2\2HI\7\4\2\2IJ\7\4\2\2JK\7\3\2\2K\17\3")
        buf.write("\2\2\2LM\7\3\2\2MN\7\5\2\2NO\7\5\2\2OP\7\3\2\2PQ\7\5\2")
        buf.write("\2QR\7\5\2\2RS\5\30\r\2ST\5\30\r\2TU\5\30\r\2UV\7\3\2")
        buf.write("\2V\21\3\2\2\2WY\5\24\13\2XW\3\2\2\2YZ\3\2\2\2ZX\3\2\2")
        buf.write("\2Z[\3\2\2\2[]\3\2\2\2\\^\5\26\f\2]\\\3\2\2\2^_\3\2\2")
        buf.write("\2_]\3\2\2\2_`\3\2\2\2`\23\3\2\2\2ab\7\3\2\2bc\7\4\2\2")
        buf.write("cd\7\4\2\2de\7\3\2\2e\25\3\2\2\2fg\7\3\2\2gh\7\5\2\2h")
        buf.write("i\7\5\2\2ij\5\30\r\2jk\5\30\r\2kl\5\30\r\2lm\7\3\2\2m")
        buf.write("\27\3\2\2\2no\t\2\2\2o\31\3\2\2\2\n\36 (\65@EZ_")
        return buf.getvalue()


class CyanaMRParser ( Parser ):

    grammarFileName = "CyanaMRParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "Integer", "Float", "Simple_name", "SPACE", 
                      "COMMENT", "LINE_COMMENT" ]

    RULE_cyana_mr = 0
    RULE_distance_restraints = 1
    RULE_distance_restraint = 2
    RULE_torsion_angle_restraints = 3
    RULE_torsion_angle_restraint = 4
    RULE_rdc_restraints = 5
    RULE_rdc_parameter = 6
    RULE_rdc_restraint = 7
    RULE_pcs_restraints = 8
    RULE_pcs_parameter = 9
    RULE_pcs_restraint = 10
    RULE_number = 11

    ruleNames =  [ "cyana_mr", "distance_restraints", "distance_restraint", 
                   "torsion_angle_restraints", "torsion_angle_restraint", 
                   "rdc_restraints", "rdc_parameter", "rdc_restraint", "pcs_restraints", 
                   "pcs_parameter", "pcs_restraint", "number" ]

    EOF = Token.EOF
    Integer=1
    Float=2
    Simple_name=3
    SPACE=4
    COMMENT=5
    LINE_COMMENT=6

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Cyana_mrContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CyanaMRParser.EOF, 0)

        def distance_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Distance_restraintsContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Distance_restraintsContext,i)


        def torsion_angle_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Torsion_angle_restraintsContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Torsion_angle_restraintsContext,i)


        def rdc_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Rdc_restraintsContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Rdc_restraintsContext,i)


        def pcs_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Pcs_restraintsContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Pcs_restraintsContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_cyana_mr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCyana_mr" ):
                listener.enterCyana_mr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCyana_mr" ):
                listener.exitCyana_mr(self)




    def cyana_mr(self):

        localctx = CyanaMRParser.Cyana_mrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_cyana_mr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CyanaMRParser.Integer:
                self.state = 28
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 24
                    self.distance_restraints()
                    pass

                elif la_ == 2:
                    self.state = 25
                    self.torsion_angle_restraints()
                    pass

                elif la_ == 3:
                    self.state = 26
                    self.rdc_restraints()
                    pass

                elif la_ == 4:
                    self.state = 27
                    self.pcs_restraints()
                    pass


                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 33
            self.match(CyanaMRParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_restraintsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def distance_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Distance_restraintContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Distance_restraintContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_distance_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_restraints" ):
                listener.enterDistance_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_restraints" ):
                listener.exitDistance_restraints(self)




    def distance_restraints(self):

        localctx = CyanaMRParser.Distance_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_distance_restraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 35
                    self.distance_restraint()

                else:
                    raise NoViableAltException(self)
                self.state = 38 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_restraintContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Integer)
            else:
                return self.getToken(CyanaMRParser.Integer, i)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Simple_name)
            else:
                return self.getToken(CyanaMRParser.Simple_name, i)

        def number(self):
            return self.getTypedRuleContext(CyanaMRParser.NumberContext,0)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_distance_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_restraint" ):
                listener.enterDistance_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_restraint" ):
                listener.exitDistance_restraint(self)




    def distance_restraint(self):

        localctx = CyanaMRParser.Distance_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_distance_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(CyanaMRParser.Integer)
            self.state = 41
            self.match(CyanaMRParser.Simple_name)
            self.state = 42
            self.match(CyanaMRParser.Simple_name)
            self.state = 43
            self.match(CyanaMRParser.Integer)
            self.state = 44
            self.match(CyanaMRParser.Simple_name)
            self.state = 45
            self.match(CyanaMRParser.Simple_name)
            self.state = 46
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Torsion_angle_restraintsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def torsion_angle_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Torsion_angle_restraintContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Torsion_angle_restraintContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_torsion_angle_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTorsion_angle_restraints" ):
                listener.enterTorsion_angle_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTorsion_angle_restraints" ):
                listener.exitTorsion_angle_restraints(self)




    def torsion_angle_restraints(self):

        localctx = CyanaMRParser.Torsion_angle_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_torsion_angle_restraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 48
                    self.torsion_angle_restraint()

                else:
                    raise NoViableAltException(self)
                self.state = 51 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Torsion_angle_restraintContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self):
            return self.getToken(CyanaMRParser.Integer, 0)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Simple_name)
            else:
                return self.getToken(CyanaMRParser.Simple_name, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.NumberContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_torsion_angle_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTorsion_angle_restraint" ):
                listener.enterTorsion_angle_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTorsion_angle_restraint" ):
                listener.exitTorsion_angle_restraint(self)




    def torsion_angle_restraint(self):

        localctx = CyanaMRParser.Torsion_angle_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_torsion_angle_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(CyanaMRParser.Integer)
            self.state = 54
            self.match(CyanaMRParser.Simple_name)
            self.state = 55
            self.match(CyanaMRParser.Simple_name)
            self.state = 56
            self.number()
            self.state = 57
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Rdc_restraintsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def rdc_parameter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Rdc_parameterContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Rdc_parameterContext,i)


        def rdc_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Rdc_restraintContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Rdc_restraintContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_rdc_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRdc_restraints" ):
                listener.enterRdc_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRdc_restraints" ):
                listener.exitRdc_restraints(self)




    def rdc_restraints(self):

        localctx = CyanaMRParser.Rdc_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_rdc_restraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 59
                    self.rdc_parameter()

                else:
                    raise NoViableAltException(self)
                self.state = 62 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

            self.state = 65 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 64
                    self.rdc_restraint()

                else:
                    raise NoViableAltException(self)
                self.state = 67 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Rdc_parameterContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Integer)
            else:
                return self.getToken(CyanaMRParser.Integer, i)

        def Float(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Float)
            else:
                return self.getToken(CyanaMRParser.Float, i)

        def getRuleIndex(self):
            return CyanaMRParser.RULE_rdc_parameter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRdc_parameter" ):
                listener.enterRdc_parameter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRdc_parameter" ):
                listener.exitRdc_parameter(self)




    def rdc_parameter(self):

        localctx = CyanaMRParser.Rdc_parameterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_rdc_parameter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(CyanaMRParser.Integer)
            self.state = 70
            self.match(CyanaMRParser.Float)
            self.state = 71
            self.match(CyanaMRParser.Float)
            self.state = 72
            self.match(CyanaMRParser.Integer)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Rdc_restraintContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Integer)
            else:
                return self.getToken(CyanaMRParser.Integer, i)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Simple_name)
            else:
                return self.getToken(CyanaMRParser.Simple_name, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.NumberContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_rdc_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRdc_restraint" ):
                listener.enterRdc_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRdc_restraint" ):
                listener.exitRdc_restraint(self)




    def rdc_restraint(self):

        localctx = CyanaMRParser.Rdc_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_rdc_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(CyanaMRParser.Integer)
            self.state = 75
            self.match(CyanaMRParser.Simple_name)
            self.state = 76
            self.match(CyanaMRParser.Simple_name)
            self.state = 77
            self.match(CyanaMRParser.Integer)
            self.state = 78
            self.match(CyanaMRParser.Simple_name)
            self.state = 79
            self.match(CyanaMRParser.Simple_name)
            self.state = 80
            self.number()
            self.state = 81
            self.number()
            self.state = 82
            self.number()
            self.state = 83
            self.match(CyanaMRParser.Integer)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pcs_restraintsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pcs_parameter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Pcs_parameterContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Pcs_parameterContext,i)


        def pcs_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.Pcs_restraintContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.Pcs_restraintContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_pcs_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPcs_restraints" ):
                listener.enterPcs_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPcs_restraints" ):
                listener.exitPcs_restraints(self)




    def pcs_restraints(self):

        localctx = CyanaMRParser.Pcs_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_pcs_restraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 85
                    self.pcs_parameter()

                else:
                    raise NoViableAltException(self)
                self.state = 88 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 91 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 90
                    self.pcs_restraint()

                else:
                    raise NoViableAltException(self)
                self.state = 93 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pcs_parameterContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Integer)
            else:
                return self.getToken(CyanaMRParser.Integer, i)

        def Float(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Float)
            else:
                return self.getToken(CyanaMRParser.Float, i)

        def getRuleIndex(self):
            return CyanaMRParser.RULE_pcs_parameter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPcs_parameter" ):
                listener.enterPcs_parameter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPcs_parameter" ):
                listener.exitPcs_parameter(self)




    def pcs_parameter(self):

        localctx = CyanaMRParser.Pcs_parameterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_pcs_parameter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.match(CyanaMRParser.Integer)
            self.state = 96
            self.match(CyanaMRParser.Float)
            self.state = 97
            self.match(CyanaMRParser.Float)
            self.state = 98
            self.match(CyanaMRParser.Integer)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pcs_restraintContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Integer)
            else:
                return self.getToken(CyanaMRParser.Integer, i)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(CyanaMRParser.Simple_name)
            else:
                return self.getToken(CyanaMRParser.Simple_name, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CyanaMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(CyanaMRParser.NumberContext,i)


        def getRuleIndex(self):
            return CyanaMRParser.RULE_pcs_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPcs_restraint" ):
                listener.enterPcs_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPcs_restraint" ):
                listener.exitPcs_restraint(self)




    def pcs_restraint(self):

        localctx = CyanaMRParser.Pcs_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_pcs_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(CyanaMRParser.Integer)
            self.state = 101
            self.match(CyanaMRParser.Simple_name)
            self.state = 102
            self.match(CyanaMRParser.Simple_name)
            self.state = 103
            self.number()
            self.state = 104
            self.number()
            self.state = 105
            self.number()
            self.state = 106
            self.match(CyanaMRParser.Integer)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(CyanaMRParser.Float, 0)

        def Integer(self):
            return self.getToken(CyanaMRParser.Integer, 0)

        def getRuleIndex(self):
            return CyanaMRParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = CyanaMRParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            _la = self._input.LA(1)
            if not(_la==CyanaMRParser.Integer or _la==CyanaMRParser.Float):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





