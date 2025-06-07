import re


def check_code(code):
    try:
        locs = {}
        exec(code, {}, locs)
        if not locs.get("main", False):
            return "Отсуствует функция main!"
        if not locs.get("get_task", False):
            return "Отсуствует функция get_task!"
        return "OK"
    except Exception as e:
        return "Ошибка в коде: " + str(e)


def run_solve_code(prototype, code, get_taskk=False):
    global_namespace = globals().copy()
    local_namespace = {}
    global_namespace.setdefault('__builtins__', __builtins__)

    try:
        exec(prototype, global_namespace, local_namespace)
        if get_taskk:
            local_namespace["main"] = local_namespace["get_task"]
        main_f = local_namespace["main"]

        for k in local_namespace:
            global_namespace[k] = local_namespace[k]
        
        code_lines = code.strip().split('\n')
        import_pattern = r'^\s*(?:from\s+\w+\s+import\s+[\w,\s]+|import\s+\w+)\s*$'
        import_lines = [line for line in code_lines if re.match(import_pattern, line)]
        other_lines = [line for line in code_lines if not re.match(import_pattern, line)]
        
        if import_lines:
            exec('\n'.join(import_lines), global_namespace, local_namespace)
            for k in local_namespace:
                global_namespace[k] = local_namespace[k]

        exec('\n'.join(other_lines), global_namespace, local_namespace)

        if local_namespace.get("main") != main_f:
            return "Не переопределяйте функцию main!"
        
        if local_namespace.get("answer", None) is None:
            return "Ответ должен быть записан в answer!"
        
        if not get_taskk and not isinstance(local_namespace["answer"], int):
            return "Ответ должен быть целым числом!"

        elif get_taskk and not isinstance(local_namespace["answer"], str):
            return "Функция get_task работает некорректно"
            
        return "OK", local_namespace["answer"]
    except Exception as e:
        return "Ошибка в коде: " + str(e)