'''
Requirements
1. Finish the team06 assignment (if necessary).
2. Change your program to process all 300 images using 1 CPU, then 2 CPUs, all the way up to the
   number of CPUs on your computer plus 4.
3. Keep track of the time it takes to process all 300 images per CPU.
4. Plot the time to process vs the number of CPUs.
   
Questions:
1. What is the relationship between the time to process versus the number of CPUs?
   Does there appear to be an asymptote? If so, what do you think the asymptote is?
   >I think that there is an asymptote 
   >
2. Is this a CPU bound or IO bound problem? Why?
   > CPU bound because we are foucused on useing all of the cpus as much a possiable
   >
3. Would threads work on this assignment? Why or why not? (guess if you need to) 
   > I dont think so becuase we are using all the cpus in this case and the work load is alread divied up
   > and there is no more space to seperate it more.
'''

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

# TODO Your final video need to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 300

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


def new_fun(files):
    create_new_frame(files[0], files[1], files[2])



if __name__ == '__main__':
    all_process_time = timeit.default_timer()

    # Use two lists: one to track the number of CPUs and the other to track
    # the time it takes to process the images given this number of CPUs.
    xaxis_cpus = []
    yaxis_times = []

    frames = []
    for image_number in range(1, FRAME_COUNT+1):
         image_file = rf'elephant/image{image_number:03d}.png'
         green_file = rf'green/image{image_number:03d}.png'
         process_file = rf'processed/image{image_number:03d}.png'

         frames.append((image_file, green_file, process_file))


    image_file = rf'elephant/image{image_number:03d}.png'
    green_file = rf'green/image{image_number:03d}.png'
    process_file = rf'processed/image{image_number:03d}.png'

    start_time = timeit.default_timer()
    create_new_frame(image_file, green_file, process_file)


    print(f'\nTime To Process all images = {timeit.default_timer() - start_time}')

    print(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')
    for i in range(1, CPU_COUNT+1): 
        with mp.Pool(i) as p:
            p.map(new_fun, frames)
        xaxis_cpus.append(i)
        if i == 1:
            yaxis_times.append(timeit.default_timer() - start_time)
        else:
            yaxis_times.append(timeit.default_timer() - (start_time + sum(yaxis_times)))

    # for i in range(CPU_COUNT):
    #     xaxis_cpus.append(i)
    # for i in range(CPU_COUNT):
    #     yaxis_times.append(timeit.default_timer() - all_process_time)
    

        
    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()
