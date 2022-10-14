@ Type exercise 5 here
	invoke 1, 2, 3
  seti r6, #0
	seti r4, #1
	seti r0, #0
  seti r7, #0
  seti r8, #0
L0:
	seti r1, #0
L1:
	invoke 3, 0, 1
  invoke 5, 5, 0
  goto_eq L3, r5, r4
  goto_eq L4, r5, r6

L2:
  add r1, r1, r4
  goto_lt L1, r1, r3
  add r0, r0, r4
  goto_lt L0, r0, r2
  stop

L3:
  invoke 4, 6, 0
  goto L2

L4:
  invoke 5, 7, 1
  goto_eq L5, r7, r4
  invoke 5, 7, 2
  goto_eq L5, r7, r4
  invoke 5, 7, 3
  goto_eq L5, r7, r4
  invoke 5, 7, 4
  goto_eq L5, r7, r4
  invoke 5, 7, 5
  goto_eq L5, r7, r4
  invoke 5, 7, 6
  goto_eq L5, r7, r4
  invoke 5, 7, 7
  goto_eq L5, r7, r4
  invoke 5, 7, 8
  goto_eq L5, r7, r4
  goto L2

L5:
  invoke 4, 4, 0
  goto L2
