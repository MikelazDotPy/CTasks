from dataclasses import dataclass
from math import comb, prod, perm
from re import fullmatch, finditer, sub

from ortools.sat.python import cp_model


@dataclass
class Conditions:
    uniq: bool = False
    non_xx: bool = False
    nonzero: bool = False
    less: bool = False
    le: bool = False
    great: bool = False
    ge: bool = False


class ORToolsSolutions(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, conds: Conditions, happy_count, start, end, set_size):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.conds = conds
        self.happy_count = happy_count
        self.mx = end - start + 1
        self.end = end
        self.start = start
        self.set_size = set_size
        self.formula = self.get_formula()
        self.ans = 0
    
    def cless(self, solution):
        if len(solution) == 0:
            return comb(self.mx, self.set_size)
        items = list(solution.items())
        items.sort(key=lambda x: x[0])
        bounds = [(items[i + 1][0] - items[i][0] - 1, items[i][1] - items[i + 1][1] - 1) for i in range(len(items) - 1)]
        if 0 not in solution:
            bounds = [(items[0][0], self.end - items[0][1])] + bounds
        if self.set_size - 1 not in solution:
            bounds += [(self.set_size - items[-1][0] - 1, items[-1][1] - self.start)]
        return prod(comb(ot[1], ot[0]) for ot in bounds)
        
    def cgreat(self, solution):
        if len(solution) == 0:
            if self.conds.nonzero:
                return comb(self.mx, self.set_size) - comb(self.mx - 1, self.set_size - 1)
            return comb(self.mx, self.set_size)
        items = list(solution.items())
        items.sort(key=lambda x: x[0])
        bounds = [(items[i + 1][0] - items[i][0] - 1, items[i + 1][1] - items[i][1] - 1) for i in range(len(items) - 1)]
        if 0 not in solution:
            bounds = [(items[0][0], items[0][1] - self.start)] + bounds
        if self.set_size - 1 not in solution:
            bounds += [(self.set_size - items[-1][0] - 1, self.end - items[-1][1])]

        p = prod(comb(ot[1], ot[0]) for ot in bounds[1:])
        if self.conds.nonzero:
            return p*(comb(bounds[0][1] , bounds[0][0]) - comb(bounds[0][1] - 1 , bounds[0][0] - 1))
        return p*comb(bounds[0][1], bounds[0][0])

    def cle(self, solution):
        if len(solution) == 0:
            if self.conds.nonzero:
                return comb(self.mx + self.set_size - 1, self.set_size) - 1
            return comb(self.mx + self.set_size - 1, self.set_size)
        items = list(solution.items())
        items.sort(key=lambda x: x[0])
        bounds = [(items[i + 1][0] - items[i][0] - 1, items[i][1] - items[i + 1][1] + 1) for i in range(len(items) - 1)]
        if 0 not in solution:
            bounds = [(items[0][0], self.end - items[0][1] + 1)] + bounds
        if self.set_size - 1 not in solution:
            bounds += [(self.set_size - items[-1][0] - 1, items[-1][1] - self.start + 1)]

        if self.conds.nonzero and bounds[0][1] == self.mx:
            p = prod(comb(ot[1] + ot[0] - 1, ot[0]) for ot in bounds[1:])
            return p*(comb(bounds[0][1] + bounds[0][0] - 1, bounds[0][0]) - comb(bounds[0][1] + bounds[0][0] - 2, bounds[0][0] - 1))
        return prod(comb(ot[1] + ot[0] - 1, ot[0]) for ot in bounds)
    
    def cge(self, solution):
        if len(solution) == 0:
            if self.conds.nonzero:
                return comb(self.mx + self.set_size - 1, self.set_size) - comb(self.mx + self.set_size - 2, self.set_size - 1)
            return comb(self.mx + self.set_size - 1, self.set_size)
        items = list(solution.items())
        items.sort(key=lambda x: x[0])
        bounds = [(items[i + 1][0] - items[i][0] - 1, items[i][1] - items[i + 1][1] + 1) for i in range(len(items) - 1)]
        if 0 not in solution:
            bounds = [(items[0][0], self.end - items[0][1] + 1)] + bounds
        if self.set_size - 1 not in solution:
            bounds += [(self.set_size - items[-1][0] - 1, items[-1][1] - self.start + 1)]

        if self.conds.nonzero:
            return prod(comb(ot[1] + ot[0] - 1, ot[0]) for ot in bounds)
        return prod(comb(ot[1] + ot[0] - 1, ot[0]) for ot in bounds)

    def get_formula(self):
        if self.conds.ge and self.conds.le:
            return lambda s: 1

        if self.conds.uniq:
            if self.conds.nonzero:
                if self.conds.less:
                    return self.cless
                elif self.conds.great:
                    return self.cgreat
                else:
                    return lambda s: (self.mx-1)*perm(self.mx-1, self.happy_count - 1)
            else:
                if self.conds.less:
                    return self.cless
                elif self.conds.great:
                    return self.cgreat
                else:
                    return lambda s: perm(self.mx, self.happy_count)
        else:
            if self.conds.nonzero:
                if self.conds.non_xx:
                    return lambda s: (self.mx - 1)**(self.happy_count)
                else:
                    if self.conds.le:
                        return self.cle
                    elif self.conds.ge:
                        return self.cge
                    else:
                        return lambda s: (self.mx-1)*self.mx**(self.happy_count - 1)
            else:
                if self.conds.non_xx:
                    return lambda s: (self.mx - 1)**self.happy_count if 0 in s else self.mx*(self.mx - 1)**(self.happy_count - 1)
                else:
                    if self.conds.le:
                        return self.cle
                    elif self.conds.ge:
                        return self.cge
                    else:
                        return lambda s: self.mx**(self.happy_count)

    def on_solution_callback(self):
        solution = {k: self.Value(var) for k, var in self.__variables.items()}
        self.ans += self.formula(solution)

    def get_solutions(self):
        return self.ans


def check_eq(s1, s2):
    if not s1 or not s2:
        return False
    if fullmatch(r"^\s*(\d+|\[\d+\])\s*([\+\-]\s*(\d+|\[\d+\])\s*)*\s*$", s1) is None:
        return False
    if fullmatch(r"^\s*(\d+|\[\d+\])\s*([\+\-]\s*(\d+|\[\d+\])\s*)*\s*$", s2) is None:
        return False

    return True


def check_idxs(eq, xc):
    for x in finditer(r"(\[\d+\])", eq):
        if int(x.group()[1:-1]) >= xc:
            return False
    for x in finditer(r"\{(\d+);(\d+)\}", eq):
        if int(x.group(1)) >= xc or int(x.group(2)) >= xc or int(x.group(1)) > int(x.group(2)):
            return False
    return True


def pretty_eq(s1, s2, op):
    cute = lambda s: sub(r"([\+\-])", r" \1 ", sub(r"\s", "", s)).strip()
    if op == "mod 2 =":
        return f"({cute(s1)}) {op} ({cute(s2)})"
    return f"{cute(s1)} {op} {cute(s2)}"

def replace_expression(match):
    n = int(match.group(1))
    m = int(match.group(2))
    
    terms = []
    for i in range(m, n - 1, -1):
        power = m - i
        if power == 0:
            terms.append(f"x[{i}]")
        else:
            terms.append(f"x[{i}]*{10 ** power}")
    
    return " + ".join(terms)

def solve(task):
    set_size = task["set_size"]
    start, end = task["start"], task["end"]
    local_conds = []
    global_conds = Conditions(nonzero=task["nonzero"])
    gcl = "Набор состоит из различных цифр,Соседние цифры набора различны,Цифры набора идут в возрастающем порядке,Цифры набора идут в неубывабщем порядке,Цифры набора идут в убывающем порядке,Цифры набора идут в невозрастающем порядке".split(",")
    sad_vars = set()

    for cond in task["conditions"]:
        if cond not in gcl:
            for idx in finditer(r"\[(\d+)\]", cond):
                sad_vars.add(int(idx.group(1)))
            for idx in finditer(r"\{(\d+);(\d+)\}", cond):
                for i in range(int(idx.group(1)), int(idx.group(2)) + 1):
                    sad_vars.add(i)
            cond = cond.replace("mod 2 =", "% 2 ==")
            cond = sub(r" = ", r" == ", sub(r"\[(\d+)\]", r"x[\1]", cond))
            cond = sub(r"\{(\d+);(\d+)\}", replace_expression, cond)
            local_conds.append(cond)
            continue

        match cond:
            case "Набор состоит из различных цифр":
                global_conds.uniq = True
            case "Соседние цифры набора различны":
                global_conds.non_xx = True
            case "Цифры набора идут в возрастающем порядке":
                global_conds.great = True
                global_conds.uniq = True
            case "Цифры набора идут в неубывабщем порядке":
                global_conds.ge = True
            case "Цифры набора идут в убывающем порядке":
                global_conds.less = True
                global_conds.uniq = True
            case _:
                global_conds.le = True
    
    if global_conds.le and (global_conds.non_xx or global_conds.uniq):
        global_conds.le = False
        global_conds.non_xx = False
        global_conds.less = True
        global_conds.uniq = True
    
    if global_conds.ge and (global_conds.non_xx or global_conds.uniq):
        global_conds.ge = False
        global_conds.non_xx = False
        global_conds.great = True
        global_conds.uniq = True

    if global_conds.uniq and (end - start + 1) < set_size:
        return 0
    
    if global_conds.great and global_conds.less and set_size != 0:
        return 0
    
    if start > 0:
        global_conds.nonzero = False

    return _solve(set_size, start, end, local_conds, sorted(sad_vars), global_conds)


def _solve(set_size, start, end, local_conds, sad_vars, global_conds: Conditions):
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()
    x = {}
    for i in sad_vars:
        if i == 0 and global_conds.nonzero:
            x[i] = model.NewIntVar(1, end, f'x{i}')
            global_conds.nonzero = False
        else:
            x[i] = model.NewIntVar(start, end, f'x{i}')
    solution_counter = ORToolsSolutions(x, global_conds, set_size - len(sad_vars), start, end, set_size)
    solver.parameters.enumerate_all_solutions = True

    for cond in local_conds:
        if '%' in cond:
            cond = cond.split(" % 2 == ")
            model.add_modulo_equality(eval(cond[-1]), eval(cond[0]), 2)
        else:
            model.Add(eval(cond))
    if global_conds.uniq:
        model.AddAllDifferent(list(x.values()))
    if global_conds.non_xx:
        for i in range(len(sad_vars) - 1):
            if sad_vars[i + 1] - sad_vars[i] == 1:
                model.Add(x[sad_vars[i]] != x[sad_vars[i + 1]])
    op = ''
    if global_conds.ge and global_conds.le:
        op = "=="
    elif global_conds.great:
        op = '<'
    elif global_conds.ge:
        op = "<="
    elif global_conds.less:
        op = '>'
    elif global_conds.le:
        op = ">="
    
    if op and sad_vars:
        for i in range(len(sad_vars) - 1):
            model.Add(eval(f"x[{sad_vars[i]}] {op} x[{sad_vars[i + 1]}]"))

    solver.Solve(model, solution_counter)
    return solution_counter.get_solutions()
