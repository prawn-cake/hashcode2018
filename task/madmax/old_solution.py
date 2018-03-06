while cur_time < T and len(priority_queue):
    picked_car = None
    ride = priority_queue.popleft()

    if cur_time > ride.finish_t:
        skipped_orders.add(ride)
        continue

    max_score = -1
    start_t, finish_t = None, None

    available_cars = []
    # print('available_cars: %s' % available_cars)
    for car in available_cars:
        score, actual_start_t, actual_finish_t = ride_score(cur_time, car, ride, radar, bonus)
        if score == -1:  # this car can't make the order in time, skip
            continue
        if score > max_score:
            max_score = score
            picked_car = car
            start_t, finish_t = actual_start_t, actual_finish_t

    if picked_car is None:
        priority_queue.append(ride)
    else:
        schedule_ride(ride, picked_car, schedule, start_t, finish_t)
        radar[picked_car.id] = ride.coord_finish
        # print('picked car: %s, ride: %s, score: %d' % (picked_car, ride, max_score))
        total_score += max_score
        scheduled_orders += 1

    cur_time += 1

print('-' * 100)
print('total score: %d' % total_score)
print('%d scheduled' % (scheduled_orders,))
print('%d skipped orders: %s' % (len(skipped_orders), skipped_orders,))