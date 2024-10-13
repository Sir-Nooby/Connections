NYT's Connections remade in Python using PyGame

Guess common words in categories in fours.

[Singleplayer]

Click on each word you want to select and hit submit.
A mistake will remove one of your lives located on the bottom of the screen.
A correct guess will change the color of the selected entries, and make them unselectable.
The game is won when all four categories are guessed correctly.
During a win or a loss, the game will reset back to the title screen.

[Custom]

To create a custom game, follow instructions on the screen.

To correctly input categories, input each category as such:

item1, item2, item3, item4, category_name

Once inputted, hit enter.
The first custom category and its words should have disappeared, allowing you to type the next category.
Continue this process until the "Generate Puzzle" button changes color, allowing you to generate your puzzle.

Any error messages that occur will inform you of the problem, in which you will need to adjust your input accordingly.
A basic rundown of the errors are:

ERROR 1: The user placed less than five entries before submitting the current category.

ERROR 2: The user tried to generate more than 4 categories.

ERROR 3: The user generated the puzzle before inputting all four categories.
