import pytest
import tkinter as tk
from Minesweeper import Minesweeper

@pytest.fixture
def game():
    root = tk.Tk()
    game = Minesweeper(root)
    return game

def test_choose_difficulty_easy(game):
    game.difficulty = 'easy'
    rows, columns, mines = game.choose_difficulty()
    assert rows == 8
    assert columns == 8
    assert mines == 10

def test_choose_difficulty_medium(game):
    game.difficulty = 'medium'
    rows, columns, mines = game.choose_difficulty()
    assert rows == 16
    assert columns == 16
    assert mines == 40

def test_choose_difficulty_hard(game):
    game.difficulty = 'hard'
    rows, columns, mines = game.choose_difficulty()
    assert rows == 24
    assert columns == 24
    assert mines == 99

def test_place_mines(game):
    game.rows, game.columns, game.mines = 8, 8, 10
    game.create_widgets()
    game.place_mines()
    assert len(game.mines_locations) == 10

def test_click_on_mine(game):
    game.rows, game.columns, game.mines = 8, 8, 10
    game.create_widgets()
    game.place_mines()
    mine_location = game.mines_locations[0]
    r, c = mine_location
    game.click(r, c)
    assert game.buttons[(r, c)]['text'] == '*'

def test_reveal_neighbors(game):
    game.rows, game.columns, game.mines = 8, 8, 10
    game.create_widgets()
    game.place_mines()
    r, c = 0, 0
    while (r, c) in game.mines_locations:
        r += 1
    game.click(r, c)
    assert game.buttons[(r, c)]['state'] == 'disabled'
