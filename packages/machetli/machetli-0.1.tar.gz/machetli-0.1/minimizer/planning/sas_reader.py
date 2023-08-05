from minimizer.planning.downward_lib.sas_tasks import SASTask, SASVariables, SASMutexGroup, SASInit, SASGoal, SASOperator, SASAxiom


def read_variables(sf, num_vars):
    axiom_layers = []
    ranges = []
    value_name_lists = []
    for var in range(num_vars):
        beginning_line = sf.readline().replace("\n", "")
        assert beginning_line == "begin_variable"
        sf.readline()  # skip variable name
        axiom_layers.append(int(sf.readline().replace("\n", "")))
        ranges.append(int(sf.readline().replace("\n", "")))
        value_names = []
        for name in range(ranges[-1]):
            value_names.append(sf.readline().replace("\n", ""))
        value_name_lists.append(value_names)
        ending_line = sf.readline().replace("\n", "")
        assert ending_line == "end_variable"
    return SASVariables(ranges, axiom_layers, value_name_lists)


def read_mutexes(sf, num_mutexes):
    mutexes = []
    for mutex_group in range(num_mutexes):
        beginning_line = sf.readline().replace("\n", "")
        assert beginning_line == "begin_mutex_group"
        num_facts = int(sf.readline().replace("\n", ""))
        facts = []
        for fact in range(num_facts):
            var, val = map(int, sf.readline().replace("\n", "").split(" "))
            facts.append((var, val))
        mutexes.append(SASMutexGroup(facts))
        ending_line = sf.readline().replace("\n", "")
        assert ending_line == "end_mutex_group"
    return mutexes


def read_init_state(sf, num_vars):
    init = []
    beginning_line = sf.readline().replace("\n", "")
    assert beginning_line == "begin_state"
    for var in range(num_vars):
        val = int(sf.readline().replace("\n", ""))
        init.append(val)
    ending_line = sf.readline().replace("\n", "")
    assert ending_line == "end_state"
    return SASInit(init)


def read_goal(sf):
    beginning_line = sf.readline().replace("\n", "")
    assert beginning_line == "begin_goal"
    num_pairs = int(sf.readline().replace("\n", ""))
    pairs = []
    for pair in range(num_pairs):
        var, val = map(int, sf.readline().replace("\n", "").split(" "))
        pairs.append((var, val))
    ending_line = sf.readline().replace("\n", "")
    assert ending_line == "end_goal"
    return SASGoal(pairs)


def read_operators(sf, num_operators):
    operators = []
    for op in range(num_operators):
        beginning_line = sf.readline().replace("\n", "")
        assert beginning_line == "begin_operator"
        name = "(" + sf.readline().replace("\n", "") + ")"
        num_prevail_conditions = int(sf.readline().replace("\n", ""))
        prevail_conditions = []
        for pre_cond in range(num_prevail_conditions):
            var, val = map(int, sf.readline().replace("\n", "").split(" "))
            prevail_conditions.append((var, val))
        num_effects = int(sf.readline().replace("\n", ""))
        pre_post = []
        for eff in range(num_effects):
            effect_line = list(map(int, sf.readline().replace("\n", "").split(" ")))
            num_effect_conditions = effect_line[0]
            cond = []
            for cond_num in range(1, 2 * num_effect_conditions, 2):
                var = effect_line[cond_num]
                val = effect_line[cond_num + 1]
                cond.append((var, val))
            var, pre, post = effect_line[-3:]
            pre_post.append((var, pre, post, cond))
        cost = int(sf.readline().replace("\n", ""))
        operators.append(SASOperator(name, prevail_conditions, pre_post, cost))
        ending_line = sf.readline().replace("\n", "")
        assert ending_line == "end_operator"
    return operators


def read_axioms(sf, num_axioms):
    axioms = []
    for ax in range(num_axioms):
        beginning_line = sf.readline().replace("\n", "")
        assert beginning_line == "begin_rule"
        length_body = int(sf.readline().replace("\n", ""))
        condition = []
        for fact in range(length_body):
            var, val = map(int, sf.readline().replace("\n", "").split(" "))
            condition.append((var, val))
        effect_line = list(map(int, sf.readline().replace("\n", "").split(" ")))
        var = effect_line[0]
        val = effect_line[2]
        assert 1 - val == effect_line[1]
        effect = (var, val)
        axioms.append(SASAxiom(condition, effect))
        ending_line = sf.readline().replace("\n", "")
        assert ending_line == "end_rule"
    return axioms


def sas_file_to_SASTask(sas_file) -> SASTask:
    with open(sas_file, "r") as sf:
        while True:
            # pos = sf.tell()
            line = sf.readline().replace("\n", "")
            if line == "begin_metric":
                break
        metric = bool(sf.readline().replace("\n", ""))
        sf.readline()  # skip end_metric
        # read variables
        num_vars = int(sf.readline().replace("\n", ""))
        variables = read_variables(sf, num_vars)
        # read mutexes
        num_mutexes = int(sf.readline().replace("\n", ""))
        mutexes = read_mutexes(sf, num_mutexes)
        # read init state
        init = read_init_state(sf, num_vars)
        # read goal
        goal = read_goal(sf)
        # read operators
        num_operators = int(sf.readline().replace("\n", ""))
        operators = read_operators(sf, num_operators)
        # read axioms
        num_axioms = int(sf.readline().replace("\n", ""))
        axioms = read_axioms(sf, num_axioms)

    sas_task = SASTask(variables, mutexes, init, goal, operators, axioms, metric)
    sas_task.validate()
    return sas_task


def write_SAS(sas_task, filename):
    with open(filename, "w") as file:
        sas_task.output(file)
