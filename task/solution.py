import random
from task import helpers, parse_input, parse_output


def main():
    meta, rides = parse_input.parse('../data/c_no_hurry.in')
    rows, columns, vehicles, num_of_rides, bonus, T = map(int, meta)

    total_score = 0
    steps = 0

    orders = [[] for _ in range(vehicles)]

    # car idx, coords x y, availability
    radar = [[i, 0, 0, True, 0] for i in range(vehicles)]
    rides_map = [[i, ride, True] for i, ride in enumerate(rides)]

    current_time = 0
    while True:
        assign_ride(rides_map, radar, current_time, orders, total_score)
        current_time += 1
        if current_time >= T:
            break
    # parse_output.output(orders, 'output.txt')
    # print('orders: %s' % orders)


def ride_score(cur_pos, ride, current_time):
    # i, j = cur_pos
    coord1, coord2, [s, f] = ride
    s = int(s)
    f = int(f)
    # print('coord1: {}'.format(coord1))
    # print('cur_pos: {}'.format(cur_pos))
    ride_distance = int(helpers.distance(coord1, coord2))
    # print(coord2)
    cost_of_start = int(helpers.distance(cur_pos, coord1))
    time_to_wait = 0 if current_time >= s else s - current_time
    # print('time_to_wait: %s' % time_to_wait)
    total_cost = helpers.total_cost(cos=cost_of_start,
                                    d=ride_distance,
                                    ttw=time_to_wait)
    score = ride_distance / total_cost
    return score, ride_distance


def assign_ride(rides_map, radar, current_time, orders, total_score):
    for car in radar:
        car_id = car[0]
        if car[3]:
            max_score_per_car = 0
            max_score_ride = None

            for r in rides_map:
                if r[2] is False:
                    continue
                score, distance = ride_score(cur_pos=[car[1], car[2]],
                                             ride=r[1],
                                             current_time=current_time)
                if score > max_score_per_car:
                    max_score_per_car = score
                    max_score_ride = r

            if max_score_ride is None:
                continue

            # booked
            max_score_ride[2] = False
            car[3] = False  # not available

            # update radar coordinates of the car
            radar[car_id][1] = max_score_ride[1][1][0]
            radar[car_id][2] = max_score_ride[1][1][1]

            radar[car_id][4] = distance
            orders[car_id].append(max_score_ride[0])  # make an order
            rides_map[max_score_ride[0]][2] = False
        else:
            radar[car_id][4] -= 1
            if radar[car_id][4] == 0:
                radar[car_id][3] = True


if __name__ == '__main__':
    main()
