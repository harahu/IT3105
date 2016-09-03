import time

def boardCheckFull(board):
	for i in range(len(board)):
		if board[i] != '0':
			for j in range(len(board)):
				if (board[j] == board[i] and j != i):
					return False
				if ((int(board[j]) == (int(board[i])+j-i) or int(board[j]) == (int(board[i])+i-j)) and board[j] != '0' and j != i):
					return False
	return True

def boardCheckTrusting(board):
	newCol = -1
	for i in range(len(board)):
		if board[i] == '0':
			if i == 0:
				return True
			newCol = i-1
			break
	if newCol == -1:
		newCol = 7
	for i in range(len(board)):
		if ((int(board[i]) == (int(board[newCol])+i-newCol) or int(board[i]) == (int(board[newCol])+newCol-i)) and board[i] != '0' and i != newCol):
			return False
	return True

def boardFilled(board):
	for col in board:
		if col == '0':
			return False
	return True

def recBack(board, selection):
	if not boardCheckTrusting(board):
		return False
	if not boardFilled(board):
		for i in range(len(board)):
			if board[i] == '0':
				for num in selection:
					if recBack(board[:i]+num+board[i+1:], selection.replace(num, '')):
						return True
				return False
	else:
		print("\n")
		print(">> "+board)
		return True

def main():
	print("###########################################\n###	8-queens solver by Harahu	###\n###########################################\n\n")
	board = input(">> ")
	start = time.clock()
	if not boardCheckFull(board):
		print("\nError: Input board in conflict")
	else:
		startSel = "12345678"
		for num in board:
			startSel = startSel.replace(num, '')
		if not recBack(board, startSel):
			print("\nError: No solution possible")
		end = time.clock()
		print("\nRuntime:")
		print(str(end - start)+" seconds")

main()