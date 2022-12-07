from parser import ll1
from lexer import get_tokens

ruta = "Tests/test2.txt"
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

    ##CREACION DE VARIABLE TIPO CADENA
    if node.symbol.symbol=="cadena" and node.father.father.children[1].symbol.symbol=="id":

            Codigo=Codigo+"   var_"
            Codigo=Codigo+str(node.father.father.children[1].lexeme)
            Codigo=Codigo+":.word 0:1 \n"
            #print(Codigo)
    for child in node.children:
            decla(child)
###############################################################################
def var(node,va):
    if node.symbol.symbol=="DECLA":
            if node.children[0].symbol.symbol=="TYPE":
                    #declaracion con type"
                    if node.children[2].children[0].symbol.symbol=="igual":
                            if node.children[2].children[1].children[0].children[0].symbol.symbol=="numero":
                                    va=va+"\n   li $a0, "
                                    va=va+str(node.children[2].children[1].children[0].children[0].lexeme)#numero id
                                    va=va+"\n   la $t0, var_"
                                    va=va+str(node.children[1].lexeme)#id
                                    va=va+"\n   sw $a0, 0($t0)\n"
                            if node.children[2].children[1].children[1].children[0].symbol.symbol=="OPE":
                                    if node.children[2].children[1].children[1].children[0].children[0].symbol.symbol=="suma":
                                            va=va+"\n   li $a0, "
                                            va=va+str(node.children[2].children[1].children[0].children[0].lexeme)#a=3
                                            va=va+"\n   sw $a0 0($sp)"
                                            va=va+"\n   add $sp $sp -4"
                                            va=va+"\n   li $a0, "
                                            va=va+str(node.children[2].children[1].children[1].children[1].children[0].lexeme)#+ 4
                                            va=va+"\n   lw $t1 4($sp)"
                                            va=va+"\n   add $a0 $t1 $a0"
                                            va=va+"\n   add $sp $sp 4"
                                            va=va+"\n   la  $t1, var_"
                                            va=va+str(node.children[1].lexeme)
                                            va=va+"\n   sw  $a0, 0($t1)\n"
            #if node.children[0].symbol.symbol=="id":
            #        #declaracion sin type, uso de variable
            #        if node.children[3].children[0].symbol.symbol=="e":
            #                va=va+"\n   li $a0, "
            #                va=va+str(node.children[2].children[0].lexeme)
            #                va=va+"\n   la $t0, var_"
            #                va=va+str(node.children[0].lexeme)
            #                va=va+"\n   sw $a0, 0($t0)"
            #        if node.children[3].children[0].symbol.symbol=="OPE":
            #                if node.children[3].children[0].children[0].symbol.symbol=="suma":
            #                        va=va+"\n   la $t0, var_"
            #                        va=va+str(node.children[2].children[0].lexeme)
            #                        va=va+"\n   lw $a0, 0($t0)"
            #                        va=va+"\n   sw $a0 0($sp)"
            #                        va=va+"\n   addiu $sp $sp -4"
            #                        va=va+"\n   li $a0, "
            #                        va=va+str(node.children[3].children[1].children[0].lexeme)
            #                        va=va+"\n   lw $t1, 4($sp)"
            #                        va=va+"\n   add $a0, $a0, $t1"
            #                        va=va+"\n   addiu $sp $sp 4"
            #                        va=va+"\n   la  $t0, var_"
            #                        va=va+str(node.children[0].lexeme)
            #                        va=va+"\n   sw  $a0, 0($t0)"
            #                        va=va+"\n   li $v0, 1"
            #                        va=va+"\n   syscall"    
    for child in node.children:
        var(child,va)
    return va
#############################################################################
#decla(root)
def var_mio(node,va):
    if node.symbol.symbol=="DECLA":
            if node.children[0].symbol.symbol=="TYPE":
                    #declaracion con type"
                    if node.children[2].children[0].symbol.symbol=="igual":
                            if node.children[2].children[1].children[0].children[0].symbol.symbol=="e":
                                    va=va+"\n   li $a0, "
                                    va=va+str(node.children[2].children[1].children[0].children[0].lexeme)#numero id
                                    va=va+"\n   la $t0, var_"
                                    va=va+str(node.children[1].lexeme)#id
                                    va=va+"\n   sw $a0, 0($t0)\n"
                            if node.children[2].children[1].children[1].children[0].symbol.symbol=="OPE":
                                    if node.children[2].children[1].children[1].children[0].children[0].symbol.symbol=="suma":
                                            va=va+"\n   li $a0, "
                                            va=va+str(node.children[2].children[1].children[0].children[0].lexeme)#a=3
                                            va=va+"\n   sw $a0 0($sp)"
                                            va=va+"\n   add $sp $sp -4"
                                            va=va+"\n   li $a0, "
                                            va=va+str(node.children[2].children[1].children[1].children[1].children[0].lexeme)#+ 4
                                            va=va+"\n   lw $t1 4($sp)"
                                            va=va+"\n   add $a0 $t1 $a0"
                                            va=va+"\n   add $sp $sp 4"
                                            va=va+"\n   la  $t1, var_"
                                            va=va+str(node.children[1].lexeme)
                                            va=va+"\n   sw  $a0, 0($t1)\n"
            #if node.children[0].symbol.symbol=="id":
            #                       va=va+"\n   syscall"    
    for child in node.children:
        var_mio(child,va)
    return va
###############################################################################
def si(node):
    global Codigo
    if node.symbol.symbol=="EST":       
        if node.children[0].symbol.symbol=="si":
            Codigo=Codigo+"\n   la $t0, var_"
            Codigo=Codigo+str(node.children[2].children[0].lexeme)
            Codigo=Codigo+"\n   lw $a0, 0($t0)"##################
            Codigo=Codigo+"\n   sw $a0, 0($sp)"#push
            Codigo=Codigo+"\n   add $sp, $sp, -4"
            Codigo=Codigo+"\n   li $a0, "
            Codigo=Codigo+str(node.children[4].children[0].lexeme)
            Codigo=Codigo+"\n   lw $t1, 4($sp)"
            Codigo=Codigo+"\n   add $sp, $sp, 4"
            Codigo=Codigo+"\n   blt $a0, $t1, label_true\n"

###############################################################################
def principal(node):
    global Codigo,sivar,sinovar,varn
    if node.symbol.symbol=="DECLA":#decla dentro del sent == si
        if node.father.father.symbol.symbol=="EST":
            if node.father.father.children[0].symbol.symbol=="si":#si
                si(node.father.father)
                sivar=sivar+"\nlabel_true:"
                #sivar=var(node,sivar)#si var automatizado
                sivar=sivar+"\n   li $a0, "
                sivar=sivar+str(node.children[1].children[1].children[0].children[0].lexeme)#valor de la sentencia dentro del si x=->10
                sivar=sivar+"\n   la $t0, var_"
                sivar=sivar+str(node.father.father.children[2].children[0].lexeme)#valor de la sentencia dentro del si ->x=10
                sivar=sivar+"\n    sw $a0, 0($t0)"
                sivar=sivar+"\nlabel_end:"
                if node.father.father.father.children[1].children[0].children[0].symbol.symbol=="sino":#sino
                    sinovar=sinovar+"label_false:"
                    #sinovar=var(node.father.father.father.children[1].children[0].children[2].children[0],sinovar)#le paso decla que esta dentro del sino, autmatizacion
                    sinovar=sinovar+"\n   li $a0, 11"
                    sinovar=sinovar+"\n   la $t0, var_"
                    sinovar=sinovar+str(node.father.father.father.children[1].children[0].children[2].children[0].children[0].lexeme)#expresion dentro del sino, variable x=11
                    sinovar=sinovar+"\n   sw $a0, 0($t0)"    
                    sinovar=sinovar+"\n   b label_end"
                    Codigo=Codigo+sinovar
                    Codigo=Codigo+sivar
                else:
                    Codigo=Codigo+sivar
        else:
            varn=varn+var(node,varn)
            Codigo=Codigo+varn
    for child in node.children:
            principal(child)

##############################################################################
def principal_mio(node):
    global Codigo,sivar,sinovar,varn
    if node.symbol.symbol=="DECLA":
        #print("DECLARACION")
        #if node.children[0].children[0].symbol.symbol!="cadena":
        #        print("IMPOSIBLE HACER LA SUMA CON VARIABLES TIPO CADENA")
        #else:
                varn=varn+var(node,varn)
                Codigo=Codigo+varn
    for child in node.children:
            principal_mio(child)



Codigo=Codigo+".data \n"
decla(root)
Codigo=Codigo+".text \n"
Codigo=Codigo+"main: "
principal(root)
Codigo=Codigo+"\n	jr $ra"
text_file = open("Codigo.txt", "w")
text_file.write(Codigo)

text_file.close()


