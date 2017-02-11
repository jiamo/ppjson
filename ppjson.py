from sly import Lexer, Parser
import sys
from copy import deepcopy

class JsonLexer(Lexer):

    tokens = {
        'LSBRACKET',
        'RSBRACKET',
        'LBRACE',
        'RBRACE',
        'COLON',
        'STRING',
        'CONSTANT',
        'COMMA',
        # 'VARIABLE',
        # 'KEYWORDS',
    }
    # WS = r'[ \t\n\r]+'
    # todo how to do it
    # literals = { '=', '+', '-', '*', '/', '(', ')' }
    ignore = " \t"
    # Tokens
    # NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    LSBRACKET = r'\['
    RSBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COLON = r':'
    COMMA = r','

    @_(r'"([^"\n]|(\\"))*"')
    def STRING(self, t):
        t.value = str(t.value[1:-1])
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, value):
        print("Illegal character '%s'" % value[0])
        self.index += 1


class JsonParser(Parser):
    debugfile = 'parser.out'

    tokens = JsonLexer.tokens
    ARRAY = 1
    DICT = 2

    def __init__(self):
        self.names = {}
        self.value = None
        self.json_type = None

    @_('value')
    def json_text(self, p):
        print("json_text")
        self.json_value = p.value
        print("self.json_value", p.value)

    @_('')
    def empty(self, p):
        print("empty")

    # @_('WS', 'empty')
    # def ws(self, p):
    #     print("ws")

    @_('object')
    def value(self, p):
        print("value-object:", p.object)
        return p.object

    @_('array')
    def value(self, p):
        print("value-array:", p.array)
        return p.array

    @_('STRING')
    def value(self, p):
        print("value-string")
        return p.STRING

    @_('LSBRACKET')
    def begin_array(self, p):
        print("begin_array")

    @_('RSBRACKET')
    def end_array(self, p):
        print("end_array")

    @_('LBRACE')
    def begin_object(self, p):
        print("begin_object")

    @_(' RBRACE ')
    def end_object(self, p):
        print("end_object")

    @_('begin_object member_list end_object ')
    def object(self, p):
        print("object")
        result = {}
        if isinstance(p.member_list, list):
            for value in p.member_list:
                result.update(value)
        else:
            result = p.member_list
        return result

    @_('begin_array value_list end_array')
    def array(self, p):
        # This is not very good. because the value_list may not be list!
        result = []
        if isinstance(p.value_list, list):
            result =  p.value_list
        else:
            result.append(p.value_list)
        return result

    # @_('member')
    # def member_list(self, p):
    #     print("member_list-member")

    @_('member')
    def member_list(self, p):
        print("member_list-member")
        return p.member

    @_('member_list COMMA member ')
    def member_list(self, p):
        print("member_list-member")
        result = []
        if isinstance(p.member_list, list):
            result = p.member_list.append(p.member)
        else:
            result = [p.member_list, p.member]
        return result

    # very same as member
    @_('value')
    def value_list(self, p):
        print("array-array")
        return p.value

    @_('value_list COMMA value')
    def value_list(self, p):
        print("array-list")
        result = []
        if isinstance(p.value_list, list):
            result = p.array.append(p.value)
        else:
            result = [p.value_list, p.value]
        return result

    @_('COLON')
    def name_separator(self, p):
        print("name_separator")

    @_('STRING name_separator value')
    def member(self, p):
        print("member, ", type(p.STRING), " ", p.STRING)
        return {
            p.STRING: p.value
        }

    # @_('expr "+" expr')
    # def expr(self, p):
    #     return p.expr0 + p.expr1
    #
    # @_('expr "-" expr')
    # def expr(self, p):
    #     return p.expr0 - p.expr1
    #
    # @_('expr "*" expr')
    # def expr(self, p):
    #     return p.expr0 * p.expr1
    #
    # @_('expr "/" expr')
    # def expr(self, p):
    #     return p.expr0 / p.expr1
    #
    # @_('"-" expr %prec UMINUS')
    # def expr(self, p):
    #     return -p.expr
    #
    # @_('"(" expr ")"')
    # def expr(self, p):
    #     return p.expr
    #
    # @_('NUMBER')
    # def expr(self, p):
    #     return p.NUMBER
    #
    # @_('NAME')
    # def expr(self, p):
    #     try:
    #         return self.names[p.NAME]
    #     except LookupError:
    #         print("Undefined name '%s'" % p.NAME)
    #         return 0


if __name__ == '__main__':
    lexer = JsonLexer()
    parser = JsonParser()
    while True:
        try:
            text = input('ppjson > ')
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)
            # debug_tokens = list(tokens)
            # for tok in debug_tokens:
            #     print(tok)
            #     sys.stdout.flush()
            parser.parse(tokens)

            print("value is {} and the python type is {}".format(
                parser.json_value, type(parser.json_value) ))
