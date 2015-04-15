.data
	string0:	.asciiz	"amit\n"
	string1:	.asciiz	"rahul\n"
	string2:	.asciiz	"amit\n"
.text

main:
	subu	$sp,	$sp,	8
	sw	$fp,	8($sp)
	sw	$ra,	4($sp)
	addiu	$fp,	$sp,	8
	subu	$sp,	$sp,	36
	li	$t4,	9
	move	$t5,	$t4
	li	$t6,	10
	move	$t7,	$t6
	mult	$t5,	$t7
	mflo		$t0
	move	$t1,	$t0
	li	$v0,	4
	la	$a0,	string0
	syscall
	move	$a0,	$t5
	li	$v0,	1
	syscall
	li	$v0,	4
	la	$a0,	string1
	syscall
	li	$v0,	4
	la	$a0,	string2
	syscall
	move	$a0,	$t1
	li	$v0,	1
	syscall
	li	$v0,	10
	syscall
