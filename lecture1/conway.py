from __future__ import print_function
import random
import sys
import os
#characters used for printing
S_CONWAY = "O"
S_BACKGROUND = "."

class World():
    """
    This class represents the world of the simulation which consits of cells.
    Currently only supports grid arrangement and no wrapping.
    The Cell in constructor should be a subclass of BaseCell
    """
    def __init__(self, width=10, height=10, Cell=None):
        self.cells = {} #a dictionary of cells which each can contain a Creature : key = (x,y), value = BaseCell()
        self.width, self.height = width, height
        #initialize cells in to a grid configuration
        for i in xrange(width):
            for j in xrange(height):
                self.cells[(i,j)] = Cell(i, j)
        #now store a reference to the neighbourhood of each cell
        for coord, cell in self.cells.iteritems():
            cell.neighbourhood = [self.cells[c] for c in self.getNeighbourIndices(coord)]

    def getNeighbourIndices(self, (i, j)):
        """
        Returns the indices for the neighbouring points in a lattice
        """
        return [(x, y) for x in range(max(0, i-1), min(self.width, i+2))
                for y in range(max(0, j-1), min(self.height, j+2))
                if not (x is i and y is j)]

    def forEachCell(self, func):
        """
        This is the interface that is used to apply the simulation logic
        """
        for cell in self.cells.values():
            func(cell)

    def draw(self):
        """
        Each cell is supposed to output a character in their draw method,
        which is then added to a list.
        Notice that we're not constructing the string until on the very last line.
        This is more efficient.
        """
        for j in xrange(self.height): #Notice there was a bug here before where these two for loops were in reverse order
            output = []
            for i in xrange(self.width):
                cell = self.cells[(i, j)]
                output.append(cell.draw())
            print(''.join(output))

class BaseCell():
    """
    Prototype for cells to be stored in World.
    Neighbourhood holds a collection of references
    to neighbouring cells. Notice that this implementation
    does not depend on coordinates as the neighbourhood
    could be anything.
    """
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.neighbourhood = []

    def draw(self):
        """
        Virtual function to indicate that
        all derived classes should implement it.
        This will happen in future too without mention.
        """
        pass

class ConwayCell(BaseCell):
    """
    In this case the cell structure is a lot simpler as we
    do not need to store different objects in each cell.
    It is enough to just store the current state of the cell
    and the one where it has to change in the next iteration
    (make sure you understand why we need to store the next state).
    """
    def __init__(self, *args, **kwargs):
        BaseCell.__init__(self, *args, **kwargs)
        self.alive = False
        self.next_state = False

    def die(self):
        self.next_state = False

    def birth(self):
        self.next_state = True

    def draw(self):
        if self.alive:
            return S_CONWAY
        else:
            return S_BACKGROUND

# # # # # # # #
#
# Rules for Game of Life
#
# # # # # # # #

def conwayRules(conwayCell):
    """
    Fairly simple set of rules, adapted from
    http://en.wikipedia.org/wiki/Conway's_Game_of_Life
    """
    cell = conwayCell
#do neighbour count
    alive_neighbours = 0
    for neighbour in cell.neighbourhood:
        if neighbour.alive:
            alive_neighbours += 1

    if cell.alive:
        if alive_neighbours < 2 or alive_neighbours > 3:
            return cell.die()
    else:
        if alive_neighbours == 3:
            return cell.birth()

def conwayUpdate(conwayCell):
    """
    Even simpler update function.
    """
    conwayCell.alive = conwayCell.next_state

# # # # # # # #
#
# End of rules
#
# # # # # # # #

def main():
    #Try out our simulation, feel free to play around with this stuff
    #Currently the only way to break the loop is to Ctrl+C
    world = World(10,10, ConwayCell) #Notice we have to pass the new type of cell here

    #a slightly better way of populating the grid (compared to how we
    #did it in the pp-system). Build up a list of all the live cells and
    #then iterate through it
    live_cells = [ (4,6), (5,6), (6,6), (1,0), (2,1), (0,2), (1,2), (2,2) ]
    for (i, j) in live_cells:
        world.cells[(i,j)].birth()

    #Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    stop = False
    while not stop:
        #the structure here has changed a little bit, ultimately it only makes a difference for how the first iteration is displayed.
        world.forEachCell(conwayUpdate)
        world.draw()
        raw_input("Press ENTER for next iteration or CTRL+C to quit") #this waits for the user to press Enter
        os.system('cls' if os.name == 'nt' else 'clear')
        world.forEachCell(conwayRules)

if __name__ == "__main__":
    main()
