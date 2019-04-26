from constraints import *
from backtracking import bt_search, GacEnforce
from csp import Variable, CSP
from csp_problems import nQueens, solve_schedules
from class_scheduling import c1, c2, c3, c4, c5, c6, c7, check_schedule_solution
import argparse

legalQs = ["q1", "q2", "q3", "q4", "q5", "q6"]
tested = [False]*5

gradeMessage = ""
grades = [0, 0, 0, 0, 0, 0]
outof  = [4, 5, 7, 2, 4, 4]
tests = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
titles = ["Q1. Table Constraint for nQueens (4 points)",
          "Q2. Forward Checking implementation (5 points)",
          "Q3. GacEnforce and GAC implementation (7 points)",
          "Q4. AllDiff for nQueens (2 points)",
          "Q5. NValues Constraint implementation (4 points)",
          "Q6. Class Scheduling (4 points)"]

def print_title(i):
    l = max([len(t) for t in titles])
    print("-"*l)
    print(titles[i])
    print("-"*l)

def print_sep(c='-'):
    l = max([len(t) for t in titles])
    print(c*l)

def print_soln(s):
    for (var, val) in s:
        print("{} = {} ".format(var.name(), val), end=' ')

def question_1():
    print_title(0)
    tested[0] = True
    ntests = 3
    fails = [False]*ntests
    #test1 constraint.check()
    q2 = Variable("Q2", [1, 2, 3, 4, 5])
    q5 = Variable("Q5", [1, 2, 3, 4, 5])
    c  = QueensTableConstraint("Q2/Q5", q2, q5, 2, 5)
    q2.setValue(2)
    for val in q5.domain():
        q5.setValue(val)
        if c.check():
            if val in [2,5]:
                print("Queens table constraint check routine failed")
                print("Q2={}, Q5={} not detected as falsifying constraint".format(q2.getValue(), q5.getValue()))
                fails[0] = True
        else:
            if val in [1,3,4]:
                print("Queens table constraint check routine failed")
                print("Q2={}, Q5={} not detected as satisfying constraint".format(q2.getValue(), q5.getValue()))
                fails[0] = True
    if fails[0]:
        print("Fail Q1 test 1")
    else:
        print("Pass Q1 test 1")
    print_sep()

    #test2 constraint.hasSupport()
    q2.reset()
    q3 = Variable("Q3", [1, 2, 3, 4, 5])
    q2.pruneValue(1, None, None)
    q2.pruneValue(4, None, None)
    q2.pruneValue(5, None, None)
    c = QueensTableConstraint("Q2/Q5", q2, q3, 2, 3)
    for val in q3.domain():
        if c.hasSupport(q3, val):
            if val not in [1, 4, 5]:
                print("Queens table constraint hasSupport routine failed")
                print("Q2 current domain = {}, Q3 = {} detected to have support (doesn't)".format(q2.curDomain(), val))
                fails[1] = True
        else:
            if val not in [2, 3]:
                print("Queens table constraint hasSupport routine failed")
                print("Q2 current domain = {}, Q3 = {} detected to not have support (does)".format(q2.curDomain(), val))
                fails[1] = True
    if fails[1]:
        print("Fail Q1 test 2")
    else:
        print("Pass Q1 test 2")
    print_sep()

    #test3 within backtracking search
    csp = nQueens(8, 'row')
    solutions, num_nodes = bt_search('BT', csp, 'fixed', True, False)
    if num_nodes != 1965:
        print("Queens table constraint not working correctly. BT should explore 1965 nodes.")
        print("With your implementation it explores {}".format(num_nodes))
        fails[2] = True
    if len(solutions) != 92:
        print("Queens table constraint not working correctly. BT should return 92 solutions")
        print("With your implementation it returns {}".format(len(solutions)))
        fails[2] = True

    if fails[2]:
        print("Fail Q1 test 3")
    else:
        print("Pass Q1 test 3")

    if any(fails):
        grades[0] = 0
    else:
        grades[0] = outof[0]

def question_2():
    print_title(1)
    tested[1] = True

    fails = [False, False]
    #test 1. Find one solution
    csp = nQueens(8, 'row')
    solutions, num_nodes = bt_search('FC', csp, 'fixed', False, False)
    errors = csp.check(solutions)

    if len(errors) > 0:
        fails[0] = True
        print("Fail Q2 test 1: invalid solution(s) returned by FC")
        for err in errors:
            print_soln(err[0])
            print("\n", err[1])

    if len(solutions) != 1:
        fails[0] = True
        print("Fail Q2 test 1: FC failed to return only one solution")
        print("  returned: ")
        for s in solutions:
            print_soln(s)
            print("")
    ok=True
    for v in csp.variables():
        if set(v.curDomain()) != set(v.domain()):
            fails[0] = True
            print("Fail Q2 test 1: FC failed to restore domains of variables")

    if not fails[0]:
        print("Pass Q2 test 1")
    print_sep()

    csp = nQueens(8, 'row')
    solutions, num_nodes = bt_search('FC', csp, 'fixed', True, False)
    errors=csp.check(solutions)

    if len(errors) > 0:
        fails[1] = True
        print("Fail Q2 test 2: invalid solution(s) returned by FC")
        for err in errors:
            print_soln(err[0])
            print("\n", err[1])

    if len(solutions) != 92:
        fails[1] = True
        print("Fail Q2 test 2: FC failed to return 92 solutions")
        print("  returned {} solutions".format(len(solutions)))

    ok=True
    for v in csp.variables():
        if set(v.curDomain()) != set(v.domain()):
            fails[1] = True
            print("Fail Q2 test 2: FC failed to restore domains of variables")

    if not fails[1]:
        print("Pass Q2 test 2")
    print_sep()

    if sum(fails) == 2:
        grades[1] = 0
    elif sum(fails) == 1:
        grades[1] = 3
    elif sum(fails) == 0:
        grades[1] = outof[1]

def question_3():
    print_title(2)
    tested[2] = True

    fails = [False, False, False, False, False]
    v1 = Variable('V1', [1, 2])
    v2 = Variable('V2', [1, 2])
    v3 = Variable('V3', [1, 2, 3, 4, 5])
    v4 = Variable('V4', [1, 2, 3, 4, 5])
    v5 = Variable('V5', [1, 2, 3, 4, 5])
    v6 = Variable('V6', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v7 = Variable('V7', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v8 = Variable('V8', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v9 = Variable('V9', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    vars = [v1, v2, v3, v4, v5, v6, v7, v8, v9]
    ac = AllDiffConstraint('test9', vars)
    testcsp = CSP('test', vars, [ac])
    GacEnforce([ac], testcsp, None, None)


    test1 = "    v1 = Variable('V1', [1, 2])\n\
    v2 = Variable('V2', [1, 2])\n\
    v3 = Variable('V3', [1, 2, 3, 4, 5])\n\
    v4 = Variable('V4', [1, 2, 3, 4, 5])\n\
    v5 = Variable('V5', [1, 2, 3, 4, 5])\n\
    v6 = Variable('V6', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v7 = Variable('V7', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v8 = Variable('V8', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v9 = Variable('V9', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    vars = [v1, v2, v3, v4, v5, v6, v7, v8, v9]\n\
    ac = AllDiffConstraint('test9', vars)\n\
    testcsp = CSP('test', vars, [ac])\n\
    GacEnforce([ac], testcsp, None, None)"


    soln_doms = [ set([1,2]), set([1,2]), set([3,4,5]), set([3,4,5]), set([3,4,5]),
                  set([6, 7, 8, 9]), set([6, 7, 8, 9]), set([6, 7, 8, 9]), set([6, 7, 8, 9]) ]

    for i, v in enumerate(vars):
        if set(v.curDomain()) != soln_doms[i]:
            fails[0] = True
            print("Error: {}.curDomain() == {}".format(v.name(), v.curDomain()))
            print("Correct curDomin should be == {}".format(list(soln_doms[i])))

    if fails[0]:
        print("\nFail Q3 test 1\nErrors were generated on the following code:")
        print(test1)
    else:
        print("Pass Q3 test 1")
    print_sep()

    v1 = Variable('V1', [1, 2])
    v2 = Variable('V2', [1, 2])
    v3 = Variable('V3', [1, 2, 3, 4, 5])
    v4 = Variable('V4', [1, 2, 3, 4, 5])
    v5 = Variable('V5', [1, 2, 3, 4, 5])
    v6 = Variable('V6', [1, 3, 4, 5])
    v7 = Variable('V7', [1, 3, 4, 5])
    ac1 = AllDiffConstraint('1', [v1,v2,v3])
    ac2 = AllDiffConstraint('1', [v1,v2,v4])
    ac3 = AllDiffConstraint('1', [v1,v2,v5])
    ac4 = AllDiffConstraint('1', [v3,v4,v5,v6])
    ac5 = AllDiffConstraint('1', [v3,v4,v5,v7])
    vars = [v1, v2, v3, v4, v5, v6, v7]
    cnstrs = [ac1,ac2,ac3,ac4,ac5]
    testcsp = CSP('test2', vars, cnstrs)
    GacEnforce(cnstrs, testcsp, None, None)

    test2 = "    v1 = Variable('V1', [1, 2])\n\
    v2 = Variable('V2', [1, 2])\n\
    v3 = Variable('V3', [1, 2, 3, 4, 5])\n\
    v4 = Variable('V4', [1, 2, 3, 4, 5])\n\
    v5 = Variable('V5', [1, 2, 3, 4, 5])\n\
    v6 = Variable('V6', [1, 3, 4, 5])\n\
    v7 = Variable('V7', [1, 3, 4, 5])\n\
    ac1 = AllDiffConstraint('1', [v1,v2,v3])\n\
    ac2 = AllDiffConstraint('1', [v1,v2,v4])\n\
    ac3 = AllDiffConstraint('1', [v1,v2,v5])\n\
    ac4 = AllDiffConstraint('1', [v3,v4,v5,v6])\n\
    ac5 = AllDiffConstraint('1', [v3,v4,v5,v7])\n\
    vars = [v1, v2, v3, v4, v5, v6, v7]\n\
    cnstrs = [ac1,ac2,ac3,ac4,ac5]\n\
    testcsp = CSP('test2', vars, cnstrs)\n\
    GacEnforce(cnstrs, testcsp, None, None)"

    soln_doms = [ set([1,2]), set([1,2]), set([3, 4, 5]), set([3,4,5]), set([3,4,5]),
                  set([1]), set([1]) ]

    #v1.pruneValue(1, None, None)

    for i, v in enumerate(vars):
        if set(v.curDomain()) != soln_doms[i]:
            fails[1] = True
            print("Error: {}.curDomain() == {}".format(v.name(), v.curDomain()))
            print("Correct curDomin should be == {}".format(list(soln_doms[i])))

    if fails[1]:
        print("\nFail Q3 test 2\nErrors were generated on the following code:")
        print(test2)
    else:
        print("Pass Q3 test 2")
    print_sep()


    v1 = Variable('V1', [1, 2])
    v2 = Variable('V2', [1, 2])
    v3 = Variable('V3', [1, 2, 3, 4, 5])
    v4 = Variable('V4', [1, 2, 3, 4, 5])
    v5 = Variable('V5', [1, 2, 3, 4, 5])
    v6 = Variable('V6', [1, 3, 4, 5])
    v7 = Variable('V7', [1, 3, 4, 5])    
    ac1 = AllDiffConstraint('1', [v1,v2,v3,v4,v5,v6,v7])
    vars = [v1, v2, v3, v4, v5, v6, v7]
    cnstrs = [ac1]
    testcsp = CSP('test2', vars, cnstrs)
    val = GacEnforce(cnstrs, testcsp, None, None)

    test3 = "    v1 = Variable('V1', [1, 2])\n\
    v2 = Variable('V2', [1, 2])\n\
    v3 = Variable('V3', [1, 2, 3, 4, 5])\n\
    v4 = Variable('V4', [1, 2, 3, 4, 5])\n\
    v5 = Variable('V5', [1, 2, 3, 4, 5])\n\
    v6 = Variable('V6', [1, 3, 4, 5])\n\
    v7 = Variable('V7', [1, 3, 4, 5])\n\
    ac1 = AllDiffConstraint('1', [v1,v2,v3,v4,v5,v6,v7])\n\
    vars = [v1, v2, v3, v4, v5, v6, v7]\n\
    cnstrs = [ac1]\n\
    testcsp = CSP('test2', vars, cnstrs)\n\
    val = GacEnforce(cnstrs, testcsp, None, None)"

    if val != "DWO":
        fails[2] = True
        print("Error: GacEnforce failed to return \"DWO\" returned {} instead".format(val))

    if fails[2]:
        print("\nFail Q3 test 3\nErrors were generated on the following code:")
        print(test3)
    else:
        print("Pass Q3 test 3")
    print_sep()

    csp = nQueens(8, 'row')
    solutions, num_nodes = bt_search('GAC', csp, 'fixed', False, False)
    errors = csp.check(solutions)

    if len(errors) > 0:
        fails[3] = True
        print("Fail Q3 test 4: invalid solution(s) returned by GAC")
        for err in errors:
            print_soln(err[0])
            print("\n", err[1])

    if len(solutions) != 1:
        fails[3] = True
        print("Fail Q3 test 4: GAC failed to return only one solution")
        print("  returned: ")
        for s in solutions:
            print_soln(s)
            print("")
    ok=True
    for v in csp.variables():
        if set(v.curDomain()) != set(v.domain()):
            fails[3] = True
            print("Fail Q3 test 4: GAC failed to restore domains of variables")

    if not fails[3]:
        print("Pass Q3 test 4")
    print_sep()

    csp = nQueens(8, 'row')
    solutions, num_nodes = bt_search('GAC', csp, 'fixed', True, False)
    errors=csp.check(solutions)

    if len(errors) > 0:
        fails[4] = True
        print("Fail Q3 test 5: invalid solution(s) returned by GAC")
        for err in errors:
            print_soln(err[0])
            print("\n", err[1])

    if len(solutions) != 92:
        fails[4] = True
        print("Fail Q3 test 5: GAC failed to return 92 solutions")
        print("  returned {} solutions".format(len(solutions)))

    ok=True
    for v in csp.variables():
        if set(v.curDomain()) != set(v.domain()):
            fails[4] = True
            print("Fail Q3 test 5: GAC failed to restore domains of variables")

    if not fails[4]:
        print("Pass Q3 test 5")
    print_sep()

    grades[2] = 0
    # First 2 tests: GACEnforce
    # 3rd test: Checking DWO
    # Last 2 tests: returning single or all solutions
    if sum(fails[:2]) == 0:
        grades[2] += 3
        if not fails[2]:
            grades[2] +=1

        if sum([fails[3], fails[4]]) == 0:
            grades[2] += 3

def question_4():
    print_title(3)
    tested[3] = True
    fails = [False, False]
    if not tested[2]:
        print_sep('=')
        print("Q4 depends on Q3, running Q3 tests")
        question_3()
        print_sep('=')

    if grades[2] == 0:
        grades[3] = 0
        print("Q3 failed, cannot mark Q4")
        return

    try:        
        csp =  nQueens(6, 'alldiff')
    except:
        grades[3] = 0
        print("\nFail Q4, not implemented")
        return

    solutions, num_nodes = bt_search('BT', csp, 'fixed', True, False)
    solution_arr = []

    for s in solutions:
           for (var,val) in s:
               solution_arr.append(((var.name(),val)))

    solns = [('Q1', 2), ('Q2', 4), ('Q3', 6), ('Q4', 1), ('Q5', 3), ('Q6', 5),\
     ('Q1', 3), ('Q2', 6), ('Q3', 2), ('Q4', 5), ('Q5', 1), ('Q6', 4),\
      ('Q1', 4), ('Q2', 1), ('Q3', 5), ('Q4', 2), ('Q5', 6), ('Q6', 3),\
       ('Q1', 5), ('Q2', 3), ('Q3', 1), ('Q4', 6), ('Q5', 4), ('Q6', 2)]

    if len(solns) == len(solution_arr):
        for i in range(len(solns)):
            if solns[i] != solution_arr[i]:
                fails[0] = True
                print("Error: your solution == {}".format(solution_arr[i]))
                print("Correct solution should be == {}".format(solns[i]))
                print("Full correct solution (including all solutions) == {}".format(solns))
    else:
        fails[0] = True
        print("Error: length of solution == {0} and should be {1}".format(len(solution_arr), len(solns)))


    if fails[0]:
        print("\nFail Q4 test 1\nErrors were generated on the following code:")
        print("python3 nqueens.py -c -a BT -m alldiff 6")
    else:
        print("Pass Q4 test 1")
        print_sep()

    csp =  nQueens(6, 'alldiff')
    solutions, num_nodes = bt_search('GAC', csp, 'fixed', True, False)
    solution_arr = []

    for s in solutions:
           for (var,val) in s:
               solution_arr.append(((var.name(),val)))

    solns = [('Q1', 2), ('Q2', 4), ('Q3', 6), ('Q4', 1), ('Q5', 3), ('Q6', 5),\
     ('Q1', 3), ('Q2', 6), ('Q3', 2), ('Q4', 5), ('Q5', 1), ('Q6', 4),\
      ('Q1', 4), ('Q2', 1), ('Q3', 5), ('Q4', 2), ('Q5', 6), ('Q6', 3),\
       ('Q1', 5), ('Q2', 3), ('Q3', 1), ('Q4', 6), ('Q5', 4), ('Q6', 2)]


    if len(solns) == len(solution_arr):
        for i in range(len(solns)):
            if solns[i] != solution_arr[i]:
                fails[1] = True
                print("Error: your solution == {}".format(solution_arr[i]))
                print("Correct solution should be == {}".format(solns[i]))
                print("Full correct solution (including all solutions) == {}".format(solns))
    else:
        fails[1] = True
        print("Error: length of solution == {0} and should be {1}".format(len(solution_arr), len(solns)))
        

    if fails[1]:
        print("\nFail Q4 test 2\nErrors were generated on the following code:")
        print("python3 nqueens.py -c -a GAC -m alldiff 6")
    else:
        print("Pass Q4 test 2")
        print_sep()

    if any(fails):
        grades[3] = 0
    else:
        grades[3] = outof[3]


def question_5():
    print_title(4)
    fails = [False]*2

    test1= "    v1 = Variable('V1', [1, 2])\n\
    v2 = Variable('V2', [1, 2])\n\
    v3 = Variable('V3', [1, 2, 3, 4, 5])\n\
    v4 = Variable('V4', [1, 2, 3, 4, 5])\n\
    v5 = Variable('V5', [1, 2, 3, 4, 5])\n\
    v6 = Variable('V6', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v7 = Variable('V7', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v8 = Variable('V8', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v9 = Variable('V9', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    vars = [v1, v2, v3, v4, v5, v6, v7, v8, v9]\n\
    nv9 = NValuesConstraint('9', vars, [9], 4, 5)\n\
    testcsp = CSP('test', vars, [nv9])\n\
    GacEnforce([nv9], testcsp, None, None)"

    v1 = Variable('V1', [1, 2])
    v2 = Variable('V2', [1, 2])
    v3 = Variable('V3', [1, 2, 3, 4, 5])
    v4 = Variable('V4', [1, 2, 3, 4, 5])
    v5 = Variable('V5', [1, 2, 3, 4, 5])
    v6 = Variable('V6', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v7 = Variable('V7', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v8 = Variable('V8', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v9 = Variable('V9', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    vars = [v1, v2, v3, v4, v5, v6, v7, v8, v9]
    nv9 = NValuesConstraint('9', vars, [9], 4, 5)
    testcsp = CSP('test', vars, [nv9])
    GacEnforce([nv9], testcsp, None, None)
    soln_doms = [set([1, 2]), set([1, 2]), set([1, 2, 3, 4, 5]),
                 set([1, 2, 3, 4, 5]), set([1, 2, 3, 4, 5]), set([9]),
                 set([9]), set([9]), set([9])]

    for i, v in enumerate(vars):
        if set(v.curDomain()) != soln_doms[i]:
            fails[0] = True
            print("Error: {}.curDomain() == {}".format(v.name(), v.curDomain()))
            print("Correct curDomin should be == {}".format(list(soln_doms[i])))

    if fails[0]:
        print("\nFail Q5 test 1\nErrors were generated on the following code:")
        print(test1)
    else:
        print("Pass Q5 test 1")
        print_sep()

    test2 = "    v1 = Variable('V1', [1, 2])\n\
    v2 = Variable('V2', [1, 2])\n\
    v3 = Variable('V3', [1, 2, 3, 4, 5])\n\
    v4 = Variable('V4', [1, 2, 3, 4, 5])\n\
    v5 = Variable('V5', [1, 2, 3, 4, 5])\n\
    v6 = Variable('V6', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v7 = Variable('V7', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v8 = Variable('V8', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    v9 = Variable('V9', [1, 2, 3, 4, 5, 6, 7, 8, 9])\n\
    vars = [v1, v2, v3, v4, v5, v6, v7, v8, v9]\n\
    nv9 = NValuesConstraint('9', vars, [9], 4, 5)\n\
    nv1 = NValuesConstraint('1', vars, [1], 5, 5)\n\
    testcsp = CSP('test', vars, [nv1, nv9])\n\
    GacEnforce([nv1, nv9], testcsp, None, None)"


    v1 = Variable('V1', [1, 2])
    v2 = Variable('V2', [1, 2])
    v3 = Variable('V3', [1, 2, 3, 4, 5])
    v4 = Variable('V4', [1, 2, 3, 4, 5])
    v5 = Variable('V5', [1, 2, 3, 4, 5])
    v6 = Variable('V6', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v7 = Variable('V7', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v8 = Variable('V8', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    v9 = Variable('V9', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    vars = [v1, v2, v3, v4, v5, v6, v7, v8, v9]
    nv9 = NValuesConstraint('9', vars, [9], 4, 5)
    nv1 = NValuesConstraint('1', vars, [1], 5, 5)
    testcsp = CSP('test', vars, [nv1, nv9])
    GacEnforce([nv1, nv9], testcsp, None, None)
    soln_doms = [set([1]), set([1]), set([1]), set([1]), set([1]),
                 set([9]), set([9]), set([9]), set([9])]

    for i, v in enumerate(vars):
        if set(v.curDomain()) != soln_doms[i]:
            fails[1] = True
            print("Error: {}.curDomain() == {}".format(v.name(), v.curDomain()))
            print("Correct curDomin should be == {}".format(list(soln_doms[i])))

    if fails[1]:
        print("\nFail Q5 test 2\nErrors were generated on the following code:")
        print(test2)
    else:
        print("Pass Q5 test 2")
        print_sep()

    if not any(fails):
        grades[4] = outof[4]


def question_6():
    print_title(5)
    fails = [False, False, False, False, False, False, False, False]

    def do_test(n, cmd, pi, nsolns, complete=True):
        solns = solve_schedules(pi, 'GAC', complete, 'mrv', True)
        if len(solns) != nsolns:
            fails[n] = True
            print("Error: expected {} solution()s got {}".format(nsolns,
                                                                 len(solns)))
        for s in solns:
            if not check_schedule_solution(pi, s):
                print("Error: got invalid solution")
                fails[n] = True
                break

        if fails[n]:
            print("\nFail Q6 test {}\nErrors were generated on the following code:".format(n+1))
            print(cmd)
        else:
            print("Pass Q6 test {}".format(n+1))
        print_sep()

    try:        
        do_test(1, "python3 class_scheduling.py -a GAC -c 2", c2, 0)
    except:
        print("Fail Q6, not implmented")
        grades[5] = 0
        return

    # 5 different tests for class scheduling 
    do_test(1, "python3 class_scheduling.py -a GAC -c 2", c2, 0)
    do_test(2, "python3 class_scheduling.py -a GAC -c 3", c3, 0)
    do_test(3, "python3 class_scheduling.py -a GAC -c 4", c4, 0)
    do_test(4, "python3 class_scheduling.py -a GAC -c 5", c5, 2)
    do_test(5, "python3 class_scheduling.py -a GAC -c 6", c6, 6)

    

    grades[5] = 0
    if sum(fails[:4]) != 0:
        grades[5] = 0
    else:
        if not fails[4]:
            grades[5] += 2
        if not fails[5]:
            grades[5] += 2

def outputGrades():
    print_sep('=')
    for i in range(len(grades)):
        print("Q{} mark = {}/{}".format(i+1, grades[i], outof[i]))
        print("-"*30)
    print("Total Mark = {}/{}".format(sum(grades), sum(outof)))
    print("The mark given by the autograder is not your final mark. More tests might be run")
    print("You are not done yet. You must also submit your assignment")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Autograder for Assignment 3')
    parser.add_argument("-q", "--question", help="The question (1-6) to mark")
    args = parser.parse_args()

    if args.question:
        if args.question not in legalQs:
            print("Error: autograder only knows how to evaluate one of {}".format(legalQs))
            exit(1)

        if args.question == legalQs[0]:
            question_1()
        if args.question == legalQs[1]:
            question_2()
        if args.question == legalQs[2]:
            question_3()
        if args.question == legalQs[3]:
            question_4()
        if args.question == legalQs[4]:
            question_5()
        if args.question == legalQs[5]:
            question_6()


    else:
        question_1()
        question_2()
        question_3()
        question_4()
        question_5()
        question_6()


    outputGrades()
