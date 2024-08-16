from tkinter import *
import random
from tkinter import messagebox
import pygame

# Set up a bouncing sound effect
pygame.mixer.init(44100, -16, 1, 0)
pygame.mixer.music.load("sounds/bounce.mp3")

# Function to initialize the game state
def init_game_state(canvas_width, canvas_height):
	# a python dictionary that stores key elements, ball, paddles, score, canvas dimensions
	return {
		"ball":{
			"x": canvas_width // 2, # start the ball in the center of the screen
			"y": canvas_height //2,
			"dx": 5, # horizontal speed of the ball 
			"dy": 5, # vertical speed of the ball
			"radius": 10, # Radius of the ball
		},
		"paddle1":{
			"x": 30, # position of the paddle near the left edge
			"y": canvas_height // 2, # put the paddle in the middle vertically
			"width": 10, # paddle width
			"height": 60, # paddle height
			"dy": 0, # vertical speed at the beginning of the game
		},
		"paddle2":{
			"x": canvas_width - 40, # position of the paddle near the right edge
			"y": canvas_height // 2, # put the paddle in the middle vertically
			"width": 10, # paddle width
			"height": 60, # paddle height
			"dy": 0, # vertical speed at the beginning of the game
		},
		"score":{
			"player1": 0,
			"player2": 0,
		},
		"players": 2, # Set the number of players
		"canvas_width": canvas_width,
		"canvas_height": canvas_height,

	}


# Function to update the ball's position and handle collisions 
def update_ball(state):
	# Define the ball and paddle states vs height and width of canvas
	ball = state["ball"]
	paddle1 = state["paddle1"]
	paddle2 = state["paddle2"]
	canvas_width = state["canvas_width"]
	canvas_height = state["canvas_height"]

	# Move the ball by adding the current speed (dx,dy) to position of the ball (x,y)
	ball["x"] += ball["dx"]
	ball["y"] += ball["dy"]
	

	# Check for collisions with the top or bottom walls
	if ball["y"] - ball["radius"] <= 0 or ball["y"] + ball["radius"] >= canvas_height:
		ball["dy"] = -ball["dy"] # Reverse the vertical direction if the ball hits the top or bottom

	# Check for collisions with the paddles
	if (ball["x"] - ball["radius"] <= paddle1["x"] + paddle1["width"] and paddle1["y"] <= ball["y"] <= paddle1["y"] + paddle1["height"]) or (ball["x"] + ball["radius"] >= paddle2["x"] and paddle2["y"] <= ball["y"] <= paddle2["y"] + paddle2["height"]):
		# Play bounce sound effect
		pygame.mixer.music.play() # Play the sound
		ball["dx"] = -ball["dx"] # Reverse the horizontal direction if the ball hits a paddle

	# Check for scoring (ball going out of bounds on either side)
	if ball["x"] - ball["radius"] <= 0:
		state["score"]["player2"] += 1 # Increment player 2's score
		# reset the ball
		reset_ball(state)
	elif ball["x"] + ball["radius"] >= canvas_width:
		state["score"]["player1"] += 1 # Increment player 1's score
		# reset the ball
		reset_ball(state)



# Funciton to reset the ball's position and speed after a point is scored
def reset_ball(state):
	ball = state["ball"]
	ball["x"] = state["canvas_width"] // 2 # reset the ball center horizontally
	ball["y"] = state["canvas_height"] // 2 # reset the ball center vertically
	ball["dx"] = random.choice([-5, 5]) # Randomize the horizontal direction of the ball / speed
	ball["dy"] = random.choice([-5, 5]) # Randomize the vertical direction of the ball / speed


# Function to update the paddle's position
def update_paddles(state):
	# Define paddles
	paddle1 = state["paddle1"]
	paddle2 = state["paddle2"]
	ball = state["ball"]
	canvas_height = state["canvas_height"]

	# Check if 1 player or 2
	# Only 1 player:
	if state["players"] == 1:
		# Set paddle speed
		state["paddle1"]["dy"] = 4
		# have the computer move the paddle
		if paddle1["y"] + paddle1["height"] // 2 < ball["y"]:
			paddle1["y"] += paddle1["dy"]
		elif paddle1["y"] + paddle1["dy"] // 2 > ball["y"]:
			paddle1["y"] -= paddle1["dy"]
	# Check for 2 players
	if state["players"] == 2:
		# Move paddle1 according to its vertical speed dy
		paddle1["y"] += paddle1["dy"]
	
	# Don't want the paddle to move off the screen 
	# Top
	if paddle1["y"] < 0:
		paddle1["y"] = 0
	# Bottom
	elif paddle1["y"] + paddle1["height"] > canvas_height:
		paddle1["y"] = canvas_height - paddle1["height"]

	

	# Move paddle2 according to its vertical speed dy
	paddle2["y"] += paddle2["dy"]
	# Don't want the paddle to move off the screen 
	# Top
	if paddle2["y"] < 0:
		paddle2["y"] = 0
	# Bottom
	elif paddle2["y"] + paddle2["height"] > canvas_height:
		paddle2["y"] = canvas_height - paddle2["height"]


# Function to draw the game 
def draw_game(canvas, state):
	canvas.delete("all") # clear the canvas before drawing the new frame

	# draw the ball
	ball = state["ball"]
	canvas.create_oval(ball["x"] - ball["radius"], ball["y"] - ball["radius"],
		ball["x"] + ball["radius"], ball["y"] + ball["radius"], fill="white")

	# draw the paddles
	paddle1 = state["paddle1"]
	paddle2 = state["paddle2"]

	# Paddle1
	canvas.create_rectangle(paddle1["x"], paddle1["y"],
		paddle1["x"] + paddle1["width"], paddle1["y"] + paddle1["height"], fill="white")

	# Paddle2
	canvas.create_rectangle(paddle2["x"], paddle2["y"],
		paddle2["x"] + paddle2["width"], paddle2["y"] + paddle2["height"], fill="white")

	# Draw a net dashed line in the center
	canvas.create_line(state["canvas_width"] // 2, 0, state["canvas_width"] // 2, state["canvas_height"], fill="white", dash=(5,2))

	# Draw the scores
	# Player1
	canvas.create_text(state["canvas_width"] // 4, 20, text=str(state["score"]["player1"]), fill="white", font=("Arial", 24))
	# Player 2
	canvas.create_text(3 * state["canvas_width"] // 4, 20, text=str(state["score"]["player2"]), fill="white", font=("Arial", 24))
	


# Function to handle key presses 
def key_press(event, state):
	# Paddle 1 movement
	if event.keysym == "w":
		state["paddle1"]["dy"] = -4 # Move paddle1 up speed 4
	elif event.keysym == "s":
		state["paddle1"]["dy"] = 4 # Move paddle1 down speed 4
	# Paddle 2 movement
	elif event.keysym == "Up":
		state["paddle2"]["dy"] = -4 # Move paddle2 up speed 4
	elif event.keysym == "Down":
		state["paddle2"]["dy"] = 4 # Move paddle2 down speed 4

# Function to handle key releases
def key_release(event, state):
	if event.keysym in ("w", "s"):
		state["paddle1"]["dy"] = 0 # stop paddle 1 from moving
	elif event.keysym in ("Up", "Down"):
		state["paddle2"]["dy"] = 0 # stop paddle 2 from moving



# Function to handle the main game loop
def game_loop(canvas, state):
	update_ball(state) # Update the ball's position and check for collisions
	update_paddles(state) # Update the paddle's position
	draw_game(canvas, state) # Redraw the game on the canvas
	canvas.after(16, game_loop, canvas, state) # scheduling the next frame (roughly 60fps)

# Get the number of players 1/2
def get_players(state):
	get_number_of_players = messagebox.askquestion("How Many Players?", "Do You Want 2 Players?")
	# Determine what they picked
	if get_number_of_players == "yes":
		state["players"] = 2
	else:
		state["players"] = 1



# Function to handle the main window
def main():
	# Create the app
	root = Tk()
	root.title("Pong Game - Tkinter.com")

	# Set some variables
	canvas_width = 600
	canvas_height = 400
	# Create the canvas
	canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="black")
	canvas.pack()


	# Initialize the game state
	state = init_game_state(canvas_width, canvas_height)

	# Popup box to select number of players
	get_players(state)
	# Windows 7 Message Box Glitch Fix
	root.focus_force()

	# Add a 1 second delay before the game starts
	root.after(2000)

	# Bind the key press and key release events to control the paddles
	root.bind("<KeyPress>", lambda event: key_press(event, state))
	root.bind("<KeyRelease>", lambda event: key_release(event, state))

	# Start the game loop
	game_loop(canvas, state)

	# Create a main loop
	root.mainloop()




# Start the app
main()

