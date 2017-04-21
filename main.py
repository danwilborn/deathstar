# Dan Wilborn

import sys, pygame, math
from math import atan2, degrees, pi

cannonX = 60
cannonY = 85

class Player(pygame.sprite.Sprite):
	
	def __init__(self, gs):
		self.gs = gs
		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/deathstar.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 50
		self.rect.centery = 50
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

		xVal = mousePos[0] - self.rect.centerx
		yVal = mousePos[1] - self.rect.centery		

		rads = atan2(xVal, yVal)
		rads %= 2*pi
		angle = degrees(rads)

		self.image = pygame.transform.rotate(self.original, angle)	
		self.rect = self.image.get_rect(center=self.rect.center)

		#cannonAngle = cannonAngle+angle

	def tick(self):
		self.rotate()

class Enemy(pygame.sprite.Sprite):

	def __init__(self, gs):
		self.gs = gs
		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/globe.png")
		self.rect = self.image.get_rect()
		self.original = self.image
		self.rect.centerx = 640
		self.rect.centery = 480
		self.hitpoints = 2000
		self.count = 0	

	def change_image(self):
		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/globe_red100.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 640
		self.rect.centery = 480

	def explosion(self):
		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/explosion/frames000a.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 640
		self.rect.centery = 480

	def tick(self, laser):
		r = pygame.Rect(self.gs.enemy.image.get_rect())
		if r.collidelist(laser):
			self.hitpoints -= 5
		if self.hitpoints < 1500 and self.hitpoints > 750:
			self.change_image()
		if self.hitpoints < 0:
			self.explosion()
		

class Laser(pygame.sprite.Sprite):

	def __init__(self, gs):
		self.gs = gs
		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/laser2.png")
		self.rect = self.image.get_rect()
		self.original = self.image
		self.list_of_lasers = list()
		self.angle = 0
		self.startX = self.gs.player.rect.centerx
		self.startY = self.gs.player.rect.centery

	def create(self):

		for i in range(5):	
			image = self.image
			rect = image.get_rect()
			rect.centerx = self.startX
			rect.centery = self.startY
	
			mousePos = pygame.mouse.get_pos()
		
			xVal = mousePos[0] - self.startX
			yVal = mousePos[1] - self.startY

			rads = atan2(xVal, yVal)
			self.angle = rads
			self.list_of_lasers.append(rect)
			self.startX -= math.sin(self.angle)*5
			self.startY -= math.cos(self.angle)*5
	
	def move(self):
		
		for rect in self.list_of_lasers:
			rect.centerx += math.sin(self.angle)*10
			rect.centery += math.cos(self.angle)*10

	def tick(self):
		self.move()		

class GameSpace(object):

	def main(self):
		pygame.init()
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		self.player = Player(self)
		self.enemy = Enemy(self)
		self.clock = pygame.time.Clock()
		self.laser_array = list()	

		running = True
		while running:
			self.clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.player.move(event.key)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					laser = Laser(self)
					laser.create()
					self.laser_array.append(laser)
				elif event.type == pygame.QUIT:
					running = False
				self.player.tick()
				self.clock.tick()
			for laser in self.laser_array:
				laser.tick()
				self.enemy.tick(laser.list_of_lasers)

			self.screen.fill(self.black)
			for laser in self.laser_array:
				for rect in laser.list_of_lasers:
					self.screen.blit(laser.original, rect)
			self.screen.blit(self.enemy.image, self.enemy.rect)
			self.screen.blit(self.player.image, self.player.rect)
			pygame.display.flip()

		pygame.quit()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()

'''
		rads = atan2(cannonX, cannonY)
		rads %= 2*pi
		cannonAngle = degrees(rads)

		xVal = mousePos[0] - cannonX
		yVal = mousePos[1] - cannonY

		rads = atan2(xVal, yVal)
		rads %= 2*pi
		angle = degrees(rads)
'''
