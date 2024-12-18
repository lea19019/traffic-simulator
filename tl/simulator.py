import random
import time
import threading
import pygame
import sys
from pathlib import Path

current_dir = Path(__file__).parent
images_dir = current_dir / 'images'

# Default values of signal timers
defaultGreen = {0:35, 1:5}  # Modified for 2 signals
defaultRed = 25  # Reduced since we only have 2 signals now
defaultYellow = 5

signals = []
noOfSignals = 2  # Changed from 4 to 2
currentGreen = 0   # Indicates which signal is green currently
nextGreen = (currentGreen+1)%noOfSignals    # Indicates which signal will turn green next
currentYellow = 0   # Indicates whether yellow signal is on or off 

speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5}

# Coordinates of vehicles' start
x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}    
y = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 
            'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 3:'truck', 2:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# Modified coordinates for 2 signals instead of 4
signalCoods = [(530,230), (810,570)]  # Only 2 signals now
signalTimerCoods = [(530,210), (810,550)]

stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

stoppingGap = 15    # stopping gap
movingGap = 15   # moving gap

pygame.init()
simulation = pygame.sprite.Group()


class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        # path = "tl/images/" + direction + "/" + vehicleClass + ".png"
        path = current_dir / "images" / direction / f"{vehicleClass}.png"
        self.image = pygame.image.load(path)

        if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
            if(direction=='right'):
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().width - stoppingGap
            elif(direction=='left'):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().width + stoppingGap
            elif(direction=='down'):
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().height - stoppingGap
            elif(direction=='up'):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]
            
        if(direction=='right'):
            temp = self.image.get_rect().width + stoppingGap    
            x[direction][lane] -= temp
        elif(direction=='left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif(direction=='down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif(direction=='up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        # Modified to check appropriate signal for each direction
        canMove = False
        if self.direction in ['right', 'left']:  # East-West signal
            canMove = currentGreen == 0 and currentYellow == 0
        else:  # North-South signal
            canMove = currentGreen == 1 and currentYellow == 0

        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):
                self.crossed = 1
            if((self.x+self.image.get_rect().width<=self.stop or self.crossed == 1 or canMove) and 
               (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):
                self.x += self.speed
        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
            if((self.y+self.image.get_rect().height<=self.stop or self.crossed == 1 or canMove) and 
               (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):
                self.y += self.speed
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<stopLines[self.direction]):
                self.crossed = 1
            if((self.x>=self.stop or self.crossed == 1 or canMove) and 
               (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):
                self.x -= self.speed
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
            if((self.y>=self.stop or self.crossed == 1 or canMove) and 
               (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):
                self.y -= self.speed

def initialize():
    # Initialize signals with modified timing for 2 signals
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])  # East-West signal
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow, defaultGreen[1])  # North-South signal
    signals.append(ts2)
    repeat()

def repeat():
    global currentGreen, currentYellow, nextGreen
    while(signals[currentGreen].green>0):
        # print(vehicles)
        updateValues()
        time.sleep(1)
    currentYellow = 1
    
    # Reset stop coordinates for the appropriate directions based on current signal
    directions = ['right', 'left'] if currentGreen == 0 else ['up', 'down']
    for direction in directions:
        for i in range(0,3):
            for vehicle in vehicles[direction][i]:
                vehicle.stop = defaultStop[direction]
    
    while(signals[currentGreen].yellow>0):
        updateValues()
        time.sleep(1)
    currentYellow = 0
    
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen
    nextGreen = (currentGreen+1)%noOfSignals
    signals[nextGreen].red = signals[currentGreen].yellow+signals[currentGreen].green
    repeat()

def updateValues(): # This is the function that updates the traffic lights counter
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                signals[i].green-=1
            else:
                signals[i].yellow-=1
        else:
            signals[i].red-=1

def generateVehicles():
    while(True):
        # We are now only generating cars, motorcycles, and buses
        rand = random.randint(1,100)
        if rand <= 75:  # 75% chance (1-75) Car
            vehicle_type = 0
        elif rand <= 90:  # 15% chance (76-90) Bus
            vehicle_type = 1
        else:  # 10% chance (91-100) Motorcycle
            vehicle_type = 2
        lane_number = random.randint(1,2)
        temp = random.randint(0,99)
        direction_number = 0
        dist = [10,50,60,100]
        if(temp<dist[0]):
            direction_number = 0
        elif(temp<dist[1]):
            direction_number = 1
        elif(temp<dist[2]):
            direction_number = 2
        elif(temp<dist[3]):
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(1)


class Main:
    def __init__(self):
        # Initialize colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # Initialize screen
        self.screenWidth = 1400
        self.screenHeight = 800
        self.screenSize = (self.screenWidth, self.screenHeight)
        
        # Initialize pygame and load resources
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("TRAFFIC SIMULATION")

        self.background = pygame.image.load(str(images_dir / 'intersection.png'))
        self.redSignal = pygame.image.load(str(images_dir / 'signals' / 'red.png'))
        self.yellowSignal = pygame.image.load(str(images_dir / 'signals' / 'yellow.png'))
        self.greenSignal = pygame.image.load(str(images_dir / 'signals' / 'green.png'))

        self.font = pygame.font.Font(None, 30)

    def start_simulation(self):
        # Create and start threads
        self.thread1 = threading.Thread(name="initialization", target=initialize)
        self.thread1.daemon = True
        self.thread1.start()

        self.thread2 = threading.Thread(name="generateVehicles", target=generateVehicles)
        self.thread2.daemon = True
        self.thread2.start()

    def run(self):
        # Start the simulation threads
        self.start_simulation()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.blit(self.background,(0,0))
            for i in range(0,noOfSignals):
                if(i==currentGreen):
                    if(currentYellow==1):
                        signals[i].signalText = signals[i].yellow
                        self.screen.blit(self.yellowSignal, signalCoods[i])
                    else:
                        signals[i].signalText = signals[i].green
                        self.screen.blit(self.greenSignal, signalCoods[i])
                else:
                    if(signals[i].red<=10):
                        signals[i].signalText = signals[i].red
                    else:
                        signals[i].signalText = "---"
                    self.screen.blit(self.redSignal, signalCoods[i])
            
            signalTexts = ["",""]  # Modified for 2 signals

            for i in range(0,noOfSignals):
                signalTexts[i] = self.font.render(str(signals[i].signalText), True, self.white, self.black)
                self.screen.blit(signalTexts[i], signalTimerCoods[i])

            for vehicle in simulation:
                self.screen.blit(vehicle.image, [vehicle.x, vehicle.y])
                vehicle.move()
            pygame.display.update()

