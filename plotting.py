from nilearn import plotting
import os
import sys
import nibabel as nb
import numpy as np
from matplotlib import pyplot as plt
from math import ceil

opj = os.path.join

def get_motion_params(mc_par, mc_abs):
    dt = dict(names = ('R1','R2','R3','T1','T2','T3'),
              formats = (np.float32,np.float32,np.float32,
                         np.float32,np.float32,np.float32))
    motion_params = np.loadtxt(mc_par, dtype=dt)

    motion_dir = {}
    motion_dir['rot_1'] = motion_params['R1']
    motion_dir['rot_2'] = motion_params['R2']
    motion_dir['rot_3'] = motion_params['R3']
    motion_dir['tran_1'] = motion_params['T1']
    motion_dir['tran_2'] = motion_params['T2']
    motion_dir['tran_3'] = motion_params['T3']
    motion_dir['tran_abs'] = np.loadtxt(mc_abs)
    return motion_dir


def plot_motion_params(mc_par, mc_abs, title = ""):
    motion_params = get_motion_params(mc_par, mc_abs)
    num_timepoints = len(motion_params['tran_1'])

    fig = plt.figure(1)

    plt.subplot(211)
    plt.title('Subject %s Motion' %title)
    #ax1 = fig.add_subplot(2,1,1)
    plt.plot(motion_params['tran_1'])
    plt.plot(motion_params['tran_2'])
    plt.plot(motion_params['tran_3'])
    plt.plot(motion_params['tran_abs'])
    plt.plot([2.5]*num_timepoints, '--', color='grey')
    plt.plot([-2.5]*num_timepoints, '--', color='grey')
    plt.plot([0]*num_timepoints, color='black')
    plt.xlim(0, num_timepoints)
    plt.ylabel('Translation (mm)')

    plt.subplot(212)
    #ax2 = fig.add_subplot(2,1,2)
    plt.plot(motion_params['rot_1'])
    plt.plot(motion_params['rot_2'])
    plt.plot(motion_params['rot_3'])
    plt.plot([0.04]*num_timepoints, '--', color='grey')
    plt.plot([-0.04]*num_timepoints, '--', color='grey')
    plt.plot([0]*num_timepoints, color='black')

    plt.ylabel('Rotation (rad)')
    plt.xlabel('Time (TR)')
    plt.xlim(0, num_timepoints)
    return fig


def plot_mosaic(img_path, orientation, cols, aspect_ratio):
    
    data = nb.load(img_path)
    dim = data.shape   
    data = data.get_data()
    data[np.isnan(data)] = 0

    sorted_data = sorted(data.flatten())
    vmax = sorted_data[int(len(sorted_data)*0.99)]
    #vmax=1	
    if orientation == 'x':
        orientation = 0
    elif orientation == 'y':
        orientation = 1
    elif orientation == 'z':
        orientation = 2    

    rows = int(ceil(dim[orientation]/float(cols)))
#    print cols, rows, dim[orientation], dim[orientation]/float(cols), ceil(dim[orientation]/cols)    
#    slices = range(cols*rows)    
    #print rows
     
    height = rows*0.8
    w, h = plt.figaspect(aspect_ratio)
    fig, axs = plt.subplots(rows, cols, figsize=(w, h), facecolor='black', edgecolor='k',
                        sharey=True, sharex=True)    

    fig.subplots_adjust(hspace = 0, wspace=0)
    fig.subplots_adjust(0,0,1,1,0,0)
    plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
    i = 0
    for ax, d in zip(axs.ravel(), data):
        ax.axis('off')
        if i == dim[orientation]:
            break
        
        if orientation == 0:
            ax.imshow(np.rot90(data[i,:,:]), vmax=vmax, cmap='gray', interpolation='Nearest')
        elif orientation == 1:
            ax.imshow(np.rot90(data[:,i,:]), vmax=vmax, cmap='gray', interpolation='Nearest')
        elif orientation == 2:
            ax.imshow(data[:,:,i], vmax=vmax,  cmap='gray', interpolation='Nearest')
        i += 1

    #    plt.savefig(file_name, bbox_inches='tight')
    return fig

#f = open(sys.argv[1])
#folder = 'Output/110553'
#plot_config = 'plot_config.txt'

folder = sys.argv[1]
plot_config = sys.argv[2]

f = open(plot_config)

try:
    os.mkdir(opj(folder, 'qa_plots'))
except:
    import shutil
    shutil.rmtree(opj(folder, 'qa_plots'), ignore_errors=True)
    os.mkdir(opj(folder, 'qa_plots'))
    pass

i = 0
for line in f:
    if not line.strip():
        continue
    if line[0] == '#':
        continue


    #print 'line: ', line
    #for words
    words = ('add_contours', 'add_edges')
    verbs = [e for e in line.split() if e in words]
    #print verbs
    line = line.replace('add_contours', '%%%%%')
    line = line.replace('add_edges', '%%%%%')
    elements = line.split('%%%%%')
    #print len(elements)
    #print elements
    
    if elements[0].startswith("mosaic"):
        #print "MOSAIC"
        _, path, orientation, cols, aspect_ratio = elements[0].split()
        path = opj(folder, path)
        cols = int(cols)
        aspect_ratio = float(aspect_ratio)
        #print _, path, orientation, cols 
        display = plot_mosaic(path, orientation, cols, aspect_ratio)

    elif elements[0].endswith('/mc\n'): # plot motion params
        path = elements[0][:-1] #everything except '\n'
        mc_par = opj(folder, path, 'prefiltered_func_data_mcf.par')
        mc_abs = opj(folder, path, 'prefiltered_func_data_mcf_abs.rms')
        display = plot_motion_params(mc_par, mc_abs)
        #fig.savefig('params')

    else:
        path, display_mode, cut_coords = elements[0].split()
        path = opj(folder, path)

        #print path, display_mode, cut_coords

        data = nb.load(path).get_data().flatten()
        data = sorted(data[~np.isnan(data)])
        vmax=data[int(len(data)*0.99)]
        #print vmax

        #title = names of plotted files
        title = '  <- edges:  '.join([e.split()[0].split('/')[-1].split('.nii.gz')[0] for e in elements])
        display = plotting.plot_anat(path,
                       vmin=0,
                       vmax=vmax,
                       display_mode=display_mode,
                       cut_coords=int(cut_coords),
                       title=title)

        #print elements
        for element in elements[1:]:
            #print
            path = element.split()[0]
            path = opj(folder, path)
            #print element, 'path = ', path
            #display.add_edges(path)
            verb = verbs.pop(0)
            #print verb
            if verb == 'add_contours':
                display.add_contours(path, levels=[0.5, 6500], colors='r')
                display.add_contours(path, levels=[ 5000], colors='g')
            elif verb == 'add_edges':
                display.add_edges(path)
            else:
                print 'error'

    display.savefig(opj(folder, 'qa_plots/%s.png' %i))
    i += 1
#
#    display.add_contours(path)
f.close()

num_of_images=len([f for f in os.listdir(opj(folder, 'qa_plots')) if f.endswith('png')])

f = open(opj(folder, 'qa_plots/index.html'), 'w')

print >> f, '<HTML><HEAD><TITLE>QA plots</TITLE></HEAD><BODY>'
for i in range(num_of_images):
    print >> f, '<img BORDER=0 SRC="%s.png" width=1000><p>' %(i)
f.close()
