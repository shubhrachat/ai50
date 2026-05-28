import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # satisfying unary constraints
        # for every variable in the crossword
        # crossword.variables is a set of all of the variables in the puzzle
        for variable in self.crossword.variables:

            # for every possible value in the crossword variable's domain of words
            # crossword.words is a set of all of the words to draw
            # from when constructing the crossword puzzle.
            for value in self.crossword.words:

                # making sure that every value in a variable’s domain has
                # the same number of letters as the variable’s length.
                if len(value) != variable.length:

                    # removing value from variable's domain
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # no change made yet
        revision = False
        # stores overlaps
        overlap = self.crossword.overlaps[x, y]

        # valeues to be removed
        inconsistent = []

        # looking for an overlap
        # for every word in domain of x
        for word1 in self.domains[x]:

            # for every word in domain of y
            for word2 in self.domains[y]:

                # checking if any overlap
                # if no direct overlap return False
                if overlap is None:
                    # no change made
                    return False

                # if there is an overlap
                # where exactly is it
                else:
                    if word1[overlap[0]] == word2[overlap[1]]:
                        # revision remains False
                        # as no change made
                        break
            else:
                # add inconsistent word from domain of x to list
                inconsistent.append(word1)
                # change made
                revision = True

        # for multiple inconsistent words
        # if no inconsistent words
        # receives an emtpy list and hence removes nothing
        for i in inconsistent:
            # removing from the domain of x
            # the valye of i
            self.domains[x].remove(i)

        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        '''
        referring to this pseudocode from Harvard CS50AI
        function AC-3(csp):

        queue = all arcs in csp
        while queue non-empty:
        (X, Y) = Dequeue(queue)
        if Revise(csp, X, Y):
        if size of X.domain == 0:
        return false
        for each Z in X.neighbors - {Y}:
        Enqueue(queue, (Z,X))
        return true
        '''

        # when arcs is none
        if arcs is None:
            # initial queue of all arcs
            queue = []
            # for every variable of x
            for x in self.crossword.variables:
                # and for every neighbour of x
                for y in self.crossword.neighbors(x):
                    # if not equal
                    if (x != y):
                        # append
                        queue.append((x, y))
        else:
            # queue is intiial set of arcs
            queue = arcs

        while queue:
            # (X, Y) = Dequeue(queue)
            (x, y) = queue.pop()

            # if Revise(csp, X, Y):
            if self.revise(x, y):

                # if size of X.domain == 0:
                if len(self.domains[x]) == 0:
                    # a domain is empty
                    return False

                for Z in self.crossword.neighbors(x):
                    '''
                    for each Z in X.neighbors - {Y}:
                       Enqueue(queue, (Z,X))
                    '''

                    if y != Z:

                        queue.append((Z, x))

        # no domains empty
        # consistency enforced
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # iterating every varaible in crossword
        for variable in self.crossword.variables:

            # checking if they have been assigned
            if variable not in assignment:

                # returning False when not in assigment dictionary
                return False

        # returning True when in assigment dictionary
        # therefore has been assigned
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        '''
        An assignment is consistent if it satisfies all of the constraints of the problem:
        that is to say, all values are distinct, every value is the correct length,
        and there are no conflicts between neighboring variables.
        '''

        # check length of value

        for variable in assignment:
            # checking whether every value is of the correct length
            if variable.length != len(assignment[variable]):
                return False

        # checking whether values are distinct

        # storing values
        values = []

        # for every item in values
        for item in assignment.values():

            # if item already exists then no distinct
            # returns false
            if item in values:
                return False
            else:
                # adds item to the list when distinct
                values.append(item)

        # checking if there are no conflicts between neighboring variables

        # for every crossword blank word
        for variable, word in assignment.items():
            # whatever is in common between the neighbors of variable and the crossword variables
            for neighbor in self.crossword.neighbors(variable).intersection(assignment.keys()):
                overlap = self.crossword.overlaps[variable, neighbor]
                # in case of conflict
                if word[overlap[0]] != assignment[neighbor][overlap[1]]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        heuristics = {}
        # neighbouring variables
        neighbors = self.crossword.neighbors(var)

        variables = self.domains[var]

        exclusion = 0

        # going through every variable
        for variable in variables:

            # when variable does not have a value
            if variable not in assignment:

                # scanning through neighbors
                for neighbor in neighbors:

                    # checking for overlap
                    if variable in self.domains[neighbor]:
                        # for every overlap increment
                        exclusion += 1

                # stores count to value of unassigned variable
                heuristics[variable] = exclusion

            else:
                # variable present in assignment already has a value,
                #  and therefore shouldn’t be counted
                continue

        # return in ascending order
        return sorted(heuristics, key=lambda key: heuristics[key])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Return an unassigned variable not already part of `assignment`.
        unassigned = []

        for variables in self.crossword.variables:

            if variables not in assignment:

                unassigned.append(variables)

        # sort according to increasing number of remaining values in its domain
        # setting degree to choose largest from

        # sorting in two ways
        # sorting the words in domain in ascending order
        # sorting the degrees (number of neighbors) in a descending order
        unassigned.sort(key=lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x))))

        # returning according to the minimum remaining value heuristic
        # and then the degree heuristic.
        # first value in the ascending list
        # has the minimum remaining domain value
        return unassigned[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        '''
        Referring to this pseudocode from CS50AI
        function Backtrack(assignment, csp):

        if assignment complete:
        return assignment
        var = Select-Unassigned-Var(assignment, csp)
        for value in Domain-Values(var, assignment, csp):
        if value consistent with assignment:
        add {var = value} to assignment
        inferences = Inference(assignment, csp)
        if inferences ≠ failure:
        add inferences to assignment
        result = Backtrack(assignment, csp)
        if result ≠ failure:
        return result
        remove {var = value} and inferences from assignment
        return failure
        '''
        failure = None
        # if assignment complete:
        if self.assignment_complete(assignment):
            return assignment

        # var = Select-Unassigned-Var(assignment, csp)
        var = self.select_unassigned_variable(assignment)

        '''
        for value in Domain-Values(var, assignment, csp):
        if value consistent with assignment:
        add {var = value} to assignment
        '''
        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                assignment[var] = value
                # result = Backtrack(assignment, csp)
                result = self.backtrack(assignment)

                '''
                 if result ≠ failure:
                 return result
                 remove {var = value} and inferences from assignment
                 '''
                if result != failure:
                    return result
            assignment.pop(var)

            return failure


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
