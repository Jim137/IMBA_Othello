# IMBA_Othello

Ising-Model-Based Algorithm for Othello Strategy with Machine Leaning.

## Background

This was the final project for computational physics lab.

We want to construct a Hamiltonian for Othello game based on Ising Model. By minimizing the energy, we can find out the most stable state of the board to win the game.

## Introduction

By now, please refer to [Final Report](https://www.jim137.eu.org/files/IMBA_Othello.pdf) for the introduction of this project.

## Features

- [X] Basic Othello Game
- [X] Player
  - [X] Offline PVP
  - [X] Offline Greedy Bot
    - Maximize the flipping number of pieces
    - Minimize the mobility of opponent
- [X] Hamiltonian of Othello
  - [X] Constructing Hamiltonian of Othello
  - [ ] Machine Learning to Obtain the Exact Value
- [X] Minimax Algorithm
  - [ ] Alpha-Beta Pruning
  - [ ] CPU Acceleration
- [X] GUI
  - [X] Command Line
  - [ ] Better GUI
- [ ] Botzone Test
  - [ ] API
  - [ ] Testing
