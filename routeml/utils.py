def routes_to_solution(routes):
    """
    Converts a list of routes into a solution (list of routes).

    Args:
        routes (list): List of routes, where each route is a list of nodes.

    Returns:
        list: Solution (list of routes).
    """
    solution = []
    for i, route in enumerate(routes):
        assert route[0] == 0
        assert route[-1] == 0
        # Skip depot node for all routes except the first one
        if i > 0:
            route = route[1:]
        solution += route
    return solution


def solution_to_routes(solution):
    """
    Converts a solution (list of nodes) into a list of routes.

    Args:
        solution (list): Solution (list of nodes).

    Returns:
        list: List of routes, where each route is a list of nodes.
    """
    routes = []
    route = []
    for node in solution:
        if node == 0 and route:
            route.append(0)
            routes.append(route)
            route = []
        route.append(node)
    return routes
