For this project using pygame I first set up the window and main loop. I understood that everything runs inside this loop, where the program keeps updating and drawing things on the screen over and over again

For creating the squares, I made a list and filled it with squares that all have random sizes, colours, and positions. This makes everything look more random and interesting without much effort

For bouncing, I just checked if a square hits the edge of the screen and reversed its direction. It’s a simple way to keep everything inside the window and make it look realistic

For movement, I used simple x and y speed values(dx and dy). I made smaller squares move faster and bigger ones slower using a function that I stumbled upon by playing aroun

For the jittering, I asked co pilot to explain the logic behind the vector rotation to show jittering. I understand it now. It rotates the vector using a small angle and it happens so many times (the squares change direction so many times due to the frame rate) that it looks like they are jittering.


For the fleeing, I thought that I'd handle it like I'd handle collision. Only in this case, the collision is not actually happening but the smaller squares are moving away from the bigger squares before they collide. This is why I added a buffer value that is added on top of the squares' sizes to make it look like the small one is fleeing from the big one. I asked copilot to guide me through the logic and it did help me get to a point where I was albe to code and understand it myself. I got confused about how pygame treats squares, like what does their coordinate refer to and got a bit lost on how to calculate the center coordinates especially since I was thinking in the Cartesian plane even though it was easy and a bit of a lapse of intelligence on my part but hey I got through it. I also introduced the distance formula between the 2 centers to anticipate when the squares are getting too close. I also found that the number of pairs you'd need to check is nC2 where n is the total number of squares. E.g, if there are 4 squares, the number of pairs to check would be 4C2 which is 6. This is what led to the idea of the nested loops. Finally, I copied the main.py to another new file and then worked on that file with the TODOs so that I'll have the skeleton main.py if I wanna play around later.


Now we gotta have a lifespan. All squares have a random lifespan between 30 and 180 seconds for example and they die at the end of their lifespan butttt each time a square dies, another one is reborn. On top of that, I want to make it like thet shrink till they die as an idea to implement on top of it, so I can visibly see them dying instead of them disappearing in an ugly way. 