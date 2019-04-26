from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search
import util


##################################################################
### NQUEENS
##################################################################

def nQueens(n, model):
    '''Return an n-queens CSP, optionally use tableContraints'''
    #your implementation for Question 4 changes this function
    #implement handling of model == 'alldiff'
    if not model in ['table', 'alldiff', 'row']:
        print("Error wrong sudoku model specified {}. Must be one of {}").format(
            model, ['table', 'alldiff', 'row'])

    i = 0
    dom = []
    for i in range(n):
        dom.append(i+1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []

    if model == 'alldiff':

        # alldiff
        ad_constructor = AllDiffConstraint
        ad_con = ad_constructor("C(Q{},Q{})", vars)
        cons.append(ad_con)

        # neq
        neq_constructor = NeqConstraint
        for qi in range(len(dom)):
            for qj in range(qi+1, len(dom)):
                neq_scope = [vars[qi], vars[qj]]
                neq_con = neq_constructor("C(Q{},Q{})".format(qi+1,qj+1),
                                            neq_scope, qi, qj)
                cons.append(neq_con)

    else:
        constructor = QueensTableConstraint if model == 'table' else QueensConstraint
        for qi in range(len(dom)):
            for qj in range(qi+1, len(dom)):
                con = constructor("C(Q{},Q{})".format(qi+1,qj+1),
                                            vars[qi], vars[qj], qi+1, qj+1)
                cons.append(con)

    csp = CSP("{}-Queens".format(n), vars, cons)
    return csp

def solve_nQueens(n, algo, allsolns, model='row', variableHeuristic='fixed', trace=False):
    '''Create and solve an nQueens CSP problem. The first
       parameer is 'n' the number of queens in the problem,
       The second specifies the search algorithm to use (one
       of 'BT', 'FC', or 'GAC'), the third specifies if
       all solutions are to be found or just one, variableHeuristic
       specfies how the next variable is to be selected
       'random' at random, 'fixed' in a fixed order, 'mrv'
       minimum remaining values. Finally 'trace' if specified to be
       'True' will generate some output as the search progresses.
    '''
    csp = nQueens(n, model)
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)
    print("Explored {} nodes".format(num_nodes))
    if len(solutions) == 0:
        print("No solutions to {} found".format(csp.name()))
    else:
       print("Solutions to {}:".format(csp.name()))
       i = 0
       for s in solutions:
           i += 1
           print("Solution #{}: ".format(i)),
           for (var,val) in s:
               print("{} = {}, ".format(var.name(),val), end='')
           print("")


##################################################################
### Class Scheduling
##################################################################

NOCLASS='NOCLASS'
LEC='LEC'
TUT='TUT'
class ScheduleProblem:
    '''Class to hold an instance of the class scheduling problem.
       defined by the following data items
       a) A list of courses to take

       b) A list of classes with their course codes, buildings, time slots, class types, 
          and sections. It is specified as a string with the following pattern:
          <course_code>-<building>-<time_slot>-<class_type>-<section>

          An example of a class would be: CSC384-BA-10-LEC-01
          Note: Time slot starts from 1. Ensure you don't make off by one error!

       c) A list of buildings

       d) A positive integer N indicating number of time slots

       e) A list of pairs of buildings (b1, b2) such that b1 and b2 are close 
          enough for two consecutive classes.

       f) A positive integer K specifying the minimum rest frequency. That is, 
          if K = 4, then at least one out of every contiguous sequence of 4 
          time slots must be a NOCLASS.

        See class_scheduling.py for examples of the use of this class.
    '''

    def __init__(self, courses, classes, buildings, num_time_slots, connected_buildings, 
        min_rest_frequency):
        #do some data checks
        for class_info in classes:
            info = class_info.split('-')
            if info[0] not in courses:
                print("ScheduleProblem Error, classes list contains a non-course", info[0])
            if info[3] not in [LEC, TUT]:
                print("ScheduleProblem Error, classes list contains a non-lecture and non-tutorial", info[1])
            if int(info[2]) > num_time_slots or int(info[2]) <= 0:
                print("ScheduleProblem Error, classes list  contains an invalid class time", info[2])
            if info[1] not in buildings:
                print("ScheduleProblem Error, classes list  contains a non-building", info[3])

        for (b1, b2) in connected_buildings:
            if b1 not in buildings or b2 not in buildings:
                print("ScheduleProblem Error, connected_buildings contains pair with non-building (", b1, ",", b2, ")")

        if num_time_slots <= 0:
            print("ScheduleProblem Error, num_time_slots must be greater than 0")

        if min_rest_frequency <= 0:
            print("ScheduleProblem Error, min_rest_frequency must be greater than 0")

        #assign variables
        self.courses = courses
        self.classes = classes
        self.buildings = buildings
        self.num_time_slots = num_time_slots
        self._connected_buildings = dict()
        self.min_rest_frequency = min_rest_frequency

        #now convert connected_buildings to a dictionary that can be index by building.
        for b in buildings:
            self._connected_buildings.setdefault(b, [b])

        for (b1, b2) in connected_buildings:
            self._connected_buildings[b1].append(b2)
            self._connected_buildings[b2].append(b1)

    #some useful access functions
    def connected_buildings(self, building):
        '''Return list of buildings that are connected from specified building'''
        return self._connected_buildings[building]


def solve_schedules(schedule_problem, algo, allsolns,
                 variableHeuristic='mrv', silent=False, trace=False):
    #Your implementation for Question 6 goes here.
    #
    #Do not but do not change the functions signature
    #(the autograder will twig out if you do).

    #If the silent parameter is set to True
    #you must ensure that you do not execute any print statements
    #in this function.
    #(else the output of the autograder will become confusing).
    #So if you have any debugging print statements make sure you
    #only execute them "if not silent". (The autograder will call
    #this function with silent=True, class_scheduling.py will call
    #this function with silent=False)

    #You can optionally ignore the trace parameter
    #If you implemented tracing in your FC and GAC implementations
    #you can set this argument to True for debugging.
    #
    #Once you have implemented this function you should be able to
    #run class_scheduling.py to solve the test problems (or the autograder).
    #
    #
    '''This function takes a schedule_problem (an instance of ScheduleProblem
       class) as input. It constructs a CSP, solves the CSP with bt_search
       (using the options passed to it), and then from the set of CSP
       solution(s) it constructs a list (of lists) specifying possible schedule(s)
       for the student and returns that list (of lists)

       The required format of the list is:
       L[0], ..., L[N] is the sequence of class (or NOCLASS) assigned to the student.

       In the case of all solutions, we will have a list of lists, where the inner
       element (a possible schedule) follows the format above.
    '''

# class CSP:
    # def __init__(self, name, variables, constraints):

    #BUILD your CSP here and store it in the varable csp
    # util.raiseNotDefined()

    # use time slots as variables
    event_in_time = {}
    for class_info in schedule_problem.classes:
        info = class_info.split('-')
        time = int(info[2])
        if time not in event_in_time:
            event_in_time[time] = [class_info]
        else:
            event_in_time[time].append(class_info)

    variables = []
    v_domain = []
    # for i in range(schedule_problem.num_time_slots):
    #     v_domain.append(NOCLASS)
    v_domain.append(NOCLASS)

    # create variables
    for i in range(schedule_problem.num_time_slots):
        new_slot_name = "{}".format(i + 1)
        if (i+1) in event_in_time:
            # change
            variables.append(Variable(new_slot_name, v_domain + event_in_time[i+1]
            + event_in_time[i+1]
            ))            
        else:
            variables.append(Variable(new_slot_name, v_domain))

    # There are 4 contstrings, 3 new and 1 alredy been implemented
    constraints = []
    
    # 1
    # use NValuesConstraint for student should take all courses on the list
    # print("c1")

    c_type = {}
    for c in schedule_problem.classes:
        info = c.split('-')
        cur_type = info[0] + '-' + info[3]
        # print(cur_type)
        if cur_type in c_type:  #already in
            c_type[cur_type].append(c)
        else:
            c_type[cur_type] =  [c]
    # print(c_type)
    for key_type in c_type:
        constraints.append(NValuesConstraint("c1_{}".format(key_type), variables, c_type[key_type], 1, 1))
    
    # 2, sep for sepcific class
    # print("c2")

    sep_class = {}
    for key_type in c_type:
        info = key_type.split('-')
        cur_class = info[0]
        lt = info[1]
        if cur_class in sep_class:  #already in
            sep_class[cur_class][lt] = c_type[key_type] # since there are no  duplicates in c_types
        else:
            sep_class[cur_class] = {lt: c_type[key_type]}
    # print(sep_class)
    for cur_class in sep_class:
        if TUT in sep_class[cur_class]:  # have both lec and tut
            constraints.append(taftercConstraint("c2_{}".format(cur_class), variables, sep_class[cur_class][LEC], sep_class[cur_class][TUT]))

    # 3
    # print("c3")

    close_distance_buildings = {}
    for building in schedule_problem.buildings:
        close_distance_buildings[building] = schedule_problem.connected_buildings(building)
    constraints.append(cdbConstraint("c3", variables, close_distance_buildings))

    # 4
    # print("c4")
    
    constraints.append(rfConstraint("c4", variables, schedule_problem.min_rest_frequency))

    csp = CSP("Class_Sheduling_Problem", variables, constraints)



    #invoke search with the passed parameters
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)

    #Convert each solution into a list of lists specifying a schedule
    #for each student in the format described above.
    final_solution = []
    for s in solutions:
        cur_soluction = []
        for (var,val) in s:
            cur_soluction.append(val)
        if cur_soluction not in final_solution:
            final_solution.append(cur_soluction)
    return final_solution

    #then return a list containing all converted solutions
    
    