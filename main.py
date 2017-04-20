# Dan Wilborn

import sys, pygame, math
from math import atan2, degrees, pi

class Player:
	
	def __init__(self):
		
		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/deathstar.png")
		self.rect = self.image.get_rect()
		self.original = self.image

	def move(self, key):
		if key == pygame.K_LEFT:
			self.rect.centerx -= 2
		if key == pygame.K_RIGHT:
			self.rect.centerx += 2
		if key == pygame.K_UP:
			self.rect.centery -= 2
		if key == pygame.K_DOWN:			
			self.rect.centery += 2

	def rotate(self):
		# Mouse Movement
		loc = self.image.get_rect().center
		mousePos = pygame.mouse.get_pos()
		rads = atan2(-mousePos[0], mousePos[1])
		rads %= 2*pi
		angle = degrees(rads)
		self.image = pygame.transform.rotate(self.image, angle)	
		self.rect = self.image.get_rect(center=self.rect.center)


class Enemy:

	def __init__(self):

		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/globe.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 360
		self.rect.centery = 600	

class GameSpace(object):

	def main(self):
		pygame.init()
		self.size = self.width, self.height = 640, 420
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

	
		self.player = Player()
		self.enemy = Enemy()
		self.clock = pygame.time.Clock()
	
		running = True
		while running:
			self.clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.player.move(event.key)
				elif event.type == pygame.QUIT:
					running = False
				self.clock.tick()
			
			self.screen.fill(self.black)
			self.screen.blit(self.enemy.image, self.enemy.rect)
			self.screen.blit(self.player.image, self.player.rect)
			pygame.display.flip()

		pygame.quit()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
