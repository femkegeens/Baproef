# USING  https://github.com/pglass/cube

import gym

#pip install rubik-cube
from rubik.cube import Cube
from rubik.solve import Solver
from rubik.optimize import optimize_moves
from itertools import chain

import time
def convert_representation(color_vector):          

# number from 0-5 are mapped to the colors in the following order white, red, blue, orange, green and yellow
    def convert_nr_to_string(n):
        match n:
            case 0:
                return "W"
            case 1:
                return "R"
            case 2:
                return "B"
            case 3:
                return "O"
            case 4:
                return "G"
            case 5:
                return "Y"
    string_vector = list(map(convert_nr_to_string, color_vector))
   
   #map the right indices of the gym env onto the string's indices
    cube_str = list(chain(
                                string_vector[0:9], 
        string_vector[36:39],   string_vector[9:12],   string_vector[18:21],   string_vector[27:30],
        string_vector[39:42],   string_vector[12:15],   string_vector[21:24],   string_vector[30:33],
        string_vector[42:45],   string_vector[15:18],   string_vector[24:27],   string_vector[33:36],
                                string_vector[51:],
                                string_vector[48:51],
                                string_vector[45:48]
    ) )

    return cube_str
def convert_nr_to_string(n):
    match n:
        case 0:
            return "W"
        case 1:
            return "R"
        case 2:
            return "B"
        case 3:
            return "O"
        case 4:
            return "G"
        case 5:
            return "Y"

def translate_moves_to_robot(solution):
   def move_to_robot(move):
    match move:
        case "L": 12#left down
        case "Li": 13 #left up
        case "R":  17 #right up
        case "Ri": 16 #right down
        case "U":  1 #upper layer clockwise
        case "Ui": 0 #upper layer counterclockwise
        case "D":  4 #bottom layer counterclockwise
        case "Di": 5 #bottom layer clockwise
        case "F":  11 #front layer clockwise
        case "Fi": 10 #front layer counterclockwise
        case "B":  6 #back layer counterclockwise
        case "Bi": 7 #back layer clockwise
        case "M":  14 #middle vertical down
        case "Mi": 15 #middle vertical up
        case "E":  2 # middle horizontal counterclockwise
        case "Ei": 3 #middle horizontal clockwise
        case "S":  9 #middle clockwise
        case "Si": 8 #middle counterclockwise
        ##HERE I EXPANDED THE ROBOT BEYOND WHAT THE GYM ENV KNOWS, SINCE IT IS STANDARD RUBIKS CUBE NOTATION
        case "X":  18 #tilt
        case "Xi": 19 #tilt x3
        case "Y":  20 #rotate entire cube clockwise
        case "Yi": 21 #otate entire cube counterclockwise
        case "Z":  22 #entire cube counterclockwise + tilt + entire cube clockwise
        case "Zi": 23 #entire cube clockwise + tilt + entire cube counter clockwise
   
    nr_moves = len(solution)
    translated  = []
    nr_of_times = 1
    i = 0
   
  
    while i < nr_moves:
        curr = solution[i]
        if (i+1) < nr_moves and curr == solution[i+1]: #second in a row, no thirds possible due to optimiser (3x one direction = 1x inverse direction)
            nr_of_times = 2
        else: nr_of_times = 1

        number_for_move = move_to_robot(curr)
        res = f"{nr_of_times}" + f"{number_for_move:02d}"
        translated.append(res)
        i += nr_of_times
    return translated




def run_pglass_algo(color_vector, to_print):
    cube_string = convert_representation(color_vector)
    cube = Cube(cube_string)
    
    if to_print:
        print("cube string:")
        print("Starting off with the following cube:")
        print(cube)

    solver = Solver(cube)
    solver.solve()
    if to_print:
        print(f"{len(solver.moves)} moves: {' '.join(solver.moves)}")
    optimised = optimize_moves(solver.moves)
    print(f"optimised moves: {optimised}")
    translated = translate_moves_to_robot(optimised)
    
    return cube, solver, optimised, translated #to access its properties

def run_random_cubes_pglass():
    successes = 0
    failures = 0

    avg_opt_moves = 0.0
    avg_moves = 0.0
    avg_time = 0.0
    while True:
        env = gym.make("RubiksCube-v0")

        env.scramble_params = 4

        obs = env.reset()

        start = time.time()
        
        C, solver = run_pglass_algo(obs, False) #runs algo after modifying notation, False bc we do not want to print every single cube we run

        duration = time.time() - start

        if C.is_solved():
            opt_moves = optimize_moves(solver.moves)
            successes += 1
            avg_moves = (avg_moves * (successes - 1) + len(solver.moves)) / float(successes)
            avg_time = (avg_time * (successes - 1) + duration) / float(successes)
            avg_opt_moves = (avg_opt_moves * (successes - 1) + len(opt_moves)) / float(successes)
        else:
            failures += 1
            print(f"Failed ({successes + failures}): {C.flat_str()}")

        total = successes + failures
        if total == 1 or total % 100 == 0:
            pass_percentage = 100 * successes / total
            print(f"{total}: {successes} successes ({pass_percentage:0.3f}% passing)"
                  f" avg_moves={avg_moves:0.3f} avg_opt_moves={avg_opt_moves:0.3f}"
                  f" avg_time={avg_time:0.3f}s")






if __name__ == "__main__":
#to run a single random cube:
    env = gym.make("RubiksCube-v0")
    print(env.scramble_params)
    obs = env.reset()
    
    run_pglass_algo(obs, True)


#to run endlessly on random cubes, printing statistics every 100 cubes.
  #  run_random_cubes()
    
#--> 0.008 seconds per solve --> 125 solves/s
#10000: 10000 successes (100.000% passing) avg_moves=252.023 avg_opt_moves=192.190 avg_time=0.035s
#50000: 50000 successes (100.000% passing) avg_moves=252.443 avg_opt_moves=192.501 avg_time=0.036s
#100000: 100000 successes (100.000% passing) avg_moves=252.374 avg_opt_moves=192.494 avg_time=0.036s