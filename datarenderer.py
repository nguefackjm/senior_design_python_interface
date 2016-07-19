# Joe Linton
# DataRenderer

import pygame
import sys
import serial
import threading
import StringIO
import json
import math
import time


class TemperatureWidget():
    '''Temp
    '''
    def __init__(self, loc=(0,0), targetloc=None, temp=0.0, name='node'):
        self.loc = loc
        self.targetloc = targetloc
        self.data = temp
        self.name = name
        self.showntemp = self.data
        self.lasttemp = self.data
        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.image = self.font.render("%s:%0.1f C" % (self.name, float(self.showntemp)), True, (0, 0, 0), (255, 255, 255))
        
    def on_render(self, screen):
        if self.showntemp != self.lasttemp:
            self.image = self.font.render("%s:%0.1f C" % (self.name, float(self.showntemp)), True, (0, 0, 0), (255, 255, 255)) 
            self.lasttemp = self.data


        rect = self.image.get_rect()
        rect = rect.move(self.loc)
        screen.blit(self.image, rect)
        
        rect = rect.inflate(4, 4)
        coords = [(rect.left, rect.top),
                  (rect.right, rect.top),
                  (rect.right, rect.bottom),
                  (rect.left, rect.bottom)]
        pygame.draw.aalines(screen, (0, 0, 0), True, coords)

        if self.targetloc:
            distfunc = lambda x, y: math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
            dist = 0
            for i in coords:
                testdist = distfunc(i, self.targetloc)
                if testdist < dist or dist ==0:
                    curcoord = i
                    dist = testdist
            pygame.draw.aaline(screen, (0, 0, 0), curcoord, self.targetloc)

    
    def on_update(self, dt):
        self.showntemp -= (self.showntemp - self.data) * (dt/1000.0)



class PressureWidget():
    '''Pres
    '''
    def __init__(self, loc=(0,0), targetloc=None, pres=0.0, name='node'):
        self.loc = loc
        self.targetloc = targetloc
        self.data = pres
        self.name = name
        self.shownpres = self.data
        self.lastpres = self.data
        self.font = pygame.font.SysFont("Courier", 36, bold=True)
        if self.data > 0:
            self.image = self.font.render("P", True, (0, 0, 0), (19, 166, 50))
        else:
            self.image = self.font.render("P", True, (0, 0, 0), (255, 255, 255))
        
    def on_render(self, screen):
        if self.shownpres != self.lastpres:
            if self.data > 0:
                self.image = self.font.render("P", True, (0, 0, 0), (19, 166, 50))
            else:
                self.image = self.font.render("P", True, (0, 0, 0), (255, 255, 255))
            self.lastpres = self.data  

        rect = self.image.get_rect()
        rect = rect.move(self.loc)
        screen.blit(self.image, rect)
        
        rect = rect.inflate(4, 4)
        coords = [(rect.left, rect.top),
                  (rect.right, rect.top),
                  (rect.right, rect.bottom),
                  (rect.left, rect.bottom)]
        pygame.draw.aalines(screen, (0, 0, 0), True, coords)

        if self.targetloc:
            distfunc = lambda x, y: math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
            dist = 0
            for i in coords:
                testdist = distfunc(i, self.targetloc)
                if testdist < dist or dist ==0:
                    curcoord = i
                    dist = testdist
            pygame.draw.aaline(screen, (0, 0, 0), curcoord, self.targetloc)

    
    def on_update(self, dt):
        self.shownpres -= (self.shownpres - self.data) * (dt/1000.0)

class LightWidget():
    '''light
    '''
    def __init__(self, loc=(0,0), targetloc=None, light=0.0, name='node'):
        self.loc = loc
        self.targetloc = targetloc
        self.data = light
        self.name = name
        self.shownlight = self.data
        self.lastlight = self.data
        self.font = pygame.font.SysFont("Courier", 36, bold=True)
        if self.data > 0:
            self.image = self.font.render("L", True, (0, 0, 0), (255, 205, 42))
        else:
            self.image = self.font.render("L", True, (0, 0, 0), (180, 180, 180))
        
    def on_render(self, screen):
        if self.shownlight != self.lastlight:
            if self.data > 0:
                self.image = self.font.render("L", True, (0, 0, 0), (255, 205, 42))
            else:
                self.image = self.font.render("L", True, (0, 0, 0), (180, 180, 180))
            self.lastlight = self.data


        rect = self.image.get_rect()
        rect = rect.move(self.loc)
        screen.blit(self.image, rect)
        
        rect = rect.inflate(4, 4)
        coords = [(rect.left, rect.top),
                  (rect.right, rect.top),
                  (rect.right, rect.bottom),
                  (rect.left, rect.bottom)]
        pygame.draw.aalines(screen, (0, 0, 0), True, coords)

        if self.targetloc:
            distfunc = lambda x, y: math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
            dist = 0
            for i in coords:
                testdist = distfunc(i, self.targetloc)
                if testdist < dist or dist ==0:
                    curcoord = i
                    dist = testdist
            pygame.draw.aaline(screen, (0, 0, 0), curcoord, self.targetloc)

    
    def on_update(self, dt):
        self.shownlight -= (self.shownlight - self.data) * (dt/1000.0)


class DataRenderer():
    def __init__(self, bgimage):
        pygame.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF

        self.screen = pygame.display.set_mode((640,480), flags)
        self.bgimage = pygame.image.load(bgimage).convert_alpha()
        rect = self.bgimage.get_rect()
        self.screen = pygame.display.set_mode((rect.width, rect.height), flags)

        self.bgimage = pygame.image.load(bgimage).convert_alpha()
        self.clock = pygame.time.Clock()
        self.quit = False
        self.renderables = {}
        self.datafile = serial.Serial((sys.argv[2]), (sys.argv[3]))
        
        self.datahandlerthread = threading.Thread(name="DataHandler_WorkerThread", target=self.data_handler)
        self.datahandlerthread.start() 

    def data_handler(self):
        while not self.quit:
            data = self.datafile.readline()
            print data
            try:
                jsonval = json.loads(data)
                event = pygame.event.Event(pygame.USEREVENT, {"Data": jsonval})
                pygame.event.post(event)
            except ValueError:
                pass

            
           
    def mainloop(self):
        while not self.quit:
            dt = self.clock.tick(60)
            self.on_update(dt)
            self.on_render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit = True
                if event.type == pygame.USEREVENT:
                    for i in event.Data.keys():
                        if i in self.renderables.keys():                              
                            self.renderables[i].data = event.Data[i]
        pygame.quit()
        sys.exit()

    def on_render(self, screen):
        rect = self.bgimage.get_rect()
        self.screen.blit(self.bgimage, rect)

        for name in self.renderables:
            self.renderables[name].on_render(screen)

        pygame.display.flip()

    def on_update(self, dt):
        for name in self.renderables:
            self.renderables[name].on_update(dt)

    def add_widget(self, widget, mapname):
        self.renderables[mapname] = widget

if len(sys.argv) < 2:
    raise ValueError('Requires a configuration file (see defaultconfig.txt)')

try:
    with open(sys.argv[1]) as file:
        config = json.load(file) 
    dr = DataRenderer(config["BackgroundImage"])

    for item in config["Widgets"]:
        if item["Type"] == 'Temperature':
            dr.add_widget(TemperatureWidget(tuple(item["Params"]["Location"]), tuple(item["Params"]["TargetLocation"]), name=item["DataMapName"]), item["DataMapName"])
        if item["Type"] == 'Pressure':
            dr.add_widget(PressureWidget(tuple(item["Params"]["Location"]), tuple(item["Params"]["TargetLocation"]), name=item["DataMapName"]), item["DataMapName"])
        if item["Type"] == 'Light':
            dr.add_widget(LightWidget(tuple(item["Params"]["Location"]), tuple(item["Params"]["TargetLocation"]), name=item["DataMapName"]), item["DataMapName"])
            
    dr.mainloop()
except KeyboardInterrupt as e:
    pygame.quit()
    dr.quit = True
