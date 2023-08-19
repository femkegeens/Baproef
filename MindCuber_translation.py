#code from David Gilday's MindCuber-RI robot, file MindCuber-RI-v1p0
#downloadable from http://mindcuber.com/mindcuberri/mindcuberri.html

#adaptations made to use equivalent functions from the PyBricks library

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.geometry import Matrix
hub = InventorHub()

motor_scan = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
color_scanner = ColorSensor(Port.F)


right_arm = Motor(Port.C, positive_direction=Direction.CLOCKWISE)
left_arm = Motor(Port.A, positive_direction= Direction.CLOCKWISE)
platform = Motor(Port.E, gears = [20,60], positive_direction = Direction.COUNTERCLOCKWISE)
motors = [right_arm, left_arm]

def run_wt(mot, pos, off): #wait until position is reached. positive offset
    while abs(mot.angle()-pos) > off: #
        wait(1)
 
def run_wt_up(mot, pos):#wait until position is reached. Moving 'up' in angle, so wait while current position is smaller than desired.
    while mot.angle() < pos:
        wait(1)

def run_wt_dn(mot, pos):#wait until position is reached. Moving 'down' in angle, so wait while current position is larger than desired.
    while mot.angle() > pos:
        wait(1)

def run_wt_dir(mot, pos, off): #wait until position is reached. 
    if off < 0:
        while mot.angle() < pos:
            wait(1)
    else:
        while mot.angle() > pos:
            wait(1)

def TiltReset(motors_array):
    global motors, up 
    motors = motors_array
    mot0 = motors[0]
    mot1 = motors[1]
    mot0.dc(-40)
    mot1.dc(40)
    pos1 = [mot0.angle(), mot1.angle()]
    pos0 = [pos1[0]+100, pos1[1]-100]
    while pos1[0] < pos0[0] or pos1[1] > pos0[1]:
        wait(200)
        pos0 = pos1
        pos1 = [mot0.angle(), mot1.angle()]
    bwd0 = mot0.angle()
    bwd1 = mot1.angle()
    #added up
    up = [bwd0, bwd1]
    mot0.dc(40)
    mot1.dc(-40)
    pos1 = [mot0.angle(), mot1.angle()]
    pos0 = [pos1[0]-100, pos1[1]+100]
    while pos1[0] > pos0[0] or pos1[1] < pos0[1]:
        wait(200)
        pos0 = pos1
        pos1 = [mot0.angle(), mot1.angle()]
    fwd0  = mot0.angle() -3
    fwd1 = mot1.angle() + 3
    global motor_tilt_fwd, motor_tilt_hld, motor_tilt_bwd
    motor_tilt_fwd = [fwd0, fwd1]
    motor_tilt_hld = [fwd0-32, fwd1+32] #adapted
    motor_tilt_bwd = [fwd0-67, fwd1+67]
    if fwd0-bwd0 < 60 or bwd1-fwd1 < 60:
        fatal_error()
    #added instead of TiltAway()
    TiltUp()
    print("done resetting")


#added
def TiltUp():
    motors[0].run_target(100, up[0], wait = False)#run_nw(motor_tilt[0], motor_tilt_bwd[0], 100) 
    motors[1].run_target(100, up[1], wait = False)#run_nw(motor_tilt[1], motor_tilt_bwd[1], 100)  

    run_wt_dn(motors[0], up[0]+3)
    run_wt_up(motors[1], up[1]-3)
    
def TiltAway():
    motors[0].run_target(100, motor_tilt_bwd[0], wait = False)#run_nw(motor_tilt[0], motor_tilt_bwd[0], 100) 
    motors[1].run_target(100, motor_tilt_bwd[1], wait = False)#run_nw(motor_tilt[1], motor_tilt_bwd[1], 100)  
    
    run_wt_dn(motors[0], motor_tilt_hld[0]-6)
    run_wt_up(motors[1], motor_tilt_hld[1]+6)

def TiltHold():
    motors[0].track_target(motor_tilt_hld[0])#run_nw(motor_tilt[0], motor_tilt_hld[0], 100)
    motors[1].track_target(motor_tilt_hld[1])#run_nw(motor_tilt[1], motor_tilt_hld[1], 100)

def TiltTilt(mid0):
    mid1 = 1 - mid0
    
    pwr  = 100
    pwra = -40
    bwd  = -20
    fwd  = -10
    hld  = 5

    if mid0 == 1:
        pwr  = -pwr
        pwra = -pwra
        bwd  = -bwd
        fwd  = -fwd
        hld  = -hld
    motors[mid1].run_target(1000, motor_tilt_bwd[mid1], wait = False)
    if abs(motors[mid0].angle() - motor_tilt_hld[mid0]) > 10:
        motors[mid0].run_target(1000, motor_tilt_hld[mid0])
    run_wt_dir(motors[mid1], motor_tilt_bwd[mid1] + bwd, bwd)
    motors[mid0].dc(pwr) #pwr 100
    run_wt_dir(motors[mid0], motor_tilt_fwd[mid0]+fwd, fwd)
    wait(100)
    motors[mid1].dc(-pwr) #pwr 40
    wait(10)
    motors[mid0].dc(pwra) #this pushes it down
    run_wt_dir(motors[mid1], motor_tilt_hld[mid1]+hld, hld) 
    motors[mid0].run_target(1000, motor_tilt_hld[mid0])#-10)
    motors[mid1].run_target(1000, motor_tilt_hld[mid1])#+10)

def tilt_counterclockwise(nr = 1):

    for i in range(nr):
        TiltTilt(0)
def tilt_clockwise(nr = 1):
    for i in range(nr):
        TiltTilt(1)


scan_speed = 75
scan_pwr   = 80

scan_mid   = 135
scan_edg   = 105
scan_crn   = 90
scan_awy   = 40
scan_rst   = -140

turn_mul   = 60
turn_div   = 20
turn_3     = int(turn_mul* 3/turn_div)
turn_45    = int(turn_mul*45/turn_div)
turn_90    = int(turn_mul*90/turn_div)

def ScanReset():
    #ColorOff()
    motor_scan.dc(55)
    pos1 = motor_scan.angle()
    pos0 = pos1-100
    while pos1 > pos0:
        wait(100)
        pos0 = pos1
        pos1 = motor_scan.angle()
    global motor_scan_base
    motor_scan_base = motor_scan.angle()+scan_rst
    motor_scan.run_target(1000, motor_scan_base) #scan_pwr
    motor_scan.brake()




Color.BLUE = Color(h=195, s=80, v=36)
Color.RED = Color(h=350, s=90, v=25)
Color.WHITE = Color(h=180, s=13, v=30)

Color.YELLOW = Color(h=70, s=60, v=30)
Color.GREEN = Color(h=120, s=65, v=35)
Color.ORANGE = Color(h=0, s=84, v=55)

my_colors = [Color.BLUE, Color.RED, Color.WHITE, Color.YELLOW, Color.GREEN, Color.ORANGE]
color_scanner.detectable_colors(my_colors)            
motor_turn = platform
def ScanPiece(spos, tpos, f, o, i, back = False):
    global slower
    spos += motor_scan_base
    motor_scan.run_target(1000,spos, wait = False)
    pos = motor_scan.angle()
    #ScanDisp(i)
    if back:
        run_wt_dn(motor_turn, tpos+3)
    else:
        run_wt_up(motor_turn, tpos-3)
    ScanRGB()#(f, o)
    off = motor_scan.angle()-spos
    if pos < spos:
        if off < -5:
            slower += 1
    else:
        if off > 5:
            slower += 1

def ScanRGB():
    hub.speaker.beep(duration = 100)
    color = color_scanner.color()
    hub.light.on(color)
    print(color)
def ScanFace(f, o, tilt = 1, back = False):
    global slower, scan_speed
    global motor_turn_base
    motor_turn_base = 45
    dir = scan_mid
    mid = True
    if f > 0:
        motor_scan.run_target(scan_speed, motor_scan_base+scan_awy, wait=False)#scan_pwr)
        TiltTilt(tilt)#, True)
        dir -= scan_awy
        mid = False
    scanning = True
    
    while scanning:
        # print("FACE "+str(f))
        slower = 0
        if mid:
            motor_scan.run_target(scan_speed, motor_scan_base+scan_mid, wait=False)#scan_pwr)
        TiltAway()
        #ScanDisp(8)
        if dir > 0:
            run_wt_up(motor_scan, motor_scan_base+scan_mid-3)
        else:
            run_wt_dn(motor_scan, motor_scan_base+scan_mid+3)
        
        ScanRGB()#(f, 8)
        #rotate the platform to continue scanning
        if back:
            motor_turn_base -= 90
            platform.run_target(scan_speed, motor_turn_base+45, wait=False)
        else:
            platform.run_target(scan_speed, motor_turn_base+90*4, wait=False)
        
        
        #i think this is the four sides
        for i in range(4):
            ScanPiece(scan_crn, motor_turn_base+45, f, o, i, back)
            if back:
                back = False
                platform.run_target(scan_speed, motor_turn_base+90*4, wait=False)
            motor_turn_base += 90
            ScanPiece(scan_edg, motor_turn_base, f, o+1, i+4)
            o += 2
            if o > 7:
                o = 0
        """
        if slower > 4:
            dir = scan_mid-scan_edg
            mid = True
            scan_speed -= 1
            print("Scan speed "+str(slower)+" "+str(scan_speed))
        scanning = False
    """
    hub.display.off()
    print("scanned")

def SolveCube():
    global tiltd
    #CubeInsert()
    scan = 0
    found = False
    while not found and scan < 3:
       # ColorOn()
        #ms = time.ticks_ms()
        scan += 1
        #tiltd += 1
        ScanFace(0, 2)
        #ScanFace(4, 4, 0)
        #ScanFace(2, 4, 0, True)
        #ScanFace(3, 2, 0, True)
        #ScanFace(5, 6)
        #ScanFace(1, 6)
        #ColorOff()
        #hub.led(0, 0, 0)
        #Show3x3('968776897')
        motor_scan.run_target(scan_pwr, motor_scan_base, wait=False)
        TiltHold()
        #Show(FACE_LEFT)
        #sms = int((time.ticks_ms()-ms)/100)
        #print("SCAN: "+str(int(sms/10))+"."+str(sms%10)+"s")
        t = -1
        for i in range(12):
            # print("TYPE "+str(i))
            #valid = c.determine_colors(i)
            valid = True #TODO
            # c.display()
            if valid:
                t = i
                # print("Valid: "+str(t))
                #valid = c.valid_positions()
                if valid:
                    found = True
                    break
        if not found and scan == 3 and t >= 0:
            #found = c.determine_colors(t)
            # c.display()
            print("Invalid? "+str(t))
    # }
TiltReset(motors)
ScanReset()
SolveCube()