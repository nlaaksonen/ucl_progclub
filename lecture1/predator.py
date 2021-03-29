from __future__ import print_function
import random
import sys
import os
PREDATOR = 0
PREY = 1
#characters used for printing
S_PREDATOR = "@"
S_PREY = "%"
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
        for i in xrange(self.width):
            output = []
            for j in xrange(self.height):
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

class CreatureCell(BaseCell):
    """
    A cell type specific to this simulation.
    Has a container for a Creature().
    """
    def __init__(self, *args, **kwargs):
        BaseCell.__init__(self, *args, **kwargs)
        self.creature = None

    def addCreature(self, creature):
        """
        This is mainly used when looping through neighbours.
        Then in a pythonic way we try to add a creature to each
        cell until this function returns True or we run out of cells.
        """
        if not self.creature:
            self.creature = creature
            return True
        else:
            return False

    def draw(self):
        if self.creature:
            return self.creature.draw()
        else:
            return S_BACKGROUND

class Creature():
    """
    Prototype for the creatures in our simulation.
    The attributes are self-explanatory. But notice that
    e.g. self.age has different use depending on the subclass
    (for prey it multiplies when age == 0 etc.).
    More importantly, none of that code lies in the Creature
    (or derived) classes.
    """
    def __init__(self):
        self.alive = True
        self.age = 1
        self.name = None
        self.moved = False #whether the creature has moved this turn, or completed any other action

    def die(self):
        """
        Used to flag this creature for deletion.
        """
        self.alive = False

    def draw(self):
        return "x" #one should never see this

class Predator(Creature):
    """
    Predator survives by eating nearby prey, getting more lifetime (age),
    if age = 0 predator dies. Birth keeps track of how long since this creature
    gave birth, if birth == 0 then spawn a new predator and let birth = 9
    """
    def __init__(self):
        Creature.__init__(self)
        self.age = 7
        self.birth = 9
        self.name = PREDATOR

    def draw(self):
        return S_PREDATOR

class Prey(Creature):
    """
    If Prey manages to survive until 0 age, it spawns another Prey adjacent to
    it if there is room.
    """
    def __init__(self):
        Creature.__init__(self)
        self.age = 5
        self.name = PREY

    def draw(self):
        return S_PREY

# # # # # # # #
#
# Rules for predator-prey system
#
# # # # # # # #

def ppRules(creatureCell):
    """
    Implementation of the rules stated above.
    """
    creature = creatureCell.creature
    if creature and creature.alive:
        creature.age -= 1
        creature.moved = False
        if creature.name == PREDATOR:
            if creature.age <= 0: #die of starvation
                creature.die()
                return
    #A predator can either give birth to a new predator,
    #or consume a prey in its neighbourhood, or move,
    #in this order of preference
            if creature.birth <= 0:
                creature.birth = 9
                for cell in creatureCell.neighbourhood:
                    if cell.addCreature(Predator()): #refer to the documentation of BaseCell
                        creature.moved = True
                        return

            for neighbourCell in creatureCell.neighbourhood:
                neighbour = neighbourCell.creature
                if neighbour and neighbour.name == PREY and neighbour.alive:
                    neighbour.die()
                    creature.age += 5
                    creature.moved = True
                    return
        elif creature.name == PREY:
    #A prey multiplies if it reaches 0 age, otherwise it moves randomly
            if creature.age <= 0:
                creature.age = 5
                for neighbourCell in creatureCell.neighbourhood:
                    if neighbourCell.addCreature(Prey()):
                        creature.moved = True
                        return

def ppClearAndMove(creatureCell):
    """
    This takes care of clearing dead creatures from cells
    and then moving those that did not act during ppRules.
    We need 2 separate functions to accomplish what we wish,
    otherwise you would run into bizarre situations where a creature
    that we updated moves to a cell that we did not update yet etc.
    """
    creature = creatureCell.creature
    if creature:
        if not creature.alive:
            creatureCell.creature = None
        elif not creature.moved:
            empty_neighbourhood = []
            for neighbourCell in creatureCell.neighbourhood:
                if not neighbourCell.creature:
                    empty_neighbourhood.append(neighbourCell)

            if empty_neighbourhood:
                random.choice(empty_neighbourhood).creature = creatureCell.creature
                creatureCell.creature = None
            creature.moved = True

# # # # # # # #
#
# End of rules
#
# # # # # # # #

def main():
    #Try out our simulation, feel free to play around with this stuff
    #Currently the only way to break the loop is to Ctrl+C
    world = World(10,10, CreatureCell)
    world.cells[(0,0)].addCreature(Predator())
    world.cells[(7,3)].addCreature(Predator())
    world.cells[(4,8)].addCreature(Predator())
    world.cells[(0,1)].addCreature(Prey())
    world.cells[(5,5)].addCreature(Prey())
    world.cells[(9,0)].addCreature(Prey())

    #Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    stop = False
    while not stop:
        print("Predator = ", S_PREDATOR)
        print("Prey = ", S_PREY)
        print()
        world.draw()
        raw_input("Press ENTER for next iteration or CTRL+C to quit") #this waits for the user to press Enter
        os.system('cls' if os.name == 'nt' else 'clear')
        #we have to do the updating in two iterations because otherwise
        #a creature could move to a cell that has not been updated yet
        world.forEachCell(ppRules)
        world.forEachCell(ppClearAndMove)

if __name__ == "__main__":
    main()
