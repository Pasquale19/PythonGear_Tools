import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Arrow
from math import pi, cos, sin

def cycloidal_profile_outer(N: int, radius: float, eccentricity: float, roller_radius: float, rotation_angle: float = 0, center_x: float = 0, center_y: float = 0, num_points: int = 1000):
    t = np.linspace(0, 2 * np.pi, num_points)
    R = radius
    E = eccentricity
    Rr = roller_radius

    psi = np.arctan2((np.sin((1 - N) * t)), ((R / (E * N)) - np.cos((1 - N) * t)))
    x = (R * np.cos(t)) - (Rr * np.cos(t + psi)) - (E * np.cos(N * t))
    y = (-R * np.sin(t)) + (Rr * np.sin(t + psi)) + (E * np.sin(N * t))

    x_rot = x * np.cos(np.radians(rotation_angle)) - y * np.sin(np.radians(rotation_angle))
    y_rot = x * np.sin(np.radians(rotation_angle)) + y * np.cos(np.radians(rotation_angle))

    x_final = x_rot + center_x
    y_final = y_rot + center_y

    return x_final, y_final

def main():
    N_init = 10
    R_init = 50
    Rr_init = 10
    delta_init = R_init / N_init
    E_init = min(4, delta_init)

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.subplots_adjust(left=0.1, bottom=0.3)

    x_cycloidal, y_cycloidal = cycloidal_profile_outer(N_init, R_init, E_init, Rr_init)
    cycloidal_gear, = ax.plot(x_cycloidal, y_cycloidal, 'b-', label="driven gear")

    driving_circle = plt.Circle((R_init - E_init, 0), Rr_init, fill=False, color='red', label="driving gear")
    ax.add_artist(driving_circle)
    x_eccentric, y_eccentric = R_init , 0
    eccentric_point, = ax.plot(x_eccentric, y_eccentric, 'ro', markersize=2)
    origin_point, = ax.plot(0, 0, 'bo', markersize=2)

    circle = plt.Circle((0, 0), R_init, fill=False, color='g')
    ax.add_artist(circle)

    # Add rotating arrow
    arrow = ax.arrow(x_eccentric, 0, -E_init, 0, head_width=Rr_init/10, head_length=Rr_init/10, fc='red', ec='red')

    ax.set_xlim(-R_init - 50, R_init + delta_init + Rr_init + 50)
    ax.set_ylim(-R_init - 50, R_init + 50)
    ax.grid()
    ax.set_aspect('equal')

    slider_color = 'lightgoldenrodyellow'
    ax_angle = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=slider_color)
    ax_N = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=slider_color)
    ax_R = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=slider_color)
    ax_E = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=slider_color)
    ax_Rr = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=slider_color)

    s_angle = Slider(ax_angle, 'Angle', 0, 360, valinit=0)
    s_N = Slider(ax_N, 'N', 3, 20, valinit=N_init, valstep=1)
    s_R = Slider(ax_R, 'R', 50, 200, valinit=R_init)
    s_E = Slider(ax_E, 'E', 0.1, delta_init, valinit=E_init)
    s_Rr = Slider(ax_Rr, 'Rr', 1, 20, valinit=Rr_init)

    angle_text = ax.text(0.05, 0.95, f'Gear 1: {0:.1f}°\nGear 2: {0:.1f}°', transform=ax.transAxes, verticalalignment='top')

    def update(val):
        angle = s_angle.val
        angle_rad = angle / 180 * pi
        N = int(s_N.val)
        R = s_R.val
        Rr = s_Rr.val
        delta = R / N

        s_E.valmax = delta
        E = min(s_E.val, delta)
        #s_E.set_val(E) #otherwise recursion appears

        cycloidal_angle = -angle * 1 / (N - 1)
        x_cycloidal, y_cycloidal = cycloidal_profile_outer(N, R, E, Rr, rotation_angle=cycloidal_angle)
        cycloidal_gear.set_data(x_cycloidal, y_cycloidal)

        x1, y1 = -E * cos(angle_rad) + R, -E * sin(angle_rad)
        driving_circle.set_radius(Rr)
        driving_circle.set_center((x1, y1))
        eccentric_point.set_data(R , 0)

        circle.set_radius(R)

        # Update rotating arrow
        arrow.set_data(x=R,y=0,dx=-E * cos(angle_rad), dy=y1)

        angle_text.set_text(f'Gear 1: {angle:.1f}°\nGear 2: {cycloidal_angle:.1f}°')

        ax.set_xlim(-R - 50, R + delta + Rr + 50)
        ax.set_ylim(-R - 50, R + 50)

        fig.canvas.draw_idle()

    s_angle.on_changed(update)
    s_N.on_changed(update)
    s_R.on_changed(update)
    s_E.on_changed(update)
    s_Rr.on_changed(update)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

if __name__ == "__main__":
    main()