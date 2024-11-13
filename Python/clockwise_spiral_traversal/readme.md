Consider a grid of characters in the form of a 2D array, 
where each cell represents a distinct character selected from a-z. 

Implement a function called spiral_traverse_and_vowels

Start from the top-left cell of the grid and move in a clockwise spiral direction. 
Go right until you hit the right boundary.
Then go down until you reach the bottom boundary.
Then g left until you encounter the left boundary.
Finally go up until you hit the top boundary
(note that the top boundary is now the first row since we already visited the first cell in the matrix). 
Once this cycle is complete, move inwards, i.e., one cell to the right, and repeat the spiral process within the remaining unvisited cells.