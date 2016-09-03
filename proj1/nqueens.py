import time

def inputBoardProcessing(board):
	board = board.split(' ')
	for i in range(len(board)):
		board[i] = int(board[i])
	return board


def boardCheckFull(board):
	for i in range(len(board)):
		if board[i] != 0:
			for j in range(len(board)):
				if (board[j] == board[i] and j != i):
					return False
				if ((board[j] == (board[i]+j-i) or board[j] == (board[i]+i-j)) and board[j] != 0 and j != i):
					return False
	return True

def boardCheckTrusting(board, newCol):
	if newCol == -1:
		return True
	for i in range(len(board)):
		if ((board[i] == (board[newCol]+i-newCol) or board[i] == (board[newCol]+newCol-i)) and board[i] != 0 and i != newCol):
			return False
	return True

def recBack(board, selection, newCol, size):
	if not boardCheckTrusting(board, newCol):
		return False
	retVal = False
	if newCol<size-1:
		for i in range(len(board)):
			if board[i] == 0:
				for num in selection:
					newBoard = board[:i]
					newBoard.append(num)
					newBoard.extend(board[i+1:])
					newSel = selection[:]
					newSel.remove(num)
					if recBack(newBoard, newSel, newCol+1, size):
						retVal = True
				break
		return retVal
	else:
		printStr = ""
		for num in board:
			printStr = printStr+str(num)+" "
		print("\n")
		print(">> "+printStr)
		return True

def main():
	print("###########################################\n###	nqueens solver by Harahu	###\n###########################################\n\n")
	size = int(input(">> "))
	board = inputBoardProcessing(input(">> "))
	start = time.clock()
	if not boardCheckFull(board):
		print("\nError: Input board in conflict")
	else:
		startSel = []
		for i in range(size):
			startSel.append(i+1)
		for num in board:
			try:
				startSel.remove(num)
			except:
				pass
		if not recBack(board, startSel, -1, size): #TODO un-hardcode
			print("\nError: No solution possible")
		end = time.clock()
		print("\nRuntime:")
		print(str(end - start)+" seconds")

main()