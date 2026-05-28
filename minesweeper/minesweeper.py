import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # creating an empty set to return in case no mines
        no_mines = set()

        # checking whether there are mines in self.cells
        if self.count > 0:

            # if the number of cells is equal to the count
            # we know that all of that sentence’s cells must be mines.
            if self.count == len(self.cells):
                # returning cells that are mines
                return self.cells

        # else no mines
        return no_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # creating an empty set to return in case mines
        mines = set()

        # if there are no mines
        # then safe
        if self.count == 0:
            # returning the safe cells
            return self.cells
        else:
            # returning that there is a mine
            return mines

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # if cell is in sentence to reduce set
        if cell in self.cells:

            # removing cell from sentence
            self.cells.remove(cell)

            # in case of mine reduce count of mines
            # to deduce which others are mines

            # for example
            # { A, B ,C} = 2
            # C is a mine
            # {A,B} = 1
            # easier for AI to deduce the last mine
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # if cell is in sentence
        if cell in self.cells:

            # removing cell from sentence to reduce set
            self.cells.remove(cell)

            # in case of safe mine
            # don't change the mine count

            # for example
            # {A, B, C} = 2
            # C is a safe mine
            # remove C
            # dont reduce count
            # {A, B} = 2
            # therefore A and B are mines , easier for AI to deduce


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        neighbour = set()

        # looping over neighbouring cells adding to all cells if unvisited

        for row in range(cell[0] - 1, cell[0] + 2):

            for column in range(cell[1] - 1, cell[1] + 2):

                # when reaching over original safe cell
                # ignore
                # already added and marked
                if (row, column) == cell:

                    # move to next iteration
                    continue

                # reduce count in case of mine
                if (row, column) in self.mines:
                    count -= 1
                    continue

                # ignore incase of safe area
                if (row, column) in self.safes:
                    continue

                # checking whether cell fits the grid
                # row wise and column wise
                if (0 <= row < self.height) and (0 <= column < self.width):

                    # add them to total cells if they are in grid
                    neighbour.add((row, column))

        # for row in range(cell[0] - 1, cell[0] + 2):
        # add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`.

        self.knowledge.append(Sentence(neighbour, count))

        # mark any additional cells as safe or as mines [ERROR]

        insert = True

        # when additional cells added
        while insert:
            insert = False

            safe_cells = set()
            mine_cells = set()

            for sentence in self.knowledge:
                # integrating new safe cells added with previous safe cells
                # via union function
                safe_cells = safe_cells.union(sentence.known_safes())

                # integrating new mine cells added with previous mine cells
                # via union function
                mine_cells = mine_cells.union(sentence.known_mines())

            # Mark safe cell
            if safe_cells:
                insert = True
                for cell in safe_cells:
                    self.mark_safe(cell)

            # Mark mine cell
            if mine_cells:
                insert = True
                for cell in mine_cells:
                    self.mark_mine(cell)

        # new sentences inference from the subset method
        for sentence in self.knowledge:

            for block in range(len(self.knowledge)):

                if (sentence != self.knowledge[block]):

                    # subset method
                    # we have two sentences set1 = count1 and set2 = count2
                    # where set1 is a subset of set2, then we can construct
                    # the new sentence set2 - set1 = count2 - count1.

                    # if sentence is a subset of self knowledge cells

                    if (sentence.cells.issubset(self.knowledge[block].cells)):
                        self.knowledge[block].cells -= sentence.cells
                        self.knowledge[block].count -= sentence.count

                    # if self knowledge cells are a subset of sentence
                    if (self.knowledge[block].cells.issubset(sentence.cells)):

                        sentence.cells -= self.knowledge[block].cells
                        sentence.count -= self.knowledge[block].count

    def make_safe_move(self):  # [EASY]
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # select a safe action
        for action in self.safes:

            # make sure it is not a previous action
            # otherwise will cause error due to overlap
            if action not in self.moves_made:

                return action

        # when no safe actions left
        return None

    def make_random_move(self):  # [EASY]
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:

            # picking a random row from [0 to height] range
            row = random.randint(0, self.height)
            # picking a random column from [0 to width] range
            column = random.randint(0, self.width)

            # if cell has not already been used and is not a mine
            if ((row, column) not in self.moves_made) and ((row, column) not in self.mines):

                # return action
                return (row, column)

        # return in case of no action
        return None
