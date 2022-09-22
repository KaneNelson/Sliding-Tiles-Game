import pygame
import random
import numpy as np
from ClassFile import *
from Solver import *
#from Functions import *



pygame.init()

# Create clock
clock = pygame.time.Clock()

# Set up game window
width = 1050
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sliding Puzzle")
n = 4

# Colors
screenColor = (35, 47, 63)
gameBackgroundColor = (150, 150, 150)
tileColor = (163, 47, 163)
black = (255,255,255)

# keep main loop running
running = True

# Tiles array with 0 being used for the empty spot
tiles = [[1, 2, 3, 4],
         [5, 6, 7, 8],
         [9, 10, 11, 12],
         [13, 14, 15, 0]]

board = Board(screen, clock)
board.generate_board(tiles)

mainFont = pygame.font.SysFont('Arial', 32)

# Initialize buttons
scrambleButton_25 = Button((100, 100, 100), 10, 250, 100, 50, 'SCRAMBLEx25')
scrambleButton_50 = Button((100, 100, 100), 10, 350, 100, 50, 'SCRAMBLEx50')
scrambleButton_100 = Button((100, 100, 100), 10, 450, 100, 50, 'SCRAMBLEx100')
scrambleButton_200 = Button((100, 100, 100), 10, 550, 100, 50, 'SCRAMBLEx200')


randomizeButton = Button((100, 100, 100), 10, 150, 100, 50, 'RANDOMIZE')
solveButton = Button((100, 100, 100), 890, 400, 100, 50, 'SOLVE')

boardTo3x3Button = Button((100, 100, 100), 150, 10, 100, 50, '3x3')
boardTo4x4Button = Button((100, 100, 100), 300, 10, 100, 50, '4x4')
boardTo5x5Button = Button((100, 100, 100), 450, 10, 100, 50, '5x5')
boardTo6x6Button = Button((100, 100, 100), 600, 10, 100, 50, '6x6')
boardTo7x7Button = Button((100, 100, 100), 750, 10, 100, 50, '7x7')
boardTo8x8Button = Button((100, 100, 100), 900, 10, 100, 50, '8x8')



# Main loop
while running:
    # Draw screen and and buttons
    screen.fill(screenColor)
    scrambleButton_25.draw(screen)
    scrambleButton_50.draw(screen)
    scrambleButton_100.draw(screen)
    scrambleButton_200.draw(screen)

    randomizeButton.draw(screen)
    solveButton.draw(screen)

    boardTo3x3Button.draw(screen)
    boardTo4x4Button.draw(screen)
    boardTo5x5Button.draw(screen)
    boardTo6x6Button.draw(screen)
    boardTo7x7Button.draw(screen)
    boardTo8x8Button.draw(screen)


    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Draw the grey board where the tiles will eventually be drawn onto
    board.draw_board(screen)

    # Draw solve button warning
    font = pygame.font.SysFont('timesnewroman', 16)
    warningText1 = font.render("Solve algorithm is very slow,", 1, (0, 0, 0))
    warningText2 = font.render("Use with 3x3 and with scramble", 1, (0, 0, 0))
    screen.blit(warningText1, (840, 460))
    screen.blit(warningText2, (840, 480))

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            board.check_for_valid_move(mouse)


            if randomizeButton.isOver(mouse):
                board.randomize_tiles()

            if scrambleButton_25.isOver(mouse):
                board.scramble(25)
            if scrambleButton_50.isOver(mouse):
                board.scramble(50)
            if scrambleButton_100.isOver(mouse):
                board.scramble(100)
            if scrambleButton_200.isOver(mouse):
                board.scramble(200)



            if solveButton.isOver(mouse):
                board.solve_board()
            if boardTo3x3Button.isOver(mouse):
                board.change_size(3)
            if boardTo4x4Button.isOver(mouse):
                board.change_size(4)
            if boardTo5x5Button.isOver(mouse):
                board.change_size(5)
            if boardTo6x6Button.isOver(mouse):
                board.change_size(6)
            if boardTo7x7Button.isOver(mouse):
                board.change_size(7)
            if boardTo8x8Button.isOver(mouse):
                board.change_size(8)


        # Allows game to be closed
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update()
    clock.tick(100)
