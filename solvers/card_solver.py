from itertools import permutations, combinations, chain
from math import comb, prod, perm
from operator import lt, le, gt, ge, eq, ne  

from ortools.sat.python import cp_model


d52 = [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3)]
d36 = [(6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3)]


op_dict = {
    '<': lt,
    '<=': le,
    '==': eq,
    '!=': ne,
    '>=': ge,
    '>': gt
}
lambda_categories = {
    "карт_бубновой_масти": lambda x: x[1] == 0,
    "карт_червовой_масти": lambda x: x[1] == 1,
    "карт_трефовой_масти": lambda x: x[1] == 2,
    "карт_пиковой_масти": lambda x: x[1] == 3,
    "красных_карт": lambda x: 0 <= x[1] <= 1,
    "черных_карт": lambda x: 2 <= x[1] <= 3,
}
card_to_num = {
    "двойка": 2,
    "тройка": 3,
    "четверка": 4,
    "пятерка": 5,
    "шестерка": 6,
    "семерка": 7,
    "восьмерка": 8,
    "девятка": 9,
    "десятка": 10,
    "валет": 11,
    "дама": 12,
    "король": 13,
    "туз": 14,
    "буби": 0,
    "черви": 1,
    "треф": 2,
    "пики": 3, 
}

for i, x in enumerate("двоек,троек,четверок,пятерок,шестерок,семерок,восьмерок,девяток,десяток,вальтов,дам,королей,тузов,джокеров".split(",")):
    lambda_categories[x] = eval(f"lambda y: y[0] == {i + 2}")


class ORToolsSolutions(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, small_decks):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.small_decks = [len(x) for x in small_decks]
        self.ans = 0

    def on_solution_callback(self):
        solution = tuple(self.Value(var) for var in self.__variables)
        self.ans += prod(comb(self.small_decks[i], x) for i, x in enumerate(solution))

    def get_solutions(self):
        return self.ans


def sum_to_n(n, size):
    seen = set()
    
    def generate(current, remaining_sum, remaining_size):
        if remaining_size == 0:
            if remaining_sum == 0:
                yield current
            return
        for i in range(0, remaining_sum + 1):
            yield from generate(current + [i], remaining_sum - i, remaining_size - 1)
    
    for combo in generate([], n, size):
        for p in set(permutations(combo)):
            if p not in seen:
                seen.add(p)
                yield list(p)


def combs_k_generator(m, num_variables, constraints, sum_constraints, set_coeffs):
    for solution in sum_to_n(m, num_variables):        
        for cond in constraints:
            idxs, check = cond[0], cond[1]
            if not check(sum(solution[i] for i in idxs)):
                break
        else:
            for cond in sum_constraints:
                if not cond(sum(solution[i]*set_coeffs[i] for i in range(num_variables))):
                    break
            else:
                yield solution


def group_by_first_element(lst):
    first_elements = sorted({x[0] for x in lst})
    result = []
    for elem in first_elements:
        group = [item for item in lst if item[0] == elem]
        result.append(group)
    
    return result


def brutforce(n, deck, condtions, sum_condtions):
    k = 0
    for x in combinations(deck, n):
        for cond in condtions:
            validate, check = cond[0], cond[1]
            if not check(sum(validate(y) for y in x)):
                break
        else:
            if sum_condtions:
                card_sum = sum(y[0] for y in x)
            for cond in sum_condtions:
                if not cond(card_sum):
                    break
            else:
                k += 1
    return k




def solve(task):
    set_size = task["set_size"]
    small_decks = [d52[:] if task["deck"] == 52 else d36[:]]
    conds = []
    conds_sum = []
    banned_cards = []
    base_sum = 0
    model_conds_sum = []

    for x in filter(lambda x: "Все карты " in x, task["conditions"]):
        x = x.replace("Все карты ", "")
        op, card = x.split()
        op = op if op != "=" else "=="
        card = card_to_num[card]
        check = eval(f"lambda y: y[0] {op} {card}")
        small_decks = [list(filter(check, small_decks[0]))]

    for x in filter(lambda x: "В наборе содержится " in x, task["conditions"]):
        x = x.replace("В наборе содержится ", "")
        card, suit = x.split()

        if (card_to_num[card], card_to_num[suit]) not in small_decks[0]:
            return 0

        small_decks[0].remove((card_to_num[card], card_to_num[suit]))
        banned_cards.append((card_to_num[card], card_to_num[suit]))

        set_size -= 1
        base_sum += card_to_num[card]
    
    if set_size < 0:
        return 0

    sp = list(filter(lambda x: "Сумма очков " in x, task["conditions"]))
    if sp:
        small_decks = group_by_first_element(small_decks[0])
    for x in sp:
        x = x.replace("Сумма очков ", "")
        op, val = x.split()
        op = op if op != "=" else "=="
        conds_sum.append(eval(f"lambda y: y {op} {int(val) - base_sum}"))
        model_conds_sum.append((op, int(val) - base_sum))

    for x in filter(lambda x: "Количество " in x, task["conditions"]):
        x = x.replace("Количество ", "")
        for y in "карт бубновой масти,карт червовой масти,карт трефовой масти,карт пиковой масти,красных карт,черных карт".split(","):
            x = x.replace(y, "_".join(y.split(" ")))
        x = x.split()
        new_decks = []
        category, op, b = x[0], x[1] if x[1] != "=" else "==", int(x[2])
        for y in banned_cards:
            if lambda_categories[category](y):
                b -= 1
        conds.append((lambda_categories[category],  eval(f"lambda y: y {op} {b}"), op, b))
        for y in small_decks:
            cond_passed = []
            cond_failed = []
            for z in y:
                if lambda_categories[category](z):
                    cond_passed.append(z)
                else:
                    cond_failed.append(z)
            if cond_passed:
                new_decks.append(cond_passed)
            if cond_failed:
                new_decks.append(cond_failed)
        small_decks = new_decks

    return _solve(small_decks, conds, conds_sum, model_conds_sum, set_size)



"""
ans = sum(
    prod(comb(len(small_decks[i]), x) for i, x in enumerate(solve))
    for solve in combs_k_generator(set_size, len(small_decks), constraints, conds_sum, [y[0][0] for y in small_decks])
)
constraints = [
    [[i for i, y in enumerate(small_decks) if x[0](y[0])]] + [x[1]]
    for x in conds
]
"""
def _solve(small_decks, conds, conds_sum, model_conds_sum, set_size):
    deck = list(chain.from_iterable(small_decks))

    if perm(set_size + len(small_decks) - 1, len(small_decks) - 1) < comb(len(deck), set_size)*10:
        constraints = [
            [i for i, y in enumerate(small_decks) if x[0](y[0])]
            for x in conds
        ]
        model = cp_model.CpModel()
        solver = cp_model.CpSolver()
        x = [model.NewIntVar(0, len(small_decks[i]), f'x{i}') for i in range(len(small_decks))]
        solution_counter = ORToolsSolutions(x, small_decks)
        solver.parameters.enumerate_all_solutions = True

        coeffs = [y[0][0] for y in small_decks]

        model.Add(sum(x[i] for i in range(len(small_decks))) == set_size)

        for op, r in model_conds_sum:
            model.Add(op_dict[op](sum(coeffs[i] * x[i] for i in range(len(small_decks))), r))

        for j in range(len(conds)):
            op, r = conds[j][-2:]
            model.Add(op_dict[op](sum(x[i] for i in constraints[j]), r))
        solver.Solve(model, solution_counter)
        return solution_counter.ans

    return brutforce(set_size, deck, conds, conds_sum)