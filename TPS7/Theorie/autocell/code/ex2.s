@ Type exercise 2 here
	INVOKE 1, 2, 3
	SETI R4, #1
	SETI R0, #0
	SETI R1, #0
	SUB R2, R2, R4
	SUB R3, R3, R4
	INVOKE 3, 0, 1
	INVOKE 4, 4, 0
	INVOKE 3, 2, 1
	INVOKE 4, 4, 0
	INVOKE 3, 0, 3
	INVOKE 4, 4, 0
	INVOKE 3, 2, 3
	INVOKE 4, 4, 0
	STOP