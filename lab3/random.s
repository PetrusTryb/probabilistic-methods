.global random

random:
	push %ebp
	mov %esp, %ebp
	mov 8(%esp), %eax
	mov $100, %ebx
	push %ebx
	finit
	fld 8(%esp)
	fld (%esp)
	fmul
	pop %ebx
	mov $50, %ebx
	push %ebx
	fld (%esp)
	fadd
	pop %ebx
	sub %esp, 4
	fistp (%esp)
	mov (%esp), %eax
	add %esp, 4
	pop %ebp
	ret
