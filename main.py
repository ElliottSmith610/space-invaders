from time import sleep
from brain import Game, Player, Enemies

# TODO: Make an enemy turtle fire a shot down and interact with the player turtle
# TODO: 3 Lives
# TODO: After x deaths, enemy turtles come down by 1 line

game = Game()
player = Player()
enemies = Enemies()

game.screen.onkey(player.move_left, "a")
game.screen.onkey(player.move_right, "d")
game.screen.onkey(player.shoot, "space")
game.screen.listen()

playing = True
while playing:
    sleep(0.1)
    game.screen.update()

    if enemies.all_dead():
        playing = False

    enemies.combatant_movement()

    if player.bullet.ycor() < 260:
        player.bullet_move()

    if enemies.check_hit(player.bullet):
        player.bullet_reset()


game.screen.exitonclick()
