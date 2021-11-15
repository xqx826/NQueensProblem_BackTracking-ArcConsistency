from typing import List, Tuple

def remove_and_add(s: set, domain) -> bool:
    # constraint for n queen problem:
    # element in domain of i != element in the domain of j
    # |element in domain i - element in domain j | != |i = j|
    pair = s.pop()
    primary_var = pair[0]
    secondary_var = pair[1]
    is_reduced = False
    val_to_be_removed = []
    for val_i in domain[primary_var]:
        consistent = False
        for val_j in domain[secondary_var]:
            if val_i != val_j and abs(val_i - val_j) != abs(primary_var - secondary_var):
                consistent = True
        if not consistent:
            #reduce domain of primary_var
            val_to_be_removed.append(val_i) 
            is_reduced = True
            print(str(val_i) + " is reduced") 

    if is_reduced:
        # remove values
        for val in val_to_be_removed:
            domain[primary_var].remove(val)
            print("Domain left:")
            print(domain)
            if not domain[primary_var]:
                return False
        # generate pairs
        size = len(domain)
        for i in range(size):
            if i != primary_var and i != secondary_var:
                new_pair = (i, primary_var)
                s.add(new_pair)
    return True

def arc_consistency(config: list[int]):
    domain = [set] * len(config)
    s = set()
    # initialize domain of each variable, domain[i] = domain of row i 
    # and put every arc in set s. Since we know the constraints in the N queen problem,
    # we will represent arc by pair (xi, xj) where xi is the primary variable and xj is the second variable.
    # the constraint for the arc is c(xi, xj) or c(xj, xi) 
    # xi, xj = the col number

    for i in range(len(config)):
        if config[i] != -1:
            domain[i] = {config[i]}
        else:
            domain[i] = set(range(len(config)))
        for j in range(len(config)):
            if i != j:
                pair = (i, j)
                rev_pair = (j, i)
                s.add(pair)
                s.add(rev_pair)

    print("DOMAIN:")
    print(domain)
    print("length of set s: " + str(len(s)) )
    print("SET S:")
    print(s)
    while s:
        result = remove_and_add(s, domain)
        if result == False:
            return False, domain
    return True, domain

def solveNQueens(n: int) -> List[List[str]]:
    """
    x_i to be the row position of the queen in column i
    where i is one of {0, 1, ..., n}
    for each x_i, domain is {0, 1, ..., n}
    Constriants: no two queens can be in the same row or diagnoal
    
    state: one queen per column in the leftmost k columns with no pair of queens attacking each other
    init_state: empty board
    goal_state: n queens on the board with no pairs of queens attacking each other
    successor function: add a queen to the leftmost empty column such that it is not attacked by any other existing queen
    """
    ans = []
    # we want to perform backtracking w/ dfs, use stack
    stack = []
    for i in range(n-1, -1, -1):
        curr_config = [-1] * n # curr_config[i] = row number in col i
        # i is the value assignment of each row in col 0
        curr_config[0] = i
        stack.append(curr_config)
    print(stack)
    while stack:
        config = stack[-1]
        stack.pop()
        result = arc_consistency(config)
        if result[0] == False:
            # no solution, terminate, don't add any children
            continue
        else:
            # check if unique solution is found by checking domain
            is_unique = True
            domain = result[1]
            curr_ans = [-1] * len(domain)
            print("domain length " + str(len(domain))) 
            for i in range(len(domain)):
                if len(domain[i]) == 1:
                    curr_ans[i] = domain[i].pop()
                else:
                    is_unique = False 
            if is_unique:
                # unique solution found
                ans.append(curr_ans)
            else:
                # based on domain, generate successor states
                for i in range(len(config)):
                    if config[i] == -1:
                        for item in domain[i]:
                            config[i] = item
                            stack.append(config)
                        break
    return ans


def pretty_print(boards:list[list[int]]):
    print(boards)
    if not boards:
        return
    for board in boards:
        size = len(board)
        pretty_board = [["."] * size for _ in range(size)]
        for i in range(size):
            pretty_board[board[i]][i] = 'Q'
        print(pretty_board)
        
            


if __name__ == "__main__":
    pretty_print(solveNQueens(4))