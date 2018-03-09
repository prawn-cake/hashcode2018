import time
from task import parse_input, parse_output
from task.madmax import helpers
from collections import namedtuple, deque


Ride = namedtuple('Ride', ['id', 'coord_start', 'coord_finish', 'start_t', 'finish_t', 'dist'])
Order = namedtuple('Order', ['ride', 'actual_start_t', 'actual_end_t'])


class Car:
    def __init__(self, idx, t=0):
        self.id = idx
        self.t = t

    def __repr__(self):
        return 'Car(%s, %s)' % (self.id, self.t)


def pick_car(ride, car_list, schedule, radar, avg_distance_per_car, reserved_cars, use_balancer=True):
    actual_start_t, actual_end_t, picked_car, min_cost = None, None, None, None

    for car in car_list:
        # Load balancer function
        if use_balancer:
            if sum([o.ride.dist for o in schedule[car]]) >= 0.7 * avg_distance_per_car:
                reserved_cars.append(car)
                continue

        if not is_car_available(car, ride, schedule):
            continue

        time_to_reach = helpers.distance(radar[car.id], ride.coord_start)
        time_to_wait = max(0, ride.start_t - car.t - time_to_reach)
        ride_distance = helpers.distance(ride.coord_start, ride.coord_finish)

        actual_start_t = car.t + time_to_reach + time_to_wait
        actual_end_t = actual_start_t + ride_distance

        if actual_end_t >= ride.finish_t:
            # a car can't make it
            continue

        cost = time_to_reach + time_to_wait + ride_distance

        if min_cost is None:
            min_cost, picked_car = cost, car
        elif cost < min_cost:
            picked_car = car
            min_cost = cost
    return picked_car, actual_start_t, actual_end_t, min_cost, reserved_cars


def prioritise_rides(rides_list):
    # Default implementation to sort by start time
    return sorted(rides_list, key=lambda r: r.start_t)


def main(meta, rides):
    rows, columns, vehicles, num_of_rides, bonus, T = meta
    print('rows: %s, columns: %s, vehicles: %s, num_of_rides: %s, bonus: %s, T: %s' % (rows, columns, vehicles, num_of_rides, bonus, T))

    rides_list = [Ride(i, item[0], item[1], item[2][0], item[2][1], helpers.distance(item[0], item[1]))
                  for i, item in enumerate(rides)]
    cars_list = [Car(i, 0) for i in range(vehicles)]

    schedule = {car: [] for car in cars_list}

    # To track cars
    radar = {car.id: (0, 0) for car in cars_list}

    # TODO: this could be reordered
    # priority_queue = deque(sorted(rides_list, key=lambda r: r.start_t))
    priority_queue = sorted(rides_list, key=lambda r: r.start_t)
    # print('priority_queue: %s' % priority_queue)
    total_distance = sum([ride.dist for ride in rides_list])
    avg_distance_per_car = total_distance / vehicles

    total_score = 0

    total_ride_cost = 0
    total_bonus = 0
    skipped_rides = 0

    for ride in priority_queue:
        # if total_score > T:
        #     break

        reserved_cars = []

        picked_car, actual_start_t, actual_end_t, min_cost, reserved_cars = pick_car(
            ride, cars_list, schedule, radar, avg_distance_per_car, reserved_cars)

        if picked_car is None:
            # Try to find a car from the reserved ones
            if reserved_cars:
                picked_car, actual_start_t, actual_end_t, min_cost, reserved_cars = pick_car(
                    ride, cars_list, schedule, radar, avg_distance_per_car, reserved_cars, use_balancer=False)
                if picked_car is None:
                    skipped_rides += 1
                    continue
            else:
                skipped_rides += 1
                continue

        # Add an order
        total_score += ride_score(total_ride_cost, picked_car, ride, radar, bonus)

        schedule[picked_car].append(Order(ride, actual_start_t, actual_end_t))
        radar[picked_car.id] = ride.coord_finish
        total_ride_cost += min_cost
        picked_car.t += min_cost

        if actual_start_t == ride.start_t:
            total_bonus += bonus

    print('skipped: %d (%d percent)' % (skipped_rides, (skipped_rides / num_of_rides) * 100))
    print('total score: %d (score: %d, bonus: %d)' % (total_score + total_bonus, total_score, total_bonus))
    return schedule


def is_car_available(car, ride, schedule):
    orders = schedule[car]
    if not orders:
        return True

    # NOTE: we assume that orders ARE ordered by time
    last_order = orders[-1]

    # Check if we can fit the order to the schedule
    if (last_order.actual_end_t + ride.dist) < ride.finish_t:
        return True
    return False


def ride_score(cur_time, car, ride, radar, bonus=0):
    car_coord = radar[car.id]

    time_to_reach = helpers.distance(car_coord, ride.coord_start)
    time_to_wait = max(0, ride.start_t - cur_time - time_to_reach)
    ride_distance = ride.dist

    actual_start_time = cur_time + time_to_reach + time_to_wait
    actual_end_time = actual_start_time + ride_distance

    if actual_start_time != ride.start_t:
        # if we pick up the passenger with delay -> no bonus
        bonus = 0

    if actual_end_time >= ride.finish_t:
        # We don't get points if we deliver the passenger late
        return 0

    return ride_distance + bonus


def ride_cost(car, ride, radar):
    car_coord = radar[car.id]

    time_to_reach = helpers.distance(car_coord, ride.coord_start)
    time_to_wait = max(0, ride.start_t - car.t - time_to_reach)
    ride_distance = ride.dist

    actual_start_t = car.t + time_to_reach + time_to_wait
    actual_end_t = actual_start_t + ride_distance

    cost = time_to_reach + time_to_wait + ride_distance
    return cost, actual_start_t, actual_end_t


def generate_result(filename):
    meta, rides = parse_input.parse('../../data/%s' % filename)
    t0 = time.time()
    schedule = main(meta, rides)
    print('Elapsed {:.4f}s'.format(time.time() - t0))

    items = []
    for car, orders in sorted(schedule.items(), key=lambda item: item[0].id):
        items.append([str(o.ride.id) for o in orders])
        # print('car %d -> %s' % (car.id, ', '.join([str(o.ride.id) for o in orders])))

    parse_output.write_output(items, '../../result/%s.txt' % filename)


if __name__ == '__main__':
    # meta, rides = parse_input.parse('../../data/a_example.in')
    names = ['a_example.in', 'b_should_be_easy.in', 'c_no_hurry.in',
             'd_metropolis.in', 'e_high_bonus.in']
    # filename = 'a_example.in'
    # filename = 'b_should_be_easy.in'
    # filename = 'c_no_hurry.in'
    # filename = 'd_metropolis.in'
    # filename = 'e_high_bonus.in'
    for filename in names:
        print('-' * 100)
        print('Generate result for %s' % filename)
        generate_result(filename)
    # generate_result(filename)
