import sys
import time

from console_tools import clear
from listener import get_listener

chars = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
empty_row = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

test_grid = '''
  | A| B| C| D| E| F| G| H| I| J|
1 |  .  .  .  .  .  .  .  .  .  .
2 |  .  .  .  .  .  .  .  .  .  .
3 |  .  .  .00.  .  .  .  .██.  .
4 |  .  .██.██.XX.██.  .  .██.  .
5 |  .  .  .  .  .  .  .  .XX.  .
6 |  .  .  .00.00.  .  .  .  .  .
7 |  .  .  .00.  .  .  .  .  .  .
8 |  .  .  .  .  .  .██.██.  .  .
9 |  .  .  .  .  .  .  .  .  .  .
10|  .  .  .  .  .  .  .  .  .  .
'''

grid_view2 = '''\r
  | A| B| C| D| E| F| G| H| I| J|            | A| B| C| D| E| F| G| H| I| J|
1 |{A1}.{B1}.{C1}.{D1}.{E1}.{F1}.{G1}.{H1}.{I1}.{J1}|          1 |{_A1}.{_B1}.{_C1}.{_D1}.{_E1}.{_F1}.{_G1}.{_H1}.{_I1}.{_J1}|
2 |{A2}.{B2}.{C2}.{D2}.{E2}.{F2}.{G2}.{H2}.{I2}.{J2}|          2 |{_A2}.{_B2}.{_C2}.{_D2}.{_E2}.{_F2}.{_G2}.{_H2}.{_I2}.{_J2}|
3 |{A3}.{B3}.{C3}.{D3}.{E3}.{F3}.{G3}.{H3}.{I3}.{J3}|          3 |{_A3}.{_B3}.{_C3}.{_D3}.{_E3}.{_F3}.{_G3}.{_H3}.{_I3}.{_J3}|
4 |{A4}.{B4}.{C4}.{D4}.{E4}.{F4}.{G4}.{H4}.{I4}.{J4}|          4 |{_A4}.{_B4}.{_C4}.{_D4}.{_E4}.{_F4}.{_G4}.{_H4}.{_I4}.{_J4}|
5 |{A5}.{B5}.{C5}.{D5}.{E5}.{F5}.{G5}.{H5}.{I5}.{J5}|          5 |{_A5}.{_B5}.{_C5}.{_D5}.{_E5}.{_F5}.{_G5}.{_H5}.{_I5}.{_J5}|
6 |{A6}.{B6}.{C6}.{D6}.{E6}.{F6}.{G6}.{H6}.{I6}.{J6}|          6 |{_A6}.{_B6}.{_C6}.{_D6}.{_E6}.{_F6}.{_G6}.{_H6}.{_I6}.{_J6}|
7 |{A7}.{B7}.{C7}.{D7}.{E7}.{F7}.{G7}.{H7}.{I7}.{J7}|          7 |{_A7}.{_B7}.{_C7}.{_D7}.{_E7}.{_F7}.{_G7}.{_H7}.{_I7}.{_J7}|
8 |{A8}.{B8}.{C8}.{D8}.{E8}.{F8}.{G8}.{H8}.{I8}.{J8}|          8 |{_A8}.{_B8}.{_C8}.{_D8}.{_E8}.{_F8}.{_G8}.{_H8}.{_I8}.{_J8}|
9 |{A9}.{B9}.{C9}.{D9}.{E9}.{F9}.{G9}.{H9}.{I9}.{J9}|          9 |{_A9}.{_B9}.{_C9}.{_D9}.{_E9}.{_F9}.{_G9}.{_H9}.{_I9}.{_J9}|
10|{A10}.{B10}.{C10}.{D10}.{E10}.{F10}.{G10}.{H10}.{I10}.{J10}|          10|{_A10}.{_B10}.{_C10}.{_D10}.{_E10}.{_F10}.{_G10}.{_H10}.{_I10}.{_J10}|
'''


grid_view = '''\r
  | A| B| C| D| E| F| G| H| I| J|
1 |{A1}.{B1}.{C1}.{D1}.{E1}.{F1}.{G1}.{H1}.{I1}.{J1}| 
2 |{A2}.{B2}.{C2}.{D2}.{E2}.{F2}.{G2}.{H2}.{I2}.{J2}|
3 |{A3}.{B3}.{C3}.{D3}.{E3}.{F3}.{G3}.{H3}.{I3}.{J3}|
4 |{A4}.{B4}.{C4}.{D4}.{E4}.{F4}.{G4}.{H4}.{I4}.{J4}|
5 |{A5}.{B5}.{C5}.{D5}.{E5}.{F5}.{G5}.{H5}.{I5}.{J5}|
6 |{A6}.{B6}.{C6}.{D6}.{E6}.{F6}.{G6}.{H6}.{I6}.{J6}|
7 |{A7}.{B7}.{C7}.{D7}.{E7}.{F7}.{G7}.{H7}.{I7}.{J7}|
8 |{A8}.{B8}.{C8}.{D8}.{E8}.{F8}.{G8}.{H8}.{I8}.{J8}|
9 |{A9}.{B9}.{C9}.{D9}.{E9}.{F9}.{G9}.{H9}.{I9}.{J9}|
10|{A10}.{B10}.{C10}.{D10}.{E10}.{F10}.{G10}.{H10}.{I10}.{J10}|
'''

ship_str = '██'
empty_str = '  '
hit_str = 'XX'
by_str = '00'


class Cell:
    def __init__(self):
        self.full = False
        self.block = False
        self.hit = False

    def shot(self):
        self.hit = True
        if self.full:
            return True
        else:
            return False
    
    def view(self, is_my_field):
        if self.full:
            if self.hit:
                return hit_str
            else:
                if is_my_field:
                    return ship_str
                else:
                    return empty_str
        else:
            if self.hit:
                return by_str
            else:
                return empty_str

    @classmethod
    def empty_col(cls):
        return [cls() for i in range(10)]

    @staticmethod
    def right(cell, jump=True):
        char = cell[0]
        char_index = chars.index(char) + 1
        if char_index == len(chars):
            if jump:
                return 'A' + (cell[1] if len(cell) == 2 else cell[1:3])
            else:
                return cell
        else:
            return chars[char_index] + (cell[1] if len(cell) == 2 else cell[1:3])

    @staticmethod
    def left(cell, jump=True):
        char = cell[0]
        char_index = chars.index(char) - 1
        if char == 'A' and not jump:
            return cell
        return chars[char_index] + (cell[1] if len(cell) == 2 else cell[1:3])

    @staticmethod
    def up(cell, jump=True):
        if len(cell) == 3:
            num = '10'
        else:
            num = cell[1]
            if num == '1' and not jump:
                return cell
        return cell[0] + (str(int(num) - 1) if num != '1' else '10')

    @staticmethod
    def down(cell, jump=True):
        if len(cell) == 3:
            num = '10'
            if not jump:
                return cell
        else:
            num = cell[1]
        return cell[0] + (str(int(num) + 1) if num != '10' else '1')

    @classmethod
    def get_cells_around(cls, cell):
        cells = [cell, cls.up(cell, jump=False), cls.down(cell, jump=False)]
        for cell in cells[:3]:
            cells.append(cls.right(cell, jump=False))
            cells.append(cls.left(cell, jump=False))
        return list(set(cells))


class Move:
    def __init__(self, table):
        self.table = table
        self.selected = 'A1'
        self.place_orientation = True
        self.place_on = ['A1']

    def update_place(self, ship=None, new_selected=None):
        if ship is None:
            ship = self.table.ship_to_place

        old_place_on = self.place_on
        self.place_on = [new_selected if new_selected is not None else self.selected]
        if ship == 1:
            return True
        else:
            if self.place_orientation:
                for i in range(ship-1):
                    next_value = Cell.down(self.place_on[-1])
                    if '1' in next_value:
                        self.place_on = old_place_on
                        if not new_selected:
                            self.place_orientation = not self.place_orientation
                        return False
                    self.place_on.append(next_value)

            else:
                for i in range(ship-1):
                    next_value = Cell.right(self.place_on[-1])
                    if 'A' in next_value:
                        self.place_on = old_place_on
                        if not new_selected:
                            self.place_orientation = not self.place_orientation
                        return False
                    self.place_on.append(next_value)

            return True

    def on_press(self, key):
        key_str = str(key)
        if not (self.table.wait_for_shot or self.table.ship_to_place):
            return

        elif key_str == 'Key.right':
            self.right()

        elif key_str == 'Key.left':
            self.left()

        elif key_str == 'Key.up':
            self.up()

        elif key_str == 'Key.down':
            self.down()

        elif key_str == 'Key.enter':
            self.select()

        elif key_str in ("'r'", "'R'"):
            self.rotate()

    def right(self):
        new_selected = Cell.right(self.selected)
        if self.table.ship_to_place and self.update_place(new_selected=new_selected):
            self.selected = new_selected

    def left(self):
        new_selected = Cell.left(self.selected)
        if self.table.ship_to_place and self.update_place(new_selected=new_selected):
            self.selected = new_selected

    def up(self):
        new_selected = Cell.up(self.selected)
        if self.table.ship_to_place and self.update_place(new_selected=new_selected):
            self.selected = new_selected

    def down(self):
        new_selected = Cell.down(self.selected)
        if self.table.ship_to_place and self.update_place(new_selected=new_selected):
            self.selected = new_selected

    def rotate(self):
        self.place_orientation = not self.place_orientation
        if self.table.ship_to_place:
            self.update_place()

    def select(self):
        if self.table.ship_to_place and self.table.check_cells_to_place():
            self.table.place()


class Field:
    def __init__(self):
        self.grid = {}
        self.wait_for_shot = False
        self.ship_to_place = None

        for char in chars:
            self.grid[char] = {x: y for x, y in zip(range(1, 11), Cell.empty_col())}

        self.move = Move(self)
        self.listener = get_listener(self)
        self.listener.start()
        self.get_ship = self.place_ships()

    def get_cell_by_str(self, cell_str):
        if len(cell_str) == 3:
            cell = self.grid[cell_str[0]][10]
        else:
            cell = self.grid[cell_str[0]][int(cell_str[1])]
        return cell

    def check_cells_to_place(self):
        for cell_str in self.move.place_on:
            cell = self.get_cell_by_str(cell_str)
            if cell.block:
                return False
        return True

    def place(self):
        for cell_str in self.move.place_on:
            self.get_cell_by_str(cell_str).full = True
            for cell in Cell.get_cells_around(cell_str):
                self.get_cell_by_str(cell).block = True

        try:
            next(self.get_ship)
        except StopIteration:
            pass

    def place_ships(self):
        available_ships = {1: 4, 2: 3, 3: 2, 4: 1}
        for ship, count in available_ships.items():
            self.ship_to_place = ship
            self.move.place_orientation = True
            self.move.selected = 'J1'
            self.move.right()
            for i in range(count):
                yield

        self.ship_to_place = None

    def select(self):
        char = self.move.selected[0]
        if len(self.move.selected) == 3:
            num = 10
        else:
            num = int(self.move.selected[1])
        self.grid[char][num].shot()

    def test_move(self):
        next(self.get_ship)
        while True:
            selected_cells = {x: y for x, y in zip(self.move.place_on, (ship_str for i in range(len(self.move.place_on))))}
            sys.stdout.write(self.view(is_my_field=True, update_cells=selected_cells))
            sys.stdout.flush()
            time.sleep(0.05)

    @classmethod
    def test_game(cls):
        players = [cls(), cls()]
        for player in players:
            next(player.get_ship)
            while player.ship_to_place is not None:
                selected_cells = {
                    x: y for x, y in zip(player.move.place_on, (ship_str for i in range(len(player.move.place_on))))
                }
                clear()
                sys.stdout.write(players[0].view_2(players[1], update_cells=selected_cells if player == players[0] else {}))
                sys.stdout.write(players[1].view_2(players[0], update_cells=selected_cells if player == players[1] else {}))
                time.sleep(0.05)

    def view(self, is_my_field, update_cells={}):
        grid_dict = {}
        for char, col in self.grid.items():
            for num, cell in col.items():
                grid_dict[char+str(num)] = cell.view(is_my_field)
                grid_dict.update(update_cells)
                
        field_view = grid_view.format(**grid_dict)
        return field_view

    def view_2(self, field_2, update_cells={}):
        grid_dict = {}
        for char, col in self.grid.items():
            for num, cell in col.items():
                grid_dict[char + str(num)] = cell.view(True)
                grid_dict.update(update_cells)

        for char, col in field_2.grid.items():
            for num, cell in col.items():
                grid_dict['_' + char + str(num)] = cell.view(False)
                grid_dict.update(update_cells)

        field_view = grid_view2.format(**grid_dict)
        return field_view


class Game:
    def __init__(self):
        self.player1 = Field()
        self.player2 = Field()


# f = Field()
# f.test_move()
# print(f.view(True))
Field.test_game()


