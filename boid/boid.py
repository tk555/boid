import turtle
import math
import time
import random


class Boid:
    MIN_SPEED=5
    MAX_SPEED=15
    TURNABLE_ANGLE=90
    MIN_UNSEEABLE_ANGLE=150
    MAX_UNSEEABLE_ANGLE=210
    SEEABLE_DISTANCE=100
    PERSONAL_DISTANCE=10
    WINDOW_WIDTH=400
    WINDOW_HEIGHT=300

    def __init__(self, x, y, theta, id, boids=[], speed = 10):
        self.t=turtle.Turtle()
        self.t.speed(0)
        self.t.up()
        self.t.goto(x, y)
        self.t.seth(theta)
        self.id=id
        self.speed=speed
        self.boids=boids
        self.t.down()
        self.current_angle=self.t.heading()

    def __str__(self):
        return "Boid<id={}, (x,y)=({},{}), angle={}>".format(self.id, self.t.xcor(), self.t.ycor(),self.t.heading())

    def clip(self,min,max,n):
        if n<min:
            return min
        elif n>max:
            return max
        return n
    def cal_average_angle(self,boids: list) -> float:
        if len(boids)==0:
            return self.t.heading()
        result=0
        for boid in boids:
            result=result+boid.t.heading()-self.t.heading()
        return (result /len(boids))+self.t.heading()

    def cal_average_speed(self, boids: list) -> float:
        if len(boids)==0:
            return self.speed
        result=0
        for boid in boids:
            result=result+boid.speed
        return result/len(boids)

    def cal_average_angle2(self,a,b) -> float:
        result = a+b
        return result /2
    def cal_average_angle3(self,a,b,n,m) -> float:
        result = a*n+b*m
        return result /(n+m)

    def cal_center_of_gravity(self,list):
        if len(list)==0:
            return self.t.pos()
        position = (0, 0)
        for bird in list:
            position = [x+y for (x,y) in zip(position,bird.t.pos())]
        return tuple([x/len(list) for x in position])

    def normalize_pos(self):
        if self.t.xcor() < -self.WINDOW_WIDTH:
            self.t.setx(self.WINDOW_WIDTH * 2 + self.t.xcor())
        elif self.WINDOW_WIDTH < self.t.xcor():
            self.t.setx(-self.WINDOW_WIDTH * 2 + self.t.xcor())
        if self.t.ycor() < -self.WINDOW_HEIGHT:
            self.t.sety(self.WINDOW_HEIGHT * 2 + self.t.ycor())
        elif self.WINDOW_HEIGHT < self.t.ycor():
            self.t.sety(-self.WINDOW_HEIGHT * 2 + self.t.ycor())

    def go_next_pos(self):
        neighbor_birds=[]
        #自分も入ってる
        medium_birds=[]
        too_near_birds=[]
        for other_bird in self.boids:
            if not(self.MIN_UNSEEABLE_ANGLE<(self.t.towards(other_bird.t)-self.t.heading())%360<self.MAX_UNSEEABLE_ANGLE):
                if self.t.distance(other_bird.t)<self.SEEABLE_DISTANCE :
                    neighbor_birds.append(other_bird)
                if self.t.distance(other_bird.t)>self.PERSONAL_DISTANCE and self.t.distance(other_bird.t)<self.SEEABLE_DISTANCE:
                    medium_birds.append(other_bird)
                if self.t.distance(other_bird.t)<self.PERSONAL_DISTANCE:
                    too_near_birds.append(other_bird)

        if len(neighbor_birds)>1:
            self.t.color("red")
        else:
            self.t.color("black")
        #self.t.seth(self.cal_average_angle(neighbor_birds))
        #print("{},{},{},{}".format(len(neighbor_birds),self.cal_average_angle(neighbor_birds),self.t.heading(),self.cal_average_angle2(self.cal_average_angle(neighbor_birds),self.t.heading())))
        angle=self.cal_average_angle(neighbor_birds)
        speed=self.clip(self.MIN_SPEED,self.MAX_SPEED,self.cal_average_speed(neighbor_birds))
        if len(medium_birds)!=0:
            #周囲にいる集団から近すぎる集団を抜いた集団の中心に向かう
            center_of_gravity=self.cal_center_of_gravity(medium_birds)
            angle=self.cal_average_angle3(angle,self.t.towards(center_of_gravity),10,1)
            if self.TURNABLE_ANGLE<(angle-self.t.heading())%360<(360-self.TURNABLE_ANGLE):
                if (angle-self.t.heading())%360<180:
                    angle=30+self.t.heading()
                else:
                    angle=330+self.t.heading()
            speed=self.clip(self.MIN_SPEED,self.MAX_SPEED,self.t.distance(center_of_gravity))
        """
        if len(neighbor_birds)!=1:
            center_of_neighbor=self.cal_center_of_gravity(neighbor_birds)
            if len(too_near_birds)==0:
                position_of_target=center_of_neighbor
            else:
                center_of_near_birds=self.cal_center_of_gravity(too_near_birds)
                position_of_target=tuple([x+y for (x,y) in zip(center_of_neighbor,[x-y for (x,y) in zip(center_of_neighbor,center_of_near_birds)])])
            angle=self.cal_average_angle2(angle,self.t.towards(position_of_target))
            if self.TURNABLE_ANGLE<(angle-self.t.heading())%360<(360-self.TURNABLE_ANGLE):
                if (angle-self.t.heading())%360<180:
                    angle=30+self.t.heading()
                else:
                    angle=330+self.t.heading()
            speed=self.clip(self.MIN_SPEED,self.MAX_SPEED,self.t.distance(position_of_target))
        """
        if len(too_near_birds)>1:
            angle=self.cal_average_angle(too_near_birds)+180
            speed=self.MAX_SPEED*2
        self.t.seth(angle)
        self.current_angle=angle
        self.t.fd(speed)
        self.speed=speed
        self.t.up()
        self.normalize_pos()
        self.t.down()
        self.t.getscreen().ontimer(self.go_next_pos, 5000)

def main():
    screen = turtle.Screen()
    turtle.mode("logo")
    boids=[]
    n=20
    width=400
    height=300
    for i in range(n):
        boid=Boid((random.random()-0.5)*width*2, (random.random()-0.5)*height*2, random.random()*360,i,boids=boids)
        boids.append(boid)
        print(boid)
    for boid in boids:
        screen.ontimer(boid.go_next_pos, 10000)
    turtle.done()


if __name__ == "__main__":
    main()
