from antlr4 import *
from SDLLexer import SDLLexer
from SDLParser import SDLParser
from MyErrorListener import MyErrorListener
from MyVisitor import MyVisitor
 
def main():
    input_stream = FileStream('test.sdl', encoding='utf8')
    lexer = SDLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SDLParser(stream)

    parser.removeErrorListeners()  
    parser.addErrorListener(MyErrorListener())

    tree = parser.program()
    visitor = MyVisitor()
    output = visitor.visit(tree)
    #print(output)

 
if __name__ == '__main__':
    main()
    