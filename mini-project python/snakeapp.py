import tkinter as tk
from random import randint
from PIL import Image, ImageTk
from tkinter import Button
from functools import partial
MOVE_INCREMENT = 20#related to snake positions
moves_per_second = 10
GAME_SPEED = 1000 // moves_per_second
#print("first")
high_score=0
class Snake(tk.Canvas):
    
    def __init__(self):
        super().__init__(
            width=600, height=620, background="black", highlightthickness=0
        )
        self.play()
    def play(self):
        global moves_per_second 
        global GAME_SPEED
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.direction = "Right"

        self.score = 0

        self.load_assets()
        self.create_objects()

        self.bind_all("<Key>", self.on_key_press)

        self.pack()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            root.destroy()
            raise

    def create_objects(self):
        global moves_per_second 
        global GAME_SPEED
        global high_score
        self.create_text(
            45, 12, text=("Score: "+str(self.score)), tag="score", fill="#fff", font=10
        )
        self.create_text(
            200, 12, text=("Speed: "+str(moves_per_second)), tag="speed", fill="#fff", font=10
        )
        self.create_text(
            400, 12, text=("High Score: "+str(high_score)), tag="high_score", fill="#fff", font=10
        )
        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#FFFFFF")

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def check_food_collision(self):
        global moves_per_second 
        global GAME_SPEED
        global high_score
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            if self.score%5==0:
                #global GAME_SPEED
                moves_per_second+=1
                GAME_SPEED = 1000 // moves_per_second
            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)
            #global moves_per_second
            score = self.find_withtag("score")
            self.itemconfigure(score, text=("Score: "+str(self.score)), tag="score")
            speed = self.find_withtag("speed")
            self.itemconfigure(speed, text=("Speed: "+str(moves_per_second)), tag="speed")
            if high_score<self.score:
                hs = self.find_withtag("high_score")
                self.itemconfigure(hs, text=("High Score: "+str(self.score)), tag="high_score")
 
    def end_game(self):
        global high_score
        self.delete(tk.ALL)
        if high_score>=self.score:
            
            self.create_text(
                self.winfo_width() / 2, 
                self.winfo_height() / 2,
                text="Game over! You scored "+str(self.score)+"!\n        High Score is "+str(high_score),
                fill="#fff",
                font=10
            )
            button1 = Button(self, text = "Quit", font=30, bg ="#FF0000",command = self.quit,height = 3, width = 10)
            button1.configure( activebackground = "#520000")
            button1_window = self.create_window(285, 400, window=button1)
            button2 = Button(self, text = "Retry", font=30, bg ='light green', command = self.retry,height = 3, width = 10)
            button2.configure( activebackground = "#41A62A")
            button2_window = self.create_window(285, 225, window=button2)  
        elif high_score<self.score:
            high_score=self.score
            self.create_text(
                self.winfo_width() / 2,
                self.winfo_height() / 2,
                text="Congratulations!!New High score.\nGame over! You scored "+str(self.score),
                fill="#fff",
                font=10)
            button1 = Button(self, text = "Quit", font=30, bg ="#FF0000",command = self.quit,height = 3, width = 10)
            button1.configure( activebackground = "#520000")
            button1_window = self.create_window(285, 400, window=button1)
            button2 = Button(self, text = "Retry", font=30, bg ='light green', command = self.retry,height = 3, width = 10)
            button2.configure( activebackground = "#41A62A")
            button2_window = self.create_window(285, 225, window=button2)
                

    def retry(self):
        self.delete(tk.ALL)
        #self.play()
        global moves_per_second 
        global GAME_SPEED
        moves_per_second = 10
        GAME_SPEED = 1000 // moves_per_second
        start_game(root)
    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def on_key_press(self, e):
        new_direction = e.keysym

        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()
        self.move_snake()

        self.after(GAME_SPEED, self.perform_actions)

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

def start_game(root):
    for ele in root.winfo_children():
        ele.destroy()
    
    board = Snake()
    board.pack()

root = tk.Tk()
root.title("Snake Game with tkinter")
#root.configure(background='green')
root.configure(background='black')

body_image = Image.open("./wp.jpg")
e_body = ImageTk.PhotoImage(body_image)
lbl=tk.Label(root,image=e_body)
lbl.place(x=85,y=25,relwidth=0.73,relheight=0.39)
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)
root.geometry("600x620")

button1 = Button(root, text = "Start Game", bg = "red", font=19,
                    fg = "black", command = partial(start_game,root)) 
button1.config( height = 2, width = 20 )
button1.place(x=230,y=330)
#root.configure(background='turquoise')
#print("ssssss")
#board = Snake()
#board.pack()
root.mainloop()