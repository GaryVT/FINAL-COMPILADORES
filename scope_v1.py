import string
from lexer import get_tokens
from parser import ll1

ruta = "Tests/test1.txt"

root, _ = ll1(ruta)

class symbol_table_node:
  def __init__(self, identifier, typ, category, father = 'main', line = None):        
    self.identifier = identifier
    self.type = typ # tipo de dato
    self.category = category # funcion o variable
    self.line = line
    self.father = father # a q función pertenece

symbol_table = []
variables = []
funciones = []
tipos = []
tiposDIC = []
estado = True

def add_symbol(identifier, typ, category, current_function):
  node_symbol = symbol_table_node(identifier, typ, category, current_function)
  symbol_table.append(node_symbol)

def find_symbol(node):
    find=False
    for symbol in symbol_table:
        if symbol.identifier==node.lexeme and symbol.father == current_function:
            find=True
            break
    return find

def find_symbol2(identifier, father):
    for symbol in symbol_table:
        if symbol.identifier == identifier and symbol.father == father:
            return symbol

def remove_symbol(father):
    for symbol in symbol_table:
        if symbol.father==father and symbol.father != symbol.identifier:
            symbol_table.remove(symbol)
            remove_symbol(father)


##------------------------------------
def find_var_declaration(node):
  global current_function, estado
  ## Esta parte es para detectar la creación de una función
  if node.symbol.symbol == 'funcion':
    piv = node.father.children[1]
    current_function = piv.lexeme # obtenmos el nombre de la función

  ## Esta parte es para detectar la finalización de una función
  if node.symbol.symbol == 'der_llave' and node.father.children[0].symbol.symbol == 'funcion':
    print("Función terminada '", node.lexeme, "' en línea", node.line )
    remove_symbol(current_function)  # eliminar todos los simbolos de current_function
    current_function = 'Principal'
    
  ## Esta parte es para ver cuando hay un nombre de función o variable
  if node.symbol.symbol == 'id':
    #print("->", node.lexeme)

    ev_categoria = node.father.children[0]
    
    if(ev_categoria.symbol.symbol == 'id' and ev_categoria.lexeme not in variables):
      print("ERROR SEMÁNTICO: Línea", node.line, "Variable <",node.lexeme,"> no fué declarada.")

    if(ev_categoria.symbol.symbol == 'TYPE'):
      category = 'Variable'
      if(find_symbol(node)):
        print("ERROR SEMÁNTICO: Línea", node.line, "Variable <",node.lexeme,"> ya fue declarada anteriormente.")
      else:
        print("Variable <",node.lexeme, "> declarada en línea:",node.line)
        variables.append(node.lexeme)

        add_symbol( node.lexeme, ev_categoria.children[0].lexeme, category, current_function)


    if(ev_categoria.symbol.symbol == 'funcion'):
      category = 'Función'
      if(node.lexeme in funciones):
        print("ERROR SEMÁNTICO: Línea", node.line, "Función <",node.lexeme,"> ya fue declarada anteriormente.")
        estado = False
      else:
        print("Función <",node.lexeme, "> declarada en línea:",node.line)
        funciones.append(node.lexeme)
      
        add_symbol( node.lexeme, None, category, current_function)

  for child in node.children:
    if estado:
      find_var_declaration(child)

find_var_declaration(root)

def table_symbol():
  print("\n------------ Tabla de Símbolos ------------")
  for symbol in symbol_table:
    print(symbol.identifier, symbol.type, symbol.category, symbol.father)
table_symbol()

##Trabajar los tipos


def find(node):
    if node.symbol.symbol=='numero' and node.father.symbol.symbol=='EXP' and node.father.father.father.symbol.symbol=='DE':
        node.type=int
        node.visited=True
        node.father.type=int
        node.father.visited=True
        print("OJO 1 ",node.father.symbol.symbol,node.father.type, node.father.father.children[1].symbol.symbol)

        if node.father.type==int and node.father.father.children[0].symbol.symbol=='EXP' and node.father.father.children[1].symbol.symbol=="ASIG'":
            #print("ENTRO AL 1ER IF")
            node.father.father.father.type=int
            node.father.father.father.visited=True
            #print("OJO 2 ", node.father.father.father.type, node.father.father.father.symbol.symbol)
            
            if node.father.father.father.type==int and node.symbol.symbol=='numero':
                node.father.father.type=int
                node.father.father.visited=True
                #print("OJO 3 ",node.father.father.symbol.symbol,node.father.father.type)
            #print("VER - ",node.father.father.symbol.symbol, node.father.father.type)
        #print("VER 2 - ",)

        if node.father.father.father.father.symbol.symbol == "DECLA" and node.father.father.father.father.children[0].symbol.symbol=="TYPE" and node.father.father.father.father.children[0].children[0].symbol.symbol=="numerico" :
           node.father.father.father.father.type = int
           node.father.father.father.father.visited = True
           node.father.father.father.father.children[0].type = int
           node.father.father.father.father.children[0].visited = True
           print("NNNNN ->",node.father.father.father.father.children[0].type, node.father.father.father.father.children[0].symbol.symbol)

        print("MMMM -> ", node.father.father.father.father.symbol.symbol)
        if node.father.father.father.father.symbol.symbol=="DECLA" and node.father.father.father.father.children[0].symbol.symbol == "TYPE" and node.father.father.father.father.children[0].children[0].symbol.symbol=="numerico":
            #node.father.father.type=int
            #node.father.father.visited=True
            #print("OJO 4 ", node.father.father.father.father.children[1].lexeme, node.father.father.father.father.children[0].symbol.symbol)

            if node.father.father.father.type == int and node.type == int and node.father.father.father.father.children[0].type == int:
                #print("Es entero", node.father.father.father.symbol.symbol)
                print("AMBOS TIPOS EN LA DECLARACION SON IGUALES")

                nomNode_t1 = str(node.father.father.father.father.children[1].lexeme)
                typeNode_t1 = str(node.father.father.father.type)
                tiposDIC.append({'nombre': nomNode_t1, 'typeNode':typeNode_t1})
                tipos.append(node.father.father.father.type)

                nomNode_t2 = str(node.father.father.father.father.children[0].symbol.symbol)
                typeNode_2 = str(node.father.father.father.father.children[0].type)
                tiposDIC.append({'nombre': nomNode_t2, 'typeNode':typeNode_2})
                tipos.append(node.father.father.father.father.children[0].type)
            else:
                print("AMBOS TIPOS EN LA DECLARACION NO SON IGUALES")


        if node.father.father.father.father.symbol.symbol=="DECLA" and node.father.father.father.father.children[0].symbol.symbol == "id"  :
                print("-----------------PROBANDO SUB-ARBOLES ->")
                node.type = int
                node.father.type = int
                node.father.father.type = int
                nomNode = str(node.father.father.father.father.children[0].lexeme)
                typeNode = str(node.father.father.type)
                tiposDIC.append({'nombre': nomNode, 'typeNode':typeNode})
                tipos.append(node.father.father.type)


    elif node.symbol.symbol=='palabra' and node.father.symbol.symbol=='EXP' and node.father.father.father.symbol.symbol=='DE':
        node.type=str 
        node.visited=True
        node.father.type=str
        node.father.visited=True
        if node.father.type==str and node.father.father.children[0].symbol.symbol=='EXP' and node.father.father.children[1].symbol.symbol=="ASIG'":
            node.father.father.father.type=str
            node.father.father.father.visited=True
            
            if node.father.father.father.type==str and node.symbol.symbol=='palabra':
                node.father.father.type=str
                node.father.father.visited=True
            elif node.father.father.father.type != str:
                print("AMBOS TIPOS EN LA DECLARACION NO SON IGUALES>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        elif node.father.type != str:
            print("AMBOS TIPOS EN LA DECLARACION NO SON IGUALES>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        if node.father.father.father.father.symbol.symbol == "DECLA" and node.father.father.father.father.children[0].symbol.symbol=="TYPE" and node.father.father.father.father.children[0].children[0].symbol.symbol=="cadena" :
           node.father.father.father.father.children[0].type = str
           node.father.father.father.father.children[0].visited = True


        if node.father.father.father.father.symbol.symbol=="DECLA" and node.father.father.father.father.children[0].symbol.symbol == "TYPE" and node.father.father.father.father.children[0].children[0].symbol.symbol=="cadena":

            if node.father.father.father.type == str and node.type == str and node.father.father.father.father.children[0].type == str:
                print("AMBOS TIPOS EN LA DECLARACION SON IGUALES")

                nomNode_t1 = str(node.father.father.father.father.children[1].lexeme)
                typeNode_t1 = str(node.father.father.father.type)
                tiposDIC.append({'nombre': nomNode_t1, 'typeNode':typeNode_t1})
                tipos.append(node.father.father.father.type)

                nomNode_t2 = str(node.father.father.father.father.children[0].symbol.symbol)
                typeNode_2 = str(node.father.father.father.father.children[0].type)
                tiposDIC.append({'nombre': nomNode_t2, 'typeNode':typeNode_2})
                tipos.append(node.father.father.father.father.children[0].type)
            elif node.type != str and node.father.father.father.type != str:
                print("AMBOS TIPOS EN LA DECLARACION NO SON IGUALES>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


    for child in node.children:
        find(child)
find(root)
            









def printFind(node):
  print("TIPOS",tipos)
  count = 1
  valor='int'
  for n in range (len(tipos)):
        if tipos[0] == tipos[count]:
          if count < len(tipos):
            #print(tipos[count])
            count = len(tipos) - 2
          #print("Todos los valores son del mismo tipo")
          count = count + 1


        else:
          if tipos[0] != tipos[count]:
            if count < len(tipos):
              #print(tipos[count])
              count = len(tipos) - 2
          #print("Todos los valores NO son del mismo tipo")
          count = count + 1

printFind(root)



def printFindDIC(node):
  #print(tiposDIC)
  count = 1
  valor='int'
  for n in range (len(tiposDIC)):
    print(tiposDIC[n])
    if (tiposDIC[n].get('typeNode') == "<class 'int'>"):
      #print(tiposDIC.get('typeNode'))
      print("Son del Mismo Tipo")
    else:
      if (tiposDIC[n].get('typeNode') == "<class 'str'>"):
        #print(tiposDIC.get('typeNode'))
        print("Son del Mismo Tipo")

printFindDIC(root)