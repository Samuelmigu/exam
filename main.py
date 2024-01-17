import csv
import math
import PySimpleGUI as sg
import matplotlib.pyplot as plt

def calculate_trajectory(speed, angle):
    g = 9.8  # acceleration due to gravity

    # Convert angle to radians
    angle_rad = math.radians(angle)

    # Calculate initial velocity components
    v0_x = speed * math.cos(angle_rad)
    v0_y = speed * math.sin(angle_rad)

    # Calculate time of flight
    time_of_flight = (2 * v0_y) / g

    # Calculate maximum height
    max_height = (v0_y ** 2) / (2 * g)

    # Calculate maximum range
    max_range = v0_x * time_of_flight

    return {
        'Speed': speed,
        'Angle': angle,
        'Time of Flight': time_of_flight,
        'Max Height': max_height,
        'Max Range': max_range
    }

def save_to_csv(data, filename='projectiles_data.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(data)

def read_from_csv(filename='projectiles_data.csv'):
    projectiles_data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                projectiles_data.append({key: float(value) for key, value in row.items()})
    except FileNotFoundError:
        pass
    return projectiles_data

def calculate_max_distance(projectiles_data):
    return max(projectiles_data, key=lambda x: x['Max Range'])

def calculate_highest_height(projectiles_data):
    return max(projectiles_data, key=lambda x: x['Max Height'])

def flight_time_exceed_limit(projectiles_data, limit=5):
    return [proj for proj in projectiles_data if proj['Time of Flight'] > limit]

def plot_trajectory(trajectory_data):
    time = [point['Time'] for point in trajectory_data]
    height = [point['Height'] for point in trajectory_data]
    distance = [point['Distance'] for point in trajectory_data]

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time, height, label='Height')
    plt.title('Projectile Trajectory')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Height (meters)')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time, distance, label='Distance')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Distance (meters)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def trajectory_analysis(projectile, time_interval=0.1):
    g = 9.8  # acceleration due to gravity
    positions = []

    time = 0
    while time <= projectile['Time of Flight']:
        height = projectile['Speed'] * math.sin(projectile['Angle']) * time - (0.5 * g * time ** 2)
        distance = projectile['Speed'] * math.cos(projectile['Angle']) * time
        positions.append({'Time': time, 'Height': height, 'Distance': distance})
        time += time_interval

    return positions

def main():
    sg.theme('DarkGrey5')  # Choose a nice theme

    layout = [[sg.Button('Add Projectile', size=(20, 2))],
              [sg.Button('Calculate Statistics', size=(20, 2))],
              [sg.Button('Max Horizontal Distance', size=(20, 2))],
              [sg.Button('Highest Maximum Height', size=(20, 2))],
              [sg.Button('Flight Time Exceeding Limit', size=(20, 2))],
              [sg.Button('Trajectory Analysis', size=(20, 2))],
              [sg.Button('Compare Projectiles', size=(20, 2))],
              [sg.Button('Plot Trajectory', size=(20, 2))],
              [sg.Button('Exit', size=(20, 2))]]

    window = sg.Window('Projectile Analyzer', layout, size=(300, 300))

    projectiles_data = read_from_csv()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'Add Projectile':
            try:
                num_projectiles = int(sg.popup_get_text('Enter the number of projectiles to launch:', default_text='1'))
                projectiles = []

                for _ in range(num_projectiles):
                    speed = float(sg.popup_get_text('Enter speed (m/s) for projectile {}: '.format(_ + 1)))
                    angle = float(sg.popup_get_text('Enter launch angle (degrees) for projectile {}: '.format(_ + 1)))
                    projectile_data = calculate_trajectory(speed, angle)
                    projectiles.append(projectile_data)

                projectiles_data.extend(projectiles)
                save_to_csv(projectiles)
                sg.popup('Projectiles added successfully!')

            except ValueError:
                sg.popup_error('Invalid input. Please enter valid numerical values for speed and angle.')

        elif event == 'Calculate Statistics':
            if projectiles_data:
                max_heights = [proj['Max Height'] for proj in projectiles_data]
                max_ranges = [proj['Max Range'] for proj in projectiles_data]

                avg_max_height = sum(max_heights) / len(max_heights)
                avg_max_range = sum(max_ranges) / len(max_ranges)

                sg.popup(f'Average Max Height: {avg_max_height:.2f} meters\n'
                         f'Average Max Range: {avg_max_range:.2f} meters')

            else:
                sg.popup('No projectiles added. Please add projectiles first.')

        elif event == 'Max Horizontal Distance':
            if projectiles_data:
                max_distance_proj = calculate_max_distance(projectiles_data)
                sg.popup(f'Launch with Maximum Horizontal Distance:\n'
                         f'Speed: {max_distance_proj["Speed"]}, Angle: {max_distance_proj["Angle"]}\n'
                         f'Max Horizontal Distance: {max_distance_proj["Max Range"]:.2f} meters')

            else:
                sg.popup('No projectiles added. Please add projectiles first.')

        elif event == 'Highest Maximum Height':
            if projectiles_data:
                highest_height_proj = calculate_highest_height(projectiles_data)
                sg.popup(f'Launch with Highest Maximum Height:\n'
                         f'Speed: {highest_height_proj["Speed"]}, Angle: {highest_height_proj["Angle"]}\n'
                         f'Highest Maximum Height: {highest_height_proj["Max Height"]:.2f} meters')

            else:
                sg.popup('No projectiles added. Please add projectiles first.')

        elif event == 'Flight Time Exceeding Limit':
            if projectiles_data:
                limit = float(sg.popup_get_text('Enter the flight time limit (in seconds):', default_text='5'))
                exceeding_launches = flight_time_exceed_limit(projectiles_data, limit)
                msg = '\n'.join([f'Speed: {proj["Speed"]}, Angle: {proj["Angle"]}, '
                                f'Flight Time: {proj["Time of Flight"]:.2f} seconds' for proj in exceeding_launches])
                sg.popup(f'Launches with Flight Time Exceeding {limit} seconds:\n{msg}')

            else:
                sg.popup('No projectiles added. Please add projectiles first.')

        elif event == 'Trajectory Analysis':
            if projectiles_data:
                projectile_index = int(sg.popup_get_text('Enter the index of the projectile for trajectory analysis:',
                                                         default_text='0'))
                if 0 <= projectile_index < len(projectiles_data):
                    projectile = projectiles_data[projectile_index]
                    trajectory_data = trajectory_analysis(projectile)
                    save_trajectory_to_file(trajectory_data)
                    sg.popup(f'Trajectory data saved to trajectory_data.csv')
                else:
                    sg.popup_error('Invalid index. Please enter a valid index.')

            else:
                sg.popup('No projectiles added. Please add projectiles first.')

        elif event == 'Compare Projectiles':
            if len(projectiles_data) > 1:
                msg = '\n'.join([f'Projectile {idx + 1}: Speed={proj["Speed"]}, Angle={proj["Angle"]}, '
                                 f'Max Height={proj["Max Height"]:.2f}, Max Range={proj["Max Range"]:.2f}'
                                 for idx, proj in enumerate(projectiles_data)])
                sg.popup(f'Comparing Projectiles:\n{msg}')

            else:
                sg.popup('Add at least two projectiles to compare.')

        elif event == 'Plot Trajectory':
            if projectiles_data:
                projectile_index = int(sg.popup_get_text('Enter the index of the projectile for trajectory plot:',
                                                         default_text='0'))
                if 0 <= projectile_index < len(projectiles_data):
                    projectile = projectiles_data[projectile_index]
                    trajectory_data = trajectory_analysis(projectile)
                    plot_trajectory(trajectory_data)
                else:
                    sg.popup_error('Invalid index. Please enter a valid index.')

            else:
                sg.popup('No projectiles added. Please add projectiles first.')

    window.close()

if __name__ == '__main__':
    main()
