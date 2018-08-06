import imageio
import numpy
import random

reader = imageio.get_reader('c:/users/Terry Kolody/OneDrive/Video/201808041445.h264', format='ffmpeg')
writer = imageio.get_writer('c:/users/Terry Kolody/OneDrive/Video/processed.mp4', fps=30, macro_block_size=8)


for i, im in enumerate(reader):
    print('Mean of frame %i is %1.1f' % (i, im.mean()))

    writer.append_data(numpy.array(im))

reader.close()
writer.close()