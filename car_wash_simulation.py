import simpy
import random
import matplotlib.pyplot as plt  # Add this import for plotting

def car(env, name, wash_station, dry_station, wax_station, wash_to_dry_queue, dry_to_wax_queue, stats):
    """A car process that goes through wash, dry, and wax."""
    print(f'{name} arrives at the car wash at {env.now:.2f}')
    
    # Wash step
    with wash_station.request() as request:
        stats['wash_queue'].append((env.now, len(wash_station.queue)))
        stats['wash_active'].append((env.now, len(wash_station.users)))
        yield request
        print(f'{name} enters the wash station at {env.now:.2f}')
        yield env.timeout(random.uniform(5, 10))  # Washing takes 5-10 minutes
        print(f'{name} leaves the wash station at {env.now:.2f}')
    
    # Move to dry queue
    yield wash_to_dry_queue.put(name)
    print(f'{name} enters the wash-to-dry queue at {env.now:.2f}')
    yield wash_to_dry_queue.get()
    
    # Dry step
    with dry_station.request() as request:
        stats['dry_queue'].append((env.now, len(dry_station.queue)))
        stats['dry_active'].append((env.now, len(dry_station.users)))
        yield request
        print(f'{name} enters the dry station at {env.now:.2f}')
        yield env.timeout(random.uniform(3, 7))  # Drying takes 3-7 minutes
        print(f'{name} leaves the dry station at {env.now:.2f}')
    
    # Move to wax queue
    yield dry_to_wax_queue.put(name)
    print(f'{name} enters the dry-to-wax queue at {env.now:.2f}')
    yield dry_to_wax_queue.get()
    
    # Wax step
    with wax_station.request() as request:
        stats['wax_queue'].append((env.now, len(wax_station.queue)))
        stats['wax_active'].append((env.now, len(wax_station.users)))
        yield request
        print(f'{name} enters the wax station at {env.now:.2f}')
        yield env.timeout(random.uniform(4, 8))  # Waxing takes 4-8 minutes
        print(f'{name} leaves the wax station at {env.now:.2f}')

def setup(env, num_washers, num_dryers, num_waxers, arrival_rate, stats):
    """Set up the car wash simulation."""
    wash_station = simpy.Resource(env, num_washers)
    dry_station = simpy.Resource(env, num_dryers)
    wax_station = simpy.Resource(env, num_waxers)
    
    # Limited queues between processes
    wash_to_dry_queue = simpy.Store(env, capacity=1)
    dry_to_wax_queue = simpy.Store(env, capacity=1)
    
    # Generate cars
    car_id = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate))  # Cars arrive randomly
        car_id += 1
        env.process(car(env, f'Car {car_id}', wash_station, dry_station, wax_station, wash_to_dry_queue, dry_to_wax_queue, stats))

def plot_stats(stats):
    """Plot the collected statistics."""
    plt.figure(figsize=(12, 8))
    
    # Plot wash station stats
    times, queue_lengths = zip(*stats['wash_queue'])
    plt.plot(times, queue_lengths, label='Wash Queue Length')
    times, active_counts = zip(*stats['wash_active'])
    plt.plot(times, active_counts, label='Wash Active Processes')
    
    # Plot dry station stats
    times, queue_lengths = zip(*stats['dry_queue'])
    plt.plot(times, queue_lengths, label='Dry Queue Length')
    times, active_counts = zip(*stats['dry_active'])
    plt.plot(times, active_counts, label='Dry Active Processes')
    
    # Plot wax station stats
    times, queue_lengths = zip(*stats['wax_queue'])
    plt.plot(times, queue_lengths, label='Wax Queue Length')
    times, active_counts = zip(*stats['wax_active'])
    plt.plot(times, active_counts, label='Wax Active Processes')
    
    plt.xlabel('Time (minutes)')
    plt.ylabel('Count')
    plt.title('Car Wash Simulation Statistics')
    plt.legend()
    plt.grid()
    plt.show()

# Initialize the simulation environment
random.seed(42)  # For reproducibility
env = simpy.Environment()

# Parameters
num_washers = 2
num_dryers = 2
num_waxers = 1
arrival_rate = 2 / 3  # Average of 1 car every 3 minutes

# Statistics collection
stats = {
    'wash_queue': [],
    'wash_active': [],
    'dry_queue': [],
    'dry_active': [],
    'wax_queue': [],
    'wax_active': []
}

# Start the setup process
env.process(setup(env, num_washers, num_dryers, num_waxers, arrival_rate, stats))

# Run the simulation for 240 minutes
env.run(until=240)

# Plot the results
plot_stats(stats)
