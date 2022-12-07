from parser import ll1
from lexer import get_tokens

ruta = "Tests/test1.txt"
root, _ = ll1(ruta)


Codigo=""
varn=""
sivar=""
sinovar=""


def decla(node):
    global Codigo
    #if node.symbol.symbol == "TYPE":
    ##CREACION DE VARIABLE TIPO NUMERICO
    if node.symbol.symbol=="numerico" and node.father.father.children[1].symbol.symbol=="id":
            #print(Codigo)
            Codigo=Codigo+"   var_"
            Codigo=Codigo+str(node.father.father.children[1].lexeme)
            Codigo=Codigo+":.word 0:1 \n"
            #print(Codigo)
            print(node.father.father.children[2].children[1].children[1].children[0].symbol.symbol)

    ##CREACION DE VARIABLE TIPO CADENA
    if node.symbol.symbol=="cadena" and node.father.father.children[1].symbol.symbol=="id":

            Codigo=Codigo+"   var_"
            Codigo=Codigo+str(node.father.father.children[1].lexeme)
            Codigo=Codigo+":.word 0:1 \n"
            #print(Codigo)
    for child in node.children:
            decla(child)
#decla(root)

Codigo=Codigo+".data \n"
decla(root)
Codigo=Codigo+".text \n"
Codigo=Codigo+"main: "
text_file = open("Codigo.txt", "w")
text_file.write(Codigo)
text_file.close()
