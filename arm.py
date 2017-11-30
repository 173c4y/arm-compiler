register = list()
for i in range(16):
	register.append(0)
flag = {'z':0, 'c':0, 'n':0, 'v':0}
memory = dict()
text = {}  #input dicionary
#----------------------------------------------
def inputReader():
	inputText=[]
	f = open("input.txt", "r")
	for line in f:
		line = line.rstrip('\n')
		line=line.rstrip('\r')
		#inputText.append(line)
		j=line.find(" ")
		#print line[0:j]
		text[int(line[0:j], 16)]= "0x"+line[j+3:].upper()
	#print text
	#print text[0xa]

#----------------------------------------------
def fetch():
	#print "------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
	print "FETCH instruction {0} from address {1}".format(text[register[15]], hex(register[15]))
	#if text[register[15]]=="0xEF000011":
	#	print "exiting"
	#	exit()
	decode(register[15],text[register[15]])
	print ""
	#print "------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

def decode(address, instruction):
	instruction = bin(int(instruction, 16))[2:]
	#print instruction
	if instruction[4:9] == "000000" and instruction[24:28] == "1001": #Multiply
		rd = instruction[12:16]
		rn = instruction[16:20]
		rs = instruction[20:24]
		rm = instruction[28:]
		if instruction[10] =='0': #multiply only
			print "DECODE: Operation is MUL First operand is R{0}. Second operand is R{1}. Third operand is R{2}. Destination is R{3}".format(int(rn),int(rs),int(rm),int(rd))
			print "Read Registers. R{0} = {1}. R{2} = {3}. R{4} = {5}. R{6} = {7}".format(int(rn), register[int(rn)], int(rs), register[int(rs)], int(rm), register[int(rm)], int(rd), register[int(rd)])
			register[int(rd)] = register[int(rm)] * register[int(rs)]
			print "EXECUTE: Multiply {0} and {1}".format(register[int(rm)],register[int(rs)])
			print "MEMORY: No memory operations"
			print "WRITEBACK: Write {0} to R{1}".format(instruction[int(rd)], int(rd))
		else:	# multiply and accumulate
			print "DECODE: Operation is MLA First operand is R{0}. Second operand is R{1}. Third operand is R{2}. Destination is R{3}".format(int(rn),int(rs),int(rm),int(rd))
			print "Read Registers. R{0} = {1}. R{2} = {3}. R{4} = {5}. R{6} = {7}".format(int(rn), register[int(rn)], int(rs), register[int(rs)], int(rm), register[int(rm)], int(rd), register[int(rd)])
			register[int(rd)] = register[int(rm)] * register[int(rs)] + register[int(rn)]
			print "EXECUTE: Multiply {0} and {1} and add {2} to it".format(register[int(rm)],register[int(rs)],register[int(rn)])
			print "MEMORY: No memory operations"
			print "WRITEBACK: Write {0} to R{1}".format(instruction[int(rd)], int(rd))

	elif instruction[4:8] == "1111": #Software interrupt
		if str(hex(int(instruction,2))) == "0xef000011":
			print "exiting"
			exit()
		opcode = instruction[8:]
		opcode = int(opcode,2)
		if opcode == 0x6b and register[0] == 1:
			print register[1]
		elif opcode == 0x6c and register[0] == 0:
			register[0] = input()
		elif opcode == 0x69 and register[0] == 1:
			print memory[register[1]]
		elif opcode == 0x6a and register[0] ==0:
			memory[register[1]] = raw_input()
			memory[register[1]] = memory[register[1]][:register[2]]


		register[15]+=4
	elif instruction[4:7] == "101": #Branch
		if(conditionChecker(int(instruction[:4],2))):
			if instruction[7] == '1': #	with link
				#link
				print "DECODE: Operation is BL. Offset is {0}".format(instruction[8:])
				r[14] = r[15]+4
				r[15] += twosComplement(instruction[8:])+8
				print "EXECUTE: Computes two's complement of offset."
				print "MEMORY: No memory operations"
				print "WRITEBACK: Write R15 + 4 to R14. Write R15 + {0} to R15".format(twosComplement(instruction[8:]))
			else: # withough branch
				print "DECODE: Operation is B. Offset is {0}".format(instruction[8:])
				r[15] += twosComplement(instruction[8:])+8
				print "EXECUTE: Computes two's complement of offset."
				print "MEMORY: No memory operations"
				print "WRITEBACK: Write R15 + {0} to R15".format(twosComplement(instruction[8:]))
		else:
			r[15] = r[15] + 4

	elif instruction[4:6] == "01": #Single data transfer  Load/Store
		if conditionChecker(int(instruction[:4],2)) == 0:
			return
		register[15]+=4
		sign = 1
		value = 0
		registerNo = 0
		if instruction[8] == "0":	#up down bit
			sign = -1
		if instruction[6] == '0':	#immediate
			value = int(instruction[20:],2)
		else: 						#shift
			registerNo = int(instruction[28:],2)
			shift = instruction[20:28]
			shiftedAmount = 0
			if shift[-1] =='0': #shift amount
				amount = shift[:5]
				if shift[5:7] == "00": #logical left
					shiftedAmount =  register[int(instruction[28:],2)]<<int(amount,2)
				elif shift[5:7] == "01":#logical right
					shiftedAmount =  register[int(instruction[28:],2)]>>int(amount,2)
				elif shift[5:7] == "10":#arithmetic right
					shiftedAmount =  register[int(instruction[28:],2)]>>int(amount,2)
				else: 					#rotate right
					shiftedAmount = register[int(instruction[28:])].zfill(32)
					svalue = int(amount,2)%32
					shiftedAmount = shiftedAmount[32-svalue:]+shiftedAmount[:32-svalue] 
			else:	#register shift
				reg = int(shitf[:4],2)
				regAmount = register[reg]
				if shift[5:7] == "00": #logical left
					shiftedAmount =  register[int(instruction[28:],2)]<<regAmount
				elif shift[5:7] == "01":#logical right
					shiftedAmount =  register[int(instruction[28:],2)]>>regAmount
				elif shift[5:7] == "10":#arithmetic right
					shiftedAmount =  register[int(instruction[28:],2)]>>regAmount
				else: 					#rotate right
					shiftedAmount = register[int(instruction[28:])].zfill(32)
					svalue = regamount%32
					shiftedAmount = shiftedAmount[32-svalue:]+shiftedAmount[:32-svalue]
			value = shiftedAmount
		baseRegNo = int(instruction[12:16],2)
		destRegNo = int(instruction[16:20],2)
		offset = register[baseRegNo] + value
		if instruction[11] == '0': #store
			#print "DECODE: Storing value {1} at address{0}".format(offset, register[destRegNo])
			print "DECODE: Operation is STR. Base Register is R{0}. Source Register is R{1}. Offset is {2}".format(baseRegNo, destRegNo, value)
			print "Read register: R{0} = {1}. R{2} = {3}".format(baseRegNo, register[baseRegNo], destRegNo, register[destRegNo])
			memory[offset] = register[destRegNo]
			print "EXECUTE: Move {0} to address {1}".format(register[destRegNo], offset)
			print "MEMORY: Access Memory address {0} to store {1}".format(offset, register[destRegNo])
			print "WRITEBACK: No writeback operation"
		else:						#load
			#print "DECODE: Loading value {1} from address{0}".format(offset, memory[offset])
			print "DECODE: Operation is STR. Base Register is R{0}. Destination Register is R{1}. Offset is {2}".format(baseRegNo, destRegNo, value)
			print "Read register: R{0} = {1}. R{2} = {3}".format(baseRegNo, register[baseRegNo], destRegNo, register[destRegNo])
			register[destRegNo] = memory[offset]
			print "EXECUTE: Read data from address {0} and write to R{1}".format(offset, destRegNo)
			print "MEMORY: Access Memory address {0} to read {1}".format(offset, register[destRegNo])
			print "WRITEBACK: Write {0} to R{1}".format(memory[offset], destRegNo)
	elif instruction[4:6] == "00":#  data processing
		register[15]+=4
		if conditionChecker(int(instruction[:4],2)) == 0:
			return
		if instruction[6] == "1":	# immediate number
			shift = int(instruction[20:24],2)
			rotatedValue = instruction[24:]
			rotatedValue.zfill(32)
			rotatedValue = rotatedValue[32-shift:] + rotatedValue[:32-shift]
			rotatedValue = int(rotatedValue,2)
			if instruction[7:11] == "0000": #and
				print "DECODE: Operation is AND. First operand is R{0}. The immediate value is {1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[24:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: {0} & {1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = register[int(instruction[16:20],2)] & rotatedValue
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "0001": #eor
				print "DECODE: Operation is EOR. First operand is R{0}. The immediate value is {1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[24:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: {0} ^ {1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = register[int(instruction[16:20],2)] ^ rotatedValue
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "0010": #sub
				print "DECODE: Operation is SUB. The first oprerand is R{1}.The immediate value is {0}. Destination is R{2}".format(int(instruction[24:],2), int(instruction[12:16],2),int(instruction[16:20],2))
				print "\tRead Registers: R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)],int(instruction[16:20],2),register[int(instruction[16:20],2)])
				register[int(instruction[16:20],2)] = (-rotatedValue) + register[int(instruction[12:16],2)]
				print "EXECUTE: subtract {0} and R{1}".format(rotatedValue, int(instruction[12:16],2))
				print "MEMORY: No memory operations"
				print "WRITEBACK: Write {0} in R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "0011": #rsub
				print "DECODE: Operation is RSUB. The first oprerand is R{1}.The immediate value is {0}. Destination is R{2}".format(int(instruction[24:],2), int(instruction[12:16],2),int(instruction[16:20],2))
				print "\tRead Registers: R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)],int(instruction[16:20],2),register[int(instruction[16:20],2)])
				register[int(instruction[16:20],2)] = rotatedValue - register[int(instruction[12:16],2)]
				print "EXECUTE: reverse subtract {0} and R{1}".format(rotatedValue, int(instruction[12:16],2))
				print "MEMORY: No memory operations"
				print "WRITEBACK: Write {0} in R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "0100": #add
				print "DECODE: Operation is ADD. The first oprerand is R{1}.The immediate value is {0}. Destination is R{2}".format(int(instruction[24:],2), int(instruction[12:16],2),int(instruction[16:20],2))
				print "\tRead Registers: R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)],int(instruction[16:20],2),register[int(instruction[16:20],2)])
				register[int(instruction[16:20],2)] = rotatedValue + register[int(instruction[12:16],2)]
				print "EXECUTE: add {0} and R{1}".format(rotatedValue, int(instruction[12:16],2))
				print "MEMORY: No memory operations"
				print "WRITEBACK: Write {0} in R{1}".format(rotatedValue, int(instruction[16:20],2))
			elif instruction[7:11] == "0101": #adc
				print "adc"
			elif instruction[7:11] == "0110": #sbc
				print "sbc"
			elif instruction[7:11] == "0111": #rsc
				print "rsc"
			elif instruction[7:11] == "1000": #tst
				print "tst"
			elif instruction[7:11] == "1001": #teq
				print "teq"
			elif instruction[7:11] == "1010": #cmp
				print "DECODE: Operation is CMP. First operand is R{0}. The immediate value is {1}".format(int(instruction[12:16],1), int(instruction[24:],2))
				print "Read Registers: R{0} = {1}".format(int(instruction[12:16],1), register[int(instruction[12:16],1)])
				tmp = register[int(instruction[12:16],1)] - rotatedValue
				if tmp ==0:
					flag[z] = 1
				else:
					flag[z] = 0
				if str(tmp)[0] == '1':
					flag[n] = 1
				else:
					flag[n] = 0
				print "EXECUTE: subtract {0} and {1}".format(register[int(instruction[12:16],1)], rotatedValue)
				print "MEMORY: No memory operation"
				print "WRITEBACK: No writeback"
			elif instruction[7:11] == "1011": #cmn
				print "cmn"
			elif instruction[7:11] == "1100": #orr
				print "DECODE: Operation is ORR. First operand is R{0}. The immediate value is {1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[24:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: {0} | {1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = register[int(instruction[16:20],2)] | rotatedValue
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "1101": #mov
				print "DECODE: Operation is MOV. The first oprerand is R{1}.The immediate value is {0}. Destination is R{2}".format(int(instruction[24:],2), int(instruction[12:16],2),int(instruction[16:20],2))
				print "\tRead Registers: R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)],int(instruction[16:20],2),register[int(instruction[16:20],2)])
				register[int(instruction[16:20],2)] = rotatedValue
				print "EXECUTE: MOV {0} to R{1}".format(rotatedValue, int(instruction[16:20],2))
				print "MEMORY: No memory operations"
				print "WRITEBACK: Write {0} in R{1}".format(rotatedValue, int(instruction[16:20],2))
			elif instruction[7:11] == "1110": #bic
				print "bic"
			#elif instruction[7:11] == 0b1111: #mvn
			else: #mvn
				print "DECODE: Operation is MVN. First operand is R{0}. The immediate value is {1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[24:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: ~{1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = ~rotatedValue
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
		else:		# register data processing
			shift = instruction[20:28]
			shiftedAmount = 0
			if shift[-1] =='0': #shift amount
				amount = shift[:5]
				if shift[5:7] == "00": #logical left
					shiftedAmount =  register[int(instruction[28:],2)]<<int(amount,2)
				elif shift[5:7] == "01":#logical right
					shiftedAmount =  register[int(instruction[28:],2)]>>int(amount,2)
				elif shift[5:7] == "10":#arithmetic right
					shiftedAmount =  register[int(instruction[28:],2)]>>int(amount,2)
				else: 					#rotate right
					shiftedAmount = register[int(instruction[28:])].zfill(32)
					svalue = int(amount,2)%32
					shiftedAmount = shiftedAmount[32-svalue:]+shiftedAmount[:32-svalue] 
			else:	#register shift
				reg = int(shitf[:4],2)
				regAmount = register[reg]
				if shift[5:7] == "00": #logical left
					shiftedAmount =  register[int(instruction[28:],2)]<<regAmount
				elif shift[5:7] == "01":#logical right
					shiftedAmount =  register[int(instruction[28:],2)]>>regAmount
				elif shift[5:7] == "10":#arithmetic right
					shiftedAmount =  register[int(instruction[28:],2)]>>regAmount
				else: 					#rotate right
					shiftedAmount = register[int(instruction[28:])].zfill(32)
					svalue = regamount%32
					shiftedAmount = shiftedAmount[32-svalue:]+shiftedAmount[:32-svalue]
			if instruction[7:11] == "0000": #and
				print "DECODE: Operation is AND. First operand is R{0}. The second operand is R{1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[28:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: R{0} & R{1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = register[int(instruction[16:20],2)] & shiftedAmount
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "0001": #eor
				print "DECODE: Operation is ORR. First operand is R{0}. The second operand is R{1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[28:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: R{0} & R{1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = register[int(instruction[16:20],2)] & shiftedAmount
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "0010": #sub
				print "DECODE: Operation is SUB. First oprerand is R{0}. Second operans is R{2}. The Destination is R{1}".format(int(instruction[12:16],2), int(instruction[16:20],2), int(instruction[28:],2))
				print "Read Registers. R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2),register[int(instruction[12:16],2)], int(instruction[28:],2), register[int(instruction[28:],2)])
				register[int(instruction[16:20],2)] = register[int(instruction[12:16],2)] - shiftedAmount
				print "EXECUTE: subtract {0} and {1}".format(register[int(instruction[12:16],2)], register[int(instruction[28:],2)])
				print "MEMORY: No memory operation"
				print "WRITEBACK: wrote {0} to R{1}".format(register[int(instruction[16:20],2)],int(instruction[16:20],2))
			elif instruction[7:11] == "0011": #rsub
				print "DECODE: Operation is RSUB. First operand is R{0}. Second operand is R{2}. The Destination is R{1}".format(int(instruction[12:16],2), int(instruction[16:20],2), int(instruction[28:],2))
				print "Read Registers. R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2),register[int(instruction[12:16],2)], int(instruction[28:],2), register[int(instruction[28:],2)])
				register[int(instruction[16:20],2)] = shiftedAmount - register[int(instruction[12:16],2)]
				print "EXECUTE: reverser subtract {0} and {1}".format(register[int(instruction[12:16],2)], register[int(instruction[28:],2)])
				print "MEMORY: No memory operation"
				print "WRITEBACK: wrote {0} to R{1}".format(register[int(instruction[16:20],2)],int(instruction[16:20],2))
			elif instruction[7:11] == "0100": #add
				print "DECODE: Operation is ADD. First operand is R{0}. Second operand is R{2}. The Destination is R{1}".format(int(instruction[12:16],2), int(instruction[16:20],2), int(instruction[28:],2))
				print "Read Registers. R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2),register[int(instruction[12:16],2)], int(instruction[28:],2), register[int(instruction[28:],2)])
				register[int(instruction[16:20],2)] = register[int(instruction[12:16],2)] + shiftedAmount
				print "EXECUTE: add {0} and {1}".format(register[int(instruction[12:16],2)], register[int(instruction[28:],2)])
				print "MEMORY: No memory operation"
				print "WRITEBACK: wrote {0} to R{1}".format(register[int(instruction[16:20],2)],int(instruction[16:20],2))
			elif instruction[7:11] == "0101": #adc
				print "adc"
			elif instruction[7:11] == "0110": #sbc
				print "sbc"
			elif instruction[7:11] == "0111": #rsc
				print "rsc"
			elif instruction[7:11] == "1000": #tst
				print "tst"
			elif instruction[7:11] == "1001": #teq
				print "teq"
			elif instruction[7:11] == "1010": #cmp
				print "DECODE: Operation is CMP. First operand is R{0}. The second operand is R{1}".format(int(instruction[12:16],1), int(instruction[24:],2))
				print "Read Registers: R{0} = {1}".format(int(instruction[12:16],1), register[int(instruction[12:16],1)])
				tmp = register[int(instruction[12:16],1)] - rotatedValue
				if tmp ==0:
					flag[z] = 1
				else:
					flag[z] = 0
				if str(tmp)[0] == '1':
					flag[n] = 1
				else:
					flag[n] = 0
				print "EXECUTE: subtract {0} and {1}".format(register[int(instruction[12:16],1)], shiftedAmount)
				print "MEMORY: No memory operation"
				print "WRITEBACK: No writeback"
			elif instruction[7:11] == "1011": #cmn
				print "cmn"
			elif instruction[7:11] == "1100": #orr
				print "DECODE: Operation is ORR. First operand is R{0}. The second operand is R{1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[28:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: R{0} | R{1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = register[int(instruction[16:20],2)] | shiftedAmount
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
			elif instruction[7:11] == "1101": #mov
				print "DECODE: Operation is MOV. The first oprerand is R{1}.The second operand is {0}. Destination is R{2}".format(int(instruction[28:],2), int(instruction[12:16],2),int(instruction[16:20],2))
				print "\tRead Registers: R{0} = {1}. R{2} = {3}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)],int(instruction[16:20],2),register[int(instruction[16:20],2)])
				register[int(instruction[16:20],2)] = shiftedAmount
				print "EXECUTE: MOV {0} to R{1}".format(shiftedAmount, int(instruction[16:20],2))
				print "MEMORY: No memory operations"
				print "WRITEBACK: Write {0} in R{1}".format(shiftedAmount, int(instruction[16:20],2))
			elif instruction[7:11] == "1110": #bic
				print "bic"
			#elif instruction[7:11] == 0b1111: #mvn
			else: #mvn
				print "DECODE: Operation is MVN. First operand is R{0}. The second operand is R{1}. The destination is R{2}".format(int(instruction[12:16],2),int(instruction[28:0],2),int(instruction[16:20],2))
				print "Read registers: R{0} = {1}".format(int(instruction[12:16],2), register[int(instruction[12:16],2)])
				print "EXECUTE: ~R{1}".format(register[int(instruction[12:16],2)], int(instruction[24:0],2))
				register[int(instruction[16:20],2)] = ~shiftedAmount
				print "MEMORY: No memory operations"
				print "WRITEBACK: write {0} to R{1}".format(register[int(instruction[16:20],2)], int(instruction[16:20],2))
	

def conditionChecker(a):
	#print "in here"
	if a == 14:
		return 1	
	elif a == 13 and (flag['z'] == 1 or (flag['n'] !=flag['v'])):
		return 1
	elif a == 12 and (flag['z'] ==0 or(flag['n'] == flag['v'])):
		return 1
	elif a == 11 and (flag['n'] != flag['v']):
		return 1
	elif a == 10 and (flag['n'] == flag['v']):
		return 1
	elif a == 9 and (flag['c'] == 0 and flag['z'] == 1):
		return 1
	elif a == 8 and (flag['c'] == 1 and flag['z'] == 0):
		return 1
	elif a == 7 and flag['v'] == 0:
		return 1
	elif a == 6 and flag['v'] == 1:
		return 1
	elif a == 5 and flag['n'] == 0:
		return 1	
	elif a == 4 and flag['n'] == 1:
		return 1
	elif a == 3 and flag['c'] == 0:
		return 1
	elif a == 2 and flag['c'] == 1:
		return 1
	elif a == 1 and flag['z'] == 0:
		return 1
	elif a == 0 and flag['z'] == 1:
		return 1
	else:
		return 0
	return 0

def twosComplement(value):
	bitLen = len(value)
	value = int(value,2)
	if (value & (1 << (bitLen - 1))) != 0:
		value = value - (1 << bitLen)        
	return value 


if __name__ == "__main__":
	inputReader()
	while(True):
		fetch()
