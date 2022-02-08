import pygame, random, Colors
import ImageLoad as il
# loading sounds
pygame.mixer.init()
# spidey sound
spideyBanter = []
spideyShoot = []
spideyDie = []
spideyBanter.append(pygame.mixer.Sound('Sound/Spidey/cuteoutfit.wav'))
#spideyBanter.append(pygame.mixer.Sound('Sound/Spidey/pizzawin.wav'))
spideyBanter.append(pygame.mixer.Sound('Sound/Spidey/sheriff.wav'))
spideyBanter.append(pygame.mixer.Sound('Sound/Spidey/youretrash.wav'))
spideyShoot.append(pygame.mixer.Sound('Sound/Spidey/Thwip.wav'))
spideyDie.append(pygame.mixer.Sound('Sound/Spidey/TobeyAHHH.wav'))
# poggle sound
pogBanter = []
pogShoot = []
pogBanter.append(pygame.mixer.Sound('Sound/Poggle/banter1.wav'))
pogBanter.append(pygame.mixer.Sound('Sound/Poggle/banter2.wav'))
pogBanter.append(pygame.mixer.Sound('Sound/Poggle/banter3.wav'))
for sound in pogBanter:
    sound.set_volume(0.5)
pogDie = pogBanter # []
pogShoot.append(pygame.mixer.Sound('Sound/Poggle/shoot.wav'))
for sound in pogShoot:
    sound.set_volume(0.5)
# goblin sound
goblinBanter = []
goblinShoot = []
goblinDie = []
goblinBanter.append(pygame.mixer.Sound('Sound/Goblin/butnow.wav'))
goblinBanter.append(pygame.mixer.Sound('Sound/Goblin/goblinvictory.wav'))
goblinBanter.append(pygame.mixer.Sound('Sound/Goblin/hellodear.wav'))
goblinBanter.append(pygame.mixer.Sound('Sound/Goblin/sleep.wav'))
goblinBanter.append(pygame.mixer.Sound('Sound/Goblin/timedie.wav'))
goblinShoot.append(pygame.mixer.Sound('Sound/Goblin/grenade.wav'))
for sound in goblinShoot:
    sound.set_volume(0.3)
goblinDie.append(pygame.mixer.Sound('Sound/Goblin/gobdeath.wav'))
goblinDie.append(pygame.mixer.Sound('Sound/Goblin/avenge.wav'))
# lemon sound
lemonBanter = []
lemonShoot = []
lemonDie = []
lemonBanter.append(pygame.mixer.Sound('Sound/Lemon/helpineed.wav'))
for sounds in lemonBanter:
    sound.set_volume(0.2)
lemonShoot.append(pygame.mixer.Sound('Sound/Lemon/drop.wav'))
lemonDie = lemonBanter
# baby sound (set to same as Poggle)
nutBanter = pogBanter
nutShoot = pogShoot
nutDie = pogDie
# chrome sound (set to same as Poggle)
chromeBanter = pogBanter
chromeShoot = pogShoot
chromeDie = pogDie
# general sounds
dash = pygame.mixer.Sound('Sound/dash.wav')
reflect = pygame.mixer.Sound('Sound/reflect.wav')
# END SOUND LOAD
class Character():
    def __init__(self, banter, shoot, die, sprite, name, nameColor):
        self.banter = banter
        self.shoot = shoot
        self.die = die
        self.sprite = sprite
        self.name = name
        self.nameColor = nameColor
        self.currentInd = 0
        
    def playBanterOn(self, channel):
        num = random.randint(0, len(self.banter) - 1)
        channel.play(self.banter[num])
        
    def playDeathOn(self, channel):
        num = random.randint(0, len(self.die) - 1)
        channel.play(self.die[num])
        
    def playShootOn(self, channel):
        num = random.randint(0, len(self.shoot) - 1)
        channel.play(self.shoot[num])
        
    def playDashOn(self, channel):
        channel.play(dash)

    def playReflectOn(self, channel):
        channel.play(reflect)
    
    def getColor(self):
        maxInd = len(self.nameColor)
        self.currentInd += 0.025 # 0.01
        if self.currentInd >= maxInd:
            self.currentInd = 0
        return self.nameColor[int(self.currentInd)]
        
# START CHARACTER LOAD
spidey = Character(spideyBanter, spideyShoot, spideyDie, il.spiderman, 'Spider-Man', [Colors.RED])
peter = Character(spideyBanter, spideyShoot, spideyDie, il.peter, 'Peter Parker', [Colors.RED])
ironman = Character(spideyBanter, spideyShoot, spideyDie, il.ironman, 'Ironman', [Colors.BLUE])
poggle = Character(pogBanter, pogShoot, pogDie, il.poggle, 'Poggle', [Colors.GREEN])
goblin = Character(goblinBanter, goblinShoot, goblinDie, il.greengoblin, 'Green Goblin', [Colors.GREEN])
lemon = Character(lemonBanter, lemonShoot, lemonDie, il.lemon, 'JOHN LEMON', [Colors.YELLOW])
r2 = Character(spideyBanter, spideyShoot, spideyDie, il.r2, 'R2D2', [Colors.BLUE])
babynut = Character(nutBanter, nutShoot, nutDie, il.nut, 'Baby Nut', [Colors.YELLOW])
chrome = Character(chromeBanter, chromeShoot, chromeDie, il.chrome, 'Google Chrome', [Colors.RED, Colors.YELLOW, Colors.GREEN])
bird = Character(nutBanter, nutShoot, nutDie, il.flap, 'Flappy Bird', [Colors.YELLOW])
donatello = Character(nutBanter, nutShoot, nutDie, il.donatello, 'Donatello', [Colors.GREEN])
hcpss = Character(nutBanter, nutShoot, nutDie, il.hcpss, 'HCPSS', [Colors.BLUE])
washMon = Character(nutBanter, nutShoot, nutDie, il.washMon, 'Washington Monument', [Colors.YELLOW])

        
