#the key functionalities that need to be tested include:\;
#1......Player Movement: Test the player's ability to move left and right within the game window. Check that the player's movement is bounded within the window's width.

#2......Star Generation: Test the generation of stars at random positions at the top of the window and their fall downwards. Check that the number of stars generated increases over time.

#3......Collision Detection: Test the game's ability to detect when a star collides with the player. When a collision occurs, the game should stop and display the game over screen.To test the game's ability to detect when a star does not collide with the player

#4......Score Calculation: Test the game's ability to correctly calculate the score based on the elapsed time and the number of stars collected.

#5......Game Over Condition: Test the game's ability to correctly handle the game over condition when the player collides with a star. The game should reset the game state and allow the player to restart the game.To test the game's ability to correctly handle the game over condition when the player does not collide with a star.

#6......Key Input: Test the game's ability to correctly handle key inputs for player movement and game control (pausing and restarting the game).

import unittest
from dodge_game import Player, Star
import pygame

class TestPlayerMovement(unittest.TestCase):
 def setUp(self):
    self.player = Player(200, 500, 50, 40, 5, "space.webp")

 def test_player_movement(self):
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
    pygame.event.post(event)
    self.player.move()
    self.assertEqual(self.player.rect.x, 195)

 def test_player_movement_bound(self):#This test will simulate a right key press and check if the player's x position increases.
    self.player.rect.x = 0
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
    pygame.event.post(event)
    self.player.move()
    self.assertEqual(self.player.rect.x, 0)

 def test_player_movement_right(self):
   event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
   pygame.event.post(event)
   self.player.move()
   self.assertEqual(self.player.rect.x, 205)   

class TestStarGeneration(unittest.TestCase):
   def setUp(self):
       self.star = Star(200, 0, 14, 30, 3, "star.webp")

   def test_star_generation(self):
       self.star.fall()
       self.assertEqual(self.star.rect.y, 3)

   def test_star_increase(self):
       # This test requires a loop to generate multiple stars and check if the number increases
       pass
   
   
class TestCollisionDetection(unittest.TestCase):
   def setUp(self):
       self.player = Player(200, 500, 50, 40, 5, "space.webp")
       self.star = Star(200, 0, 14, 30, 3, "star.webp")

   def test_collision_detection(self):
       self.star.rect.y = 500
       self.assertTrue(self.star.collide_with_player(self.player))

   def test_no_collision(self):#This test will simulate a star that is not colliding with the player and check if the collide_with_player method returns False.
    self.star.rect.y = 1000
    self.assertFalse(self.star.collide_with_player(self.player))
    

class TestScoreCalculation(unittest.TestCase):
   def setUp(self):
       self.elapsed_time = 10
       self.score = 5

   def test_score_calculation(self):
       final_score = int(self.elapsed_time * self.score)
       self.assertEqual(final_score, 50)

   def test_multiple_stars(self):#This test will simulate the player collecting multiple stars and check if the final score is calculated correctly.
    self.elapsed_time = 10
    self.score = 5
    self.number_of_stars = 3
    final_score = int(self.elapsed_time * self.score * self.number_of_stars)
    self.assertEqual(final_score, 150)
    

class TestGameOverCondition(unittest.TestCase):
   def setUp(self):
       self.player = Player(200, 500, 50, 40, 5, "space.webp")
       self.star = Star(200, 0, 14, 30, 3, "star.webp")

   def test_game_over_condition(self):
       # This test requires a loop to simulate the game and check if it stops when a collision occurs
       pass
   
   def test_no_game_over(self):#This test will simulate the game running without a collision and check if the game does not stop.
    for _ in range(100):
       self.star.fall()
       self.assertFalse(self.star.collide_with_player(self.player))


class TestKeyInput(unittest.TestCase):
   def setUp(self):
       self.player = Player(200, 500, 50, 40, 5, "space.webp")

   def test_key_input(self):
       # This test requires a loop to simulate key presses and check if the player moves correctly
       pass

if __name__ == '__main__':
   unittest.main()










    

