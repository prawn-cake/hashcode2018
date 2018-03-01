from task import helpers, parse_input


def main():
    meta, rides = parse_input.parse()
    rows, columns, vehicles, num_of_rides, bonus, T = meta

    total_score = 0
    orders = [[] for _ in range(vehicles)]
    radar = [[0, 0] for _ in range(vehicles)]

    print(meta, rides)
    for i, ride in enumerate(rides):
        pass


def ride_score(cur_pos, ride):
    # i, j = cur_pos
    coord1, coord2, [s, f] = ride

    ride_distance = helpers.distance(coord1, coord2)
    cost_of_start = helpers.distance(cur_pos, ride_distance)
    time_to_wait = 0
    total_cost = helpers.total_cost(cos=helpers,
                                    distance=cost_of_start,
                                    ttw=time_to_wait)
