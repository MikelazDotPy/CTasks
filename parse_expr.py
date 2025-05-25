from math import comb, perm, factorial


def parse_expr(expr):
    expr = expr.replace("/", "//")
    return eval(expr, {'C': comb, 'A': perm, 'F': factorial, 'С': comb, 'А': perm}, {})

