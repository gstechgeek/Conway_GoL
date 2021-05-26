import argparse
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('dark_background')

parser = argparse.ArgumentParser(description="Training Script")
parser.add_argument('-w', '--init-world', type=str, help='Path to image file for world initialization', default=None)
parser.add_argument('-s', '--world-size', type=int, help='Size of square canvas.', default=100)
parser.add_argument('-i', '--interval', type=int, help='Interval between consecutive frames in ms.', default=50)
args = parser.parse_args()

canvas = (args.world_size, args.world_size)
if args.init_world == None:
    frame = np.random.choice([1, 0], size=canvas[0] * canvas[1], p=[0.3, 0.7]).reshape(canvas)
else :
    img = ImageOps.invert(Image.open(args.init_world).convert('L'))
    frame = np.array(img.getdata()).reshape(img.size[0], img.size[1]) / 255
    frame = frame.astype(dtype=np.uint8)
    canvas = frame.shape

# frame = np.zeros(shape=canvas)
# add glider gun
# glider = np.array([[0, 1, 0],
#                    [0, 0, 1],
#                    [1, 1, 1]])
# for i in range(0, canvas[1], 10):
#     frame[10:13, i:i+3] = glider
#     frame[(canvas[0]-10):(canvas[0]-10) + 3, i:i+3] = np.rot90(np.rot90(glider))


def init():
    global frame
    return frame


def update(data):
    mat.set_data(data)
    return mat

def frame_gen(num_frames=None):
    global frame
    grid = frame.copy()
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            tot = int(frame[(i-1) % canvas[0]][(j-1) % canvas[1]] + frame[(i-1) % canvas[0]][j] + frame[(i-1) % canvas[0]][(j+1) % canvas[1]] + frame[i][(j-1) % canvas[1]] + \
                frame[i][(j+1) % canvas[1]] + frame[(i+1) % canvas[0]][(j-1) % canvas[1]] + \
                frame[(i+1) % canvas[0]][j] + \
                frame[(i+1) % canvas[0]][(j+1) % canvas[1]])
            
            if frame[i][j] == 1:
                if tot < 2 or tot > 3:
                    grid[i][j] = 0
            elif tot == 3:
                    grid[i][j] = 1
    frame = grid

    yield frame


fig, ax = plt.subplots()
fig.canvas.set_window_title('Sim')
mat = ax.matshow(init())
# plt.colorbar(mat)
anim = animation.FuncAnimation(
    fig, update, frame_gen, init_func=init, interval=args.interval)

plt.title('Game of Life Sim ({}x{})'.format(canvas[0], canvas[1]))
plt.axis('off')
plt.tight_layout()

# anim.save('test.gif', writer='imagemagick', fps=60)
plt.show()