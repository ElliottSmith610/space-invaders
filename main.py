from time import sleep
from brain import Game, Player, Enemies

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

    enemies.combatant_movement()
    enemies.combatant_advance()
    enemies.shoot()

    if player.bullet.ycor() < 260:
        player.bullet_move()

    for bullet in enemies.bullet_list:
        if player.check_hit(bullet):
            enemies.bullet_reset(bullet)

        if bullet.ycor() < 260:
            enemies.bullet_move()
        if bullet.ycor() < -110:
            enemies.bullet_reset(bullet)


    if enemies.check_hit(player.bullet):
        player.bullet_reset()

    if enemies.all_dead() or player.health == 0:
        game.game_over()
        game.screen.update()
        playing = False


game.screen.exitonclick()
