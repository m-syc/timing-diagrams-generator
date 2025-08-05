import matplotlib.pyplot as plt
from random import random
import os
from matplotlib.backends.backend_pdf import PdfPages

SIGNAL_PATTERN = 2
OUTPUT_PATTERN = 2
PAGE_NB = 3

MAX_X = 20.5
MAX_Y = 26.5
NUMENATOR = 3
DENOMINATOR = 5

def cm_to_inch(cm):
    return cm / 2.54

def fraction(x):
    return x * NUMENATOR / DENOMINATOR

def reverse_fraction(x):
    return x * DENOMINATOR / NUMENATOR

def draw_clk(ax, x_start, y_start, n, step=1.0, latch='r'):
    y = fraction(y_start)
    for i in range(n):
        x = x_start + i * step

        # vertical line
        ax.plot([x, x], [y, y + step], color='black')

        if i % 2 == 0:
            # upper horizontal line
            ax.plot([x, x + step], [y + step, y + step], color='black')
            if latch == 'r':
                ax.arrow(x, y + 0.2 * step, 0, 0.2 * step,
                     head_width=0.2, head_length=0.2, fc='black', ec='black')
        else:
            # lower horizontal line
            ax.plot([x, x + step], [y, y], color='black')
            if latch == 'f':
                ax.arrow(x, y + 0.8 * step, 0, -0.2 * step,
                     head_width=0.2, head_length=0.2, fc='black', ec='black')

def draw_signal(ax, x_start, y_start, n, step=1.0):
    i = 0
    x = x_start
    y = fraction(y_start)

    while x < n:
        dx = random() * step * 5  # random length of vertical line

        if i % 2 == 0:
            # lower horizontal line
            ax.plot([x, x + dx], [y, y], color='black')
        else:
            # upper horizontal line
            ax.plot([x, x + dx], [y + step, y + step], color='black')
    
        x = x + dx
        i += 1
        
        # vertical line
        ax.plot([x, x], [y, y + step], color='black')

def create_figure(width, height):
    width_inch = cm_to_inch(width - 1)
    height_inch = cm_to_inch(height - 1)
    fig, ax = plt.subplots(figsize=(width_inch, height_inch))
    return fig, ax

def draw_background(ax, max_y):
    for y in range(0, int(reverse_fraction(max_y)), 2):
        ax.axhspan(fraction(y), fraction(y + 1), facecolor='lightblue', alpha=0.3)

def draw_grid(ax, max_x, max_y):
    for y in range(int(reverse_fraction(max_y))):
        ax.axhline(fraction(y), color='gray', linestyle='--', linewidth=0.5)
    for x in range(int(reverse_fraction(max_x))):
        ax.axvline(fraction(x), color='gray', linestyle='--', linewidth=0.5)

def draw_figure(ax):
    draw_background(ax, MAX_Y)
    draw_grid(ax, MAX_X, MAX_Y)

    # spacing for clock and signals input/output
    spacing = (1 + SIGNAL_PATTERN + OUTPUT_PATTERN) * 2

    for row in range(0, int(reverse_fraction(MAX_Y)), spacing):
        draw_clk(ax, x_start=0, y_start=row, n=40, step=fraction(1), latch='f')
        # draw_clk(ax, x_start=0, y_start=row, n=40, step=fraction(1), latch='f')

    for i in range(2 * (SIGNAL_PATTERN + OUTPUT_PATTERN), int(reverse_fraction(MAX_Y)), spacing):
        for j in range(SIGNAL_PATTERN):
            draw_signal(ax, x_start=0, y_start=(i - 2 * j), n=40, step=fraction(1))

    ax.set_xlim(1, MAX_X)
    ax.set_ylim(1, MAX_Y)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()

def main():
    pdf_path = "timing-circuits.pdf"
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    with PdfPages(pdf_path) as pdf:
        for idx in range(PAGE_NB):  # Example: generate 3 figures
            fig, ax = create_figure(MAX_X, MAX_Y)
            draw_figure(ax)
            pdf.savefig(fig)
            plt.close(fig)

main()
