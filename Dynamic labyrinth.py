###To do:



#implement GUI login system
#implement leaderboard
#implement endscreen window allowing player to logout, play again (if game lost)
#implement pause/ save and exit feature
#delete saved games when plyer loses and set new gameIDs
#use MAX() aggregate function


#checkList: Graph, depth-first search algorithm, stack, 2d array, dictionary, OOP
#Note: coin sprites were taken from OpenGameArt.org

import pygame,sys,random,math, time
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
from db import getGames, validate, updateDB, login, sign_up, Manager



def howToPlay():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("How To Play")
    instructionFont=pygame.font.SysFont('Comic Sans MS', 20)
    instruction1=instructionFont.render("1. Use the arrow keys to move through the maze", False, (255,255,255))
    instruction2=instructionFont.render("2. Collect as many coins as you can", False, (255,255,255))
    instruction3=instructionFont.render("3. Avoid the zombies and make it to the exit in time", False, (255,255,255))
    instruction4=instructionFont.render("4. Press the spacebar to pause the game and use the arrow keys to select an option and press enter", False, (255,255,255))

    
    
    
    
    surface=pygame.display.set_mode((1000, 500))

    surface.blit(instruction1, (0,0))
    surface.blit(instruction2, (0,100))
    surface.blit(instruction3, (0,200))
    surface.blit(instruction4, (0,300))
    
    while True:
        
        for event in GAME_EVENTS.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
        pygame.display.update()
    



def exitGame():
    leaderboard=Manager.getTop10()

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Leaderboard")
    headerFont=pygame.font.SysFont('Comic Sans MS', 40)
    statsFont=pygame.font.SysFont('Comic Sans MS', 30)
    surface=pygame.display.set_mode((600,600))

    username=headerFont.render("Username", False , (255,255,255))
    highScore=headerFont.render("Best Score", False, (255,255,255))
    
    surface.blit(username, (10,0))
    surface.blit(highScore, (250,0))
    username_x=10
    score_x=250

    username_y=40
    score_y=40
    
    for record in leaderboard:
        name=statsFont.render(record[0], False, (255,255,255))
        score=statsFont.render(str(record[1]), False, (255,255,255))

        surface.blit(name, (username_x, username_y))
        surface.blit(score, (score_x, score_y))

        username_y+=40
        score_y+=40
        
        
        
    while True:
        for event in GAME_EVENTS.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()
        
        
                
    
    



Manager.display_menu()

if Manager.gameState == "not playing":
    exitGame()

howToPlay() # display instructions

level, maze_size, score= Manager.gameSelectedInfo


WIDTH=600
HEIGHT=600





cell_size=WIDTH//maze_size





pi=math.pi    

gameOver=False

maze_grid=[]

zombies=[]

tmp_spawn_interval=20- 5*(level-1)
if tmp_spawn_interval>5:
    spawn_interval=tmp_spawn_interval
else:
    spawn_interval=5



    
lastSpawned=0


zombie_speed=0.1
stack=[]

timeLeft=120
start_time=0

lastSpawn=0

levelStartScore=score
coinPhase=0

lastCoinFrame=0
justReset=False





#Game code


def countDown(timeLeft,start_time):
    timeLeft=120-(GAME_TIME.get_ticks()//1000-start_time)
    if timeLeft>10:
        time_colour=(0,255,50)
    else:
        time_colour=(255,0,0)
    timeDisplay=gameFont.render(str(timeLeft),False, time_colour)
    surface.blit(timeDisplay, (520,20))
    return timeLeft,time_colour


class Cell:
    
    
    
    
 
    

    def __init__(self,x,y,cell_size):
        self.row=y//cell_size
        self.column=x//cell_size
        self.x=x
        self.y=y
        self.size=cell_size
        self.num_rows,self.num_columns= HEIGHT//self.size, WIDTH//self.size
        self.wall= {'top':1, 'right':1, 'bottom':1, 'left':1}
        self.visited=False
        self.coin=None
        #stores the row and column of adjacent cells for every cell
        if self.row>0:
            self.top=(self.row-1,self.column)
        else:
            self.top=None

        if self.column<self.num_columns-1:
            self.right=(self.row,self.column+1)
        else:
            self.right=None

        if self.row<self.num_rows-1:
            self.bottom=(self.row+1,self.column)
        else:
            self.bottom=None

        if self.column>0:
            self.left=(self.row,self.column-1)
        else:
            self.left=None
        
        
        
        

    def draw(self):
        if self.visited:
            pygame.draw.rect(surface, pygame.Color('black') , (self.x,self.y,self.size,self.size))

        if self.x==exit_cell.x and self.y==exit_cell.y:
            pygame.draw.rect(surface, pygame.Color('green') , (self.x,self.y,self.size,self.size))

        if self.wall['top']:
            pygame.draw.line(surface, pygame.Color('darkorange'), (self.x,self.y),(self.x+self.size, self.y),1)

        if self.wall['right']:
            pygame.draw.line(surface, pygame.Color('darkorange'), (self.x+self.size,self.y), (self.x+self.size, self.y+self.size),1)

        if self.wall['bottom']:
            pygame.draw.line(surface, pygame.Color('darkorange'), (self.x,self.y+self.size), (self.x+self.size, self.y+self.size),1)

        if self.wall['left']:
            
            pygame.draw.line(surface, pygame.Color('darkorange'), (self.x,self.y), (self.x, self.y+self.size),1)

    def get_next(self,curr):
        
        neighbours=[]
        
        

        #checks if going to the up is possible
        if curr.top:
            if not maze_grid[curr.top[0]][curr.top[1]].visited:
                neighbours.append('top')

        #checks if going right is possible 
        if curr.right:
            if not maze_grid[curr.right[0]][curr.right[1]].visited:
                neighbours.append('right')

        #checks if going down is possible
        if curr.bottom:
            
            if not maze_grid[curr.bottom[0]][curr.bottom[1]].visited:
                neighbours.append('bottom')

        #checks if going left is possible
        if curr.left:
            if not maze_grid[curr.left[0]][curr.left[1]].visited:
                neighbours.append('left')

        return neighbours




    
    


def create_grid(cell_size):
    maze_size=WIDTH//cell_size
    for row in range(0,WIDTH,cell_size):
        r=[]
        for column in range(0,WIDTH,cell_size):
            
            r.append(Cell(column,row,cell_size))
        maze_grid.append(r)
    curr_cell=maze_grid[0][maze_size//2]
    curr_cell.visited=True

    #creates maze circuit
    for row in range(0,maze_size,maze_size-1):
        
        for column in range(0,maze_size-1):
            
            
            maze_grid[row][column].wall['right']=0
            maze_grid[row][column+1].wall['left']=0
            maze_grid[column][row].wall['bottom']=0
            maze_grid[column+1][row].wall['top']=0
            

    
    
     
    stack.append(curr_cell)

    return maze_size



  
    
    

create_grid(cell_size)                
          



       
                
class Player:
   
    
    
    
    def __init__(self, row, column):
        self.curr_cell=maze_grid[row][column]
        self.row=row
        self.column=column
        self.radius=self.curr_cell.size/2
        self.x,self.y=self.curr_cell.x+self.radius,self.curr_cell.y+self.radius

        

    def update(self):
        self.x,self.y=self.curr_cell.x+self.radius,self.curr_cell.y+self.radius
        self.row,self.column=self.x//self.curr_cell.size,self.y//self.curr_cell.size




   

   
    def draw(self):
        
        pygame.draw.circle(surface, pygame.Color('orange'), (self.x,self.y), self.radius,0)

    
    def moveAllowed(self,cell,direction):
        if direction== 'top':
     
            return (cell.top is not None) and (not cell.wall['top'])
        elif direction== 'right':
            
            return (cell.right is not None) and (not cell.wall['right'])
        elif direction == 'bottom':
            
            return (cell.bottom is not None) and (not cell.wall['bottom'])
        else:
            return (cell.left is not None) and (not cell.wall['left'])

    
    def move(self,direction):
        if direction=='top':
            self.curr_cell=maze_grid[self.curr_cell.top[0]][self.curr_cell.top[1]]
            self.update()
  
        elif direction == 'right':
            self.curr_cell=maze_grid[self.curr_cell.right[0]][self.curr_cell.right[1]]
            self.update()

        elif direction == 'bottom':
            self.curr_cell=maze_grid[self.curr_cell.bottom[0]][self.curr_cell.bottom[1]]
            self.update()

        else:
            self.curr_cell=maze_grid[self.curr_cell.left[0]][self.curr_cell.left[1]]
            self.update()

    
    def levelComplete(self):
        return self.curr_cell==exit_cell # checks that the player has reached the exit

   


















class Zombie(Player):
    
    
    
    path={}
    
    
    moving=False
    next_cell=None
    
    
    
    def __init__(self, row, column, speed):
        self.speed=speed
       
        
        super().__init__(row,column)
        
   
        
                

    

    
        
        
        
    #polymorphism + inheritance
    def move(self, direction): # getDir() passed as parameter
     
        if direction == 'top' and self.moveAllowed(self.curr_cell, 'top'):
            if (self.curr_cell.y+self.radius)-(self.y-self.speed) < self.curr_cell.size:
                self.y-=self.speed
                self.moving=True
                self.next_cell=maze_grid[self.curr_cell.top[0]][self.curr_cell.top[1]]

            
               
            else:
                del self.path[self.curr_cell]
                self.curr_cell=maze_grid[self.curr_cell.top[0]][self.curr_cell.top[1]]
                self.update()
                self.moving=False
                
                
        elif direction == 'right' and self.moveAllowed(self.curr_cell, 'right'):
            if (self.x+self.speed)-(self.curr_cell.x+self.radius) < self.curr_cell.size:
                    self.x+=self.speed
                    self.moving=True
                    self.next_cell=maze_grid[self.curr_cell.right[0]][self.curr_cell.right[1]]
                    
            else:
                del self.path[self.curr_cell]
                self.curr_cell=maze_grid[self.curr_cell.right[0]][self.curr_cell.right[1]]
                self.update()
                self.moving=False
                
                    
        elif direction == 'bottom' and self.moveAllowed(self.curr_cell, 'bottom'):
            if (self.y+self.speed)-(self.curr_cell.y+self.radius) < self.curr_cell.size:
                self.y+=self.speed

                self.moving=True
                self.next_cell=maze_grid[self.curr_cell.bottom[0]][self.curr_cell.bottom[1]]
               
            else:
                del self.path[self.curr_cell]
                self.curr_cell=maze_grid[self.curr_cell.bottom[0]][self.curr_cell.bottom[1]]
                self.update()
                self.moving=False
                

        elif direction == 'left' and self.moveAllowed(self.curr_cell, 'left'):
            if (self.curr_cell.x+self.radius)-(self.x-self.speed) < self.curr_cell.size:
                self.x-=self.speed
                
                self.moving=True
                self.next_cell=maze_grid[self.curr_cell.left[0]][self.curr_cell.left[1]]
                
            else:
                del self.path[self.curr_cell]
                self.curr_cell=maze_grid[self.curr_cell.left[0]][self.curr_cell.left[1]]
                self.update()
                self.moving=False
        
                
        
        
    def draw(self):
        pygame.draw.circle(surface, pygame.Color('green'), (self.x,self.y), self.radius,0)

    def getDistance(self,a,b):
        return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
    
    def setHeuristic(self):
        #heurisitic = distance from player + length of path calculated
        return len(self.path)+self.getDistance(self.curr_cell, player.curr_cell)


    def getPath(self,target):
        # weight=cost(ie a move)+distance
        
        cell=self.curr_cell
        start=cell
        
        
        costs={cell: float('inf') for row in maze_grid for cell in row}
        costs[cell]=0
        
        weights={cell: float('inf') for row in maze_grid for cell in row}
        weights[cell]=self.getDistance(cell,target)
        

        queue={}
        #(overall weight, distance from target)
        queue[cell]=(weights[cell], weights[cell])
        reversedPath={}
        
       
        
        while cell!=target:
            
            pointers={"top":cell.top, "right":cell.right, "bottom":cell.bottom, "left":cell.left}
            
            
            
            
            
            
            
            for i in pointers: 
                if self.moveAllowed(cell,i):
                    adj_cell=maze_grid[pointers[i][0]][pointers[i][1]]
                    temp_cost=costs[cell]+1
                    temp_weight=temp_cost+self.getDistance(adj_cell,target)
                   

                    if temp_weight<weights[adj_cell]:
                        costs[adj_cell]=temp_cost
                        weights[adj_cell]=temp_weight
                        queue[adj_cell]=weights[adj_cell], self.getDistance(adj_cell,target)
                        reversedPath[adj_cell]=cell
                    
                        
                        
                    
                        
                  
            queue=dict(sorted(queue.items(), key=lambda item: item[1]))

            

            
            del queue[cell]
            
            cell=[i for i in queue.items()][0][0]
            
            

            
       
            
                
        
        
        #creates path by reversing the links
       
        path={}
        
        while cell!=start:
            
            path[reversedPath[cell]]=cell
            cell=reversedPath[cell]
        
       
        self.path= path
        
        
        
        
       
        
                                
                
                
            
            
        






       
        
    def getDir(self):
        if len(self.path)>1:
            next_cell=self.path[self.curr_cell]
            pointers={self.curr_cell.top:"top", self.curr_cell.right:"right", self.curr_cell.bottom: "bottom", self.curr_cell.left: "left"}
            return pointers[(next_cell.row,next_cell.column)]
        else:
            
            self.getPath(player.curr_cell)
            next_cell=self.path[self.curr_cell]
            pointers={self.curr_cell.top:"top", self.curr_cell.right:"right", self.curr_cell.bottom: "bottom", self.curr_cell.left: "left"}
            return pointers[(next_cell.row,next_cell.column)]
            
        
            
        

       
    def bitPlayer(self):
       
        return self.getDistance(player, self) < self.radius

    











class Coin(Player):
    
    
    def __init__(self):
        curr_cell=self.hash()
        curr_cell.coin=self
        self.curr_cell=curr_cell
        
        self.collected=False
        

    
  

    def hash(self):
     
   
        pos=0
        for i in str(self):
            pos+=ord(i)
      

         
        num_of_cells=maze_size**2
        
        for i in range(num_of_cells):
            if (pos+i) % num_of_cells == 0:
                row=(num_of_cells-i-1)//(maze_size)
                column= (num_of_cells-i-1) % maze_size
              
                break
        
        curr_cell=maze_grid[row][column]
        
        if curr_cell.coin:
            
            curr_cell=self.reHash(curr_cell)
        
        return curr_cell 

    
    #recursion
    def reHash(self, cell, prev=None):
        
        #if cell already contains a coin, the coin will be placed in an adjacent cell that the player can access
        if not cell.coin:
            return cell

        else:
            dirs={'top': cell.top, 'right': cell.right, 'bottom': cell.bottom, 'left': cell.left}
            prevs={'top':'bottom', 'bottom':'top', 'right':'left', 'left':'right'}


            tmp = [i for i in dirs if self.moveAllowed(cell, i)]
            if len(tmp)>1 and prev: #ie if not at a dead end don't check previously visited cell
                tmp.remove(prev)

            direction=random.choice(tmp)
            pointer=dirs[direction]

            next_cell=maze_grid[pointer[0]][pointer[1]]
            

            return self.reHash(next_cell, prevs[direction])
      









    def draw(self):
        image=pygame.image.load(str(coinPhase)+ ".png")
        surface.blit(image, (self.curr_cell.x-20, self.curr_cell.y-20))
        
        




    def checkIfCollected(self):
        
 
        
        if (self.curr_cell.row, self.curr_cell.column) == (player.curr_cell.row, player.curr_cell.column):
            self.collected=True
        
        
        
                               
    













def generate_maze():
    #creates maze, implementing backtracking 
    while stack:

    
    
        curr=stack[-1]
        
        
            
        
        
           
        neighbours=curr.get_next(curr)
            
            
            
        if neighbours: # ie if there is an unvisited cell left
            
            next_cell_dir=random.choice(neighbours)
            #removes walls accordingly
            if next_cell_dir=='top':
                next_cell=maze_grid[curr.top[0]][curr.top[1]]
                curr.wall[next_cell_dir]=0
                next_cell.wall['bottom']=0
                stack.append(next_cell)
                next_cell.visited=True

            elif next_cell_dir == 'right':
                next_cell=maze_grid[curr.right[0]][curr.right[1]]
                curr.wall[next_cell_dir]=0
                next_cell.wall['left']=0
                stack.append(next_cell)
                next_cell.visited=True

            elif next_cell_dir == 'bottom':
                next_cell=maze_grid[curr.bottom[0]][curr.bottom[1]]
                curr.wall[next_cell_dir]=0
                next_cell.wall['top']=0
                stack.append(next_cell)
                next_cell.visited=True

            else:
                next_cell=maze_grid[curr.left[0]][curr.left[1]]
                curr.wall[next_cell_dir]=0
                next_cell.wall['right']=0
                stack.append(next_cell)
                next_cell.visited=True
        else:
            stack.pop()
        
def draw_maze(maze_size):
    
    for row in range(maze_size):
        for column in range(maze_size):
            maze_grid[row][column].draw()
            
             
                
            
             
generate_maze()


# creates exit in centre of the maze
exit_cell=maze_grid[maze_size//2][maze_size//2] 


def nextLevel(cell_size):
    maze_grid.clear()
   
    
    if cell_size==60:
        new_cell_size=30
        
    elif cell_size==30:
        new_cell_size=25

    elif cell_size==25:
        new_cell_size = 20
        
    
        
    else:
        new_cell_size=cell_size
        
    
   
    new_maze_size=create_grid(new_cell_size)
    generate_maze()

    
    Player.curr_cell=maze_grid[0][maze_size//2]
    Player.radius=new_cell_size//2
    return new_maze_size,new_cell_size
        



    

player=Player(0,maze_size//2)


def spawnZombies(maze_size, speed):
    
    
    zombies.append(Zombie(random.randint(0,maze_size-1),maze_size-1, speed))
    
    
    for zombie in zombies:
        
        if not zombie.moving:
            
            zombie.getPath(player.curr_cell)
            
        



def generateCoins(level):

    if level == 1:
        count=random.randint(1,5)
    elif level >= 2 and level <=4:
        count=random.randint(5,10)
    else:
        count=random.randint(5,15)
    for i in range(count):
        Coin()
  
       
def drawCoins():
    
    for row in range(maze_size):
        for column in range(maze_size):
            
            if maze_grid[row][column].coin:
                
                
              
                maze_grid[row][column].coin.checkIfCollected()
                
                if not maze_grid[row][column].coin.collected:
                    
                    maze_grid[row][column].coin.draw()
                    
                else:
                    
                    maze_grid[row][column].coin=None


    




def pause():
    button1= "Resume"
    button2= "Save and log out"
    button3= "Log out"    
    label_1=gameFont.render(button1,False, (0,0,0))
    label_2=gameFont.render(button2,False, (0,0,0))
    label_3=gameFont.render(button3,False, (0,0,0))
    colours=[pygame.Color('gray90'), pygame.Color('gray86'), pygame.Color('gray86')]
    optionSelected=False
    index=0
    pygame.draw.rect(screen, (128,128,128,150), (0,0, WIDTH, HEIGHT))
    surface.blit(screen, (0,0))

    while not optionSelected:
        tmp=index
              
        for event in GAME_EVENTS.get():

            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    index = (index +1)%3

                if event.key == pygame.K_UP:
                    index=(index-1)%3

                if event.key == pygame.K_RETURN:
                    optionSelected=True
            colours[tmp]= pygame.Color('gray86')
            colours[index]= pygame.Color('gray90')


        colour1, colour2, colour3 = colours           
        pygame.draw.rect(surface, colour1, (150, 150, 250, 50))
        pygame.draw.rect(surface, colour2, (150, 210, 250, 50))
        pygame.draw.rect(surface, colour3, (150, 270, 250, 50))
        surface.blit(label_1, (150, 150))
        surface.blit(label_2, (150, 210))
        surface.blit(label_3, (150, 270))

        pygame.display.update()
       
    if index == 0:
        return 

    if index ==1:
       
        
       
        return "save and leave game"
        

    if index == 2:
        
        return "leave game"





def endScreen():
    button1= "Play again"
    button2= "Quit and log out"
    
    
    label_1=gameFont.render(button1,False, (0,0,0))
    label_2=gameFont.render(button2,False, (0,0,0))
    

    colours=[pygame.Color('gray90'), pygame.Color('gray86')]

    optionSelected=False

    index=0
    pygame.draw.rect(screen, (128,128,128,150), (0,0, WIDTH, HEIGHT))
    surface.blit(screen, (0,0))

    while not optionSelected:
        tmp=index
        
        
        
        for event in GAME_EVENTS.get():

            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    index = (index +1)%2

                if event.key == pygame.K_UP:
                    index=(index-1)%2

                if event.key == pygame.K_RETURN:
                    optionSelected=True
            colours[tmp]= pygame.Color('gray86')
            colours[index]= pygame.Color('gray90')
            
        colour1, colour2= colours           
        pygame.draw.rect(surface, colour1, (150, 150, 250, 50))
        pygame.draw.rect(surface, colour2, (150, 210, 250, 50))
        
        surface.blit(label_1, (150, 150))
        surface.blit(label_2, (150, 210))
        

        pygame.display.update()
            
    return index == 1 # returns true if player wants to quit
    


def reset():
    
    level=1
    maze_size=10
    cell_size=60
    timeLeft=120
    spawn_interval=20
    
    
    
    return  level, maze_size, cell_size, timeLeft, spawn_interval






spawnZombies(maze_size, zombie_speed)

generateCoins(random.randint(5,10))





pygame.init()
pygame.font.init()
gameFont=pygame.font.SysFont('Comic Sans MS', 30)

surface=pygame.display.set_mode((WIDTH,HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # semi-transparent when game is paused
while not gameOver:
    justReset=False
    
    for event in GAME_EVENTS.get():
        
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start=GAME_TIME.get_ticks()//1000
                choice=pause()
                end=GAME_TIME.get_ticks()//1000
                pause_duration=end-start
                start_time+=pause_duration
                if choice == "save and leave game":
                    Manager.logOff(score,levelStartScore, level, maze_size, True)
                    exitGame()
                elif choice == "leave game":
                    Manager.logOff(score,levelStartScore, level, maze_size, False)
                    exitGame()
                    
                
           
            if event.key==pygame.K_ESCAPE:
                
                Manager.logOff(score,levelStartScore, level, maze_size, False, True)
                exitGame()

            if event.key==pygame.K_UP and player.moveAllowed(player.curr_cell,'top'):

                if maze_grid[player.curr_cell.top[0]][player.curr_cell.top[1]].coin:
                    score+=1
                                                      
                player.move('top')
                
                
            if event.key==pygame.K_RIGHT and player.moveAllowed(player.curr_cell,'right'):
                if maze_grid[player.curr_cell.right[0]][player.curr_cell.right[1]].coin:
                    score+=1
                
                player.move('right')
                
             

            if event.key==pygame.K_DOWN and player.moveAllowed(player.curr_cell,'bottom'):
                if maze_grid[player.curr_cell.bottom[0]][player.curr_cell.bottom[1]].coin:
                    score+=1
            
                player.move('bottom')
               
             

            if event.key==pygame.K_LEFT and player.moveAllowed(player.curr_cell,'left'):
                if maze_grid[player.curr_cell.left[0]][player.curr_cell.left[1]].coin:
                    score+=1
               
                player.move('left')
                
               
                
        



                
        if event.type==GAME_GLOBALS.QUIT:
            Manager.logOff(score,levelStartScore, level, maze_size, False, True)
           
            exitGame()

        
                               

    
  
    pygame.display.set_caption(f"Score: {score}")
   



    
    
    
    draw_maze(maze_size)
    drawCoins()
    player.draw()
    
    
    
        
    
    
    



    
        
                  

    pathfinder_queue={}
    for zombie in zombies:
        
        
        zombie.draw()
        pathfinder_queue[zombie]=zombie.setHeuristic()

 
    
            
        
                      
                      
      
        
        if zombie.bitPlayer() or timeLeft==0:
            #call endScreen
            
     
            gameOver=endScreen()
            tmp=maze_grid
            if not gameOver: # if plays again
                updateDB(score,levelStartScore, level, maze_size, False) #checks for new highscore
                level, maze_size, cell_size, timeLeft, spawn_interval=reset() #resets variables
                
                maze_grid.clear()
                create_grid(cell_size)
               
                generate_maze()
                player=Player(0,maze_size//2)
                zombies.clear()
                generateCoins(level)
                
                score=0
                justReset=True
                exit_cell=maze_grid[maze_size//2][maze_size//2]
                pathfinder_queue.clear()
                zombie_speed=0.1
                spawnZombies(maze_size, zombie_speed)
                
               
              
            else: # if logs out
                Manager.logOff(score,levelStartScore, level, maze_size, False, True)
                exitGame()
                
                
             

    pathfinder_queue=dict(sorted(pathfinder_queue.items(), key=lambda items: items[1]))
    if len(pathfinder_queue)>0:
        queue=[]
        for i in pathfinder_queue.items():
            if not i[0].moving:
                i[0].getPath(player.curr_cell)
                break
                
        
    for zombie in zombies:
        zombie.move(zombie.getDir())
            
        
    

        
            
        
   

    timeLeft,colour=countDown(timeLeft,start_time)
    
    if justReset:
        timeLeft=120
        start_time=GAME_TIME.get_ticks()//1000
        
    

    if player.levelComplete():
        level+=1
        levelStartScore=score
        maze_size,cell_size=nextLevel(cell_size)
       
        
        exit_cell=maze_grid[maze_size//2][maze_size//2]
        timeLeft=120
        start_time=GAME_TIME.get_ticks()//1000
        player=Player(0,maze_size//2)
        zombies.clear()
        
        
        
        
        generateCoins(random.randint(5,10))
        
        if zombie_speed<=0.5: # this stops zombies going through walls
            zombie_speed=1/((1/zombie.speed)-1)
            
        spawnZombies(maze_size, zombie_speed)
        if spawn_interval>5:
            spawn_interval-=5
       
      
        

    #spawns zombies
            
    if GAME_TIME.get_ticks()/1000 - lastSpawn >= spawn_interval:
        
      
        spawnZombies(maze_size, zombie_speed)
        lastSpawn=GAME_TIME.get_ticks()/1000

      
    if GAME_TIME.get_ticks()/1000 - lastCoinFrame >=0.004: #each loop takes approximately 0.004 seconds
        
        
        coinPhase=(coinPhase+1)% 8
        lastCoinFrame=GAME_TIME.get_ticks()/1000
   
    #visual countdown effect
    pygame.draw.arc(surface, colour, (520,20,50,50),(2*pi)*((GAME_TIME.get_ticks()/1000-start_time)/120),0,5)
    
    pygame.display.update()







        

        
    
