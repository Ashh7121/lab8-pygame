For this project using pygame I first set up the window and main loop. I understood that everything runs inside this loop, where the program keeps updating and drawing things on the screen over and over again

For creating the squares, I made a list and filled it with squares that all have random sizes, colours, and positions. This makes everything look more random and interesting without much effort

For bouncing, I just checked if a square hits the edge of the screen and reversed its direction. It’s a simple way to keep everything inside the window and make it look realistic

For movement, I used simple x and y speed values(dx and dy). I made smaller squares move faster and bigger ones slower using a function that I stumbled upon by playing aroun

For the jittering, I asked co pilot to explain the logic behind the vector rotation to show jittering. I understand it now. It rotates the vector using a small angle and it happens so many times (the squares change direction so many times due to the frame rate) that it looks like they are jittering.