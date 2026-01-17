"""
Bubble Sort Visualizer (matplotlib animation)

How to use:
  - Install dependencies:
      pip install matplotlib numpy

  - Run:
      python bubble_sort_visual.py
    Optional args:
      --n N         # number of elements (default 20)
      --interval I  # ms between frames (default 150)
      --seed S      # random seed

What it does:
  - Generates a random integer list and produces an animated bar chart.
  - Highlights the two elements being compared (yellow) and swapped (red).
  - When finished, bars turn green (sorted).
"""

import argparse
import random
import copy
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def bubble_sort_steps(arr):
    """
    Generator yielding steps for visualization.
    Yields tuples: (action, i, j, array_snapshot)
      action: 'compare', 'swap', 'done'
      i, j: indices involved (-1 if none)
      array_snapshot: shallow copy of current array
    """
    a = arr[:]  # work on copy
    n = len(a)
    if n <= 1:
        yield ('done', -1, -1, a.copy())
        return

    for passnum in range(n - 1):
        made_swap = False
        for j in range(n - passnum - 1):
            # comparison step
            yield ('compare', j, j + 1, a.copy())
            if a[j] > a[j + 1]:
                # swap step
                a[j], a[j + 1] = a[j + 1], a[j]
                made_swap = True
                yield ('swap', j, j + 1, a.copy())
        # if no swaps were made, array is sorted -> we can finish early
        if not made_swap:
            break

    yield ('done', -1, -1, a.copy())


def make_animation(data, interval=150, title="Bubble Sort Visualization"):
    """
    Create a matplotlib FuncAnimation from a list of steps produced by bubble_sort_steps.
    """
    steps = list(data)  # materialize generator into frames
    if len(steps) == 0:
        raise ValueError("No steps to animate")

    # final array length from first snapshot
    _, _, _, arr0 = steps[0]
    n = len(arr0)
    indices = np.arange(n)

    fig, ax = plt.subplots(figsize=(max(6, n * 0.25), 4))
    plt.title(title)
    bar_container = ax.bar(indices, arr0, align='center', color='tab:blue', edgecolor='black')
    ax.set_xlim(-0.5, n - 0.5)
    padding = max(1, int(max(arr0) * 0.05))
    ax.set_ylim(0, max(arr0) + padding)

    # Text to show current operation
    op_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=10, verticalalignment='top')

    def update(frame_index):
        action, i, j, arr = steps[frame_index]
        # update bar heights
        for rect, h in zip(bar_container, arr):
            rect.set_height(h)
            rect.set_color('tab:blue')  # default

        # Color-code relevant bars
        if action == 'compare':
            if 0 <= i < n:
                bar_container[i].set_color('gold')
            if 0 <= j < n:
                bar_container[j].set_color('gold')
            op_text.set_text(f"Comparing indices {i} and {j}")
        elif action == 'swap':
            if 0 <= i < n:
                bar_container[i].set_color('crimson')
            if 0 <= j < n:
                bar_container[j].set_color('crimson')
            op_text.set_text(f"Swapped indices {i} and {j}")
        elif action == 'done':
            # mark all bars as sorted (green)
            for rect in bar_container:
                rect.set_color('seagreen')
            op_text.set_text("Sorted ✔")
        else:
            op_text.set_text(str(action))

        return (*bar_container, op_text)

    ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=interval, blit=False, repeat=False)
    return ani


def ascii_visual(arr, width=50):
    """
    Simple ASCII visualization for terminal: prints horizontal bars scaled to width.
    Useful if you can't run the graphical animation.
    """
    maxv = max(arr) if arr else 1
    for v in arr:
        bar = '#' * int((v / maxv) * width)
        print(f"{v:3} |{bar}")


def main():
    parser = argparse.ArgumentParser(description="Bubble Sort Visualizer")
    parser.add_argument('--n', type=int, default=20, help='number of elements to sort')
    parser.add_argument('--interval', type=int, default=150, help='milliseconds between frames')
    parser.add_argument('--seed', type=int, default=None, help='random seed')
    parser.add_argument('--ascii', action='store_true', help='print ASCII steps in terminal (non-graphical)')
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    if args.n <= 0:
        print("n must be > 0")
        sys.exit(1)

    # Create random data
    data = list(np.random.randint(1, args.n * 5 + 1, size=args.n))
    print("Initial array:", data)

    if args.ascii:
        # Produce ASCII step-by-step with a short pause
        import time
        for step in bubble_sort_steps(data):
            action, i, j, arr = step
            print("\033[H\033[J", end="")  # clear terminal (works on many terminals)
            print(f"Action: {action}  indices: {i},{j}")
            ascii_visual(arr, width=60)
            time.sleep(args.interval / 1000.0)
        print("Done.")
        return

    # Graphical animation
    ani = make_animation(bubble_sort_steps(data), interval=args.interval,
                         title="Bubble Sort Visualization (blue=idle, yellow=compare, red=swap, green=done)")

    # To show interactively:
    plt.show()

    # If you'd like to save the animation to file (mp4 or gif), uncomment below:
    # Requires ffmpeg (for mp4) or pillow (for gif). Example to save:
    # ani.save('bubble_sort.mp4', writer='ffmpeg', fps=1000/args.interval)
    # ani.save('bubble_sort.gif', writer='pillow', fps=1000/args.interval)


if __name__ == '__main__':
    main()