import imageio
import numpy
import random

from gmeter import GMeter
from rpm import RPM

gm = GMeter(size=256, fontfile='Jura-SemiBold.ttf')
rpm = RPM(size=512, fontfile='Jura-SemiBold.ttf')


from PIL import Image

reader = imageio.get_reader('my_video.h264', format='ffmpeg')
fps = reader.get_meta_data()['fps']
writer = imageio.get_writer('processed.mp4', fps=fps, macro_block_size=8)


for i, im in enumerate(reader):
    print('Mean of frame %i is %1.1f' % (i, im.mean()))
    gm_image = gm.draw_meter(x=random.random()-0.5*2.5, y=random.random()-0.5*2.5)
    rpm_image = rpm.draw_meter(rpm=100)

    pim = Image.fromarray(im)

    pc = pim.crop([0,1080-265, 256, 1071])
    prpm = pim.crop([512, 1080-512, 512+512, 1080])

    pcnew=Image.alpha_composite(pc.convert('RGBA'), gm_image)
    prpmnew=Image.alpha_composite(prpm.convert('RGBA'), rpm_image)

    pim.paste(pcnew, (0,1080-265))
    pim.paste(prpmnew, (512, 1080-512))

    writer.append_data(numpy.array(pim))

    if i > 30:
        break

reader.close()
writer.close()
