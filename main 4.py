# Puissance 4

import copy
from random import randint

# Constantes
X = 1
O = 2

def create_board():
    board = []
    for i in range(6):
        row = [' ' for _ in range(7)]
        board.append(row)
    return board

def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 13)

def drop_piece(board, column, piece):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = piece
            return True
    return False

def demander():
    while True:
        mode = input("Voulez-vous jouer contre un ami (1) ou contre un bot (2) ? ")
        if mode in ['1', '2']:
            return mode
        print("Veuillez entrer 1 ou 2.")

def choisir_colone(board, joueur):
    while True:
        try:
            column = int(input("Joueur " + str(joueur) + " choisissez une colonne (0-6) : "))
            if 0 <= column <= 6:
                piece = 'X' if joueur == 1 else 'O'
                if drop_piece(board, column, piece):
                    return column
                else:
                    print("Cette colonne est pleine.")
            else:
                print("Veuillez entrer un nombre entre 0 et 6.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def verif_coup(board, piece):
    # lignes
    for row in board:
        for i in range(4):
            if row[i] == piece and row[i+1] == piece and row[i+2] == piece and row[i+3] == piece:
                return True

    # colonnes
    for col in range(7):
        for i in range(3):
            if board[i][col] == piece and board[i+1][col] == piece and board[i+2][col] == piece and board[i+3][col] == piece:
                return True

    # diagonales \
    for i in range(3):
        for j in range(4):
            if board[i][j] == piece and board[i+1][j+1] == piece and board[i+2][j+2] == piece and board[i+3][j+3] == piece:
                return True

    # diagonales /
    for i in range(3, 6):
        for j in range(4):
            if board[i][j] == piece and board[i-1][j+1] == piece and board[i-2][j+2] == piece and board[i-3][j+3] == piece:
                return True

    return False

def play_friend(board):
    joueur = 1

    while True:
        print_board(board)

        choisir_colone(board, joueur)

        piece = 'X' if joueur == 1 else 'O'
        if verif_coup(board, piece):
            print_board(board)
            print(f"Le joueur {joueur} a gagné !")
            break

        joueur = 2 if joueur == 1 else 1

def bot1(board):
    # choisir une colonne aléatoire valide
    while True:
        coup_bot = randint(0, 6)
        if drop_piece(board, coup_bot, 'O'):
            print("Le bot a choisi la colonne", coup_bot)
            return coup_bot

def play_vs_bot(board):
    joueur = 1

    while True:
        print_board(board)

        if joueur == 1:
            choisir_colone(board, joueur)
            piece = 'X'
        else:
            bot1(board)
            piece = 'O'

        if verif_coup(board, piece):
            print_board(board)
            if joueur == 1:
                print("Vous avez gagné !")
            else:
                print("Le bot a gagné !")
            break

        joueur = 2 if joueur == 1 else 1


# bot niveau intermédiaire
def colonnes_valides(board):
    """Retourne la liste des colonnes jouables."""
    valides = []
    for col in range(7):
        if board[0][col] == ' ':
            valides.append(col)
    return valides


def simuler_coup(board, column, piece):
    """Simule un coup sur une copie du plateau."""
    temp_board = copy.deepcopy(board)
    drop_piece(temp_board, column, piece)
    return temp_board


def bot_vision1(board):
    # 1. Colonnes jouables
    coups = colonnes_valides(board)

    # 2. Vérifier si le bot peut gagner
    for col in coups:
        temp = simuler_coup(board, col, 'O')
        if verif_coup(temp, 'O'):
            drop_piece(board, col, 'O')
            print("Bot joue pour gagner en colonne", col)
            return col

    # 3. Vérifier si le joueur peut gagner et bloquer
    for col in coups:
        temp = simuler_coup(board, col, 'X')
        if verif_coup(temp, 'X'):
            drop_piece(board, col, 'O')
            print("Bot bloque en colonne", col)
            return col

    # 4. Sinon jouer aléatoirement
    col = coups[randint(0, len(coups) - 1)]
    drop_piece(board, col, 'O')
    print("Bot joue au hasard en colonne", col)
    return col


def main():
    board = create_board()
    mode = demander()

    if mode == '1':
        play_friend(board)
    else:
        #choisir le niveau du bot
        return None

main()
