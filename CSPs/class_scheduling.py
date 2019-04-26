import csp_problems
import backtracking
import argparse
import itertools
import random

#test-sequence--one solution (only one legal sequencing)
c1 = csp_problems.ScheduleProblem(
  #courses
  ['CSC108'],
  #classes
  ['CSC108-BA-2-LEC-01', 'CSC108-BA-3-TUT-01'],
  #buildings
  ['BA'],
  #number of time slots
  3,
  # connected buildings
  [],
  #min rest frequency
  3
)

#no solution due to lecture/tutorial order
c2 = csp_problems.ScheduleProblem(
  #courses
  ['CSC108', 'CSC165'],
  #classes
  ['CSC108-SF-2-LEC-01',
   'CSC108-SF-1-TUT-01',
   'CSC165-MP-4-LEC-01',
   'CSC165-MP-5-TUT-01'],
  #buildings
  ['SF', 'MP'],
  #number of time slots
  5,
  # connected building
  [('SF', 'MP')],
  #min rest frequency
  5
)

#no solution due to building connectivity
c3 = csp_problems.ScheduleProblem(
  #courses
  ['CSC108', 'CSC165'],
  #classes
  ['CSC108-SF-1-LEC-01',
   'CSC108-SF-2-TUT-01',
   'CSC165-MP-3-LEC-01',
   'CSC165-MP-4-TUT-01'],
  #buildings
  ['SF', 'MP'],
  #number of time slots
  5,
  # connected building
  [],
  #min rest frequency
  5
)

#no solution due to frequency
c4 = csp_problems.ScheduleProblem(
  #courses
  ['CSC108', 'CSC165'],
  #classes
  ['CSC108-SF-1-LEC-01',
   'CSC108-SF-2-TUT-01',
   'CSC165-MP-3-LEC-01',
   'CSC165-MP-4-TUT-01'],
  #buildings
  ['SF', 'MP'],
  #number of time slots
  5,
  # connected building
  [('SF', 'MP')],
  #min rest frequency
  3
)

#multiple solutions
c5 = csp_problems.ScheduleProblem(
  #courses
  ['CSC108'],
  #classes
  ['CSC108-BA-1-LEC-01', 'CSC108-BA-2-LEC-02', 'CSC108-BA-3-TUT-01'],
  #buildings
  ['BA'],
  #number of time slots
  3,
  # connected buildings
  [],
  #min rest frequency
  3
)

c6 = csp_problems.ScheduleProblem(
  #courses
  ['CSC108', 'CSC165', 'MAT137'],
  #classes
  ['CSC108-BA-1-LEC-01', 
   'CSC108-MP-2-LEC-02', 
   'CSC108-SF-4-TUT-01',
   'CSC165-BA-3-LEC-01', 
   'CSC165-MP-5-LEC-02', 
   'CSC165-MP-6-TUT-01', 
   'CSC165-MP-8-TUT-02',
   'MAT137-SF-7-LEC-01', 
   'MAT137-BA-5-LEC-02', 
   'MAT137-SF-10-TUT-01', 
   'MAT137-SF-9-TUT-02'],
  #buildings
  ['BA', 'MP', 'SF'],
  #number of time slots
  10,
  # connected buildings
  [('BA', 'MP'), ('BA', 'SF')],
  #min rest frequency
  6
)

LEC = 'LEC'
TUT = 'TUT'
NOCLASS = 'NOCLASS'

# number of courses
n = 5
# number of buildings
l = 5

slots = random.randint(n * 2, n * 3)
rest = random.randint(slots // 2, slots)

MAX_LEC_SECTIONS = 3
MAX_TUT_SECTIONS = 3

def custom_shuffle(array):
  random.shuffle(array)
  return array

courses = ['CSC' + str(i) for i in range(1, n+ 1)]
buildings = ['R' + str(i) for i in range(1, l + 1)]

classes = []
for class_i in range(1, n + 1):
  for type in [TUT, LEC]:
    max_sections = MAX_LEC_SECTIONS if type == LEC else MAX_TUT_SECTIONS
    for i in range(1, random.randint(1, max_sections) + 1):
      classes.append('CSC{}-{}-{}-{}-{}'.format(class_i, 'R' + str(random.randint(1, l)), random.randint(1, min(slots, slots // 3 + 3)) if type == LEC else random.randint(min(slots, slots // 3), slots), type, i))

connected_buildings = custom_shuffle(list(itertools.combinations(['R' + str(i + 1) for i in range(l)], r=2)))[:random.randint(l, l * (l - 1) / 2)]

c7 = csp_problems.ScheduleProblem(
  #courses
  courses,
  #classes
  classes,
  #buildings
  buildings,
  #number of time slots
  slots,
  # connected building
  connected_buildings,
  #min rest frequency
  rest
)

problems = [c1, c2, c3, c4, c5, c6, c7]

def get_class_info(class_section):
  space_index = class_section.index(' ')
  return class_section[:space_index], class_section[space_index + 1:]

def check_schedule_solution(problem, schedule):
  if len(schedule) == 0:
    return False
  tests = [check_valid_classes, 
           check_consecutive_classes_buildings, check_taken_courses_once, 
           check_resting]
  
  for test in tests:
      if not test(problem, schedule):
        return False

  return True

def check_valid_classes(problem, schedule):
  for time_slot in schedule:
    if time_slot == NOCLASS:
      continue
    if time_slot not in problem.classes:
      print("Error solution invalid, non-existent class {} in the schedule".format(c))
      return False
  return True

def check_consecutive_classes_buildings(problem, schedule):
  for i, _ in enumerate(schedule):
    if i + 1 == len(schedule) or schedule[i] == NOCLASS or schedule[i + 1] == NOCLASS:
      continue
    
    building_1 = schedule[i].split('-')[1]
    building_2 = schedule[i + 1].split('-')[1]
    if building_2 not in problem.connected_buildings(building_1):
      print("Error solution invalid, consecutive classes {}, {} in the schedule is too far apart".format(schedule[i], schedule[i + 1]))
      return False

  return True      

def check_taken_courses_once(problem, schedule):
  checklist = dict()
  for course in problem.courses:
    checklist[course] = [0, 0]

  for class_1 in schedule:
    if class_1 == NOCLASS:
      continue
    class_1_info = class_1.split('-')
    if class_1_info[0] not in checklist:
      print("Error solution invalid, class {} should not be taken by the student".format(course_1))
      return False

    if class_1_info[3] == LEC:
      checklist[class_1_info[0]][0] += 1

    if class_1_info[3] == TUT:
      if checklist[class_1_info[0]][0] == 0:
        print("Error solution invalid, tutorial for class {} should not be taken before lecture".format(class_1))
        return False
      checklist[class_1_info[0]][1] += 1

  if any([val > 1 for val in checklist[class_1_info[0]]]):
    print("Error solution invalid, class {} is taken more than once for some class type".format(class_1))
    return False

  for key in checklist:
    if checklist[key][0] + checklist[key][1] < 2:
      print("Error solution invalid, class {} is taken less than once for some class type".format(key))
      return False
  return True

def check_resting(problem, schedule):
  if len(schedule) < problem.min_rest_frequency:
    return True
  for i in range(len(schedule) - problem.min_rest_frequency + 1):
    count = 0
    for j in range(problem.min_rest_frequency):
      if schedule[i + j] == NOCLASS:
        count += 1
    if count == 0:
      print("Error solution invalid, student takes to many classes before resting")
      return False
  return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve a class scheduling csp problem')
    parser.add_argument("p", help="The problem number to solve", type=int)
    parser.add_argument("-a", "--algorithm", help="which backtracking algorithm to use", choices=['BT', 'FC', 'GAC'], default='GAC')
    parser.add_argument("-c", "--allSolns", help="Complete search (Find all solutions)", action="store_true")
    parser.add_argument("-v", "--varHeur", help="Heuristic for selecting next variable to assign", choices=['fixed', 'random', 'mrv'], default='mrv')
    parser.add_argument("-t", "--trace", help="Trace the search", action="store_true")
    args = parser.parse_args()

    if args.p < 1 or args.p > len(problems):
        print("{} is invalid problem number. I only know about problems {} to {}".format(args.b, 1, len(boards)))
        print("If you want to add new problems define them and add them to the list \"problems\"")
        exit(1)

    ip = problems[args.p-1]
    print("="*66)
    print("Solving problem {}".format(args.p))
    print("Courses: {}".format(ip.courses))
    print("Classes: {}".format(ip.classes))
    print("Buildings: {}".format(ip.buildings))
    print("Adjacency List:")
    for i in ip.buildings:
      print("Building {}: {}".format(i, ip.connected_buildings(i)))
    print("Rest Frequency: {}".format(ip.min_rest_frequency))
    print("Number of Time Slots: {}".format(ip.num_time_slots))
    print("Solving using {}".format(args.algorithm))
    solns = csp_problems.solve_schedules(ip, args.algorithm, args.allSolns, args.varHeur, False, args.trace)
    print("")
    for i, s in enumerate(solns):
        print("Solution {}.".format(i+1))
        if not check_schedule_solution(ip, s):
            print("ERROR solution is invalid")
    
        print(s)
        print("------------------------------\n")