import pygame
import random
import numpy as np
import Solver

class Button():
    def __init__(self, color, x, y, width, height, text='', fontsize=15, outline=(255,255,255)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fontsize = fontsize
        self.outline = outline


    def draw(self, win):
        # Call this method to draw the button on the screen
        if self.outline:
            pygame.draw.rect(win, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.fontsize)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

class Tile():
    def __init__(self, color, x, y, width, height, number, fontsize):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.number = number
        self.fontsize = fontsize

    @property
    def solved(self):
        """
        The puzzle is solved if the flattened board's numbers are in
        increasing order from left to right and the '0' tile is in the
        last position on the board
        """



    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)


        font = pygame.font.SysFont('comicsans', self.fontsize)
        text = font.render(str(self.number), 1, (0, 0, 0))
        win.blit(text, (
        self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

class Board():
    def __init__(self, screen, clock):
        self.tiles = []
        self.size = 4
        self.backgroundX = int(1000 / 2 - 300)
        self.backgroundY = int(800 / 2 - 250)
        self.backgroundWidth = 600+5
        self.backgroundHeight = 600+5
        self.backgroundColor = (150, 150, 150)
        self.screen = screen
        self.clock = clock

    @property
    def tile_size(self):

        return (self.backgroundWidth-5) / self.size

    # Turn an 2D array of a board instance into an array of tile objects
    def generate_board(self, layout):
        self.size = len(layout)
        self.tiles = [[0] * self.size for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                tileColor = (55 + layout[i][j] * (200/self.size**2), 0, 200 - layout[i][j] * (200/self.size**2))
                self.tiles[i][j] = Tile(color=tileColor,
                                        x=(j * self.tile_size + self.backgroundX) + 5,
                                        y=(i * self.tile_size + self.backgroundY) + 5,
                                        width=self.tile_size - 5,
                                        height=self.tile_size - 5,
                                        number=layout[i][j],
                                        fontsize=int((self.tile_size+10)/3))
        return

    def draw_board(self, screen):
        pygame.draw.rect(self.screen, self.backgroundColor, (self.backgroundX, self.backgroundY,  self.backgroundWidth, self.backgroundHeight))
        for i in self.tiles:
            for j in i:
                if j.number != 0:
                    j.draw(screen)
        return

    #check if a move is possible when tile is clicked
    def check_for_valid_move(self, mouse):

        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j].isOver(mouse):

                    # Check if left of tile is open
                    if 0 <= j - 1 < self.size:
                        if self.tiles[i][j - 1].number == 0:
                            # Move tile to empty space
                            self.move_tile(self.tiles[i][j], self.tiles[i][j - 1], 'left')
                            self.tiles[i][j], self.tiles[i][j - 1] = self.tiles[i][j - 1], self.tiles[i][j]

                    # Check if right of tile is open
                    if 0 <= j + 1 < self.size:
                        if self.tiles[i][j + 1].number == 0:
                            # Move tile to empty space
                            self.move_tile(self.tiles[i][j], self.tiles[i][j + 1], 'right')
                            self.tiles[i][j], self.tiles[i][j + 1] = (self.tiles[i][j + 1], self.tiles[i][j])

                    # check if above tile is open
                    if 0 <= i - 1 < self.size:
                        if self.tiles[i - 1][j].number == 0:
                            # Move tile to empty space
                            self.move_tile(self.tiles[i][j], self.tiles[i - 1][j], 'up')
                            self.tiles[i][j], self.tiles[i - 1][j] = self.tiles[i - 1][j], self.tiles[i][j]

                    # Check if below tile is open
                    if 0 <= i + 1 < self.size:
                        if self.tiles[i + 1][j].number == 0:
                            # Move tile to empty space
                            self.move_tile(self.tiles[i][j], self.tiles[i + 1][j], 'down')
                            self.tiles[i][j], self.tiles[i + 1][j] = self.tiles[i + 1][j], self.tiles[i][j]


        return


    def move_tile(self, tile, empty, direction, move_speed=200):
        # Needed to keep original position so coordinates can be properly updated after animating tile
        originalTilePosition = (getattr(tile, 'x'), getattr(tile, 'y'))
        increment = int(self.tile_size / (150/(self.size**2)))

        # Loop to animate the tile moving to empty square
        for _ in range(int(150/(self.size**2))):
            for i in self.tiles:
                for j in i:
                    if j.number == tile.number:
                        if direction == 'left':
                            j.x -= increment
                        if direction == 'right':
                            j.x += increment
                        if direction == 'up':
                            j.y -= increment
                        if direction == 'down':
                            j.y += increment


            pygame.draw.rect(self.screen, self.backgroundColor, (self.backgroundX, self.backgroundY,  self.backgroundWidth, self.backgroundHeight))
            self.draw_board(self.screen)

            pygame.display.update()
            self.clock.tick(move_speed)

        # Since animation loop doesn't change tile coordinates to exact spot this is needed to adjust for that
        # Also moves the coordinates of the empty spot
        for i in self.tiles:
            for j in i:
                if j.number == tile.number:
                    if direction == 'left':
                        j.x = originalTilePosition[0] - self.tile_size
                        empty.x += self.tile_size
                    if direction == 'right':
                        j.x = originalTilePosition[0] + self.tile_size
                        empty.x -= self.tile_size
                    if direction == 'up':
                        j.y = originalTilePosition[1] - self.tile_size
                        empty.y += self.tile_size
                    if direction == 'down':
                        j.y = originalTilePosition[1] + self.tile_size
                        empty.y -= self.tile_size



        return

    def randomize_tiles(self):
        newTiles = []
        notSolvable = True
        while (notSolvable):
            # generate 1D array which contains the tile nums in a random order
            newTiles = [0] * (self.size**2)
            newTiles = [newTiles[i] + i for i in range(len(newTiles))]
            random.shuffle(newTiles)

            # Get number of inversions which is needed to determine if solvable
            inversions = 0
            for i in range(len(newTiles)):

                if newTiles[i] == 0:
                    continue

                j = i + 1
                while j < len(newTiles):
                    if newTiles[i] > newTiles[j] and newTiles[j] != 0:
                        inversions += 1
                    j += 1

            # Check if current randomized configuration is solvable
            notSolvable = not self.isSolvable(np.reshape(newTiles, (self.size, self.size)).tolist(), inversions)

        self.generate_board(np.reshape(newTiles, (self.size, self.size)).tolist())

        return

    def isSolvable(self, tileLayout, inversions):
        # If width is even
        if self.size % 2 == 0:

            # Need to get the row number of where the blank is from the bottom
            # in order to determine solvability
            zeroRowFromBottom = 0
            for i in range(self.size):
                for j in range(self.size):
                    if tileLayout[i][j] == 0:
                        zeroRowFromBottom = self.size - i

            # Solvable if row from bottom is even and inversions is odd or if
            # row is odd and inversions is even
            if zeroRowFromBottom % 2 == 0 and inversions % 2 == 1:
                return True

            elif zeroRowFromBottom % 2 == 1 and inversions % 2 == 0:
                return True

            else:
                return False

        # If width is odd then is solvable if inversions is even
        return inversions % 2 == 0

    def solve_board(self):
        tileOrder = [[0] * self.size for i in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                tileOrder[i][j] = self.tiles[i][j].number

        puzzle = Solver.Puzzle(tileOrder)
        s = Solver.Solver(puzzle)
        p = s.solve()

        moveList = []
        for node in p:
            moveList.append(node.move)

        moveList.pop(0)

        self.execute_solve_order(moveList)
        return

    def execute_solve_order(self, moveList):
        for i in moveList:
            zero = (0, 0)
            moved = (0, 0)

            for j in range(self.size):
                for k in range(self.size):

                    if self.tiles[j][k].number == 0:
                        zero = (j, k)

                        if i == 'left':
                            moved = (j, k+1)
                        if i == 'right':
                            moved = (j, k-1)
                        if i == 'up':
                            moved = (j+1, k)
                        if i == 'down':
                            moved = (j-1, k)

            self.move_tile(self.tiles[moved[0]][moved[1]], self.tiles[zero[0]][zero[1]],  i)

            self.tiles[zero[0]][zero[1]], self.tiles[moved[0]][moved[1]] = (self.tiles[moved[0]][moved[1]],
                                                                            self.tiles[zero[0]][zero[1]])

        return

    # Randomly moves the tiles a certain amount of times
    def scramble(self, count):
        for _ in range(count):
            possibleMoves = []
            zero = (0, 0)
            movedTile = (0, 0)
            randomMove = ''
            for i in range(self.size):
                for j in range(self.size):

                    if self.tiles[i][j].number == 0:
                        zero = (i, j)
                        if 0 <= j+1 < self.size:
                            possibleMoves.append('left')
                        if 0 <= j-1 < self.size:
                            possibleMoves.append('right')
                        if 0 <= i+1 < self.size:
                            possibleMoves.append('up')
                        if 0 <= i-1 < self.size:
                            possibleMoves.append('down')

                        randomMove = possibleMoves[random.randint(0,len(possibleMoves)-1)]

                        if randomMove == 'left':
                            movedTile = (i, j+1)
                        if randomMove == 'right':
                            movedTile = (i, j-1)
                        if randomMove == 'up':
                            movedTile = (i+1, j)
                        if randomMove == 'down':
                            movedTile = (i-1, j)

                        self.move_tile(self.tiles[movedTile[0]][movedTile[1]], self.tiles[zero[0]][zero[1]],
                                       randomMove)

            self.tiles[movedTile[0]][movedTile[1]], self.tiles[zero[0]][zero[1]] = (self.tiles[zero[0]][zero[1]],
                                                                                    self.tiles[movedTile[0]][movedTile[1]])
        return

    # Make adjustments when the board is changed to more or less tiles
    def change_size(self, newSize):
        self.size = newSize
        # Make a 1D array of the new tiles in order
        newTiles = [(i+1) % newSize**2 for i in range(newSize**2)]

        # Convert new array to 2D
        newTiles = np.reshape(newTiles, (newSize, newSize)).tolist()

        self.generate_board(newTiles)
        return

