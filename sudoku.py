import tkinter as tk
from tkinter import messagebox


class Solution:

    def calculate_sets(self, board):
        FULL = set(map(str, range(1, 10)))
        sets_of_sets = {}
        for i in range(9):
            sets_of_sets["Hset{0}".format(i)] = FULL.difference(set(board[i]))

        R_board = list(zip(*board[::-1]))
        for i in range(9):
            sets_of_sets["Vset{0}".format(i)] = FULL.difference(set(R_board[i]))

        for i in range(3):
            for j in range(3):
                sets_of_sets["Sset{0}{1}".format(i, j)] = FULL.difference(
                    set([board[3 * i + k][3 * j + l] for k in range(3) for l in range(3)]))

        final_set = {}
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    final_set["Pset{0}{1}".format(i, j)] = sets_of_sets["Hset{0}".format(i)].intersection(
                        sets_of_sets["Vset{0}".format(j)]).intersection(
                        sets_of_sets["Sset{0}{1}".format(i // 3, j // 3)])

        return final_set, list(final_set.keys())

    def solve(self, board):
        final_set, final_list = self.calculate_sets(board)

        if len(final_list) == 0:
            return False
        if len(final_list) == 1:
            board[int(final_list[0][4])][int(final_list[0][5])] = list(final_set[final_list[0]])[0]
            final_set.clear()
            final_list.clear()
            return True

        smallest = 10
        for i in final_list:
            if len(final_set[i]) < smallest:
                smallest = len(final_set[i])
                smallest_key = i

        for i in final_set[smallest_key]:
            board[int(smallest_key[4])][int(smallest_key[5])] = i
            if self.solve(board):
                return True
            board[int(smallest_key[4])][int(smallest_key[5])] = "."

        for i in range(9):
            if "." in board[i]:
                return False

    def solveSudoku(self, board: list[list[str]]) -> None:
        self.solve(board)


class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")
        master.configure(bg='#d9d9d9')

        self.cells = {}
        self.create_board()

        # Solve Button
        self.solve_button = tk.Button(
            master, text="Solve", command=self.solve, bg='black', fg='white', font=('Arial', 14, 'bold'),
            relief='raised', bd=3, cursor='hand2', highlightbackground='black', highlightthickness=2,
            borderwidth=5)
        self.solve_button.grid(row=9, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Clear Button
        self.clear_button = tk.Button(
            master, text="Clear", command=self.clear_board, bg='black', fg='white', font=('Arial', 14, 'bold'),
            relief='raised', bd=3, cursor='hand2', highlightbackground='black', highlightthickness=2,
            borderwidth=5)
        self.clear_button.grid(row=9, column=5, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Configure grid weights for responsiveness
        for i in range(9):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)
        master.grid_rowconfigure(9, weight=1)

    def create_board(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(
                    self.master, width=2, font=('Arial', 18), justify='center',
                    bg='#f7f7f7' if (row // 3 + col // 3) % 2 == 0 else '#e2e2e2', fg='black', relief='ridge', bd=1,
                    highlightthickness=0
                )
                entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                self.cells[(row, col)] = entry

                # Add bold borders for 3x3 grids
                if col % 3 == 0 and col != 0:
                    entry.grid(padx=(6, 1))
                if row % 3 == 0 and row != 0:
                    entry.grid(pady=(6, 1))

    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.cells[(row, col)].get()
                if val == '':
                    current_row.append('.')
                elif val in '123456789':
                    current_row.append(val)
                else:
                    messagebox.showerror("Invalid Input", "Please enter numbers between 1 and 9.")
                    return None
            board.append(current_row)
        return board

    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, tk.END)
                if board[row][col] != '.':
                    self.cells[(row, col)].insert(0, board[row][col])

    def solve(self):
        board = self.get_board()
        if board:
            original_board = [row[:] for row in board]  # Copy for checking if solved
            solution = Solution()
            solution.solveSudoku(board)
            if self.is_solved(board):
                self.set_board(board)
            else:
                messagebox.showinfo("Sudoku Solver", "No solution exists for the provided puzzle.")
                self.set_board(original_board)

    def clear_board(self):
        for cell in self.cells.values():
            cell.delete(0, tk.END)

    def is_solved(self, board):
        for row in board:
            if '.' in row:
                return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x550")
    root.resizable(False, False)
    gui = SudokuGUI(root)
    root.mainloop()