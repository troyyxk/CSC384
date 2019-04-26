from csp import Constraint, Variable
import util

class TableConstraint(Constraint):
    '''General type of constraint that can be use to implement any type of
       constraint. But might require a lot of space to do so.

       A table constraint explicitly stores the set of satisfying
       tuples of assignments.'''

    def __init__(self, name, scope, satisfyingAssignments):
        '''Init by specifying a name and a set variables the constraint is over.
           Along with a list of satisfying assignments.
           Each satisfying assignment is itself a list, of length equal to
           the number of variables in the constraints scope.
           If sa is a single satisfying assignment, e.g, sa=satisfyingAssignments[0]
           then sa[i] is the value that will be assigned to the variable scope[i].


           Example, say you want to specify a constraint alldiff(A,B,C,D) for
           three variables A, B, C each with domain [1,2,3,4]
           Then you would create this constraint using the call
           c = TableConstraint('example', [A,B,C,D],
                               [[1, 2, 3, 4], [1, 2, 4, 3], [1, 3, 2, 4],
                                [1, 3, 4, 2], [1, 4, 2, 3], [1, 4, 3, 2],
                                [2, 1, 3, 4], [2, 1, 4, 3], [2, 3, 1, 4],
                                [2, 3, 4, 1], [2, 4, 1, 3], [2, 4, 3, 1],
                                [3, 1, 2, 4], [3, 1, 4, 2], [3, 2, 1, 4],
                                [3, 2, 4, 1], [3, 4, 1, 2], [3, 4, 2, 1],
                                [4, 1, 2, 3], [4, 1, 3, 2], [4, 2, 1, 3],
                                [4, 2, 3, 1], [4, 3, 1, 2], [4, 3, 2, 1]])
          as these are the only assignments to A,B,C respectively that
          satisfy alldiff(A,B,C,D)
        '''

        Constraint.__init__(self,name, scope)
        self._name = "TableCnstr_" + name
        self.satAssignments = satisfyingAssignments

    def check(self):
        '''check if current variable assignments are in the satisfying set'''
        assignments = []
        for v in self.scope():
            if v.isAssigned():
                assignments.append(v.getValue())
            else:
                return True
        return assignments in self.satAssignments

    def hasSupport(self, var,val):
        '''check if var=val has an extension to an assignment of all variables in
           constraint's scope that satisfies the constraint. Important only to
           examine values in the variable's current domain as possible extensions'''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in
        vindex = self.scope().index(var)
        found = False
        for assignment in self.satAssignments:
            if assignment[vindex] != val:
                continue   #this assignment can't work it doesn't make var=val
            found = True   #Otherwise it has potential. Assume found until shown otherwise
            for i, v in enumerate(self.scope()):
                if i != vindex and not v.inCurDomain(assignment[i]):
                    found = False  #Bummer...this assignment didn't work it assigns
                    break          #a value to v that is not in v's curDomain
                                   #note we skip checking if val in in var's curDomain
            if found:     #if found still true the assigment worked. We can stop
                break
        return found     #either way found has the right truth value


class QueensConstraint(Constraint):
    '''Queens constraint between queen in row i and row j'''
    def __init__(self, name, qi, qj, i, j):
        scope = [qi, qj]
        Constraint.__init__(self,name, scope)
        self._name = "QueenCnstr_" + name
        self.i = i
        self.j = j

    def check(self):
        qi = self.scope()[0]
        qj = self.scope()[1]
        if not qi.isAssigned() or not qj.isAssigned():
            return True
        return self.queensCheck(qi.getValue(),qj.getValue())

    def queensCheck(self, vali, valj):
        diag = abs(vali - valj) == abs(self.i - self.j)
        return not diag and vali != valj
    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''
        #hasSupport for this constraint is easier as we only have one
        #other variable in the constraint.
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in
        otherVar = self.scope()[0]
        if otherVar == var:
            otherVar = self.scope()[1]
        for otherVal in otherVar.curDomain():
            if self.queensCheck(val, otherVal):
                return True
        return False

class QueensTableConstraint(TableConstraint):
    '''Queens constraint between queen in row i and row j, but
       using a table constraint instead. That is, you
       have to create and add the satisfying tuples.

       Since we inherit from TableConstraint, we can
       call TableConstraint.__init__(self,...)
       to set up the constraint.

       Then we get hasSupport and check automatically from
       TableConstraint
    '''
    #your implementation for Question 1 goes
    #inside of this class body. You must not change
    #the existing function signatures.
    def __init__(self, name, qi, qj, i, j):
        self._name = "Queen_" + name
        scope = [qi, qj]
        cons_assignment = []
        for q_i in qi.domain():
            for q_j in qj.domain():
                if (q_i != q_j) and (abs(q_i - q_j) != abs(i - j)):  # not on the same column and not diagonos
                    cons_assignment.append([q_i, q_j])
        TableConstraint.__init__(self, name, scope, cons_assignment)

    # def __init__(self, name, scope, satisfyingAssignments):

class NeqConstraint(Constraint):
    '''Neq constraint between two variables'''
    def __init__(self, name, scope, i, j):
        if len(scope) != 2:
            print("Error Neq Constraints are only between two variables")
        Constraint.__init__(self,name, scope)
        self._name = "NeqCnstr_" + name
        self._abs_diff = abs(i - j)

    def check(self):
        v0 = self.scope()[0]
        v1 = self.scope()[1]
        if not v0.isAssigned() or not v1.isAssigned():
            return True
        return self._abs_diff != abs(v0.getValue() - v1.getValue())

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''
        #hasSupport for this constraint is easier than AllDiff as we only have one
        #other variable in the constraint.
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in
        otherVar = self.scope()[0]
        if otherVar == var:
            otherVar = self.scope()[1]
        
        def notEqual(l):
            return self._abs_diff != abs(l[0][1] - l[1][1])

        return findvals([otherVar], [(var, val)], notEqual, notEqual)


class AllDiffConstraint(Constraint):
    '''All diff constraint between a set of variables'''
    def __init__(self, name, scope):
        Constraint.__init__(self,name, scope)
        self._name = "AllDiff_" + name

    def check(self):
        assignments = []
        for v in self.scope():
            if v.isAssigned():
                assignments.append(v.getValue())
            else:
                return True
        return len(set(assignments)) == len(assignments)

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in

        #since the constraint has many variables use the helper function 'findvals'
        #for that we need two test functions
        #1. for testing complete assignments to the constraint's scope
        #   return True if and only if the complete assignment satisfies the constraint
        #2. for testing partial assignments to see if they could possibly work.
        #   return False if the partial assignment cannot be extended to a satisfying complete
        #   assignment
        #
        #Function #2 is only needed for efficiency (sometimes don't have one)
        #  if it isn't supplied findvals will use a function that never returns False
        #
        #For alldiff, we do have both functions! And they are the same!
        #We just check if the assignments are all to different values. If not return False
        def valsNotEqual(l):
            '''tests a list of assignments which are pairs (var,val)
               to see if they can satisfy the all diff'''
            vals = [val for (var, val) in l]
            return len(set(vals)) == len(vals)
        varsToAssign = self.scope()
        varsToAssign.remove(var)
        x = findvals(varsToAssign, [(var, val)], valsNotEqual, valsNotEqual)
        return x


def findvals(remainingVars, assignment, finalTestfn, partialTestfn=lambda x: True):
    '''Helper function for finding an assignment to the variables of a constraint
       that together with var=val satisfy the constraint. That is, this
       function looks for a supporing tuple.

       findvals uses recursion to build up a complete assignment, one value
       from every variable's current domain, along with var=val.

       It tries all ways of constructing such an assignment (using
       a recursive depth-first search).

       If partialTestfn is supplied, it will use this function to test
       all partial assignments---if the function returns False
       it will terminate trying to grow that assignment.

       It will test all full assignments to "allVars" using finalTestfn
       returning once it finds a full assignment that passes this test.

       returns True if it finds a suitable full assignment, False if none
       exist. (yes we are using an algorithm that is exactly like backtracking!)'''

    #sort the variables call the internal version with the variables sorted
    remainingVars.sort(reverse=True, key=lambda v: v.curDomainSize())
    return findvals_(remainingVars, assignment, finalTestfn, partialTestfn)

def findvals_(remainingVars, assignment, finalTestfn, partialTestfn):
    '''findvals_ internal function with remainingVars sorted by the size of
       their current domain'''
    if len(remainingVars) == 0:
        return finalTestfn(assignment)
    var = remainingVars.pop()
    for val in var.curDomain():
        assignment.append((var, val))
        if partialTestfn(assignment):
            if findvals_(remainingVars, assignment, finalTestfn, partialTestfn):
                return True
        assignment.pop()   #(var,val) didn't work since we didn't do the return
    remainingVars.append(var)
    return False


class NValuesConstraint(Constraint):
    '''NValues constraint over a set of variables.  Among the variables in
       the constraint's scope the number that have been assigned
       values in the set 'required_values' is in the range
       [lower_bound, upper_bound] (lower_bound <= #of variables
       assigned 'required_value' <= upper_bound)

       For example, if we have 4 variables V1, V2, V3, V4, each with
       domain [1, 2, 3, 4], then the call
       NValuesConstraint('test_nvalues', [V1, V2, V3, V4], [3,2], 2,
       3) will only be satisfied by assignments such that at least 2
       the V1, V2, V3, V4 are assigned the value 3 or 2, and at most 3
       of them have been assigned the value 3 or 2.

    '''

    #Question 5 you have to complete the implementation of
    #check() and hasSupport. You can change __init__ if you want
    #but do not change its parameters.

    def __init__(self, name, scope, required_values, lower_bound, upper_bound):
        Constraint.__init__(self,name, scope)
        self._name = "NValues_" + name
        self._required = required_values
        self._lb = lower_bound
        self._ub = upper_bound

    def check(self):
        amount = 0
        for v in self.scope():
            if not v.isAssigned():
                return True
            # print(v.getValue)
            if v.getValue() in self._required:
                amount += 1
        if amount <= self._ub and amount >= self._lb:
            return True
        return False
        # amount = [0 for i in range(len(self._required))]
        # for cur_var in self.scope():
        #     if not cur_var.isAssigned():
        #         return True
        #     if cur_var in self._required:
        #         ind = self._required.index(cur_var)
        #         amount[ind] += 1
        #         if amount[ind] > self._ub:
        #             return False
        # for i in amount:
        #     if i < self._lb:
        #         return False
        # return True

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint

           HINT: check the implementation of AllDiffConstraint.hasSupport
                 a similar approach is applicable here (but of course
                 there are other ways as well)
        '''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in

        def inBound(l):
            ''' nvalue
            '''
            amount = 0
            vals = [val for (var, val) in l]
            for v in vals:
                if v in self._required:
                    amount += 1
            if amount <= self._ub and amount >= self._lb:
                return True
            return False

        varsToAssign = self.scope()
        varsToAssign.remove(var)
        x = findvals(varsToAssign, [(var, val)], inBound)
        return x


class taftercConstraint(Constraint):
    ''' c2
    '''

    def __init__(self, name, scope, lec_list, tut_list):
        Constraint.__init__(self,name, scope)
        self._name = "tafterc" + name
        self.lec_list = lec_list
        self.tut_list = tut_list

    def check(self):
        # f for first
        flec = -1
        ftut = -1
        for cur_var in self.scope():
            if not cur_var.isAssigned():
                return True

            if cur_var.getValue() in self.lec_list and flec < 0:
                flec = self.scope().index(cur_var)
            if cur_var.getValue() in self.tut_list and ftut < 0:
                ftut = self.scope().index(cur_var)
        if flec < 0 or ftut < 0:
            print("Error flec < 0 or ftut < 0")
            return False
        return flec < ftut

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint

           HINT: check the implementation of AllDiffConstraint.hasSupport
                 a similar approach is applicable here (but of course
                 there are other ways as well)
        '''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in

        def inBound(l):
            '''tests a list of assignments which are pairs (var,val)
               to see if they can satisfy the all diff'''
            flec = -1
            ftut = -1
            vals = [val for (var, val) in l]
            for v in vals:
                if v in self.lec_list and flec < 0:
                    flec = vals.index(v)
                if v in self.tut_list and ftut < 0:
                    ftut = vals.index(v)
            return flec < ftut


        varsToAssign = self.scope()
        varsToAssign.remove(var)
        x = findvals(varsToAssign, [(var, val)], inBound)
        return x

# close distance building
class cdbConstraint(Constraint):
    ''' c3
    '''

    def __init__(self, name, scope, close_distance_buildings):
        Constraint.__init__(self,name, scope)
        self._name = "tafterc" + name
        self.cdb = close_distance_buildings

    def check(self):
        prev_c = None
        cur_c = None
        for cur_var in self.scope():
            if not cur_var.isAssigned():
                return True

            prev_c = cur_c
            cur_c = cur_var
            
            if prev_c is not None and cur_c is not None:
                if prev_c.getValue() != "NOCLASS" and cur_c.getValue() != "NOCLASS":
                    info_p = prev_c.getValue().split('-')
                    prev_b = info_p[1]
                    info_c = cur_c.getValue().split('-')
                    cur_b = info_c[1]
                    if prev_b not in self.cdb[cur_b]:
                        return False
        return True

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint

           HINT: check the implementation of AllDiffConstraint.hasSupport
                 a similar approach is applicable here (but of course
                 there are other ways as well)
        '''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in

        def inBound(l):
            '''tests a list of assignments which are pairs (var,val)
               to see if they can satisfy the all diff'''

            vals = [val for (var, val) in l]
            prev_c = None
            cur_c = None
            for v in vals:
                prev_c = cur_c
                cur_c = v

            if prev_c is not None and cur_c is not None:
                if prev_c != "NOCLASS" and cur_c != "NOCLASS":
                    info_p = prev_c.split('-')
                    prev_b = info_p[1]
                    info_c = cur_c.split('-')
                    cur_b = info_c[1]
                    if prev_b not in self.cdb[cur_b]:
                        return False
            return True


        varsToAssign = self.scope()
        varsToAssign.remove(var)
        x = findvals(varsToAssign, [(var, val)], inBound)
        return x

# rf for rest frequence
class rfConstraint(Constraint):
    ''' c3
    '''

    def __init__(self, name, scope, rest_frequence):
        Constraint.__init__(self,name, scope)
        self._name = "tafterc" + name
        self.rf = rest_frequence

    def check(self):
        count = 0
        for cur_var in self.scope():
            if not cur_var.isAssigned():
                return True

            if cur_var.getValue() == "NOCLASS":
                count = 0
            else:
                count += 1

            if count >= self.rf:
                return False

        return True


    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint

           HINT: check the implementation of AllDiffConstraint.hasSupport
                 a similar approach is applicable here (but of course
                 there are other ways as well)
        '''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in

        def inBound(l):
            '''tests a list of assignments which are pairs (var,val)
               to see if they can satisfy the all diff'''

            vals = [val for (var, val) in l]
            count = 0
            for v in vals:
                if v == "NOCLASS":
                    count = 0
                else:
                    count += 1
                if count >= self.rf:
                    return False
            return True


        varsToAssign = self.scope()
        varsToAssign.remove(var)
        x = findvals(varsToAssign, [(var, val)], inBound)
        return x