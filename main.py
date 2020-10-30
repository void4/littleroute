#https://chrisseaton.com/truffleruby/ruby-stm/
from random import randint

w = h = 32

NPOINTS = 16
NROUTES = 4

points = [(randint(0,w-1), randint(0,h-1)) for i in range(NPOINTS)]

routes = [(randint(0,NPOINTS-1), randint(0,NPOINTS-1)) for i in range(NROUTES)]

depth = [[0 for x in range(w)] for y in range(h)]

obstructed = [[0 for x in range(w)] for y in range(h)]


def getAdjacent(p):
    for delta in [[1,0],[-1,0],[0,1],[0,-1]]:
        np = (p[0]+delta[0], p[1]+delta[1])
        if 0 <= np[0] < w and 0 <= np[1] < h:
            yield np

def depthCost(p):
    return depth[p[1]][p[0]]+1

def expand(p1, p2):
    cost = [[0 for x in range(w)] for y in range(h)]
    cost[p1[1]][p1[0]] = 1
    wavefront = [p1]

    while True:
        new_wavefront = []

        for point in wavefront:
            point_cost = cost[point[1]][point[0]]

            for adjacent in getAdjacent(point):
                if obstructed[adjacent[1]][adjacent[0]] == 1 and adjacent != p2:
                    continue

                current_cost = cost[adjacent[1]][adjacent[0]]

                new_cost = point_cost + depthCost(adjacent)

                if current_cost == 0 or new_cost < current_cost:
                    cost[adjacent[1]][adjacent[0]] = new_cost
                    new_wavefront.append(adjacent)

        cost_at_route_end = cost[p2[1]][p2[0]]
        minimum_new_costs = [cost[marked[1]][marked[0]] for marked in new_wavefront]

        if cost_at_route_end > 0 and (len(minimum_new_costs) == 0 or cost_at_route_end < min(minimum_new_costs)):
            break

        wavefront = new_wavefront

    return cost

def solve(p1, p2, cost):
    solution = [p2]

    while True:
        lowest_cost = min([adjacent for adjacent in getAdjacent(solution[-1]) if cost[adjacent[1]][adjacent[0]] > 0], key=lambda a:cost[a[1]][a[0]])
        solution.append(lowest_cost)

        if lowest_cost == p1:
            break

    return solution

def lay(depth, solution):
    for point in solution:
        depth[point[1]][point[0]] += 1

for route in routes:
    p1 = points[route[0]]
    p2 = points[route[1]]

    cost = expand(p1, p2)
    solution = solve(p1, p2, cost)
    lay(depth, solution)

from visualize import save
save(depth)
