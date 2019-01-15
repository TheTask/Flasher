import pygame,random,math
from time import sleep

pygame.init()

#window resolution
screen_width = 800
screen_height = 800

screen = pygame.display.set_mode( ( screen_width,screen_height ) )
pygame.display.set_caption( 'The Flash Game - Marek Borik' )

n_squares_in_row = 7
line_thickness = 20 #pixels

wait_duration = 1.5 #seconds
flash_duration = 0.3 #seconds

fontsize = screen_width // 25
rounds = 10 #rounds of flashes

#defining colors
RED = ( 255,0,0 )
BLUE = ( 0,0,255 )
WHITE = ( 255,255,255 )
BLACK = ( 0,0,0 )


def TextObjects( string,font,color ):
    textSurface = font.render( string,True,color )
    return textSurface,textSurface.get_rect()


def DrawText( string,fontSizeX,color,x,y ):
    text = pygame.font.SysFont( "timesnewroman",int( math.ceil( fontSizeX ) ) )
    TextSurf, TextRect = TextObjects( string,text,color )
    TextRect.center = ( x,y )
    screen.blit( TextSurf,TextRect )


def GenerateColorInfo( n_squares_in_row ):
    n_squares_total = n_squares_in_row ** 2

    not5050 = True #Prevents from having the same amount of red and blue squares if applicable ( e.g. field with dimentions 7 x 7 squares squares will never have this issue )

    while( not5050 ):
        color_info = []

        for i in range( n_squares_total + 1 ):
            rand = random.randint( 0,1 )
            color_info.append( rand )

        counter_red = 0
        counter_blue = 0

        for i in color_info:
            if i == 0:
                counter_red += 1
            if i == 1:
                counter_blue += 1

        if counter_red == n_squares_total // 2 or counter_blue == n_squares_total // 2 or counter_red == counter_blue:
            not5050 = True
        else:
            not5050 = False


    return color_info,counter_red,counter_blue


def DrawSquares( n_squares_in_row,color_info,square_width,square_height ):
    for i in range( n_squares_in_row ):
        for j in range( n_squares_in_row ):
            color = RED if color_info[ i * n_squares_in_row + j ] == 0 else BLUE
            pygame.draw.rect( screen, color, ( j * square_width,i * square_height,j * square_width + square_width,i * square_height + screen_height ),0 )


def DrawGrid( n_squares_in_row,line_thickness,square_width,square_height ):
    for i in range( 1,n_squares_in_row ):
        pygame.draw.line( screen,BLACK,( i * square_width,0 ),( i * square_width,screen_height ),line_thickness )

    for i in range( 1,n_squares_in_row ):
        pygame.draw.line( screen,BLACK,( 0,i * square_height ),( screen_height,i * square_width ),line_thickness )

    for ( start,end ) in [ ( ( 0,0 ),( 0,screen_height) ),
                      ( ( 0,0 ),( screen_width,0 ) ),
                      (( screen_width,0 ),( screen_width,screen_height )),
                      (( 0,screen_height ),( screen_width,screen_height )) ]:
        pygame.draw.line( screen,BLACK,start,end,line_thickness )


def DrawStartScreen():
    end = False

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    end = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill( BLACK )

        DrawText( "The Flash Game - Created by Marek Borik",fontsize * 1.4,WHITE,screen_width * 0.5,screen_height * 0.05 )

        DrawText( "This game will test your subconscious perception.",fontsize,WHITE,screen_width * 0.5,screen_height * 0.2 )
        DrawText( ( "You will be shown a grid of red and blue squares " + str( rounds ) + " times." ),fontsize,WHITE,screen_width * 0.5, screen_height * 0.25 )
        DrawText( "Your task is to determine if you saw more red or blue circles.",fontsize,WHITE,screen_width * 0.5, screen_height * 0.3 )

        DrawText( "If you see more:",fontsize,WHITE,screen_width * 0.3,screen_height * 0.45 )
        DrawText( "If you see more:",fontsize,WHITE,screen_width * 0.7,screen_height * 0.45 )

        pygame.draw.rect( screen,RED,( screen_width * 0.2, screen_height * 0.5,screen_width * 0.2,screen_height * 0.2 ),0 )
        pygame.draw.rect( screen,BLUE,( screen_width * 0.6, screen_height * 0.5,screen_width * 0.2,screen_height * 0.2 ),0 )

        DrawText( "Press Left Arrow",fontsize,WHITE,screen_width * 0.3,screen_height * 0.75 )
        DrawText( "Press Right Arrow",fontsize,WHITE,screen_width * 0.7,screen_height * 0.75 )

        DrawText( "Press spacebar to start",fontsize,WHITE,screen_width * 0.5,screen_height * 0.93 )


        pygame.display.update()


def DoRound():
    left_arrow = False
    right_arrow = False
    turn = False

    #if the windows isn't square, then squares are not squares and we need to treat them like rectangles
    square_width = screen_width / n_squares_in_row

    color_info,n_red,n_blue = GenerateColorInfo( n_squares_in_row )

    screen.fill( BLACK )
    pygame.display.update()

    sleep( wait_duration )

    #flicker squares for the flash duration

    DrawSquares( n_squares_in_row,color_info,square_width,square_width )
    DrawGrid( n_squares_in_row,line_thickness,square_width,square_width )

    pygame.display.update()

    sleep( flash_duration )
    screen.fill( BLACK )
    pygame.display.update()

    while not turn: # after flash wait for the turn to be completed by pressing either arrow to indicate the answer
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_arrow = True
                    turn = True
                if event.key == pygame.K_RIGHT:
                    right_arrow = True
                    turn = True

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    #if the arrow coresponds to the correct answer, return 1, else 0
    return ( n_red >= n_blue and left_arrow ) or ( n_blue >= n_red and right_arrow )


def Game():
    return [ DoRound() for _ in range( rounds ) ].count( True ) #count ones, meaning correct answers


def EndScreen( correct ):
    screen.fill( BLACK )

    DrawText( "You got " + str( correct ) + " / " + str(  rounds ) + " correct!",fontsize * 2,WHITE,screen_width * 0.5,screen_height * 0.5 )

    pygame.display.update()

    end = False

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    end = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


DrawStartScreen()
correct = Game()
EndScreen( correct )
pygame.quit()
quit()
