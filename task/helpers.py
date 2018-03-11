import math


def total_cost(cos, d, ttw=0):
    return sum([cos, d, ttw])


def distance(coord1, coord2):
    a, b = coord1
    x, y = coord2
    return math.fabs(a - x) + math.fabs(b - y)


def score(distance, total_cost):
    return distance / total_cost


def ride_priority(cur_time, ride):
    """Ride score priority regarding the current moment in time

    """
    ttw = max(0, ride.start_t - cur_time)  # time to wait to start
    d = distance(ride.coord_start, ride.coord_finish)

    if cur_time >= ride.finish_t:
        return 0
    # return distance - ttw
    return ride.start_t