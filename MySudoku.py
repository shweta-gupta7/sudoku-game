import pygame

pygame.init()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)
button_font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 28)
congrats_font = pygame.font.SysFont(None, 48)

WIDTH = 800
HEIGHT = 760

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

icon = pygame.image.load("sudoku.png")
pygame.display.set_icon(icon)

CELL_SIZE = 60
GRID_SIZE = CELL_SIZE * 9

margin_x = (WIDTH - GRID_SIZE) // 2
margin_y = 80


# ---------------- BOARD ----------------

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solution_board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],

    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],

    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]


# ---------------- GAME VARIABLES ----------------

player_board = []

for row in board:
    player_board.append(row[:])

selected_row = None
selected_col = None

errors = 0
wrong_cells = []
selected_number = 0
locked_cells = []

game_completed = False


# ---------------- BUTTONS ----------------

number_buttons = []

for i in range(9):
    number_buttons.append(
        pygame.Rect(
            margin_x + i * 60,
            690,
            50,
            50
        )
    )

# Eraser and Reset buttons
eraser_button = pygame.Rect(620, 25, 60, 45)
reset_button = pygame.Rect(700, 25, 60, 45)

# Congratulations - New Game button
new_game_button = pygame.Rect(300, 500, 200, 55)


# ---------------- RESET FUNCTION ----------------

def reset_game():
    global player_board
    global selected_row
    global selected_col
    global errors
    global wrong_cells
    global selected_number
    global locked_cells
    global game_completed

    player_board = []

    for row in board:
        player_board.append(row[:])

    selected_row = None
    selected_col = None
    errors = 0
    wrong_cells = []
    selected_number = 0
    locked_cells = []
    game_completed = False


# ---------------- CHECK COMPLETION ----------------

def check_completed():
    for row in range(9):
        for col in range(9):
            if player_board[row][col] != solution_board[row][col]:
                return False

    return True


# ---------------- MAIN LOOP ----------------

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ==================================================
        # CONGRATULATIONS WINDOW
        # ==================================================

        if game_completed:

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if new_game_button.collidepoint(mouse_x, mouse_y):
                    reset_game()

            continue


        # ==================================================
        # MOUSE CLICK
        # ==================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # ---------------- Sudoku grid ----------------

            if (
                margin_x <= mouse_x <= margin_x + GRID_SIZE
                and
                margin_y <= mouse_y <= margin_y + GRID_SIZE
            ):

                selected_col = (mouse_x - margin_x) // CELL_SIZE
                selected_row = (mouse_y - margin_y) // CELL_SIZE

                selected_number = player_board[selected_row][selected_col]


            # ---------------- Number buttons ----------------

            for i in range(9):

                if number_buttons[i].collidepoint(mouse_x, mouse_y):

                    if (
                        selected_row is not None
                        and
                        selected_col is not None
                    ):

                        num = i + 1

                        if board[selected_row][selected_col] == 0:

                            if (
                                selected_row,
                                selected_col
                            ) not in locked_cells:

                                if num == solution_board[selected_row][selected_col]:

                                    # Correct number
                                    player_board[selected_row][selected_col] = num

                                    locked_cells.append(
                                        (selected_row, selected_col)
                                    )

                                    if (
                                        selected_row,
                                        selected_col
                                    ) in wrong_cells:

                                        wrong_cells.remove(
                                            (selected_row, selected_col)
                                        )

                                    selected_number = num

                                    # Check if game is complete
                                    if check_completed():
                                        game_completed = True

                                else:

                                    # Wrong number
                                    errors += 1

                                    player_board[selected_row][selected_col] = num

                                    if (
                                        selected_row,
                                        selected_col
                                    ) not in wrong_cells:

                                        wrong_cells.append(
                                            (selected_row, selected_col)
                                        )

                                    selected_number = num


            # ==================================================
            # ERASER BUTTON
            # ==================================================

            if eraser_button.collidepoint(mouse_x, mouse_y):

                if (
                    selected_row is not None
                    and
                    selected_col is not None
                ):

                    cell = (selected_row, selected_col)

                    # Only erase user's WRONG entry
                    if cell in wrong_cells:

                        player_board[selected_row][selected_col] = 0

                        wrong_cells.remove(cell)

                        selected_number = 0


            # ==================================================
            # RESET BUTTON
            # ==================================================

            if reset_button.collidepoint(mouse_x, mouse_y):

                reset_game()


        # ==================================================
        # KEYBOARD INPUT
        # ==================================================

        if event.type == pygame.KEYDOWN:

            if (
                selected_row is not None
                and
                selected_col is not None
            ):

                # Numbers 1-9
                if event.unicode != "" and event.unicode in "123456789":

                    num = int(event.unicode)

                    if (
                        board[selected_row][selected_col] == 0
                        and
                        (selected_row, selected_col)
                        not in locked_cells
                    ):

                        if num == solution_board[selected_row][selected_col]:

                            # Correct number
                            player_board[selected_row][selected_col] = num

                            locked_cells.append(
                                (selected_row, selected_col)
                            )

                            if (
                                selected_row,
                                selected_col
                            ) in wrong_cells:

                                wrong_cells.remove(
                                    (selected_row, selected_col)
                                )

                            selected_number = num

                            # Check completion
                            if check_completed():
                                game_completed = True

                        else:

                            # Wrong number
                            errors += 1

                            player_board[selected_row][selected_col] = num

                            if (
                                selected_row,
                                selected_col
                            ) not in wrong_cells:

                                wrong_cells.append(
                                    (selected_row, selected_col)
                                )

                            selected_number = num

                # Backspace = erase wrong number
                if event.key == pygame.K_BACKSPACE:

                    cell = (selected_row, selected_col)

                    if cell in wrong_cells:

                        player_board[selected_row][selected_col] = 0

                        wrong_cells.remove(cell)

                        selected_number = 0


    # ======================================================
    # DRAW SCREEN
    # ======================================================

    screen.fill((255, 255, 255))


    # ======================================================
    # HIGHLIGHTING
    # ======================================================

    if selected_row is not None and selected_col is not None:

        # ---------------- Highlight 3x3 box ----------------

        box_row = (selected_row // 3) * 3
        box_col = (selected_col // 3) * 3

        for row in range(box_row, box_row + 3):

            for col in range(box_col, box_col + 3):

                pygame.draw.rect(
                    screen,
                    (252, 215, 225),
                    (
                        margin_x + col * CELL_SIZE,
                        margin_y + row * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )


        # ---------------- Highlight row ----------------

        for col in range(9):

            pygame.draw.rect(
                screen,
                (252, 215, 225),
                (
                    margin_x + col * CELL_SIZE,
                    margin_y + selected_row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )


        # ---------------- Highlight column ----------------

        for row in range(9):

            pygame.draw.rect(
                screen,
                (252, 215, 225),
                (
                    margin_x + selected_col * CELL_SIZE,
                    margin_y + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )


        # ---------------- Highlight same numbers ----------------

        if selected_number != 0:

            for row in range(9):

                for col in range(9):

                    if (
                        player_board[row][col] == selected_number
                        and
                        (row, col) != (selected_row, selected_col)
                    ):

                        pygame.draw.rect(
                            screen,
                            (235, 158, 170),
                            (
                                margin_x + col * CELL_SIZE,
                                margin_y + row * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE
                            )
                        )


        # ---------------- Highlight selected cell ----------------

        pygame.draw.rect(
            screen,
            (213, 124, 141),
            (
                margin_x + selected_col * CELL_SIZE,
                margin_y + selected_row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )


    # ======================================================
    # WRONG CELLS
    # ======================================================

    for row, col in wrong_cells:

        pygame.draw.rect(
            screen,
            (255, 180, 180),
            (
                margin_x + col * CELL_SIZE,
                margin_y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )


    # ======================================================
    # DRAW SUDOKU GRID
    # ======================================================

    for i in range(10):

        if i % 3 == 0:
            thickness = 4
        else:
            thickness = 1

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (
                margin_x,
                margin_y + i * CELL_SIZE
            ),
            (
                margin_x + GRID_SIZE,
                margin_y + i * CELL_SIZE
            ),
            thickness
        )

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (
                margin_x + i * CELL_SIZE,
                margin_y
            ),
            (
                margin_x + i * CELL_SIZE,
                margin_y + GRID_SIZE
            ),
            thickness
        )


    # ======================================================
    # DRAW NUMBERS
    # ======================================================

    for row in range(9):

        for col in range(9):

            if player_board[row][col] != 0:

                if board[row][col] != 0:

                    color = (0, 0, 0)

                elif (row, col) in wrong_cells:

                    color = (200, 0, 0)

                else:

                    color = (155, 34, 98)

                number = font.render(
                    str(player_board[row][col]),
                    True,
                    color
                )

                text_rect = number.get_rect(
                    center=(
                        margin_x
                        + col * CELL_SIZE
                        + CELL_SIZE // 2,

                        margin_y
                        + row * CELL_SIZE
                        + CELL_SIZE // 2
                    )
                )

                screen.blit(number, text_rect)


    # ======================================================
    # NUMBER BUTTONS
    # ======================================================

    for i in range(9):

        num_text = button_font.render(
            str(i + 1),
            True,
            (157, 34, 103)
        )

        text_rect = num_text.get_rect(
            center=number_buttons[i].center
        )

        screen.blit(num_text, text_rect)


    # ======================================================
    # ERASER BUTTON
    # ======================================================

    eraser_text = small_font.render(
        "Erase",
        True,
        (157, 34, 103)
    )

    eraser_rect = eraser_text.get_rect(
        center=eraser_button.center
    )

    screen.blit(eraser_text, eraser_rect)


    # ======================================================
    # RESET BUTTON
    # ======================================================

    reset_text = small_font.render(
        "Reset",
        True,
        (157, 34, 103)
    )

    reset_rect = reset_text.get_rect(
        center=reset_button.center
    )

    screen.blit(reset_text, reset_rect)


    # ======================================================
    # ERRORS
    # ======================================================

    error_text = font.render(
        f"Errors: {errors}",
        True,
        (0, 0, 0)
    )

    screen.blit(
        error_text,
        (50, 30)
    )


    # ======================================================
    # CONGRATULATIONS WINDOW
    # ======================================================

    if game_completed:

        # Dark transparent overlay
        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 100))

        screen.blit(
            overlay,
            (0, 0)
        )


        # Popup box
        pygame.draw.rect(
            screen,
            (255, 235, 242),
            (180, 220, 440, 360),
            border_radius=20
        )


        # Congratulations text
        congrats_text = congrats_font.render(
            "Congratulations!",
            True,
            (157, 34, 103)
        )

        congrats_rect = congrats_text.get_rect(
            center=(400, 300)
        )

        screen.blit(
            congrats_text,
            congrats_rect
        )


        # Message
        message_text = small_font.render(
            "You solved the Sudoku!",
            True,
            (80, 50, 60)
        )

        message_rect = message_text.get_rect(
            center=(400, 360)
        )

        screen.blit(
            message_text,
            message_rect
        )


        # New Game button
        pygame.draw.rect(
            screen,
            (213, 124, 141),
            new_game_button,
            border_radius=10
        )

        new_game_text = small_font.render(
            "New Game",
            True,
            (255, 255, 255)
        )

        new_game_rect = new_game_text.get_rect(
            center=new_game_button.center
        )

        screen.blit(
            new_game_text,
            new_game_rect
        )


    pygame.display.update()

    clock.tick(60)


pygame.quit()