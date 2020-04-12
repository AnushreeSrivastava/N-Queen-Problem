from statistics import mean, stdev
from All_searches import steepest_ascent_hill_climb, random_restart_hill_climb


# Returns the average number of steps
def calculate_avg_pathcost(result_list, key):
    results = [result[key] for result in result_list]
    if len(result_list) == 1:
        return {'mean': result_list[0][key], 'sd': 0}
    elif not result_list:
        return {'mean': 0, 'sd': 0}
    return {'mean': mean(results), 'sd': stdev(results)}

# Print results for Steepest Ascent hill climbing algo
def print_results(results):
    title_col_width = 30
    data_col_width = 15

    def print_data_row(row_title, data_string, data_func, results):
        nonlocal title_col_width, data_col_width
        row = (row_title + '\t').rjust(title_col_width)
        result_groups = iter(results)
        next(result_groups)
        for result_group in result_groups:
            row += data_string.format(**data_func(result_group)).ljust(data_col_width)
        print(row)

    # Printing four search sequences
    def print_search_sequence(results):
        print('\nSearch sequence path:')
        i = 1
        for result in results[0]:
            print('Search sequence ', i)
            for sol_path in result['solution']:
                seqs = sol_path.queen_positions
                print([list(x) for x in seqs])
            i += 1
            if i > 4:  # break when 4 sequences are printed
                break

    num_iterations = len(results[0])

    # Print Header
    print('\t'.rjust(title_col_width) +
          'Successes'.ljust(data_col_width) +
          'Failures'.ljust(data_col_width))

    # Print success and failure percentages
    print_data_row('Success/Failure Rate:',
                   '{percent:.1%}',
                   lambda x: {'percent': len(x) / num_iterations},
                   results)

    # Print Average number of steps
    print_data_row('Average number of steps:',
                   '{mean:.0f}',
                   lambda x: calculate_avg_pathcost(x, 'path_length'),
                   results)

    # Print search sequence for steepest ascent hill-climbing algorithms
    print_search_sequence(results)


# Print results for Random-restart hill climbing algo
def print_Random_Search_results(results, Avg_restarts):
    title_col_width = 30
    data_col_width = 15

    def print_data_row(row_title, data_string, data_func, results):
        nonlocal title_col_width, data_col_width
        row = (row_title + '\t').rjust(title_col_width)
        result_groups = iter(results)
        next(result_groups)
        for result_group in result_groups:
            row += data_string.format(**data_func(result_group)).ljust(data_col_width)
        print(row)

    def print_random_restart_data(row_title, avg):
        nonlocal title_col_width, data_col_width
        row = (row_title + '\t').rjust(title_col_width) + str(avg)
        print(row)


    num_iterations = len(results[0])

    print('\t'.rjust(title_col_width) +
          'Successes'.ljust(data_col_width) +
          'Failures'.ljust(data_col_width))

    print_data_row('Success/Failure Rate:',
                   '{percent:.1%}',
                   lambda x: {'percent': len(x) / num_iterations},
                   results)

    print_random_restart_data('Average number of Restarts:', Avg_restarts)

    print_data_row('Average number of steps:',
                   '{mean:.0f}',
                   lambda x: calculate_avg_pathcost(x, 'path_length'),
                   results)


# Returns a results list containing all the possible solutions, successes and failures
def get_results(problem_set, search_function):
    results = []
    print('\rSolving problems...wait...')
    for problem_num, problem in enumerate(problem_set):
        result = search_function(problem)
        result['path_length'] = len(result['solution']) - 1
        results.append(result)
    results = [results,
               [result for result in results if result['outcome'] == 'success'],
               [result for result in results if result['outcome'] == 'failure']]

    # Calculate Average number of random restarts
    if 'NoRestarts' in results[0][00]:
        ran_restarts = []
        for result in results[0]:
            ran_restarts.append(result['NoRestarts'])
        Avg_restarts = mean(ran_restarts)
        print_Random_Search_results(results, Avg_restarts)
    else:
        print_results(results)


# Function calls all the variants of the hill climbing algorithm
def hill_climbing_algo(queens_state):
    print('\nSteepest ascent hill climb (no sideways moves):')
    get_results(queens_state, steepest_ascent_hill_climb)

    print('\nSteepest ascent hill climb (100 sideways moves):')
    get_results(queens_state, lambda x: steepest_ascent_hill_climb(x, allow_sideways=True))

    print('\nResult from random restart hill climb (no sideways moves):')
    get_results(queens_state, lambda x: random_restart_hill_climb(queens_state[0].__class__, allow_sideways=False)
                )
    print('\nResult from random restart hill climb (100 sideways moves):')
    get_results(queens_state, lambda x: random_restart_hill_climb(queens_state[0].__class__, allow_sideways=True))


# Driver Code-----------MAIN--------------------------
from queens import QueensProblem

# run n queen problem for 500 times
queens_state = [QueensProblem() for _ in range(500)]
hill_climbing_algo(queens_state)
