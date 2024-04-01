import tkinter

import numpy as np

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.tri as tri
import itertools

root = tkinter.Tk()
root.wm_title("OC WISK")

fig = Figure(figsize=(8, 6), dpi=100)

an = np.linspace(0, 2 * np.pi, 100)

t = np.arange(0, 3, 0.01)
ax = fig.add_subplot()
circle = ax.plot(8 * np.cos(an), 8 * np.sin(an))
ax.axis("equal")
ax.grid()
ax.set(xlim=(-10, 10), ylim=(-10, 10))
ax.set_xlabel("x")
ax.set_ylabel("y")

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

def key_press_handler(event):
    match event.key:
        case 'right':
            slider_update.set(slider_update.get() + 1)
        case 'left':
            slider_update.set(slider_update.get() - 1)

canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

def count_figures(points, amount):
    points = [tuple(point) for point in points]

    figures = 0

    for x in range(3, amount + 1):
        combinations = itertools.combinations(points, x)
        unique_figures = set(combinations)

        print(f"{str(x)}: {len(unique_figures)}")
        
        figures += len(unique_figures)

    return figures

def update_points(new_val):
    points = []
    ax.cla()

    circle = ax.plot(8 * np.cos(an), 8 * np.sin(an))
    ax.grid()

    # retrieve frequency
    n = int(new_val)
    r = 8

    alpha = np.pi * 2
    center = (0, 0)

    for i in range(1, n + 1):
        angle = alpha / n * i
        x = np.cos(angle) * r
        y = np.sin(angle) * r

        point = ax.plot(x, y, marker="o", markersize=5, markerfacecolor="red")
        points.append([x, y])

    print(count_figures(points, len(points)))

    ax.plot(
        *zip(*itertools.chain.from_iterable(itertools.combinations(points, 2))),
        marker='o', markerfacecolor='red'
    )

    # Draw lines
    # triang = tri.Triangulation(points["x"], points["y"])
    # ax.triplot(triang, 'bo-', lw=1)

    # required to update canvas and attached toolbar!
    canvas.draw()


slider_update = tkinter.Scale(
    root,
    from_=0,
    to=100,
    orient=tkinter.HORIZONTAL,
    command=update_points,
    label="Punten",
    length=400
)

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tkinter.BOTTOM)
slider_update.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

tkinter.mainloop()
