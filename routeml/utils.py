import re
import requests
import math

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


def parse_vrplib_file(source):
    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        content = response.text
    else:
        with open(source, 'r') as file:
            content = file.read()

    data = {}

    # Extracting problem information using regex
    name_match = re.search(r'NAME\s*:\s*(\S+)', content)
    if name_match:
        data['name'] = name_match.group(1)

    comment_match = re.search(r'COMMENT\s*:\s*"(.+)"', content)
    if comment_match:
        data['comment'] = comment_match.group(1)

    type_match = re.search(r'TYPE\s*:\s*(\S+)', content)
    if type_match:
        data['type'] = type_match.group(1)

    dimension_match = re.search(r'DIMENSION\s*:\s*(\d+)', content)
    if dimension_match:
        data['dimension'] = int(dimension_match.group(1))

    edge_weight_type_match = re.search(r'EDGE_WEIGHT_TYPE\s*:\s*(\S+)', content)
    if edge_weight_type_match:
        data['edge_weight_type'] = edge_weight_type_match.group(1)

    capacity_match = re.search(r'CAPACITY\s*:\s*(\d+)', content)
    if capacity_match:
        data['capacity'] = int(capacity_match.group(1))

    # Extracting node coordinates
    node_coords_match = re.search(r'NODE_COORD_SECTION\s*(.+?)\s*DEMAND_SECTION', content, re.DOTALL)
    if node_coords_match:
        node_coords_str = node_coords_match.group(1).strip()
        node_coords = {}
        for line in node_coords_str.split('\n'):
            node_id, x, y = re.findall(r'(\d+)\s+(\d+)\s+(\d+)', line)[0]
            node_coords[int(node_id)] = (int(x), int(y))
        data['node_coords'] = node_coords

    # Extracting demand information
    demand_section_match = re.search(r'DEMAND_SECTION\s*(.+?)\s*DEPOT_SECTION', content, re.DOTALL)
    if demand_section_match:
        demand_section_str = demand_section_match.group(1).strip()
        demand = {}
        for line in demand_section_str.split('\n'):
            node_id, demand_val = re.findall(r'(\d+)\s+(-?\d+)', line)[0]
            demand[int(node_id)] = int(demand_val)
        data['demand'] = demand

    # Extracting depot information
    depot_section_match = re.search(r'DEPOT_SECTION\s*(.+?)\s*EOF', content, re.DOTALL)
    if depot_section_match:
        depot_section_str = depot_section_match.group(1).strip()
        depot_ids = [int(node_id) for node_id in re.findall(r'(\d+)\s*[^-0-9]', depot_section_str)]
        data['depot_ids'] = depot_ids

    return data

def parse_vrplib_solution(source):
    """
    Parses a solution file from the VRPLIB website and returns the routes and cost.

    Args:
        source (str): Path to the solution file or URL to the solution file.

    Returns:
        tuple: Tuple containing the routes (list of lists) and the cost (float).
    """
    route_regex = re.compile(r'Route #(\d+): (.+)')
    cost_regex = re.compile(r'Cost ([\d.]+)')

    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        solution_text = response.text
    else:
        with open(source, 'r') as file:
            solution_text = file.read()

    routes = []
    cost = None

    lines = solution_text.strip().split('\n')
    for line in lines:
        route_match = route_regex.match(line)
        if route_match:
            route_number = int(route_match.group(1))
            nodes = list(map(int, route_match.group(2).split()))
            routes.append(nodes)

        cost_match = cost_regex.match(line)
        if cost_match:
            cost = float(cost_match.group(1))

    return routes, cost

def get_cvrp_cost(routes_or_solution, coordinates):
    """
    Compute the total cost of a CVRP solution.

    Args:
        routes_or_solution (list or solution): List of routes or a solution.
        coordinates (dict): Dictionary containing node IDs as keys and corresponding coordinates as values.

    Returns:
        float: Total cost of the CVRP solution.
    """
    if isinstance(routes_or_solution, list) and isinstance(routes_or_solution[0], list):
        solution = routes_to_solution(routes_or_solution)
    elif isinstance(routes_or_solution, list):
        solution = routes_or_solution
    else:
        raise ValueError("Invalid input. Expected a nested list of routes or a solution.")

    total_cost = 0.0
    for i in range(len(solution) - 1):
        node1 = solution[i]
        node2 = solution[i + 1]
        coord1 = coordinates[node1]
        coord2 = coordinates[node2]
        distance = math.dist(coord1, coord2)
        total_cost += distance

    return total_cost
