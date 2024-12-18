import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# def optimize_signal_timing():
#    current_state = get_current_traffic_state()
#    best_action = hill_climbing(current_state)
#    apply_action(best_action)

# def repeat():
#    while True:
#        optimize_signal_timing()
#        update_traffic_signals()
#        time.sleep(1)


# Can you add this file for fake data creation 



def simulate_mexico_city_traffic(num_days=30, intersections=5):
    # Generate dates
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(num_days)]

    data = []
    for date in dates:
        for hour in range(24):
            for intersection in range(intersections):
                time = date.replace(hour=hour, minute=0, second=0)

                # Define peak hours
                is_peak_hour = (5 <= hour <= 10) or (18 <= hour <= 21)
                is_weekend = date.weekday() >= 5

                # Traffic volume
                base_volume = np.random.poisson(100 if is_peak_hour else 30)
                volume_multiplier = 0.7 if is_weekend else 1.0
                traffic_volume = int(base_volume * volume_multiplier)

                # Average speed
                base_speed = np.random.normal(20 if is_peak_hour else 40, 5)
                speed_multiplier = 1.2 if is_weekend else 1.0
                average_speed = max(5, min(80, base_speed * speed_multiplier))

                # Road types
                road_types = ['Avenida Principal', 'Calle Secundaria', 'Eje Vial', 'Circuito Interior']
                road_type = np.random.choice(road_types)

                # Weather conditions
                weather_conditions = ['Clear', 'Rainy', 'Cloudy', 'Smog Alert']
                weather_weights = [0.6, 0.1, 0.2, 0.1]
                weather_condition = np.random.choice(weather_conditions, p=weather_weights)

                # Special events
                special_events = ['None', 'Zócalo Event', 'Estadio Azteca Match', 'Auditorio Nacional Concert']
                event_weights = [0.85, 0.05, 0.05, 0.05]
                special_event = np.random.choice(special_events, p=event_weights)

                # Adjust for special events
                if special_event != 'None':
                    traffic_volume *= 1.5
                    average_speed *= 0.8

                # Adjust for weather
                if weather_condition == 'Rainy':
                    traffic_volume *= 0.9
                    average_speed *= 0.8
                elif weather_condition == 'Smog Alert':
                    traffic_volume *= 0.95
                    average_speed *= 0.9

                data.append({
                    'datetime': time,
                    'intersection_id': intersection,
                    'traffic_volume': int(traffic_volume),
                    'average_speed': round(average_speed, 2),
                    'road_type': road_type,
                    'weather_condition': weather_condition,
                    'special_event': special_event
                })

    return pd.DataFrame(data)

