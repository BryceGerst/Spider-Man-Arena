# This is the main game file
# The code is broken up into multiple python files for clarity in reading the code
# Ideally, this file will almost look like pseudocode, as the other files be doing the heavy lifting
import MainMenu, Scaler, ArenaFight, pygame, sys, MapSelection, Colors, CharSelection, SpiderSoccer
import ImageLoad as il
# --------------------------
# Initializing the game
def main(screen, screenW, screenH, fps, clock):
     allDisplayInfo = [screen, clock, screenW, screenH, fps]
     gameScaler = Scaler.Scaler(screenW, screenH)
     p1Victory = pygame.transform.scale(il.p1win, (screenW, screenH))
     p2Victory = pygame.transform.scale(il.p2win, (screenW, screenH))
     # --------------------------

     # --------------------------
     # Game Variables
     gameStage = 0 # This stores an integer corresponding to what part of the game the player is in, so stage 1 is the title screen, 2 is selecting character, etc

     # --------------------------

     # --------------------------
     # Game Loop
     playing = True
     victoryFrames = 0
     while playing:
         # This for loop is for finding key presses and for quitting out of the game
          for event in pygame.event.get():
              # This if statement checks when to stop running the game code
             if event.type == pygame.QUIT or pygame.key.get_pressed()[27]: # key 27 is escape
                 playing = False

          if gameStage == 0:
               gameStage, sprite1, sprite2, ball1, ball2 = CharSelection.run(allDisplayInfo)
          if gameStage == 1:
               gameStage, mapNum, bo = MapSelection.run(allDisplayInfo) # MainMenu.run() returns an integer which corresponds to the gameStage selected by the player in the main menu
          # Not an else if (elif) because if MainMenu.run() returns 2 then we went this next code to run right after
          if gameStage == 2:
               gameStage = ArenaFight.run(allDisplayInfo, (0, 0), sprite1, sprite2, mapNum, ball1, ball2, bo)#SpiderSoccer.run(allDisplayInfo, (0,0), sprite1, sprite2, bo)
          if gameStage == 4:
               screen.blit(p1Victory, (0,0))
               victoryFrames += 1
          if gameStage == 5:
               screen.blit(p2Victory, (0,0))
               victoryFrames += 1
          if gameStage == -1: # gameStage will only be -1 if the player tries to quit out of the game during a run() method
               playing = False

          if victoryFrames >= 1200:
               gameStage = 0
               victoryFrames = 0

          pygame.display.update()

     
     pygame.quit()
     sys.exit() # Quits out of the program without causing issues
     # --------------------------
