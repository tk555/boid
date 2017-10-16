from turtle import Turtle, Screen
import turtle
import random
import math

class TurtleObject:
    def __init__(self, position, color, speed):
        self.t = Turtle(shape='classic', visible=False)
        self.t.fillcolor(color)
        self.t.speed(speed)
        self.t.penup()
        self.t.goto(position)
        self.t.pendown()
        self.t.showturtle()
        self.toward_t=self.t

    def set_toward_turtle(self, toward_t):
        self.toward_t = toward_t

    def get_turtle(self):
        return self.t

    def on_top_of(self, n):
        other = n.get_turtle()
        return abs(self.t.xcor() - other.xcor()) < 5 and abs(self.t.ycor() - other.ycor()) < 5

    def move_towards(self):
        self.t.setheading(self.t.towards(self.toward_t.get_turtle())+90)
        self.t.pensize((math.pow(self.t.xcor(),2)+math.pow(self.t.ycor(),2))/10000)
        if (math.floor(((self.t.xcor()+150)/300))- math.floor((self.t.ycor()+150)/300))%5 ==0:
            self.t.color("#C2E812")
        elif (math.floor(((self.t.xcor()+150)/300))- math.floor((self.t.ycor()+150)/300))%5  ==1:
            self.t.color("#91F5AD")
        elif (math.floor(((self.t.xcor()+150)/300))- math.floor((self.t.ycor()+150)/300))%5  ==2:
            self.t.color("#8B9EB7")
        elif (math.floor(((self.t.xcor()+150)/300))- math.floor((self.t.ycor()+150)/300))%5   ==3:
            self.t.color("#745296")
        elif (math.floor(((self.t.xcor()+150)/300))- math.floor((self.t.ycor()+150)/300))%5   ==4:
            self.t.color("#632A50")
        self.t.forward(10)
        self.t.getscreen().ontimer(self.move_towards, 500)

def main():
    turtle_list=[]
    width=600
    height=500
    n=10
    for i in range(n):
        print(i == n-1)
        turtle_list.append(TurtleObject(((random.random()-0.5)*width*2, (random.random()-0.5)*height*2), (random.random(),random.random(),random.random()), 10))
    for i in range(n):
        if i == n-1:
            turtle_list[i].set_toward_turtle(turtle_list[0])
        else:
            turtle_list[i].set_toward_turtle(turtle_list[i+1])
    screen = Screen()
    for i in range(n):
            screen.ontimer(turtle_list[i].move_towards, 500)
    turtle.done()


if __name__ == "__main__":
    main()
