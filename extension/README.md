This is my attempt at the extension of maze runner using flood fill algorithm instead of left hug algorithm.
In it I use a 2D list values to store the value of each cell, which represents number of steps to the goal.
Using the queue data structure, I add the goal and its value of 0, then iteratively check its neighbors without walls, add them to the queue as well and give them increasing values by 1 as long as they don't already have values to reflect more steps from the goal.
Move function now check cells with lowest value to move there.
No wall is needed anymore and runner can start or reach goals that are not on the edges of the maze.