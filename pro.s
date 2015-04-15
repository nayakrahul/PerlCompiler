 .data
theString:
    .space 64
    .text
main:
   	subu	$sp,	$sp,	8
	sw		$fp,	8($sp)
	sw		$ra,	4($sp)
	addiu	$fp,	$sp,	8
	subu	$sp,	$sp,	8
	li		$t4,	nfdkjn
	move	$t5,	$ts;lx
	move $a0, $t5
	li $v0, 1
	syscall
	jr $ra