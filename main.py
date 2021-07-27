import math,pygame,sys

# initialisation pygame ------------------------$
pygame.init()
width,height=300,419
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("projet")
clock=pygame.time.Clock()
fps=150

# classes --------------------------------------$
class Mon_im():
    def __init__(self):
        self.pos=(0,0)
        self.pos_C=(0,0)
        self.height=height-200
        self.width=width
        self.image=pygame.image.load("images/Mandelset.png")
        self.image=pygame.transform.scale(self.image,(self.width,self.height))

        self.bord_sup_height=409
        self.bord_inf_height=213
        self.bord_sup_width=299
        self.bord_inf_width=3
        self.inside=(False,False)

        self.plan_VU=int(abs(self.bord_inf_height-self.bord_sup_height)/2)
        self.plan_center=(200,311)
        self.Cdeb=(0,0)

        self.C=(0,0)
    
    def draw(self):
        mouse_pos=pygame.mouse.get_pos()
        screen.blit(self.image,self.pos)
        if self.inside == (True,True):
            pygame.draw.line(screen,(255,0,0),(mouse_pos[0],self.bord_inf_height),(mouse_pos[0],self.bord_sup_height),1)
            pygame.draw.line(screen,(255,0,0),(self.bord_inf_width,mouse_pos[1]),(self.bord_sup_width,mouse_pos[1]),1)
    
    def update(self):
        mouse_pos=pygame.mouse.get_pos()
        if mouse_pos[1] <= self.bord_sup_height and mouse_pos[1] >= self.bord_inf_height:
            self.inside=(self.inside[0],True)
        else:
            self.inside=(self.inside[0],False)

        if mouse_pos[0] <= self.bord_sup_width and mouse_pos[0] >= self.bord_inf_width:
            self.inside=(True,self.inside[1])
        else:
            self.inside=(False,self.inside[1])
        
        if self.inside == (True,True):
            self.Cdeb=mouse_pos
            self.C=(float("%.2f"%((self.Cdeb[0]-self.plan_center[0])/self.plan_VU)),-float("%.2f"%((self.Cdeb[1]-self.plan_center[1])/self.plan_VU)))

class Image_1():
    def __init__(self):
        self.pos=(200,0)
        self.image=pygame.image.load("images/julia_exp.png")
        
    def draw(self):
        screen.blit(self.image,self.pos)

class Aff_C():
    def __init__(self):
        self.pos=(200,100)
        self.color=(0,0,0)
        self.image=pygame.image.load("images/C_coord.png")
        self.font=pygame.font.Font(None,25)
        self.text=('','')
    
    def draw(self):
        screen.blit(self.image,self.pos)
        self.surface0=self.font.render(self.text[0],True,self.color)
        self.surface1=self.font.render(self.text[1],True,self.color)
        screen.blit(self.surface0,(246,125))
        screen.blit(self.surface1,(246,155))

class Calcul():
    def __init__(self):
        self.C=(0,0)
        self.P=self.C
    
    def update(self):
        if self.C != self.P:
            self.P=self.C
            self.var_point(1,1)
    
    def var_point(self,sign1,sign2):
        for i in range(-100,101,1):
            for j in range(-100,101,1):
                point=((i*1.5*sign1)/100,(j*1.5*sign2)/100)
                self.check_point(point,i+100,-j+100)
    
    def check_point(self,point,i,j):
        U=point
        p=40
        for k in range(0,p,1):
            U=mult(U,U)
            U=add(U,self.C)
            if math.sqrt((U[0])**2+(U[1])**2) > 4:
                pygame.draw.rect(screen,(0,int(255*(min(1,k/(p/3)))),0),(i,j,1,1))
                break
            if k == (p-1):
                pygame.draw.rect(screen,(0,0,0),(i,j,1,1))
            
# fonctions ------------------------------------$
def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

def mult(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])

# setup ----------------------------------------$
mon=Mon_im()
mon.pos=(0,200)
im1=Image_1()
affc=Aff_C()
cal=Calcul()


# main loop ------------------------------------$
while 1:
    # logic ------------------------------------$
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if mon.inside == (True,True):
                    cal.update()

    mon.update()
    affc.text=(str("%.2f"%mon.C[0]),str("%.2f"%mon.C[1]))
    cal.C=mon.C
    
    # draw -------------------------------------$
    mon.draw()
    im1.draw()
    affc.draw()

    # update screen ----------------------------$
    pygame.display.flip()
    clock.tick(fps)