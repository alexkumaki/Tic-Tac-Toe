# Tic-Tac-Toe AI

This is a very basic implementation of a Tic-Tac-Toe game, with three modes:

- The first mode is just Player vs Player
  - Both X and O are controlled by the user
- The second mode is Player vs AI
  - The X is controlled by the user
  - The O is controlled by the AI
- The third mode is AI vs AI
  - Both X and O are controlled by AI
  - The AI are actually differently programmed (more details below)
  - This is mostly for training the O AI, as it goes pretty fast and has no human control

The different AI:

- The X AI is very simple, and operates similar to a human who doesn't have any prior biases in the game of Tic-Tac-Toe
  - If there is a guaranteed win, it takes it
  - If there is an opportunity for O to win, it blocks it
  - Otherwise it picks a random open spot

- The O AI is much more complicated, as is perhaps evident by the other included txt file
  - During the game, it takes a snapshot of the board after it moves and adds it to a list
  - At the end of the game, it takes all the snapshots and associates a value with them based on the game outcome
    - This is defaulted to -10 for a loss, 10 for a win, and 0 for a draw
  - This dictionary of board states is then added to the dictionary and updated
  - When the AI is required to make a move, it looks through the possible moves in the board dictionary and chooses which has the highest associated value
  - The idea is that as more games are played, the AI will learn which board states to avoid, or which board states make it more likely for it to win
