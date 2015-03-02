import serial
import re
from math import fabs
import random as python_random

from numpy import *
from scipy import linalg
 #                       PROJECTOR 
 #                           ^
 #                          / \
 #                         /   \
 #
 #                   y
 # (0,0)    |---------------------------------|
 # on right |        1 UL     |      7        |
 # side     |                 |               |
 #         x|  4 LL       2 UR| 6           8 |
 #          |                 |               |
 #          |       3 LR      |      5        |
 #          |---------------------------------| (0,0) on left side 
 #                                              (left as your back is to the projector -- e.g., screen's left)


DEBUG = False
DEBUG_INPUT = 'hitdata'
FILE_OUTPUT = 'coefficients'

BAUD = 9600
#PORT = 6    # PORT = 5 means COM6. FOR WINDOWS
PORT = '/dev/tty.usbmodem411' # FOR MAC
SERIAL_TIMEOUT = .1 # in seconds

# the true positions of all the training points
# here, we use inches
positions = array([[6, 6],
                  [6, 18],
                  [6, 30],
                  [6, 42],
                  [18, 6],
                  [18, 18],
                  [18, 30],
                  [18, 42],
                  [30, 6],
                  [30, 18],
                  [30, 30],
                  [30, 42],
                  [42, 6],
                  [42, 18],
                  [42, 30],
                  [42, 42],
                  [54, 6],
                  [54, 18],
                  [54, 30],
                  [54, 42]])
REPETITIONS = 5

repeated_positions = array([[6, 6], [6, 6], [6, 6], [6, 6], [6, 6], 
                  [6, 18], [6, 18], [6, 18], [6, 18], [6, 18], 
                  [6, 30], [6, 30], [6, 30], [6, 30], [6, 30], 
                  [6, 42], [6, 42], [6, 42], [6, 42], [6, 42], 
                  [18, 6], [18, 6], [18, 6], [18, 6], [18, 6], 
                  [18, 18], [18, 18], [18, 18], [18, 18], [18, 18], 
                  [18, 30], [18, 30], [18, 30], [18, 30], [18, 30], 
                  [18, 42], [18, 42], [18, 42], [18, 42], [18, 42], 
                  [30, 6], [30, 6], [30, 6], [30, 6], [30, 6],
                  [30, 18], [30, 18], [30, 18], [30, 18], [30, 18], 
                  [30, 30], [30, 30], [30, 30], [30, 30], [30, 30], 
                  [30, 42], [30, 42], [30, 42], [30, 42], [30, 42], 
                  [42, 6], [42, 6], [42, 6], [42, 6], [42, 6], 
                  [42, 18], [42, 18], [42, 18], [42, 18], [42, 18], 
                  [42, 30], [42, 30], [42, 30], [42, 30], [42, 30], 
                  [42, 42], [42, 42], [42, 42], [42, 42], [42, 42], 
                  [54, 6], [54, 6], [54, 6], [54, 6], [54, 6], 
                  [54, 18], [54, 18], [54, 18], [54, 18], [54, 18], 
                  [54, 30], [54, 30], [54, 30], [54, 30], [54, 30], 
                  [54, 42], [54, 42], [54, 42], [54, 42], [54, 42]])
                  
x = matrix(repeated_positions[:,0]).transpose()
y = matrix(repeated_positions[:,1]).transpose()

def open_serial(port, baud):
    """ Initializes the Arduino serial connection """
    arduino_serial = serial.Serial(port, baudrate=baud, timeout=SERIAL_TIMEOUT)
    return arduino_serial

def read_hit(arduino_serial):
    """ Gets a hit from the Arduino serial connection """
    
    while True:
        line = arduino_serial.readline()
        
        if line == None or line == "":
            continue
        else:
            return line

def parse_hit(line):
    print(line)
    hit_re = re.match("hit: {(?P<sensor_one>\d+) (?P<sensor_two>\d+) (?P<sensor_three>\d+) (?P<sensor_four>\d+) (?P<side>[lr])}", line)
    if hit_re is None:
        print "none"
        return None
    else:
        hit = {
                "one": int(hit_re.group("sensor_one")),
                "two": int(hit_re.group("sensor_two")),
                "four": int(hit_re.group("sensor_four")),
                "three": int(hit_re.group("sensor_three"))
        }
        print hit
        
        return generate_diffs(hit)
            
            
def generate_diffs(hit):
    """ Takes a hit location and returns diffs like ONE_TWO: upper left to upper right """
    first_sensor = None
    for key in hit.keys():
        if hit[key] == 0:
            first_sensor = key
            break

    diffs = {
             "ONE_TWO" : (hit["one"] - hit["two"]),
             "ONE_THREE" : (hit["one"] - hit["three"]),
             "ONE_FOUR" : (hit["one"] - hit["four"]),
             "TWO_THREE" : (hit["two"] - hit["three"]),
             "TWO_FOUR" : (hit["two"] - hit["four"]),
             "THREE_FOUR" : (hit["three"] - hit["four"]),
             "first_sensor": first_sensor
             }
    return diffs
                
def generate_random_hit():
    """ For DEBUG mode, generates hits without the arduino attached"""

    hits = ["hit: {1404 1268 0 440 r}", "hit: {2328 1240 0 1516 l}", "hit: {1376 1944 1484 0 l}"]
    hit = python_random.choice(hits)
    
    return parse_hit(hit)

def get_hits_from_file(is_right_side):
    filename = DEBUG_INPUT
    if is_right_side:
        filename += "-right.txt"
    else:
        filename += "-left.txt"
    
    reader = open(filename, 'r')
    lines = reader.readlines()
    lines = filter(lambda line: (line != "\n" and line[0] != "#"), lines)
    print lines
    return lines
    
def average_repetitions(repetitions):
    """ Averages all the timing values for the repeated trainings """
    averages = {
         "ONE_TWO" : sum([diff["ONE_TWO"] for diff in repetitions]) / len(repetitions),
         "ONE_THREE" : sum([diff["ONE_THREE"] for diff in repetitions]) / len(repetitions),
         "ONE_FOUR" : sum([diff["ONE_FOUR"] for diff in repetitions]) / len(repetitions),
         "TWO_THREE" : sum([diff["TWO_THREE"] for diff in repetitions]) / len(repetitions),
         "TWO_FOUR" : sum([diff["TWO_FOUR"] for diff in repetitions]) / len(repetitions),
         "THREE_FOUR" : sum([diff["THREE_FOUR"] for diff in repetitions]) / len(repetitions),
         "first_sensor": repetitions[0]['first_sensor']
    }
    return averages
    
def collect_points(arduino_serial, is_right_side):
    training_values = []
    training_hits = None
    
    if DEBUG:
        lines = get_hits_from_file(is_right_side)
    else:
        filename = DEBUG_INPUT
        if is_right_side:
            filename += "-right.txt"
        else:
            filename += "-left.txt"
        training_hits = open(filename, 'w')
    
    for point in range(len(positions)): 
        while(True):
            repetitions = []
            hit_strings = []
            for repetition in range(REPETITIONS):
            	if is_right_side:
            		side = "Right side, "
            	else:
            		side = "Left side, "
                print(side + "drop the ping pong ball at (%d,%d): repetition %d" % (positions[point][0], positions[point][1], repetition+1))
                
                if DEBUG:
                    hit_string = lines.pop(0)
                    diffs = parse_hit(hit_string)
                else:
                    hit_string = read_hit(arduino_serial)
                    diffs = parse_hit(hit_string)
                if diffs is not None:
                    repetitions.append(diffs)
                    hit_strings.append(hit_string)

            if not DEBUG:
                is_OK = prompt_if_OK()
                arduino_serial.flushInput()
            else:
                is_OK = True
                
            if (is_OK):
                for repetition in repetitions:
                    average = average_repetitions([ repetition ])
                    training_values.append(average)
                if not DEBUG:
                    training_hits.write(''.join(hit_strings))
                    training_hits.flush()
                break

    if training_hits is not None:
        training_hits.close()
    return training_values

def prompt_if_OK():
    while(True):
        user_response = raw_input("Were all the tests OK? Press enter if OK, or enter 'r' to redo: ")
        if user_response == 'r':
            return False
        elif user_response == '':
            return True
        else:
            print "Not a valid response. Please press enter or 'r', then enter."

    
def populate_matrices(training_values):
    M1 = []
    M2 = []
    M3 = []
    M4 = []
    
    for average in training_values:
        t12 = average['ONE_TWO']
        t13 = average['ONE_THREE']
        t14 = average['ONE_FOUR']
        t23 = average['TWO_THREE']
        t24 = average['TWO_FOUR']
        t34 = average['THREE_FOUR']
        
        first_ul = int(average['first_sensor'] == 'one')
        first_ur = int(average['first_sensor'] == 'two')
        first_ll = int(average['first_sensor'] == 'four')
        first_lr = int(average['first_sensor'] == 'three')

        # don't need first_lr because the other three 0/1 dummy variables take care of it, when they're all 0, the lin_reg knows this one is 1
        # http://dss.princeton.edu/online_help/analysis/dummy_variables.htm
        M1.append([t12**2, t13**2, t14**2, t12*t13, t12*t14, t13*t14, t12, t13, t14, 1])#, first_ul, first_ur, first_ll, 1])
        M2.append([t12**2, t23**2, t24**2, t12*t23, t12*t24, t23*t24, t12, t23, t24, 1])#first_ul, first_ur, first_ll, 1])
        M3.append([t13**2, t23**2, t34**2, t13*t23, t13*t34, t23*t34, t13, t23, t34, 1])#first_ul, first_ur, first_ll, 1])
        M4.append([t14**2, t24**2, t34**2, t14*t24, t14*t34, t24*t34, t14, t24, t34, 1])#first_ul, first_ur, first_ll, 1])
        
    return [M1, M2, M3, M4]
    
def write_vector(vector, output):
    for num in vector.flat:
        output.write("%.20f\n" % (num))

def train(arduino_serial, is_right_side):        
    training_values = collect_points(arduino_serial, is_right_side)
    [M1, M2, M3, M4] = populate_matrices(training_values)
    
    # find inverses using singular value decomposition
    M1inv = linalg.pinv2(M1)
    M2inv = linalg.pinv2(M2)
    M3inv = linalg.pinv2(M3)
    M4inv = linalg.pinv2(M4)
    
    print M1inv.shape
    print x.shape

    # find coefficients
    xCoeff1 = M1inv * x
    xCoeff2 = M2inv * x
    xCoeff3 = M3inv * x
    xCoeff4 = M4inv * x
    print xCoeff1

    yCoeff1 = M1inv * y
    yCoeff2 = M2inv * y
    yCoeff3 = M3inv * y
    yCoeff4 = M4inv * y
    print yCoeff1
    
    return [xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4]

def write(is_right_side, xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4):
    # File format:
    # X1_1
    # X1_2
    # ...
    # X1_10
    # X2_1
    # ...
    # X2_10
    # ...
    # ...
    # X4_10
    # Y1_1
    # ...
    # ...
    # Y4_10
    
    filename = FILE_OUTPUT
    if is_right_side:
        filename += "-right.txt"
    else:
        filename += "-left.txt"
    
    output = open(filename, 'w')
    write_vector(xCoeff1, output)
    write_vector(xCoeff2, output)
    write_vector(xCoeff3, output)
    write_vector(xCoeff4, output)
    write_vector(yCoeff1, output)
    write_vector(yCoeff2, output)
    write_vector(yCoeff3, output)
    write_vector(yCoeff4, output)    
    output.close()    


def error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4, is_right_side, lines, positions):  
    distances = []
    x_distances = []
    y_distances = []
    for point in range(len(lines)):
        hit_string = lines[point]
        diffs = parse_hit(hit_string)
        average = average_repetitions([diffs])
        [predicted_x, predicted_y] = predict(average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4)
        true_x = positions[point][0]
        true_y = positions[point][1]
        predicted = array( (predicted_x, predicted_y) )
        true = array( ( true_x, true_y) )
        print "Predicted: " + str(predicted)
        print "True: " + str(true)
        distance = linalg.norm(predicted - true)
        print "Distance: " + str(distance)
        distances.append(distance)
        
        x_distances.append( fabs(true_x - predicted_x) )
        y_distances.append( fabs(true_y - predicted_y) )

    print sort(distances)
            
    print "Median distance: " + str(median(distances))
    print "Median X distance: " + str(median(x_distances))
    print "Median Y distance: " + str(median(y_distances))
        
def test(xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4, is_right_side):
    ###############
    #    TEST     #
    ###############
    # test some points
    training_hits = None
    
    if not DEBUG:
        filename = DEBUG_INPUT
        if is_right_side:
            filename += "-right.txt"
        else:
            filename += "-left.txt"
        training_hits = open(filename, 'a')
    
    for i in range(20):
        print "TEST: hit the table somewhere"
        if DEBUG:
            diffs = generate_random_hit()
        else:
            diffs = read_hit(arduino_serial, training_hits)
            
        average = average_repetitions([ diffs ])
        [avgx, avgy] = predict(average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4)

        print str(avgx) + " ," + str(avgy)

    if training_hits is not None:
        training_hits.close()

def predict(average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4):
        t12 = average['ONE_TWO']
        t13 = average['ONE_THREE']
        t14 = average['ONE_FOUR']
        t23 = average['TWO_THREE']
        t24 = average['TWO_FOUR']
        t34 = average['THREE_FOUR']
        first_ul = int(average['first_sensor'] == 'one')
        first_ur = int(average['first_sensor'] == 'two')
        first_ll = int(average['first_sensor'] == 'four')
        first_lr = int(average['first_sensor'] == 'three')        

        Poly1 = matrix([t12**2, t13**2, t14**2, t12*t13, t12*t14, t13*t14, t12, t13, t14, 1])#first_ul, first_ur, first_ll, 1])
        Poly2 = matrix([t12**2, t23**2, t24**2, t12*t23, t12*t24, t23*t24, t12, t23, t24, 1])#first_ul, first_ur, first_ll, 1])
        Poly3 = matrix([t13**2, t23**2, t34**2, t13*t23, t13*t34, t23*t34, t13, t23, t34, 1])#first_ul, first_ur, first_ll, 1])
        Poly4 = matrix([t14**2, t24**2, t34**2, t14*t24, t14*t34, t24*t34, t14, t24, t34, 1])#first_ul, first_ur, first_ll, 1])

        x = zeros(4)
        y = zeros(4)

        print(Poly1.shape)
        print(xCoeff1.shape)
        print xCoeff1
        x[0] = Poly1*xCoeff1   
        x[1] = Poly2*xCoeff2
        x[2] = Poly3*xCoeff3
        x[3] = Poly4*xCoeff4

        y[0] = Poly1*yCoeff1   
        y[1] = Poly2*yCoeff2
        y[2] = Poly3*yCoeff3
        y[3] = Poly4*yCoeff4
        
        avgx = (x[0] + x[1] + x[2] + x[3])/4
        avgy = (y[0] + y[1] + y[2] + y[3])/4
        return [avgx, avgy]
        
    
if __name__ == '__main__':
    if not DEBUG:
        arduino_serial = open_serial(PORT, BAUD)
    else:
        arduino_serial = None
        
    side = None
    while side is None:
        side = raw_input("Calibrate [l]eft side only, [r]ight side only, or [b]oth?: ")
        if side != 'l' and side != 'r' and side != 'b':
            print 'Please enter l, r, or b.'
            side = None
    
    if side == 'l' or side == 'b':
        [xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4] = train(arduino_serial, False)
        write(False, xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4)
        error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4, False, get_hits_from_file(False), repeated_positions)
    if side == 'r' or side == 'b':
        [xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4] = train(arduino_serial, True)
        write(True, xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4)
        error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, yCoeff1, yCoeff2, yCoeff3, yCoeff4, True, get_hits_from_file(True), repeated_positions)

