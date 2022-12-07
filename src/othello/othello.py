from util.game import game

def pvp():
    match = game()
    match.print_board()
    while match.end == False:
        if match.turn == -1:
            print('Black\'s turn')
            print('Valid moves for black:', str(match.pos_name(match.valid_move_black())).upper())
        else:
            print('White\'s turn')
            print('Valid moves for white:', str(match.pos_name(match.valid_move_white())).upper())
        pos = input('Please enter the position you want to place a piece: ').lower().strip()
        if match.to_place(pos):
            match.print_board()
        else:
            print('Invalid position. Please try again.')
    print('Game over. The winner is', match.winner())

if __name__ == "__main__":
    pvp()