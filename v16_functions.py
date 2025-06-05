import math

numbers: list[int] = [1,2,3,4,5,6,7,8,9]
cellNotes = {}
missingNumbersData = {"row": {}, "column": {}, "box":{}}

sudokuBox = {
    0: {"row": [0,1,2], "column": [0,1,2]},
    1: {"row": [0,1,2], "column": [3,4,5]},
    2: {"row": [0,1,2], "column": [6,7,8]},

    3: {"row": [3,4,5], "column": [0,1,2]},
    4: {"row": [3,4,5], "column": [3,4,5]},
    5: {"row": [3,4,5], "column": [6,7,8]},

    6: {"row": [6,7,8], "column": [0,1,2]},
    7: {"row": [6,7,8], "column": [3,4,5]},
    8: {"row": [6,7,8], "column": [6,7,8]},

}


def PrintBoard(board: list[int]) -> None:
    line: str = "- - - - - - - - - - -"
    content: str = line + "\n"

    for i, data in enumerate(board):
        index = i+1
        data = str(data)
        content = content + data + " "

        if (index) % 3 == 0 and (index) % 9 != 0:
            content += "| "
        
        if (index) % 9 == 0:
            content += "\n"

        if (index) % 27 == 0:
            content = content + line + "\n"

    print(content)

# --------------------------------------------------------------------- NOTES
def GetCellNote(ValuesData):
    answers = []
    for number in numbers:
        valid = True
        for values in ValuesData:
            if number in values:
                valid = False
                break
        if valid: answers.append(number)
    return answers


def GetAllNotes(board):
    for cell, cellValue in enumerate(board):
        if cellValue != 0: continue

        cellRow, cellColumn = CellToCoordinate(cell)
        cellBox = CellToBox(cell)

        rowValues = RowValues(cellRow, board)
        rowMissingNumbers = MissingNumbers(rowValues)

        columnValues = ColumnValues(cellColumn, board)
        columnMissingNumbers = MissingNumbers(columnValues)

        boxValues = BoxValues(cell, board)
        boxMissingNumbers = MissingNumbers(boxValues)

        valuesData = [rowValues, columnValues, boxValues]

        cellNote = GetCellNote(valuesData)

        if cell not in cellNotes:
            cellNotes[cell] = cellNote
        
        elif len(cellNotes[cell]) < len(cellNote):
            newNotes = [number for number in cellNotes[cell] if number in cellNote]
            cellNotes[cell] = newNotes
            # print(f"newNotes: {newNotes}")
        else: cellNotes[cell] = cellNote
            
        missingNumbersData["row"][cellRow] = rowMissingNumbers
        missingNumbersData["column"][cellColumn] = columnMissingNumbers
        missingNumbersData["box"][cellBox] = boxMissingNumbers

# --------------------------------------------------------------------- NOTES


def MissingNumbers(array: list[int])-> list[int]:
    missingNumbers: list[int] = [num for num in numbers if num not in array]
    return missingNumbers

# CELL MANIPULATION START
def CellToRow(cell:int) -> int:
    return math.floor(cell / 9)

def CellToColumn(cell:int) -> int:
    return cell % 9

def CellToCoordinate(cell:int)-> list[int]:
    return [CellToRow(cell), CellToColumn(cell)]

def CoordinateToCell(row: int, column: int) -> int:
    return 9 * row + column

def RowCells(row): return list(range(row*9,row*9+9))

def ColumnCells(column): return list(range(column, 81, 9))

# CELL MANIPULATION END

# ROW COLUMN AND BOX START
def RowValues(row: int, board: list[int]) -> list[int]:
    start: int = row * 9
    end: int = start + 9
    rowValues: list[int] = board[start:end]
    return rowValues

def ColumnValues(column: int,board: list[int]) -> list[int]:
    columnValues: list[int] = board[column : 72 * (column + 1) + 1 : 9]
    return columnValues


def BoxCells(cell: int, board: list[int]) -> list[int]:
    sequence = [ [0,1,2], [3,4,5], [6,7,8] ]
    row, column = CellToCoordinate(cell)

    # cek cell berada di rentang box apa
    for seq in sequence:
        if row in seq:
            rowSequence = seq
        if column in seq:
            columnSequence = seq
    
    # ambil semua koordinat box nya
    boxCells = []
    for row in rowSequence:
        for column in columnSequence:
            cell = CoordinateToCell(row, column)
            boxCells.append(cell)
    return boxCells

def BoxValues(cell:int, board:list[int]) -> list[int]:
    boxCells:list[int] = BoxCells(cell, board)
    boxValues:list[int] = [board[cell] for cell in boxCells]
    return boxValues
# ROW COLUMN AND BOX END


def CellToBox(cell):
    cellRow, cellColumn = CellToCoordinate(cell)
    for box, boxItems in sudokuBox.items():
        if cellRow in boxItems["row"] and cellColumn in boxItems["column"]: return box

def BoxDetails(boxNumber, board):
    boxRow = sudokuBox[boxNumber]["row"][0]
    boxColumn = sudokuBox[boxNumber]["column"][0]
    cell = CoordinateToCell(boxRow, boxColumn)
    return BoxCells(cell, board), BoxValues(cell, board)


def SolveThreeTypes(type, index, board):
    match type:
        case "row"      : dataCells = RowCells(index)
        case "column"   : dataCells = ColumnCells(index)
        case "box"      : dataCells = BoxDetails(index, board)[0]

    for missingNumber in missingNumbersData[type][index]:
        count = 0
        for cell in dataCells:
            if board[cell] != 0: continue
            if missingNumber in cellNotes[cell]:
                count += 1
                if count > 1: break
                answerCell = cell
        
        if count != 1: continue
        board[answerCell] = missingNumber
        cellNotes.pop(answerCell)
        print(f"           {type} {index} -> cell {answerCell}: {missingNumber}")
        GetAllNotes(board)



def PointingNotes(index, board):
    boxCells = BoxDetails(index, board)[0]
    for missingNumber in missingNumbersData["box"][index]:
        rowData = set()
        columnData = set()
        cellsWithMissingNumber = []
        for cell in boxCells:
            if board[cell] != 0: continue
            if missingNumber in cellNotes[cell]:
                cellRow, cellColumn = CellToCoordinate(cell)
                rowData.add(cellRow)
                columnData.add(cellColumn)
                cellsWithMissingNumber.append(cell)
        
        if len(rowData) == 1:
            [rowNumber] = [number for number in rowData]
            rowCells = RowCells(rowNumber)
            for rowCell in rowCells:
                if board[rowCell] != 0: continue
                if missingNumber in cellNotes[rowCell] and rowCell not in cellsWithMissingNumber:
                    cellNotes[rowCell].remove(missingNumber)
                    print(f"           row method -> remove {missingNumber} in row {rowNumber} cell {rowCell}")

        
        if len(columnData) == 1:
            [columnNumber] = [number for number in columnData]
            columnCells = ColumnCells(columnNumber)
            for columnCell in columnCells:
                if board[columnCell] != 0: continue
                if missingNumber in cellNotes[columnCell] and columnCell not in cellsWithMissingNumber:
                    cellNotes[columnCell].remove(missingNumber)
                    print(f"           column method -> remove {missingNumber} in column {columnNumber} cell {columnCell}")
        
    
def ObviousPair(type, index, board) -> None:
    # print("obvious pair")
    match type:
        case "row" :
            if len(MissingNumbers(RowValues(index, board))) == 2: return
            dataCells = RowCells(index)
        case "column" : 
            if len(MissingNumbers(ColumnValues(index, board))) == 2: return
            dataCells = ColumnCells(index)
        case "box" : 
            dataCells, boxValues = BoxDetails(index, board)
            if len(MissingNumbers(boxValues)) == 2: return
    
    currentCellNotes = {}
    pairs = {}
    triplesCells = []
    triples = set()

    for cell in dataCells:
        if board[cell] != 0: continue
        if len(cellNotes[cell]) == 2: currentCellNotes[cell] = cellNotes[cell]
    
    if len(currentCellNotes) < 2: return

    # FOR PAIRS
    for cell, note in currentCellNotes.items():
        for currentCell, currentNote in currentCellNotes.items():
            if currentCell == cell: continue
            if note == currentNote: pairs[tuple(note)] = [currentCell, cell]
    
    # FOR TRIPLES, EXAMPLE: {18: [1, 5], 19: [1, 8], 20: [5, 8]}
    for cell, note in currentCellNotes.items():
        if pairs.get(tuple(note)) is None:
            triplesCells.append(cell)
            for number in note: triples.add(number)

    if len(pairs) != 0:
        for pair, pairCells in pairs.items():
            for cell in dataCells:
                if board[cell] != 0: continue
                if cell in pairCells: continue
                for number in pair:
                    if number in cellNotes[cell]: 
                        cellNotes[cell].remove(number)
                        print(f"           obvious pair {pair} -> remove {number} on cell {cell}")
    
    if len(triplesCells) == 3 and len(triples) == 3:
        for cell in dataCells:
            if board[cell] != 0: continue
            if cell in triplesCells: continue
            for number in triples:
                if number not in cellNotes[cell]: continue
                cellNotes[cell].remove(number)
                print(f"           obvious triples {triples} -> remove {number} on cell {cell}")


def ObviousTriples(type, index, board) -> None:
    # print("obvious triple")
    match type:
        case "row" :
            if len(MissingNumbers(RowValues(index, board))) == 2: return
            dataCells = RowCells(index)
        case "column" : 
            if len(MissingNumbers(ColumnValues(index, board))) == 2: return
            dataCells = ColumnCells(index)
        case "box" : 
            dataCells, boxValues = BoxDetails(index, board)
            if len(MissingNumbers(boxValues)) == 2: return
    
    twoNumbersNote = {}
    threeNumbersNote = {}
    pairs = {}
    for cell in dataCells:
        if board[cell] != 0: continue
        if len(cellNotes[cell]) == 3: threeNumbersNote[cell] = cellNotes[cell]
    
    for cell, note in threeNumbersNote.items():
        if tuple(note) not in pairs:
            pairs[tuple(note)] = set()
        for currentCell, currentNote in threeNumbersNote.items():
            if currentCell == cell: continue
            if note == currentNote:
                pairs[tuple(note)].add(cell)
                pairs[tuple(note)].add(currentCell)
    
    for pair, pairCells in pairs.items():
        if not bool(pairCells): continue

        if len(pairCells) == 2:
            for cell in dataCells:
                if board[cell] != 0: continue
                if len(cellNotes[cell]) == 2:
                    firstNumber, secondNumber = cellNotes[cell]
                    if firstNumber in pair and secondNumber in pair:
                        pairs[pair].add(cell)
    
    for pair, pairCells in pairs.items():
        if not bool(pairCells): continue
        if len(pairCells) == 3:
            for cell in dataCells:
                if board[cell] != 0: continue
                if cell in pairCells: continue
                for number in pair:
                    if number not in cellNotes[cell]: continue
                    cellNotes[cell].remove(number)
                    print(f"           obvious triples {pair} -> remove {number} on cell {cell}")

    
def HiddenPair(type, index, board) -> None:
    match type:
        case "row" :
            missingNumbers = missingNumbersData["row"][index]
            if len(missingNumbers) == 2: return
            dataCells = RowCells(index)
        case "column" : 
            missingNumbers = missingNumbersData["column"][index]
            if len(missingNumbers) == 2: return
            dataCells = ColumnCells(index)

        case "box" : 
            missingNumbers = missingNumbersData["box"][index]
            if len(missingNumbers) == 2: return
            dataCells, boxValues = BoxDetails(index, board)

    possibleNumbers = {}
    pairs = {}

    for number in missingNumbers:
        
        cellsWithNumber = []
        for cell in dataCells:
            if board[cell] != 0: continue
            if number in cellNotes[cell]: cellsWithNumber.append(cell)
        if len(cellsWithNumber) != 2: continue
        possibleNumbers[number] = cellsWithNumber
    
    # print("hidden pair!")
    # print(possibleNumbers)
    # return
    if len(possibleNumbers) < 2: return
    pairsNumbers = []
    for number, cells in possibleNumbers.items():
        for currentNumber, currentCells in possibleNumbers.items():
            if number == currentNumber: continue
            if cells == currentCells:
                if number in pairsNumbers or currentNumber in pairsNumbers: continue
                pairs[tuple([number, currentNumber])] = currentCells
                pairsNumbers.append(number)
                pairsNumbers.append(currentNumber)
    
    if len(pairs) == 0: return
    print(f"hidden pair {type} {index} -> {pairs}")
    
    for cell in dataCells:
        if board[cell] != 0: continue

        for pair, pairCells in pairs.items():
            if cell in pairCells:
                if len(cellNotes[cell]) > 2:
                    cellNotes[cell] = list(pair)
                    print(f"   cell {cell} change notes to {pair}")

            if cell not in pairCells:
                for number in pair:
                    if number in cellNotes[cell]:
                        cellNotes[cell].remove(number)
                        print(f"   here! remove {number} on cell {cell} => cellnote: {cellNotes[cell]}")

        
    

    




    
def Solving(cell, board):
    print(f"cell {cell}")

    cellRow, cellColumn = CellToCoordinate(cell)
    cellBox = CellToBox(cell)
    cellNote = cellNotes[cell]

    # jika cellnote hanya berisi satu angka maka jawab cell dengan angka tersebut
    if len(cellNote) == 1:
        board[cell] = cellNote[0]
        print(f"           only one cellnote: {cellNote[0]}")
        cellNotes.pop(cell)
        GetAllNotes(board)
        return
    
    SolveThreeTypes("row", cellRow, board)
    SolveThreeTypes("column", cellColumn, board)
    SolveThreeTypes("box", cellBox, board)
    
    GetAllNotes(board)

    PointingNotes(cellBox, board)

    ObviousPair("row", cellRow, board)
    ObviousPair("column", cellColumn, board)
    ObviousPair("box", cellBox, board)

    ObviousTriples("row", cellRow, board)
    ObviousTriples("column", cellColumn, board)
    ObviousTriples("box", cellBox, board)

    HiddenPair("row", cellRow, board)
    HiddenPair("column", cellColumn, board)
    HiddenPair("box", cellBox, board)


        




    









