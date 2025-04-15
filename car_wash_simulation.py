import simpy
import random

def car(env, name, car_wash, drying, waxing, wait_times):
    """Car process that goes through wash, dry, and wax steps."""
    print(f"{name} arriving at car wash at {env.now}")
    arrival_time = env.now

    with car_wash.request() as request:
        yield request
        #print(f"{name} entering car wash at {env.now}")
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        yield env.timeout(random.uniform(5, 10))  # Washing takes 5-10 minutes
        #print(f"{name} leaving car wash at {env.now}")

    with drying.request() as request:
        yield request
        #print(f"{name} entering drying at {env.now}")
        yield env.timeout(random.uniform(3, 7))  # Drying takes 3-7 minutes
        #print(f"{name} leaving drying at {env.now}")

    with waxing.request() as request:
        yield request
        #print(f"{name} entering waxing at {env.now}")
        yield env.timeout(random.uniform(4, 8))  # Waxing takes 4-8 minutes
        print(f"{name} leaving waxing at {env.now}")

def car_generator(env, car_wash, drying, waxing, arrival_rate, max_queue_length, queue_data, car_wash_data, lost_cars, wait_times):
    """Generates cars arriving at the car wash and collects data."""
    car_count = 0
    while True:
        if len(car_wash.queue) < max_queue_length:
            car_count += 1
            env.process(car(env, f"Car {car_count}", car_wash, drying, waxing, wait_times))
        else:
            lost_cars.append(env.now)  # Record the time when a car is lost
            print(f"Car lost at {env.now} due to queue limit")
        yield env.timeout(random.expovariate(arrival_rate))

def validate_inputs(run_length, num_systems, max_queue_length, arrival_rate):
    if run_length <= 0:
        raise ValueError("Run length must be greater than 0.")
    if num_systems <= 0:
        raise ValueError("Number of systems must be greater than 0.")
    if max_queue_length <= 0:
        raise ValueError("Max queue length must be greater than 0.")
    if arrival_rate <= 0:
        raise ValueError("Arrival rate must be greater than 0.")

def record_state(env, car_wash, queue_data, car_wash_data, lost_cars_data, lost_cars, run_length):
    """Records the state of the system at regular intervals."""
    last_recorded_time = 0
    while env.now < run_length:
        queue_data.append(len(car_wash.queue))
        car_wash_data.append(len(car_wash.users))

        # Count lost cars only for the current time step
        lost_cars_in_step = len([t for t in lost_cars if last_recorded_time < t <= env.now])
        lost_cars_data.append(lost_cars_in_step)
        print(f"Time: {env.now}, Queue Length: {len(car_wash.queue)}, Cars in Wash: {len(car_wash.users)}, Lost Cars: {lost_cars_in_step}")

        last_recorded_time = env.now
        yield env.timeout(1)  # Record data every minute

def run_simulation_with_data(run_length, num_systems, max_queue_length, arrival_rate):
    """Run the car wash simulation and collect data."""
    validate_inputs(run_length, num_systems, max_queue_length, arrival_rate)

    env = simpy.Environment()
    car_wash = simpy.Resource(env, capacity=num_systems)
    drying = simpy.Resource(env, capacity=num_systems)
    waxing = simpy.Resource(env, capacity=num_systems)

    queue_data = []
    car_wash_data = []
    lost_cars = []
    lost_cars_data = []
    wait_times = []

    env.process(car_generator(env, car_wash, drying, waxing, arrival_rate, max_queue_length, queue_data, car_wash_data, lost_cars, wait_times))
    print("Starting simulation...")
    env.process(record_state(env, car_wash, queue_data, car_wash_data, lost_cars_data, lost_cars, run_length))
    print("Simulation in progress...")
    env.run(until=run_length)
    print("Simulation complete.")

    # Calculate metrics
    longest_wait = max(wait_times) if wait_times else 0
    average_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    total_reneged = len(lost_cars)

    return queue_data, car_wash_data, lost_cars_data, longest_wait, average_wait, total_reneged

if __name__ == "__main__":
    run_simulation_with_data(run_length=500, num_systems=2, max_queue_length=5, arrival_rate=0.6)
