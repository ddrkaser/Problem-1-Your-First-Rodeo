import random

walls = [(5,5),(5,6),(5,7),(6,7),(7,5),(7,6),(7,7)]

def hureisticValue(point1, point2):
    x1,y1=point1
    x2,y2=point2
    return abs(x1 - x2) + abs(y1 - y2)

def b_move(b_pos, c_pos):
    x, y = b_pos
    dist = float("inf")
    #sense in_sight surrounding cells 5x5
    surroundings = [(x2, y2) for y2 in range(y-2, y+3)
                 for x2 in range(x-2, x+3)
                 if (-1 < y < 13 and -1 < x < 13 and
                     (y != y2 or x != x2) and
                     (0 <= y2 < 13) and (0 <= x2 < 13))]
    #if the robot is in_sight, compute shortest distance
    if c_pos in surroundings:
        dist = hureisticValue(b_pos,c_pos)
    move_range = []
    #find movable directions which is closer to robot
    if x > 0 and hureisticValue(c_pos,(x-1,y)) <= dist:
        move_range.append((x-1,y))
    if x < 12 and hureisticValue(c_pos,(x+1,y)) <= dist:
        move_range.append((x+1,y))
    if y > 0 and hureisticValue(c_pos,(x,y-1)) <= dist:
        move_range.append((x,y-1))
    if y < 12 and hureisticValue(c_pos,(x,y+1)) <= dist:
        move_range.append((x,y+1))
    #stay if robot is nearby
    if c_pos in move_range:
        return b_pos
    next_move = random.sample(move_range,1)[0]
    #stay if bump the wall
    if next_move in walls:
        next_move = b_pos
    return next_move    

def c_move(b_pos, c_pos):
    x, y = c_pos
    next_move = c_pos
    #find avialiable surroundings 3x3
    surroundings = [(x2, y2) for y2 in range(y-1, y+2)
                 for x2 in range(x-1, x+2)
                 if (-1 < y < 13 and -1 < x < 13 and
                     (y != y2 or x != x2) and
                     (0 <= y2 < 13) and (0 <= x2 < 13))]
    #this is outter cells of surroundings, which is 5x5 circle.
    waiting_zones = [(x2, y2) for y2 in range(y-2, y+3)
                 for x2 in range(x-2, x+3)
                 if (-1 < y < 13 and -1 < x < 13 and
                     (y != y2 or x != x2) and
                     (0 <= y2 < 13) and (0 <= x2 < 13) and ((x2, y2) not in surroundings))]
    #if bull is in waiting zone, robot stays
    if b_pos in waiting_zones:
        return c_pos
    #neither in surrounding, try to catch up the bull
    elif b_pos not in surroundings:
        min_dist = hureisticValue(b_pos,c_pos)
        for surrounding in surroundings:
            if (hureisticValue(b_pos,surrounding) < min_dist) and (surrounding not in walls) and surrounding != (6,6):
                next_move = surrounding
                min_dist = hureisticValue(b_pos,surrounding)
        return next_move
    #the bull is nearby
    else:
        #pull the bull to target position
        if c_pos != (6,4):
            return move_to_target(c_pos,b_pos,surroundings)
        elif b_pos == (6,3):
            return (6,5)
        elif b_pos == (5,4):
            return (7,4)
        elif b_pos == (7,4):
            return (5,4)
        else:
            return c_pos
            
#when the bull is nearby, the robot will pull the bull to the target position            
def move_to_target(c_pos,b_pos,surroundings):
    x, y = c_pos
    min_dist = float("inf")
    next_move = c_pos
    if y >4 and x <7:
        target = (5,4)
    elif y >4 and x > 6:
        target = (7,4)
    else:
        target = (6,4)
    for surrounding in surroundings:
            if (hureisticValue(target,surrounding) < min_dist) and (surrounding not in walls) and (surrounding != b_pos):
                next_move = surrounding
                min_dist = hureisticValue(target,surrounding)       
    return next_move
        
#this is the stategy to lead the bull to position X,
#the robot tries to lead the bull from (6,4) to (6,5)
#if it fails, the robot will pull the bull back to the initial position (6,4)
#the robot will repeat this action until the bull enters the position X.
def end_game(c_pos, b_pos):
    if b_pos == (6,4):
        if c_pos == (6,5):
            return (7,4)
        elif c_pos == (7,4):
            return (8,5)
        elif c_pos == (5,4):
            return (4,5)
        else:
            return c_pos
    elif b_pos == (6,5):
        if c_pos == (8,5):
            return (8,6)
        elif c_pos == (4,5):
            return (4,6)
        else:
            return c_pos
    elif b_pos == (7,4):
        if c_pos == (8,5):
            #print ("back to position")
            return (8,4)
        elif c_pos == (8,4):
            return (7,3)
        elif c_pos == (7,3):
            return (6,4)
        elif c_pos == (6,4):
            return (5,4)
        else:
            return c_pos
    elif b_pos == (5,4):
        if c_pos == (4,5):
            #print ("back to position")
            return (4,4)
        elif c_pos == (4,4):
            return (5,3)
        elif c_pos == (5,3):
            return (6,4)
        elif c_pos == (6,4):
            return (7,4)
        else:
            return c_pos
    else:
        return c_pos     

def start_game(b_pos,c_pos):
    in_position = False
    count = 0
    while b_pos != (6,6):
        count += 1
        #if both are in the target position, we enter the end_game statues
        if c_pos in [(7,4),(5,4),(6,5)] and b_pos == (6,4) and not in_position:
            in_position = True
            #print("in position")
        if not in_position:
            if c_pos == (6,5) and b_pos in [(4,5),(8,5)]:
                c_pos = (6,4)
            elif c_pos in [(4,5),(8,5)] and b_pos == (6,5):
                x,y = c_pos
                c_pos = (x,y+1)
            else:
                c_pos = c_move(b_pos, c_pos)
        else:
            c_pos = end_game(c_pos, b_pos)
        b_pos = b_move(b_pos, c_pos)
        #print("robot {}, bull {}".format(c_pos,b_pos))
    #print("you pened the bull")
    return count
              
def compute_turns(b_pos,c_pos,max_trial):
    trial = 0
    total_turn = 0
    while trial < max_trial:
        print("running trial:{}".format(trial))
        total_turn += start_game(b_pos,c_pos) 
        trial += 1
    avg_turn = total_turn/max_trial
    return avg_turn
        
compute_T_prime = compute_turns((6,4),(7,4),50000)
expected_turn = compute_turns((0,0),(12,12),50000)
                                    