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
usoDIC = []
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
    if node.symbol.symbol=='numero'  and node.father.father.father.father.symbol.symbol=='DECLA':
        node.type=float
        if node.father.father.father.father.children[0].symbol.symbol=='TYPE' and node.father.father.father.father.children[0].children[0].symbol.symbol=='numerico' :
            #print("CREACION DE VARIABLE FLOAT")
            #node.type = float #tipo float al numero (numero)
            node.father.father.father.father.children[1].type = float #tipo float a la variable (id)
            nomVar = node.father.father.father.father.children[1].lexeme
            nomTip = node.type

            #print(nomVar, nomTip)
            tiposDIC.append({'nombre': nomVar, 'typeNode':nomTip})
            #print(tiposDIC)
        if node.father.father.father.father.children[0].symbol.symbol=='id':
            #print("USO DE VARIABLE FLOAT")
            nomVarUso = node.father.father.father.father.children[0].lexeme
            tipoVarUSo = node.type     
            usoDIC.append({'nombre': nomVarUso, 'typeNode':tipoVarUSo})
            #print("DICCIONARIO DE USOS:")
            #print(usoDIC)

    if node.symbol.symbol=='palabra'  and node.father.father.father.father.symbol.symbol=='DECLA':
        node.type = str
        if node.father.father.father.father.children[0].symbol.symbol=='TYPE' and node.father.father.father.father.children[0].children[0].symbol.symbol=='cadena' :
            #print("CREACION DE VARIABLE STRING")
            #node.type = str #tipo str al numero (palabra)
            node.father.father.father.father.children[1].type = str #tipo str a la variable (id)
            nomVar = node.father.father.father.father.children[1].lexeme
            nomTip = node.type

            #print(nomVar, nomTip)
            tiposDIC.append({'nombre': nomVar, 'typeNode':nomTip})
            #print(tiposDIC)
        if node.father.father.father.father.children[0].symbol.symbol=='id':
            #print("USO DE VARIABLE STRING")
            nomVarUso = node.father.father.father.father.children[0].lexeme
            tipoVarUSo = node.type     
            usoDIC.append({'nombre': nomVarUso, 'typeNode':tipoVarUSo})
            #print("DICCIONARIO DE USOS:")
            #print(usoDIC)

    for child in node.children:
        find(child)
find(root)
            


def printFindDIC(node):
  #print(tiposDIC)
  count = 1
  valor='int'
  for n in range (len(tiposDIC)):
      print(" ")
      #print("AL MOMENTO DE LA CREACION")
      print ("TIPO: ",tiposDIC[n].get('typeNode'),"NOMBRE : ", tiposDIC[n].get('nombre'))
      for m in range (len(usoDIC)):
        
        if tiposDIC[n].get('typeNode') == usoDIC[m].get('typeNode') and (tiposDIC[n].get('nombre') == usoDIC[m].get('nombre')):
            #print("AL MOMENTO DEL USO")
            print("TIPO: ",  usoDIC[m].get('typeNode'), " NOMBRE: ", usoDIC[m].get('nombre') )
            print("SON DEL MISMO TIPO")
            #print("SON DEL MISMO TIPO: ", usoDIC[m].get('typeNode'))
        elif tiposDIC[n].get('typeNode') != usoDIC[m].get('typeNode') and (tiposDIC[n].get('nombre') == usoDIC[m].get('nombre')):
            #print("AL MOMENTO DEL USO")
            print("TIPO: ",  usoDIC[m].get('typeNode'), " NOMBRE: ", usoDIC[m].get('nombre') )
            print("NO SON DEL MISMO TIPO")

            #print("NO SON DEL MISMO TIPO: ",usoDIC[m].get('typeNode'))
        

printFindDIC(root)

