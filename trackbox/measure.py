from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt

def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    x1, y1 = int(x1), int(y1)
    x2, y2 = int(x2), int(y2)

    time_spent = time_map[y1:y2, x1:x2].copy()
    time_spent = time_spent.sum()
    time_spent = float(time_spent) / frame_rate
    travel_distance = distance[y1:y2, x1:x2].copy()
    travel_distance = travel_distance.sum()

    title_string = "Coordinate of the selected rectangle (%d, %d) --> (%d, %d)\n" % (x1, y1, x2, y2)
    title_string += "Time spent in selected region: %.1fs at a framerate of %.1f\n" % (time_spent, frame_rate)
    title_string += "Travel distance in the selected region: %.2f cm" % (travel_distance * pixel_dist)

    plt.title(title_string)
    print(" Start and end coord: (%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print(" The button you used were: %s %s" % (eclick.button, erelease.button))


def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)


def interactive_measure(heatmap, center_video, ditance_map, perpix_dist, frate=15):
    global data, time_map, distance
    global frame_rate, pixel_dist
    data = center_video.copy()
    time_map = center_video.sum(0)
    distance = ditance_map.copy()
    frame_rate = frate
    pixel_dist = perpix_dist

    fig, current_ax = plt.subplots()    # make a new plotting range
    print("\n click  -->  release")
    plt.imshow(heatmap)

    # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                        drawtype='box', useblit=True,
                                        button=[1, 3],  # don't use middle button
                                        minspanx=5, minspany=5,
                                        spancoords='pixels',
                                        interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()