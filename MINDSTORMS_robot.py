from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop, Color, Icon, Side
from pybricks.geometry import Matrix
from pybricks.tools import wait
hub = InventorHub()
# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll
from ustruct import unpack


from MindCuber_translation import TiltReset, tilt_counterclockwise, tilt_clockwise
QMARK = Matrix(
    
        [[0, 100, 100, 100, 0],
        [100, 0, 0, 0, 100],
        [0, 0, 100, 100, 0],
        [0, 0, 100, 0, 0],
        [0, 0, 100, 0, 0]]
    
)

ANIM_ONE = Matrix(
    
        [[0, 100, 0, 100, 0],
        [100, 0, 100, 0, 100],
        [0, 100, 0, 100, 0],
        [100, 0, 100, 0, 100],
        [0, 100, 0, 100, 0]]
    
)

ANIM_TWO = Matrix(
    
        [[100, 0, 100, 0, 100],
        [0, 100, 0, 100, 0],
        [100, 0, 100, 0, 100],
        [0, 100, 0, 100, 0],
        [100, 0, 100, 0, 100]]
    
)


right_arm = Motor(Port.C, positive_direction=Direction.CLOCKWISE)
left_arm = Motor(Port.A, positive_direction= Direction.CLOCKWISE)
platform = Motor(Port.E, gears = [20,60], positive_direction = Direction.COUNTERCLOCKWISE)

angle_arm_up = 0
angle_arm_hold = 41
right_arm.control.target_tolerances(50, 2)
left_arm.control.target_tolerances(50, 2)


# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

def reset_angles():
    platform.reset_angle(0)
    #left_arm.run_until_stalled(2000, duty_limit=100)
    #right_arm.run_until_stalled(-2000, duty_limit=100)
    left_arm.dc(50)
    
    wait(500)
    right_arm.dc(-50)
    wait(500)
    left_arm.reset_angle(0)
    right_arm.reset_angle(0)

def setup():
    reset_angles()
    TiltReset([right_arm, left_arm])
    is_robot_positioned = True

def move_arms(angle):
    left_arm.track_target(-angle)
    right_arm.track_target(angle)

def arms_hold_cube():
    move_arms(angle_arm_hold)

def arms_up():
    move_arms(angle_arm_up)

def rotate_platform(angle):
    platform.run_angle(1000, angle)
    
def rotate_platform_clockwise(nr = 1):
    for i in range(nr):
        rotate_platform(90)

def rotate_platform_counterclockwise(nr = 1):
    for i in range(nr):
        rotate_platform(-90)


def rotate_cube_clockwise(nr = 1):
    arms_up()
    rotate_platform_counterclockwise(nr)

def rotate_cube_counterclockwise(nr = 1):
    arms_up()
    rotate_platform_clockwise(nr)

def bottom_layer_counterclockwise(nr = 1): #move nr 4
    arms_hold_cube()
    rotate_platform_clockwise(nr)

def bottom_layer_clockwise(nr = 1): #move nr 5
    arms_hold_cube()
    rotate_platform_counterclockwise(nr)


def top_counterclockwise(nr = 1): #0
    tilt_clockwise(2)
    bottom_layer_counterclockwise(nr)
    tilt_counterclockwise(2)

def top_clockwise(nr = 1): #1
    tilt_clockwise(2)
    bottom_layer_clockwise(nr)
    tilt_counterclockwise(2)


   
def middle_hor_counterclockwise(nr = 1): #2 front view middle horizontal
    bottom_layer_clockwise(nr)
    tilt_clockwise(2)
    
    bottom_layer_counterclockwise(nr)
    tilt_clockwise(2)
    rotate_cube_counterclockwise(nr)

def middle_hor_clockwise(nr = 1): #3 front view middle horizontal
    bottom_layer_counterclockwise(nr)
    tilt_clockwise(2)
    bottom_layer_clockwise(nr)
    tilt_clockwise(2)
    rotate_cube_clockwise(nr)


def back_counterclockwise(nr = 1):#6
    rotate_cube_clockwise()
    tilt_counterclockwise()
    rotate_platform_clockwise(nr)
    tilt_clockwise()
    rotate_cube_counterclockwise()

def back_clockwise(nr = 1): #7
    rotate_cube_clockwise()
    tilt_counterclockwise()
    rotate_platform_counterclockwise(nr)
    tilt_clockwise()
    rotate_cube_counterclockwise()

def front_counterclockwise(nr = 1):#10
    rotate_cube_counterclockwise()
    tilt_counterclockwise()
    rotate_platform_clockwise(nr)
    tilt_clockwise()
    rotate_cube_clockwise()

def front_clockwise(nr = 1):#11
    rotate_cube_counterclockwise()
    tilt_counterclockwise()
    rotate_platform_counterclockwise(nr)
    tilt_clockwise()
    rotate_cube_clockwise()

def left_clockwise(nr = 1): #13 left downward
    tilt_counterclockwise()
    rotate_platform_counterclockwise(nr)
    tilt_clockwise()

def left_counterclockwise(nr = 1): #12 left up
    tilt_counterclockwise()
    rotate_platform_clockwise(nr)
    tilt_clockwise()

#TODO 8,9, 14 and 15 use other moves defined above, hence why they are out of order
#TODO
def middle_counterclockwise(nr = 1): # 8 top view middle layer
    front_clockwise(nr)
    back_counterclockwise(nr)
    tilt_counterclockwise(nr)
def middle_clockwise(nr = 1): #9 top view middle layer
    front_counterclockwise(nr)
    back_clockwise(nr)
    tilt_clockwise(nr)


def right_counterclockwise(nr = 1): #16 downward
    tilt_clockwise()
    rotate_platform_clockwise(nr)
    tilt_counterclockwise()

def right_clockwise(nr = 1): #17 upward
    tilt_clockwise()
    rotate_platform_counterclockwise(nr)
    tilt_counterclockwise()


def middle_vert_clockwise(nr = 1):#14 down
    left_counterclockwise(nr)
    right_clockwise(nr)
    rotate_cube_clockwise()
    tilt_clockwise(nr)
    rotate_cube_counterclockwise()

def middle_vert_counterclockwise(nr = 1):#15 up
    left_clockwise(nr)
    right_counterclockwise(nr)
    rotate_cube_clockwise()
    tilt_counterclockwise(nr)
    rotate_cube_counterclockwise()

def tilt_backward(nr = 1):#18 = X
    rotate_cube_clockwise()
    tilt_counterclockwise(nr)
    rotate_cube_counterclockwise()

def tilt_forward(nr = 1):#19 = Xi
    rotate_cube_clockwise()
    tilt_clockwise(nr)
    rotate_cube_counterclockwise()


#MAIN
hub.display.orientation(Side.RIGHT)
brightness = list(range(0, 100, 4)) + list(range(100, 0, -4))
is_robot_positioned = False
setup()
while not is_robot_positioned:  #do setup   
        #hub.speaker.beep()
        is_robot_positioned = True
        hub.light.blink(Color.GREEN, [500, 500])
        hub.display.icon(Icon.TRUE)
        stdout.buffer.write(b"pos")
        wait(2000)
        hub.light.off() 
        hub.display.animate([Icon.SQUARE * i / 100 for i in brightness], 50)

while True:
    hub.light.blink(Color.MAGENTA, [500, 500])
    # Optional: Check available input.
    while not keyboard.poll(0):
        # Optional: Do something here.
        wait(10)

    # Read three bytes.
    cmd = stdin.buffer.read(3)
    print(f"command received: {cmd}")
    ba = bytearray(cmd)
    decoded = unpack("sss", cmd)
    move = decoded[1] + decoded[2]
    nr_of_times_bs = decoded[0]
    nr_of_times = None
    if  nr_of_times_bs == b'1':
        nr_of_times = 1
    elif nr_of_times_bs == b'2':
        nr_of_times = 2
    
    
    print(f"move= {move} nr= {nr_of_times}")

    # Decide what to do based on the command.
    #turns out match case isn't in micropython,  so, enjoy

    if cmd == b"0w8":
        hub.display.animate([QMARK * i / 100 for i in brightness], 50)
    elif cmd == b"don":
        stdout.buffer.write(b"DON")
        hub.display.animate([ANIM_ONE, ANIM_TWO], 150)
        hub.light.animate([Color(h=i * 8) for i in range(45)], interval=40)

    elif move == b'00':
        top_counterclockwise(nr_of_times)
    elif move == b"01":
        top_clockwise(nr_of_times)
    elif move == b"02":
        middle_hor_counterclockwise(nr_of_times)
    elif move == b"03":
        middle_hor_clockwise(nr_of_times)
    elif move == b'04':
        bottom_layer_counterclockwise(nr_of_times)
    elif move == b"05":
        bottom_layer_clockwise(nr_of_times)
    elif move == b"06":
        back_counterclockwise(nr_of_times)
    elif move == b"07":
        back_clockwise(nr_of_times)
    elif move == b"08":
        middle_counterclockwise(nr_of_times)
    elif move == b"09":
        middle_clockwise(nr_of_times)
    elif move == b"10":
        front_counterclockwise(nr_of_times)
    elif move == b"11":
        front_clockwise(nr_of_times)
    elif move == b"12":
        left_counterclockwise(nr_of_times)
    elif move == b"13":
        left_clockwise(nr_of_times)
    elif move == b"14":
        middle_vert_clockwise(nr_of_times)
    elif move == b"15":
        middle_vert_counterclockwise(nr_of_times)
    elif move == b"16":
        right_counterclockwise(nr_of_times)
    elif move == b"17":
        right_clockwise(nr_of_times)

    elif move == b"18":
        tilt_backward(nr_of_times) #equates to standard notation X
    elif move == b"19":
        tilt_forward(nr_of_times) #standard notation Xi
    elif move == b"20":
        rotate_cube_counterclockwise(nr_of_times) #Y
    elif move == b"21":
        rotate_cube_clockwise(nr_of_times) #Yi
    elif move == b"22": #Z
        tilt_clockwise(nr_of_times)
    elif move == b"23": #Zi
        tilt_counterclockwise(nr_of_times)

    # Send a response.
    stdout.buffer.write(b"oki")