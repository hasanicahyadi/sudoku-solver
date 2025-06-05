from v16_functions import *

def GetSudoku() -> list[int]:
    valid = False
    while not valid:
        sudoku = list(input("Enter sudoku:\n"))

        if len(sudoku) == 0:
            exit(1)
        
        if len(sudoku) == 81:
            valid = True
    
    sudoku = [int(data) for data in sudoku]
    return sudoku

    
def main() -> None:
    board = GetSudoku()
    GetAllNotes(board)
    print(cellNotes)
    tries = 10

    for i in range(tries):
        print(f"------------------------ TRY {i+1} ------------------------")
        oldBoard = board.copy()
        for cell, cellValue in enumerate(board):
            # if cell != 64: continue
            if cellValue == 0:
                Solving(cell, board)

        PrintBoard(board)

        if 0 not in board: return print(f"SOLVED! {i+1} try")  
        
        if board == oldBoard: 
            print(f"STUCKED AT {i+1} try")
            break

    res = ''.join(map(str, board))
    print(res)

    print(cellNotes)





if __name__ == "__main__":
    main()

