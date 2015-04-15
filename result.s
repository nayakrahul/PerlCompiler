.data
String:
	.space 64
string0:	.asciiz	"hello"
.text
main:
	subu	$sp,	$sp,	8
	sw	$fp,	8($sp)
	sw	$ra,	4($sp)
	addiu	$fp,	$sp,	8
	subu	$sp,	$sp,	20
	li	$t4,	0
	move	$t5,	$t4
	li	$t6,	0
	seq	$t7,	$t5,	$t6
	beq	$t7,	$zero,	label0
	la	$t0,	string0
	move	$a0,	$t0
	li	$v0,	4
	syscall
label0:
	li	$v0,	10
	syscall
