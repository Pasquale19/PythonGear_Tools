import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon,Point,MultiPolygon

def GearRack2D(modul: float, pressure_angle_alpha: float, profile_shift_x: float, 
                                    center_x: float, center_y: float, number_of_teeth: int) -> tuple[np.ndarray, np.ndarray]:
    pitch = modul * np.pi
    tooth_height = 2.25 * modul
    addendum = (1 + profile_shift_x) * modul
    dedendum = (1.25 - profile_shift_x) * modul
    pressure_angle_rad = np.radians(pressure_angle_alpha)
    
    x_coords = []
    y_coords = []

    for i in range(number_of_teeth):
        start_x = center_x + i * pitch -pitch/4
        
        # Left side of tooth
        x_coords.extend([start_x- dedendum * np.tan(pressure_angle_rad), start_x + addendum * np.tan(pressure_angle_rad)])
        y_coords.extend([center_y - dedendum, center_y + addendum])
        
        # Top of tooth
        x_coords.append(start_x + pitch/2 - addendum * np.tan(pressure_angle_rad))
        y_coords.append(center_y + addendum)
        
        # Right side of tooth
        x_coords.append(start_x + pitch/2 + dedendum * np.tan(pressure_angle_rad))
        y_coords.append(center_y - dedendum)
# Closing the polygon
    x_coords.append(x_coords[-1])
    y_coords.append(y_coords[-1]-modul*10)
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0]-modul*10)
    return np.array(x_coords), np.array(y_coords)

def GearRack_Poly(modul: float, pressure_angle_alpha: float=20, profile_shift_x: float=0, 
                                    center_x: float=0, center_y: float=0, number_of_teeth: int=3) -> Polygon:
    x,y=GearRack2D(modul,pressure_angle_alpha,profile_shift_x,center_x,center_y,number_of_teeth)
    coords = list(zip(x, y))
    return Polygon(coords)

def plot_gear_racks():
    fig, ax = plt.subplots(figsize=(12, 8))
    racks = [
        (2.0, 20.0, 0.0, 0.0, 0.0, 1),
        (2.5, 25.0, 0.5, 0.0, 20.0, 8),
        (3.0, 15.0, -0.5, 0.0, 40.0, 1),
        (1.5, 30.0, 0.25, 0.0, 60.0, 15),
        (2.0, 22.5, -0.25, 0.0, 80.0, 10),
        (3.5, 18.0, 0.1, 0.0, 100.0, 7)
    ]
    
    lines = []
    for i, rack_params in enumerate(racks):
        x, y = GearRack2D(*rack_params)
        label = f'Rack {i+1}: m={rack_params[0]}, α={rack_params[1]}°, x={rack_params[2]}, n={rack_params[5]}'
        line, = ax.plot(x, y, label=label)
        lines.append(line)
    
    lines=ax.lines[:]
    legend=ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    leglines=legend.get_lines()
    graphs={}
    for count,l in enumerate(leglines):
        l.set_picker(True)
        l.set_pickradius(5)
        graphs[l]=lines[count]



    def on_pick(event):
        legline = event.artist
        graph=graphs[legline]
        vis = not graph.get_visible()
        graph.set_visible(vis)
        legline.set_alpha(1.0 if vis else 0.2)
        fig.canvas.draw()



    ax.set_aspect('equal', 'box')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid()
    ax.set_title('Gear Rack Profiles')
    fig.canvas.mpl_connect('pick_event', on_pick)
    plt.tight_layout() #adjust the spacing between plot elements
    plt.show()

if __name__ == "__main__":
    plot_gear_racks()