ADDI x1, x0, 5
ADDI x2, x0, 3
ADDI x3, x0, 0b1100
ADDI x4, x0, 0b1010
ADD x5, x1, x2
SUB x6, x1, x2
AND x7, x3, x4
OR x8, x3, x4
XOR x9, x3, x4
ANDI x10, x3, 0b101
SW x5, 0(x0)
SW x6, 4(x0)
LW x11, 0(x0)
LW x12, 4(x0)
ADDI x13, x0, 3
ADDI x14, x0, 1
ADDI x15, x0, 0
ADD x15, x15, x13
SUB x13, x13, x14
BEQ x13, x0, 21
SW x15, 8(x0)