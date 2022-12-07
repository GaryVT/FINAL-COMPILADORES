.data 
   var_x:.word 0:1 
.text 
main: 
   li $a0, 10
   la $t0, var_x
   sw $a0, 0($t0)

   la $t0, var_x
   lw $a0, 0($t0)
   sw $a0, 0($sp)
   add $sp, $sp, -4
   li $a0, 20
   lw $t1, 4($sp)
   add $sp, $sp, 4
   blt $a0, $t1, label_true
label_false:
   li $a0, 11
   la $t0, var_x
   sw $a0, 0($t0)
   b label_end
label_true:
   li $a0, 10
   la $t0, var_x
    sw $a0, 0($t0)
label_end:
	jr $ra