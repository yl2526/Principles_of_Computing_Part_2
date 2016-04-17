"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        for row in xrange(self._grid_height):
            for col in xrange(self._grid_width):
                self.set_empty(row, col)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        out = 0
        while self.num_zombies() > 0 and self.num_zombies() > out:
            yield self._zombie_list[out]
            out += 1
            

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
        
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        out = 0
        while self.num_humans() > 0 and self.num_humans() > out:
            yield self._human_list[out]
            out += 1
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        max_distance = self._grid_width * self._grid_height
        distance_field = [[max_distance for dummy_col in xrange(self._grid_width)] for dummy_row in xrange(self._grid_height)]
        if entity_type == ZOMBIE:
            boundary = poc_queue.Queue()
            for entity in self._zombie_list:
                boundary.enqueue(entity)
                visited.set_full(entity[0], entity[1])
                distance_field[entity[0]][entity[1]] = 0
        else:
            boundary = poc_queue.Queue()
            for entity in self._human_list:
                boundary.enqueue(entity)
                visited.set_full(entity[0], entity[1])
                distance_field[entity[0]][entity[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            if entity_type == ZOMBIE:
                neighbor_cell = visited.four_neighbors(current_cell[0], current_cell[1])
            else:
                neighbor_cell = visited.four_neighbors(current_cell[0], current_cell[1])
            for current_neighbor in neighbor_cell:
                if self.is_empty(current_neighbor[0], current_neighbor[1]) \
                    and visited.is_empty(current_neighbor[0], current_neighbor[1]):
                        visited.set_full(current_neighbor[0], current_neighbor[1])
                        boundary.enqueue(current_neighbor)
                        distance_field[current_neighbor[0]][current_neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human_id in xrange(len(self._human_list)):
            human = self._human_list[human_id]
            neighbors = self.eight_neighbors(human[0], human[1])
            possible_moves = [n for n in neighbors if self.is_empty(n[0], n[1])]
            possible_moves.append(human)
            max_distance = max([zombie_distance_field[n[0]][n[1]] for n in possible_moves])
            max_distance_move = [n for n in possible_moves if max_distance == zombie_distance_field[n[0]][n[1]]]
            # - 1 to offset index and sample
            self._human_list[human_id] = max_distance_move[random.randint(1, len(max_distance_move))-1]
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie_id in xrange(len(self._zombie_list)):
            zombie = self._zombie_list[zombie_id]
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            possible_moves = [n for n in neighbors if self.is_empty(n[0], n[1])]
            possible_moves.append(zombie)
            min_distance = min([human_distance_field[n[0]][n[1]] for n in possible_moves])
            min_distance_move = [n for n in possible_moves if min_distance == human_distance_field[n[0]][n[1]]]
            # - 1 to offset index and sample
            self._zombie_list[zombie_id] = min_distance_move[random.randint(1, len(min_distance_move))-1]

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))

#aka = Apocalypse(5, 5)
#aka.add_zombie(1,1)
#aka.add_zombie(3,4)
#print aka._zombie_list
#print aka.num_zombies()
#for s in aka.zombies():
#    print s
#
#aka.add_human(2,2)
#    
#for i in range(5):
#    print aka.compute_distance_field('zombie')[i]

#print random.randint(1, 1)


