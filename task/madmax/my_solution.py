from task import parse_input
from task.madmax import helpers
from collections import namedtuple


Ride = namedtuple('Ride', ['id', 'coord_start', 'coord_finish', 'start_t', 'finish_t'])
Car = namedtuple('Ride', ['id'])


def main():
    meta, rides = parse_input.parse('../../data/b_should_be_easy.in')
    rows, columns, vehicles, num_of_rides, bonus, T = meta
    print('rows: %s, columns: %s, vehicles: %s, num_of_rides: %s, bonus: %s, T: %s' % (rows, columns, vehicles, num_of_rides, bonus, T))

    rides_list = [Ride(i, item[0], item[1], item[2][0], item[2][1])
                  for i, item in enumerate(rides)]
    cars_list = [Car(i) for i in range(vehicles)]
    cur_time = 10000

    # print(sorted(rides_list, key=lambda r: r.start_t))
    priority_queue = sorted([(ride_priority(cur_time, r), r) for r in rides_list], reverse=True)
    print('priority_queue: %s' % priority_queue)
    ride = priority_queue[0]

    # To track cars
    radar = {car.id: (0, 0) for car in cars_list}

    # Main loop
    # - pick the ride with the higher priority
    # - find the car based on the score


def ride_score(cur_time, car, ride, radar, bonus=0):
    car_coord = radar[car.id]

    time_to_reach = helpers.distance(car_coord, ride.coord_start)
    time_to_wait = max(0, ride.start_t - cur_time - time_to_reach)
    ride_distance = helpers.distance(ride.coord_start, ride.coord_finish)

    actual_start_time = cur_time + time_to_reach + time_to_wait
    actual_end_time = actual_start_time + ride_distance

    if actual_start_time != ride.start_t:
        # if we pick up the passenger with delay -> no bonus
        bonus = 0

    if actual_end_time >= ride.finish_t:
        # We don't get points if we deliver the passenger late
        return 0

    return ride_distance + bonus


def ride_priority(cur_time, ride):
    """Ride score priority regarding the current moment in time

    """
    ttw = max(0, ride.start_t - cur_time)  # time to wait to start
    distance = helpers.distance(ride.coord_start, ride.coord_finish)

    if cur_time >= ride.finish_t:
        return 0
    return distance - ttw


if __name__ == '__main__':
    main()
