from turtle import *
import random

BORDER = 240
UNIT_MOVE = 3


class Game(Turtle):

    def __init__(self):
        super().__init__()
        self.screen_setup()
        self.border_draw()
        # self.screen.exitonclick()

    def screen_setup(self):
        self.screen = Screen()
        self.screen.setup(width=500, height=600)
        self.screen.bgcolor("black")
        self.screen.tracer(0)

    def border_draw(self):
        """ Draws a border for debugging """
        self.border_turtle = Turtle()
        self.border_turtle.hideturtle()
        self.border_turtle.penup()
        self.border_turtle.shape("square")
        self.border_turtle.pencolor("limegreen")
        self.border_turtle.goto(-BORDER, -BORDER)
        self.border_turtle.pendown()
        self.border_turtle.goto(-BORDER, BORDER)
        self.border_turtle.goto(BORDER, BORDER)
        self.border_turtle.goto(BORDER, -BORDER)

    def game_over(self):
        t = Turtle()
        t.hideturtle()
        t.penup()
        t.color("limegreen")
        t.write("GAME OVER", font=("Impact", 40, "bold"), align="center")

class Enemies(Turtle):

    def __init__(self):
        super().__init__()
        self.enemy_list = []
        self.bullet_list = []
        self.advance = [i for i in range(4, 37, 4)]
        self.killed_units = 0
        self.initiate_combatants()
        self.setup_bullets()
        self.x_move = UNIT_MOVE

    def all_dead(self):
        if len(self.enemy_list) == 0:
            return True

    def initiate_combatants(self):
        x_pos = []
        y_pos = []
        # offset = False TODO: Alternating rows offset x pos
        for x in range(-100, 101, 25):
            x_pos.append(x)
        for y in range(100, 176, 25):
            y_pos.append(y)
        for a in y_pos:
            for b in x_pos:
                foe = Turtle()
                foe.shape("turtle")
                foe.color("limegreen")
                foe.penup()
                foe.setheading(270)
                foe.goto(b, a)
                self.enemy_list.append(foe)

    def check_wall(self):
        for foe in self.enemy_list:
            if not -220 < foe.xcor() < 220:
                self.bounce()
                self.enemy_list = self.enemy_list[::-1]
                return

    def bounce(self):
        self.x_move *= -1

    def combatant_movement(self):
        self.check_wall()
        for foe in self.enemy_list:
            new_x = foe.xcor() + self.x_move
            foe.goto(new_x, foe.ycor())

    def check_hit(self, bullet):
        for foe in self.enemy_list:
            if foe.distance(bullet) < 9:
                foe.hideturtle()
                self.enemy_list.remove(foe)
                self.killed_units += 1
                self.speed_up()
                return True

    def speed_up(self):
        # Increases the movement speed of the turtles by 1
        # everytime one is removed, can this be simplified?
        if self.killed_units % 8 == 0:
            if self.x_move > 0:
                self.x_move += 1
            else:
                self.x_move += -1

    def setup_bullets(self):
        for i in range(5):
            bullet = Turtle()
            bullet.shape("square")
            bullet.shapesize(.5, .1)
            bullet.color("white")
            bullet.penup()
            bullet.hideturtle()
            bullet.goto(0, 260)
            self.bullet_list.append(bullet)
        self.bullet_x = 0

    def shoot(self):
        gun = random.choice(self.enemy_list)
        gun_x, gun_y = gun.pos()
        for bullet in self.bullet_list:
            if bullet.ycor() > 250:
                bullet.goto(gun_x, gun_y)
                bullet.showturtle()

    def bullet_move(self):
        for bullet in self.bullet_list:
            new_y = bullet.ycor() - 1
            current_x = bullet.xcor()
            bullet.goto(current_x, new_y)
            if bullet.ycor() > 250:
                bullet.hideturtle()

    def bullet_reset(self, bullet):
        bullet.hideturtle()
        bullet.goto(0, 260)

    def combatant_advance(self):
        if self.killed_units in self.advance:
            for combatant in self.enemy_list:
                x, y = combatant.pos()
                combatant.goto(x, y - 25)
            self.advance.remove(self.killed_units)


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.setup_player()
        self.setup_bullet()
        self.setup_health()

    def setup_player(self):
        self.doom_turtle = Turtle()
        self.doom_turtle.penup()
        self.doom_turtle.shape("turtle")
        self.doom_turtle.setheading(90)
        self.doom_turtle.color("red")
        self.doom_turtle.goto(0, -100)

    def setup_health(self):
        self.health = 3
        self.hp_turtle = Turtle()
        self.hp_turtle.hideturtle()
        self.hp_turtle.penup()
        self.hp_turtle.goto(-200, -200)
        self.hp_turtle.color("red")
        self.update_health()

    def update_health(self):
        self.hp_turtle.clear()
        self.hp_turtle.write(f"{self.health * '❤'}", move=False, font=("Arial", 16, "normal"))

    def move_left(self):
        new_x = self.doom_turtle.xcor() - 10
        self.doom_turtle.goto(new_x, -100)

    def move_right(self):
        new_x = self.doom_turtle.xcor() + 10
        self.doom_turtle.goto(new_x, -100)

    def setup_bullet(self):
        self.bullet = Turtle()
        self.bullet.shape("square")
        self.bullet.shapesize(.4, .1)
        self.bullet.color("white")
        self.bullet.penup()
        self.bullet.hideturtle()
        self.bullet.goto(0, 260)
        self.bullet_x = 0

    def bullet_move(self):
        new_y = self.bullet.ycor() + 8
        self.bullet.goto(self.bullet_x, new_y)
        if self.bullet.ycor() > 250:
            self.bullet.hideturtle()

    def bullet_reset(self):
        self.bullet.hideturtle()
        self.bullet.goto(0, 260)

    def shoot(self):
        if self.bullet.ycor() > 250:
            self.bullet.goto(self.doom_turtle.pos())
            self.bullet_x = self.doom_turtle.xcor()
            self.bullet.showturtle()

    def check_hit(self, bullet):
        if self.doom_turtle.distance(bullet) < 9:
            self.doom_turtle.goto(0, -100)
            self.health -= 1
            self.update_health()
            return True

