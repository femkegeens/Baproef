import twophase.solver  as sv
from itertools import chain
import time
import gym
#import gym_rubiks_cube
import numpy as np
import twophase.performance as pf
from gym_rubiks_cube.envs.rubiksCubeEnv import TransformCubeObject
#https://github.com/hkociemba/RubiksCube-TwophaseSolver

""""
import twophase.start_server
from threading import Thread
background_thread = Thread(target=twophase.start_server.start, args=(8080, 20, 2))
background_thread.start()


import twophase.client_gui
"""

def convert_representation(color_vector):

    translated_cube_vect = list(chain(color_vector[0:9], #U 
                        color_vector[18:27], #R
                        color_vector[9:18], #F
                        #string_vector[51:], string_vector[48:51], string_vector[45:48], #D
                        color_vector[51:],
                            color_vector[48:51],
                            color_vector[45:48],
                        color_vector[36:45], #L
                        color_vector[27:36]) ) #B


  #this representation does some funny stuff. It looks at the faces of the cube in the order URFDLB (up, right, front, down, left, back)
  # and assigns the color variables by the middle facelet of each face in that order. Therefore, I create a dictionary
  # that does this. If i simply map 0 (in the Gym representation) to U and so on.
    middle_colors = []
    for index_middle_facelet in range(4, 53, 9): #facelet indices are 4, 13, 22, 31, 40 , 49
        middle_colors.append(translated_cube_vect[index_middle_facelet])
    
    colors_assigning_order = ["U", "R", "F", "D", "L", "B"]

    color_dict =  {middle_colors[i]: colors_assigning_order[i] for i in range(len(middle_colors))}
 
    #modify entire cube vector using dict
    mapped_vector = list(map(color_dict.get, translated_cube_vect))
    #make string from array of strings
    listToStr = ''.join(mapped_vector)
    return listToStr

def nr_of_moves(solution_string):
    total = 0
    split_string = solution_string.split()
    for i in range((len(split_string))-1): #since last el in list is (5f) for example
        head = split_string[i]
        if head.endswith("1"):
            total += 1
        elif head.endswith("2"):
            total += 2
        elif head.endswith("3"):
            total += 3
    return total

#the robot numbers moves in the same way as the gym env. Beyond this we use the first digit to show how many times this move must
#be done. Since the robot has to, for example, tilt the cube twice before rotating the bottom row to then tilt twice again in order 
# to perform U1, we significantly lower the amount of moves from the robot needed for U2 from 10 (tilt x2, rotate bottom, tilt x2 and repeat) to
# 6 (tilt x2, rotate bottom x2, tilt x2) by allowing for this parameter to be given to the robot along with the move.
def translate_moves_to_robot(solution_string):
    def decide_move(move_string):
        action = None
        nr_of_times = 1
        if move_string.startswith("U"):
            if move_string.endswith("1"): #MOVE = U1 = up clockwise = action 1
                action = 1
            elif move_string.endswith("2"): #MOVE = U2 = up clockwise x2 = action 1 x2
                action = 1
                nr_of_times = 2
            else:#MOVE = U3 = up counterclockwise = action 0
                action = 0
        elif move_string.startswith("D"):
            if move_string.endswith("1"):#MOVE = D1 = down clockwise = action 5
                action = 5
            elif move_string.endswith("2"):#MOVE = D2 = down clockwise x2 = action 5 x2
                action = 5
                nr_of_times = 2
            else:##MOVE = D3 = down counterclockwise = action 4
                action = 4
        elif move_string.startswith("F"):
            if move_string.endswith("1"):#MOVE = F1 = front clockwise = action 11
                action = 11
            elif move_string.endswith("2"):#MOVE = F2 = front clockwise x2 = action 11
                action = 11
                nr_of_times = 2
            else:#MOVE = F3 = front counterclockwise = action 10
                action = 10
        elif move_string.startswith("R"):
            if move_string.endswith("1"):#MOVE = R1 = right upwards = action 17
                action = 17
            elif move_string.endswith("2"):#MOVE = R2 = right upwards x2 = action 17 x2
                action = 17
                nr_of_times = 2
            else:#MOVE = R3 = right downwards = action 16
                action = 16
        elif move_string.startswith("L"):
            if move_string.endswith("1"):#MOVE = L1 = left downwards = action 13
                action = 13
            elif move_string.endswith("2"):#MOVE = L2 = left downwards  x2 = action 13 x2
                action = 13
                nr_of_times = 2
            else:#MOVE = L3 = left upwards = action 12
                action = 13
        elif move_string.startswith("B"):
            if move_string.endswith("1"):#MOVE = B1 = back clockwise = action 7
                action = 7
            elif move_string.endswith("2"):#MOVE = B2 = back counterclockwise x2 = action 7 x2
                action = 7
                nr_of_times = 2
            else:#MOVE = B3 = back clockwise = action 7
                action = 6
       #returns action in a string, filled with leading zeros to length 3
        res = f"{nr_of_times}" + f"{action:02d}"
        return res

    split_string = solution_string.split()
    new_moves = []
    for i in range((len(split_string))-1): #since last el in list is (5f) for example
        head = split_string[i]
        new_moves.append(decide_move(head))
    return new_moves



def run_kociemba(color_vector, to_print = True):
    print(f"in kociemba, color vector = {color_vector}")
    cubestring = convert_representation(color_vector)
    solution = sv.solve(cubestring,20,10)
    nr_moves = nr_of_moves(solution)
    translated = translate_moves_to_robot(solution)

    if to_print:
        print(f"Found a solution in {nr_moves} moves:")
        print(solution)
        print(f"translated: {translated}")
    return nr_moves, solution, translated
        


def run_random_cubes_kociemba():
    successes = 0
    failures = 0

    avg_moves = 0.0
    avg_time = 0.0
    while True:
        env = gym.make("RubiksCube-v0")

        obs = env.reset()

        start = time.time()
        
        nr_of_moves, solution, translated = run_kociemba(obs, False) #runs algo after modifying notation, False bc we do not want to print every single cube we run

        duration = time.time() - start

        #if C.is_solved():
        successes += 1
        avg_moves = (avg_moves * (successes - 1) + nr_of_moves) / float(successes)
        avg_time = (avg_time * (successes - 1) + duration) / float(successes)
        """""
        else:
            failures += 1
            print(f"Failed ({successes + failures}): {C.flat_str()}")
        """""
        total = successes
        if total == 1 or total % 10000 == 0:
            pass_percentage = 100 * successes / total
            print(f"{total}: {successes} successes ({pass_percentage:0.3f}% passing)"
                  f" avg_moves={avg_moves:0.3f}"
                  f" avg_time={avg_time:0.3f}s")


if __name__ == "__main__":
#to run a single random cube:
    env = gym.make("RubiksCube-v0")
    obs = env.reset()
    run_kociemba(obs, True)
    
#to run endlessly on random cubes, printing statistics every 100 cubes.
    #run_random_cubes_kociemba()
    
#--> 0.008 seconds per solve --> ca.  solves/s
#10000: 10000 successes (100.000% passing) avg_moves=9.624 avg_time=0.008s
#50000: 50000 successes (100.000% passing) avg_moves=17.533 avg_time=0.007s
#100000:100000 successes (100.000% passing) avg_moves=17.565 avg_time=0.007s
#350000: 350000 successes (100.000% passing) avg_moves=17.556 avg_time=0.007s
