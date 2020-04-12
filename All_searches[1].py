from random import choice


# Steepest accent hill climbing algorithm with and without sideway moves
def steepest_ascent_hill_climb(problem, allow_sideways=False, max_sideways=100):
    def get_minCost_child(node, problem):
        children = node.get_children()
        children_cost = [problem.Calculate_heuristic(child) for child in children]
        min_cost = min(children_cost)

        # Best child is chosen randomly from the list of minimum cost child
        best_child = choice([child for child_index, child in enumerate(children) if children_cost[
            child_index] == min_cost])
        return best_child

    node = problem.start_state
    node_cost = problem.Calculate_heuristic(node)
    path = []
    sideways_moves = 0

    while True:
        path.append(node)
        best_child = get_minCost_child(node, problem)
        # print("\n" + str(best_child))
        best_child_cost = problem.Calculate_heuristic(best_child)

        if best_child_cost > node_cost:
            break
        elif best_child_cost == node_cost:
            if not allow_sideways or sideways_moves == max_sideways:
                break
            else:
                sideways_moves += 1
        else:
            sideways_moves = 0
        node = best_child
        node_cost = best_child_cost

    return {'outcome': 'success' if problem.goal_test(node) else 'failure',
            'solution': path,
            'problem': problem}


# Random restart hill climbing algorithm with and without sideway moves
def random_restart_hill_climb(random_problem_generator, num_restarts=100, allow_sideways=False, max_sideways=100):
    path = []
    nRestart = 0
    while 1:
        result = steepest_ascent_hill_climb(random_problem_generator(), allow_sideways=allow_sideways,
                                            max_sideways=max_sideways)
        nRestart += 1
        path += result['solution']
        if result['outcome'] == 'success':
            break
    result['solution'] = path
    result['NoRestarts'] = nRestart
    return result
