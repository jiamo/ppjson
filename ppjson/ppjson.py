from sly import Lexer, Parser
import sys
from copy import deepcopy


class JsonLexer(Lexer):

    tokens = {
        LSBRACKET,
        RSBRACKET,
        LBRACE,
        RBRACE,
        COLON,
        STRING,
        SINGLE_STRING,
        CONSTANT,
        COMMA,
        INT,
        FLOAT,
        LITERRAL_VALUE,
        TRUE,
        FALSE,
        NULL,
    }
    # WS = r'[ \t\n\r]+'
    # todo how to do it
    # literals = { '=', '+', '-', '*', '/', '(', ')' }
    ignore = ' \t\n\r'
    # Tokens
    LITERRAL_VALUE = r'[a-zA-Z_][a-zA-Z0-9_]*'
    LITERRAL_VALUE['true'] = TRUE
    LITERRAL_VALUE['false'] = FALSE
    LITERRAL_VALUE['null'] = NULL


    LSBRACKET = r'\['
    RSBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COLON = r':'
    COMMA = r','

    @_(r'"([ !#-\[\]-\U0010ffff]+|\\(["\/\\bfnrt]|u[0-9A-Fa-f]{4}))*"')
    def STRING(self, t):
        t.value = str(t.value[1:-1])
        return t

    @_(r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([Ee][+-]?[0-9]+)?')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'-?(0|[1-9][0-9]*)')
    def INT(self, t):
        t.value = int(t.value)
        return t

    # @_(r"'([^'\n]|(\\'))*'")
    # def STRING(self, t):
    #     t.value = str(t.value[1:-1])
    #     return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        raise Exception(str(t))


class JsonParser(Parser):
    debugfile = 'parser.out'

    tokens = JsonLexer.tokens
    ARRAY = 1
    DICT = 2

    def __init__(self):
        self.names = {}
        self.value = None
        self.json_type = None
        self.json_value = None

    @_('value')
    def json_text(self, p):
        print("json_text")
        self.json_value = p.value
        print("self.json_value", p.value)

    @_('')
    def empty(self, p):
        print("empty")

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

    @_('TRUE')
    def value(self, p):
        print("LITERRAL_VALUE", p)
        return True

    @_('FALSE')
    def value(self, p):
        print("LITERRAL_VALUE", p)
        return False

    @_('NULL')
    def value(self, p):
        print("LITERRAL_VALUE", p)
        return None

    @_('INT')
    def value(self, p):
        return p.INT

    @_('FLOAT')
    def value(self, p):
        return p.FLOAT

    @_('LSBRACKET')
    def begin_array(self, p):
        print("begin_array")

    @_('RSBRACKET')
    def end_array(self, p):
        print("end_array")

    @_('LBRACE')
    def begin_object(self, p):
        print("begin_object")

    @_('RBRACE')
    def end_object(self, p):
        print("end_object")

    @_('begin_object [ member_list ] end_object')
    def object(self, p):
        # TODO simple the process may be can just return the p.memlist
        print("object --- is", p.member_list)
        result = {}
        if isinstance(p.member_list, list):
            for value in p.member_list:
                result.update(value)
        elif p.member_list is not None:
            result = p.member_list
        return result

    @_('begin_array [ value_list ] end_array')
    def array(self, p):
        # This is not very good. because the value_list may not be list!
        result = []
        if isinstance(p.value_list, list):
            result = p.value_list
        elif p.value_list is not None:
            result.append(p.value_list)
        return result

    @_('member')
    def member_list(self, p):
        print("member_list-member ---", p.member)
        return p.member

    @_('member_list COMMA member')
    def member_list(self, p):
        print("member_list - member")
        result = []
        if isinstance(p.member_list, list):
            p.member_list.append(p.member)
            result = p.member_list
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

        result = []
        if isinstance(p.value_list, list):
            p.value_list.append(p.value)
            result = p.value_list
        else:
            result = [p.value_list, p.value]
        print("array-list", p.value_list, p.value, 'r is ', result)
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

    def error(self, p):
        raise Exception(str(p))


def loads(s):

    lexer = JsonLexer()
    parser = JsonParser()
    tokens = lexer.tokenize(s)
    # print(list(tokens))
    parser.parse(tokens)
    return parser.json_value


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
