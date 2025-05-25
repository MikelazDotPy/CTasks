from dataclasses import dataclass
from math import perm, comb, ceil


def solve(task):
    g, s = task["g_s"]
    conds = Conditions()
    g_cmp, s_cmp, g_s_cmp = [], [] ,[]
    for cond in set(task["conditions"]):
        if cond == "Слово является палиндромом":
            conds.palindrome = True
        elif cond == "Гласные и согласные чередуются":
            conds.alternation = True
        elif cond == "После каждой гласной идет согласная":
            conds.alternation_g_s = True
        elif cond == "После каждой согласной идет гласная":
            conds.alternation_s_g = True
        else:
            c = cond.split()
            if c[0] == "Гласных" and c[-1] == "Согласных":
                g_s_cmp.append(eval(f"lambda v, c: v {c[1] if c[1] != '=' else '=='} c")) 
            elif c[0] == "Гласных":
                g_cmp.append(eval(f"lambda v: v {c[1] if c[1] != '=' else '=='} {c[-1]}"))
            else:
                s_cmp.append(eval(f"lambda c: c {c[1] if c[1] != '=' else '=='} {c[-1]}"))
    return _solve(
        task["word_len"], g, s, conds, g_cmp, s_cmp, g_s_cmp, not task["not_uniq"]
    )


@dataclass
class Conditions:
    palindrome: bool = False
    alternation: bool = False
    alternation_g_s: bool = False
    alternation_s_g: bool = False


def alph_proccesor(alph: str, uniq=False):
    alph = set(alph.lower()) if uniq else alph.lower()
    return sum(x in "аеёиоуыэюя" for x in alph),\
           sum(x in "бвгджзйклмнпрстфхцчшщ" for x in alph),\
           "".join(x for x in alph if x in "аеёиоуыэюябвгджзйклмнпрстфхцчшщ")


def v_c_perm(n):
    for v in range(n + 1):
        yield v, n - v


def get_formula(conds: Conditions, n, N):
    if conds.alternation:
        return lambda v, c: 1 if v != c else 2

    if conds.palindrome:
        if conds.alternation_s_g:
            if N % 2 == 0:
                return lambda v, c: comb(v - 1, c)
            return lambda v, c: comb(v, c)
        if conds.alternation_g_s:
            if N % 2 == 0:
                return lambda v, c: comb(v - 1, c)
            return lambda v, c: comb(v, c)

    if conds.alternation_s_g:
        return lambda v, c: comb(v, c)
    if conds.alternation_g_s:
        return lambda v, c: comb(c, v)

    return lambda v, c: comb(n, v)


def get_facecontrol(conds: Conditions):
    if conds.alternation:
        return [lambda v, c: abs(v - c) <= 1]
    if conds.alternation_s_g:
        return [lambda v, c: v >= c]
    if conds.alternation_g_s:
        return [lambda v, c: c >= v]
    return []


def _solve(n, g, s, conds: Conditions = Conditions(), g_cmp: tuple = (),
                            s_cmp: tuple = (),
                            g_s_cmp: tuple = (), uniq=False):
    if n == 0:
        return 1
    if n % 2 == 0 and conds.alternation and conds.palindrome:
        return 0
    if conds.alternation_g_s and conds.alternation_s_g:
        return 0
    if (conds.alternation_g_s or conds.alternation_s_g) and conds.alternation:
        new_conditions = Conditions(alternation=conds.alternation, palindrome=conds.palindrome)
        if n % 2 == 0:
            return _solve(n, g, s, new_conditions, g_cmp, s_cmp, g_s_cmp, uniq=uniq)//2
        s2 = _solve(n - 1, g, s, new_conditions, g_cmp, s_cmp, g_s_cmp, uniq=uniq)//(2 if n - 1 != 0 else 1)
        if uniq:
            s2 *= ((g if conds.alternation_g_s else s) - n // 2)
        else:
            s2 *= g if conds.alternation_g_s else s
        return _solve(n, g, s, new_conditions, g_cmp, s_cmp, g_s_cmp, uniq=uniq) - s2
    
    ans = 0
    N = n
    n = ceil(n / 2) if conds.palindrome else n
    formula = get_formula(conds, n, N)
    facecontrol = get_facecontrol(conds)

    if uniq:
        p = lambda v, c: perm(g, v)*perm(s, c)
        facecontrol.append(lambda v, c: v <= g and c <= s)
    else:
        p = lambda v, c: g**v*s**c

    for v, c in v_c_perm(n):
        if not all((
            all(x(v) for x in g_cmp), all(x(c) for x in s_cmp),
            all(x(v, c) for x in g_s_cmp), all(x(v, c) for x in facecontrol)
        )):
            continue
        ans += formula(v, c)*p(v, c)

    return ans
