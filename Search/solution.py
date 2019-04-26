#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

grid = []
grid_y_first = []

deadlock_list = []



unsign_int = 0
storage_int = -1
obsticle_int = -2
deadlock_int = -3

deadend_value = float('inf')


def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.


    total_distance = 0
    for cur_box in state.boxes:
        cur_distances = []
        for storage_point in state.storage:
            cur_distances.append(abs(cur_box[0] - storage_point[0]) + abs(cur_box[1] - storage_point[1]))
        total_distance += min(cur_distances)
        # print(total_distance)
    return total_distance


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    global grid
    # global first_time

    if state.parent is None:
        # deadlock_list = []
        grid = init_grid(state)
        # print(grid)
        # print(deadlock_list)

    free_box = []
    not_free_storage = []
    free_storage = []
    for cur in state.boxes:
        if iff_box(state, cur) is False:
            free_box.append(cur)
        else:
            not_free_storage.append(cur)

    for storage in state.storage:
        if storage not in not_free_storage:
            free_storage.append(storage)

    total_distance = 0
    for box in free_box:
        if box in deadlock_list:
            return float('inf')
        box_storage = float('inf') # distance
        for storage in free_storage:
            tmp_b_s = direct_distance(box, storage)
            if tmp_b_s < box_storage:
                box_storage = tmp_b_s
        total_distance += box_storage

        box_robot = float('inf') # distance        
        for robot in state.robots:
            tmp_b_r = direct_distance(box, robot)
            if tmp_b_r < box_robot:
                box_robot = tmp_b_r
        total_distance += box_robot
    return total_distance


def iff_box(state, cur):
    if cur in state.storage:
        return True
    return False


def direct_distance(f, s):
    return abs(f[0] - s[0]) + abs(f[1] - s[1])

    
    

def init_grid(state):
    ''' 
    Create a whole gride of obsticles and deadlocks
    whole_grid[<x coordinatge>][<y coordinate>]
    '''
    global deadlock_list

    global unsign_int # -1
    global storage_int # 0
    global obsticle_int # -2
    global deadend_value # float('inf')

    deadlock_list = []
    local_deadlock_list = []
    grid = []

    ##########################################################
    # create the grid with only unsign
    for x in range(state.width):
        # vertical
        y_dimension = []
        for y in range(state.height):
            y_dimension.append(unsign_int)
        grid.append(y_dimension)
    
    # add the obstacle
    for ob in state.obstacles:
        grid[ob[0]][ob[1]] = obsticle_int

    # add the storage
    for st in state.storage:
        grid[st[0]][st[1]] = storage_int
    ##########################################################

    # add deadlocks
    # first round
    # add the corner ones
    for x in range(state.width):
        for y in range(state.height):
            if grid[x][y] == unsign_int:
                cur = (x, y)
                if corner_deadlock(state,cur) == True:
                    grid[x][y] = deadlock_int
                    deadlock_list.append(cur)
                    local_deadlock_list.append(cur)
    # print("deadlock_list, initial", deadlock_list)
    # print("local_deadlock_list, initial", local_deadlock_list)

    ##########################################################
    # create tow lists, one for x coordinates of deadlocks, one for y coordiantes for the dead locks
    x_deadlock_list = []
    y_deadlock_list = []
    # for dl in deadlock_list:
    #     x_deadlock_list.append(dl[0])
    #     print("x_deadlock_list", x_deadlock_list)
    #     y_deadlock_list.append(dl[1])
    #     print("y_deadlock_list",y_deadlock_list)
    for dl in deadlock_list:
        x_deadlock_list.append(dl[0])
        y_deadlock_list.append(dl[1])
    # print("x_deadlock_list", x_deadlock_list)
    # print("y_deadlock_list", y_deadlock_list)


    
    ##########################################################
    # create dealocks in between dead locks:
    dl_ind = 0
    while local_deadlock_list != []:
        # print("loop:", dl_ind)
        # print(local_deadlock_list)
        cur_dl = local_deadlock_list.pop(0)
        x_value = cur_dl[0]
        y_value = cur_dl[1]

        same_hori_line = indices(y_deadlock_list, y_value) # indexes
        same_hori_line = elim_before_index(same_hori_line, dl_ind)
        if len(same_hori_line) >= 2: # else, no same ones that are not been checked (after this one)
            for i in same_hori_line:
                if abs(x_value - x_deadlock_list[i]) > 1: # if same one or closer, then do not need to check
                    start_ind = min(x_value, x_deadlock_list[i])
                    end_ind = max(x_value, x_deadlock_list[i])
                    hori_seg_between = create_hori_between(grid, y_value, start_ind, end_ind)
                    # print("hori_seg_between", hori_seg_between)
                    # print("between_check(hori_seg_between)", between_check(hori_seg_between))
                    # print("hori_check_bounded(state, y_value, start_ind, end_ind)", hori_check_bounded(state, y_value, start_ind, end_ind))
                    if (between_check(hori_seg_between) and hori_check_bounded(state, y_value, start_ind, end_ind)): # if only unsign and deadlocks in between
                        j = start_ind + 1
                        while j < end_ind:
                            if (j, y_value) not in deadlock_list:
                                grid[j][y_value] =deadlock_int
                                new_deadlock = (j, y_value)
                                local_deadlock_list.append(new_deadlock)
                                deadlock_list.append(new_deadlock)
                                x_deadlock_list.append(j)
                                y_deadlock_list.append(y_value)
                            j += 1


        same_verti_line = indices(x_deadlock_list, x_value) # indexes
        same_verti_line = elim_before_index(same_verti_line, dl_ind)
        if len(same_verti_line) >= 2: # else, no same ones that are not been checked (after this one)
            # print("same_verti_line", same_verti_line)
            for i in same_verti_line:
                if abs(y_value - y_deadlock_list[i]) > 1: # if same one or closer, then do not need to check
                    start_ind = min(y_value, y_deadlock_list[i])
                    # print("start_ind", start_ind)
                    end_ind = max(y_value, y_deadlock_list[i])
                    # print("end_ind", end_ind)                    
                    verti_seg_between = grid[x_value][start_ind + 1:end_ind]
                    # print("cur compare with", (x_value, y_deadlock_list[i]))
                    # print("verti_seg_between", verti_seg_between)
                    # print("between_check(verti_seg_between)", between_check(verti_seg_between))
                    # print("verti_check_bounded(state, x_value, start_ind, end_ind)", verti_check_bounded(state, x_value, start_ind, end_ind))

                    if (between_check(verti_seg_between) and verti_check_bounded(state, x_value, start_ind, end_ind)): # if only unsign and deadlocks in between
                        j = start_ind + 1
                        while j < end_ind:
                            if (x_value, j) not in deadlock_list:
                                grid[x_value][j] = deadlock_int
                                new_deadlock = (x_value, j)
                                local_deadlock_list.append(new_deadlock)
                                deadlock_list.append(new_deadlock)
                                x_deadlock_list.append(x_value)
                                y_deadlock_list.append(j)
                            j += 1        
        dl_ind += 1
    # print("deadlock_list, final", deadlock_list)
    # print("local_deadlock_list, final", local_deadlock_list)

    return grid


def create_hori_between(grid, y_ind, start, end):
    inds_between = []
    i = start + 1
    while i < end:
        inds_between.append(grid[i][y_ind])
        i += 1
    return inds_between


def between_check(li):
    if storage_int in li or obsticle_int in li:
        return False
    return True

def indices(dll, value):
    all_indices = []
    for i in range(len(dll)):
        if dll[i] == value:
            all_indices.append(i)
    return all_indices

def elim_before_index(li, cur):
    configed_li = []
    for i in range(len(li)):
        if li[i] >= cur:
            configed_li.append(li[i])
    return configed_li


def hori_check_bounded(state, y_ind, start, end):
    i = start + 1
    while i < end:
        if is_bounded(state, i, y_ind) == False:
            return False
        i += 1
    return True

def verti_check_bounded(state, x_ind, start, end):
    i = start + 1
    while i < end:
        if is_bounded(state, x_ind, i) == False:
            return False
        i += 1
    return True


def is_bounded(state, x, y):
    '''if block is bounded, 1 or more return True, else False'''
    # at edges
    if x == 0 or x == state.width - 1:
        # print("edge1")
        return True
    if y == 0 or y == state.height - 1:
        # print("edge2")
        return True
    # if obstacles around
    if (x - 1, y) in state.obstacles:
        # print("obstacles1")
        return True
    if (x + 1, y) in state.obstacles:
        # print("obstacles2")
        return True
    if (x, y - 1) in state.obstacles:
        # print("obstacles3")
        return True
    if (x, y + 1) in state.obstacles:
        # print("obstacles4")
        return True
    
    return False


def line_seg_grid(grid, ori_x, ori_y):
    revers_grid = []
    for y in range(ori_y):
        x_dimension = []
        for x in range(ori_x):
            x_dimension.append(grid[x][y])
        revers_grid.append(x_dimension)
    return revers_grid





def corner_deadlock(state, cur):
    global obsticle_int

    x = cur[0]
    y = cur[1]

    # if 2 adjcent side are bound or obsticle, aka corner, first round
    if (x == 0) or (x == state.width - 1) or (x - 1, y) in state.obstacles or (x + 1, y) in state.obstacles:
        up_down = True
    else:
        up_down = False
    
    if (y == 0) or (y == state.height - 1) or (x, y - 1) in state.obstacles or (x, y + 1) in state.obstacles:
        left_right = True
    else:
        left_right = False
    
    if up_down and left_right:
        return True

    return False

    

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight*sN.hval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    # initialize the time
    time = os.times()[0]  #start time
    due_time = time + timebound

    # initialize the search engine
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    cur_search = SearchEngine('custom')
    cur_search.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)
    cur_state = cur_search.search(timebound)
    best_state = cur_state
    # best state for now, will change later (maybe)

    # after the initial search, find a new remaining time
    time_remain = due_time - os.times()[0]

    cost_bound = (float('inf'), float('inf'), float('inf'))

    time = os.times()[0]
    if cur_state == False: # no other solutions
        return best_state

    while (time_remain > 0):
        time = os.times()[0]
        fn_val = heur_fn(cur_state)
        if (cur_state.gval + fn_val <= cost_bound[2]):
            cost_bound = (float('inf'), float('inf'), cur_state.gval + fn_val)
            best_state = cur_state
        cur_state = cur_search.search(time_remain, cost_bound)
        if cur_state == False: # no other solutions
            return best_state
        time_remain -= (os.times()[0] - time)
    return best_state


def anytime_gbfs(initial_state, heur_fn, timebound = 10):
    #IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    # initialize the time
    time = os.times()[0]  #start time
    due_time = time + timebound

    # initialize the search engine
    cur_search = SearchEngine('custom')
    cur_search.init_search(initial_state, sokoban_goal_state, heur_fn)
    cur_state = cur_search.search(timebound)
    best_state = cur_state
    # best state for now, will change later (maybe)

    # after the initial search, find a new remaining time
    time_remain = due_time - os.times()[0]

    cost_bound = (float('inf'), float('inf'), float('inf'))

    time = os.times()[0]
    if cur_state == False: # no other solutions
        return best_state

    while (time_remain > 0):
        time = os.times()[0]
        if (cur_state.gval <= cost_bound[0]):
            cost_bound = (cur_state.gval, float('inf'), float('inf'))
            best_state = cur_state
        cur_state = cur_search.search(time_remain, cost_bound)
        if cur_state == False: # no other solutions
            return best_state
        time_remain -= (os.times()[0] - time)
    return best_state
