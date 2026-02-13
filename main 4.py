# Puissance 4

import copy
from random import randint

# ------------------------------
# Affichage et plateau
# ------------------------------

def create_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

def print_board(board):
    # numéros de colonnes
    print(" 1   2   3   4   5   6   7")
    print("+---+---+---+---+---+---+---+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+---+---+---+---+---+---+")


def drop_piece(board, column, piece):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = piece
            return True
    return False

def colonnes_valides(board):
    return [col for col in range(7) if board[0][col] == ' ']

def plateau_plein(board):
    return len(colonnes_valides(board)) == 0

# ------------------------------
# Vérification victoire
# ------------------------------

def verif_coup(board, piece):

    # lignes
    for row in board:
        for i in range(4):
            if row[i:i+4] == [piece]*4:
                return True

    # colonnes
    for col in range(7):
        for row in range(3):
            if all(board[row+i][col] == piece for i in range(4)):
                return True

    # diagonales \
    for row in range(3):
        for col in range(4):
            if all(board[row+i][col+i] == piece for i in range(4)):
                return True

    # diagonales /
    for row in range(3, 6):
        for col in range(4):
            if all(board[row-i][col+i] == piece for i in range(4)):
                return True

    return False

# ------------------------------
# Joueurs humains
# ------------------------------

def choisir_colone(board, joueur):
    while True:
        try:
            col = int(input(f"Joueur {joueur} (colonne 1-7) : "))
            col -= 1  # conversion vers index interne 0–6

            if col in colonnes_valides(board):
                return col

            print("Colonne invalide.")
        except:
            print("Entrée invalide.")


def play_friend(board):
    joueur = 1

    while True:
        print_board(board)

        col = choisir_colone(board, joueur)
        piece = 'X' if joueur == 1 else 'O'
        drop_piece(board, col, piece)

        if verif_coup(board, piece):
            print_board(board)
            print(f"Joueur {joueur} a gagné !")
            break

        if plateau_plein(board):
            print("Match nul !")
            break

        joueur = 2 if joueur == 1 else 1

# ------------------------------
# BOT NIVEAU 1 (aléatoire)
# ------------------------------

def bot1(board):
    coups = colonnes_valides(board)
    col = coups[randint(0, len(coups)-1)]
    drop_piece(board, col, 'O')
    print("Le bot joue colonne", col + 1)

# ------------------------------
# BOT NIVEAU 2 (vision 1)
# ------------------------------

def simuler_coup(board, column, piece):
    temp = copy.deepcopy(board)
    drop_piece(temp, column, piece)
    return temp

def bot_vision1(board):

    coups = colonnes_valides(board)

    # gagner
    for col in coups:
        if verif_coup(simuler_coup(board, col, 'O'), 'O'):
            drop_piece(board, col, 'O')
            print("Le bot joue colonne ", col+1)
            return

    # bloquer
    for col in coups:
        if verif_coup(simuler_coup(board, col, 'X'), 'X'):
            drop_piece(board, col, 'O')
            print("Le bot joue colonne ", col+1)
            return

    bot1(board)

# ------------------------------
# BOT NIVEAU 3 (vision 2)
# ------------------------------

def bot_vision2(board):

    coups = colonnes_valides(board)

    # gagner
    for col in coups:
        if verif_coup(simuler_coup(board, col, 'O'), 'O'):
            drop_piece(board, col, 'O')
            print("Le bot joue colonne ", col+1)
            return

    # éviter coups dangereux
    coups_surs = []
    for col in coups:
        temp = simuler_coup(board, col, 'O')
        danger = False
        for col_j in colonnes_valides(temp):
            if verif_coup(simuler_coup(temp, col_j, 'X'), 'X'):
                danger = True
                break
        if not danger:
            coups_surs.append(col)

    if coups_surs:
        col = coups_surs[randint(0, len(coups_surs)-1)]
        drop_piece(board, col, 'O')
        print("Le bot joue colonne ", col+1)
        return

    # bloquer
    for col in coups:
        if verif_coup(simuler_coup(board, col, 'X'), 'X'):
            drop_piece(board, col, 'O')
            print("Le bot joue colonne ", col+1)
            return

    bot1(board)

# ------------------------------
# Partie contre bot
# ------------------------------

def play_vs_bot(board, niveau):

    while True:
        print_board(board)

        col = choisir_colone(board, 1)
        drop_piece(board, col, 'X')

        if verif_coup(board, 'X'):
            print_board(board)
            print("Vous avez gagné !")
            break

        if plateau_plein(board):
            print("Match nul !")
            break

        if niveau == 1:
            bot1(board)
        elif niveau == 2:
            bot_vision1(board)
        else:
            bot_vision2(board)

        if verif_coup(board, 'O'):
            print_board(board)
            print("Le bot a gagné !")
            break

        if plateau_plein(board):
            print("Match nul !")
            break

# ------------------------------
# MAIN
# ------------------------------

def main():
    board = create_board()
    mode = input("1 = Joueur vs Joueur | 2 = Joueur vs Bot : ")

    if mode == '1':
        play_friend(board)
    else:
        niveau = int(input("Niveau bot (1, 2, 3) : "))
        play_vs_bot(board, niveau)

main()
