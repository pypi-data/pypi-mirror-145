import os
from typing import List
import ssqueezepy
import numpy as np
import test_material_brain as mb
from scipy import signal as sgl
import matplotlib.pyplot as plt
from skimage import transform,morphology,io,color

FIGSIZE = (14, 7)
LC_LINE_COLOR = 'r'
FIRST_PEAK_LINE_COLOR = 'g'

__all__ = ['check_data', 'findNearestValue', 'plot_lcs', 'plot_lc', 'plot_lc_panorama', 'ComputeFs', 'normalize', 'display_wavelets_type',
           'scalogram', 'errors_overview', 'find_first_peak_by_distance', 'downscale_panorama', 'display_panorama','getImageLength', 
           'setImageToDataLength', 'cropImage', 'resizeImage', 'list_files', 'listImages', 'FIGSIZE', 'LC_LINE_COLOR', 'FIRST_PEAK_LINE_COLOR']

def check_data(scratchs:List['mb.Scratch'], signals = ['Ft', 'Ae', 'Pd', 'FnC', 'Pf', 'Rd', 'Fn', 'mu'], lcs = [1, 2, 3, 4], check_panorama = True):
    """
    ### Function to check scratch files content
    
    #### Inputs:
    - scratchs          List of scratchs to be checked
    - signals           Name of the signals to be checked, can be : 'Ft', 'Ae', 'Pd', 'FnC', 'Pf', 'Rd', 'Fn' or 'mu' (ex. [Ft, Pd] to check Ft and Pd)
    - lcs               Numbers of the critical loads to be checked (ex. [1,3] to check LC1 and LC3)
    - check_panorama    Boolean, if true check panorama image
    """

    for scratch in scratchs:

        is_missing = False

        message = f"------------------------------------------------------------------------------------------------------------\n" \
              f"{scratch.filename}\n" \
              f"------------------------------------------------------------------------------------------------------------\n"

        # Check signals
        for signal in signals:
            if not scratch.has_signal(signal):
                is_missing = True
                message += f"No {signal} signal found.\n"

        # Check critical loads
        for lc in lcs:
            if not scratch.has_lc(lc):
                is_missing = True
                message += f"No LC{lc} found.\n"

        # Check panorama image
        if check_panorama:
            if not scratch.has_panorama():
                is_missing = True
                message += "No panorama image found.\n"

        if is_missing == True:
            print(message)

def findNearestValue(array, value):
    """
    ### Function to find the index of the nearest value in an array
    
    #### Inputs:
    - array     Aarray where to search the nearest value
    - value     value to look for

    #### Outputs:
    - idx       Nearest value index
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def plot_lcs(scratch:'mb.Scratch', ax, lcs = [1,2,3,4], xAxis = 'position', color = LC_LINE_COLOR):
    """
    ### Function to plot vertical lines at critical loads on graph
    
    #### Inputs:
    - scratch   Scratch
    - ax        Axis where to plot the lines
    - lcs       Numbers of the critical loads to plot (ex. [1,3] to plot LC1 and LC3)
    - xAxis     Name of the x-axis, can be : 'time', 'position' or 'none'
    - color     Lines color
    """

    for lc in lcs:
        if scratch.has_lc(lc):
            plot_lc(scratch, lc, ax, xAxis, color)

def plot_lc(scratch:'mb.Scratch', lc, ax, xAxis = 'position', color = LC_LINE_COLOR, label = None):
    """
    ### Function to plot a vertical line at critical load on graph
    
    #### Inputs:
    - scratch   Scratch
    - lc        Number of the critical load (ex. 1 for LC1)
    - ax        Axis where to plot the line
    - xAxis     Name of the x-axis, can be : 'time', 'position' or 'none'
    - color     Line color
    - label     label that will be displayed in the legend
    """

    index = scratch.lc_index(lc)

    if xAxis == 'time':
        position = scratch.t[index]
    elif xAxis == 'position':
        position = scratch.pos[index]
    else:
        position = index

    # Plot vertical line
    ax.axvline(position, c = color, label = label)

    # Compute text position
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    xgap = 0.5 * (xmax - xmin) / 100    # 0.5   %
    ygap = 3 * (ymax - ymin) / 100      # 3     %

    # Plot text
    ax.text(position + xgap, ymax - ygap, f"LC{lc}", c = color)
            
def plot_lc_panorama(scratch:'mb.Scratch', ax, lcs=[1,2,3,4], len_xAxis=None, start_ind=0, end_ind=-1, color='red', label=None):
    """
    ### Function to plot a vertical line at critical load on graph
    
    #### Inputs:
    - scratch   Scratch
    - lcs       Number of the critical load (ex. 1 for LC1)
    - ax        Axis where to plot the line
    - len_xAxis len of full x axis
    - start_ind select pixel start if you are not diplaying the whole panorama
    - color     Line color
    - label     label that will be displayed in the legend
    """
    if isinstance(lcs, int):
        lcs = [lcs]

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    xgap = 0.5 * (xmax - xmin) / 100    # 0.5   %
    ygap = 3 * (ymax - ymin) / 100      # 3     %

    if len_xAxis is None:
        len_xAxis = np.shape(scratch.panorama)[1]

    if end_ind == -1:
        end_ind = len_xAxis

    for lc in lcs:
        if scratch.has_lc(lc):
            index = scratch.lc_index(lc)
            pixel = (index / scratch.length() * len_xAxis)-start_ind

            if pixel >= 0 and pixel < end_ind-start_ind:
                ax.axvline(pixel, c=color, label = label)
                ax.text(pixel + xgap, ymin + ygap, f"LC{lc}", c = color)     

def ComputeFs(t):
    """
    ### Function to compute the sampling frequency on a time vector
    
    #### Inputs:
    - t     the time vector
    
    #### Outputs:
    - Fs    the sampling frequency
    """
    return len(t) / (max(t)-min(t))

def normalize(signal):
    """
    ### Function to normalize a signal
    
    #### Inputs:
    - signal        signal
    
    #### Outputs:
    - normSignal    normalized signal
    """
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal))

def display_wavelets_type():
    """
    Function to display ssqueezepy builtin wavelets.
    """

    wavelets = ssqueezepy.wavs()

    # Display
    print('ssqueezepy builtin wavelets:')

    for i, wavelet in enumerate(wavelets, start = 1):
        print(f'  {i}. {wavelet}')

def scalogram(scratch:'mb.Scratch', signal_name, func = None, wavelet = 'gmw', savgol = False, x_min = None, x_max = None, scalo_infos = False, scales_thresh = None, lc = 2, prominence = 0.08, max_distance = 50, σ_coef = 3, figsize = FIGSIZE):
    """
    Function to compute and display a signal's continuous wavelet transform (CWT).
    This function can also display CWT's mean and standard deviation.
    
    Arguments:
    -------------------
    - scratch               Scratch object
    - signal_name           Name of the signal, can be : 'Ft', 'Ae', 'Pd', 'FnC', 'Pf', 'Rd', 'Fn' or 'mu'
    - func                  Function to apply to the selected signal (ex. func = lambda signal : process(signal, param1, param2))
    - wavelet               Name of builtin wavelet. See `ssqueezepy.wavs()` or `Wavelet.SUPPORTED`.
    - savgol                Boolean, if true compute first derivative to the signal before doing continuous wavelet transform (CWT)
    - xMin                  Index of the minimum value for the x-axis
    - xMax                  Index of the maximum vlaue for the x-axis
    - scalo_infos           Boolean, if true display scalogram mean and standard deviation
    - scales_thresh         Scales treshold
    - lc                    Number of the critical load to predict (ex. 1 for LC1)
    - porminence            Prominence of the peaks in the mean signal of the scalogram
    - max_distance          Required maximal horizontal distance in % of the total signal lenghth between first peak and next peak
    - figsize               Size of the figure to display
    
    Returns:
    -------------------
    - error                 Error of the prediction in %
    """

    # Variables
    #-----------------------------------------------------------
    pos = scratch.pos[x_min:x_max]

    if not func is None:
        signal = func(scratch.signals[signal_name][x_min:x_max])
    else:
        signal = scratch.signals[signal_name][x_min:x_max]

    if savgol:
        signal = sgl.savgol_filter(signal, 3, 1, deriv = 1)
    
    # Do the continuous wavelet transform (CWT)
    #-----------------------------------------------------------
    Wx, scales = ssqueezepy.cwt(signal, wavelet, scales = 'log-piecewise', fs = scratch.fs)
    
    # PLot scalogram
    #-----------------------------------------------------------
    fig, ax = plt.subplots(figsize = figsize)
    ssqueezepy.visuals.imshow(Wx, show = False, yticks = scales, xticks = pos, abs = 1,
                              title = f'abs(CWT) | {wavelet} wavelet',
                              ylabel = "scales", xlabel = "time [s]",
                              fig = fig, ax = ax)
    if scratch.has_lc(lc):
        plot_lc(scratch, lc, ax, xAxis = 'None')

    plt.show()
    
    if scalo_infos:
        # Compute scalogram mean and std
        #-----------------------------------------------------------
        nbCol = np.size(Wx, 1)
        mean = np.zeros(nbCol)
        std = np.zeros(nbCol)
        
        if scales_thresh is None:
            index = -1
        else:
            index = findNearestValue(scales, scales_thresh)
            
        for i in range(nbCol):
            mean[i] = np.mean(np.abs(Wx[0:index,i]))
            std[i] = np.std(np.abs(Wx[0:index,i]))
        
        # Find peaks (maxima) in mean
        #-----------------------------------------------------------
        std_norm = normalize(std)
        mean_norm = normalize(mean)   
        peaks, _ = sgl.find_peaks(mean_norm, height = None, prominence = prominence)
        peaks_pos_std = np.std(peaks)
        peaks_mean = np.mean(peaks)
        first_peak = find_first_peak_by_distance(pos, peaks, max_distance)
        
        # Find accurate first peak
        #-----------------------------------------------------------
        peaks_pos_std = pos[round(np.std(peaks))]
        peaks_pos_mean = pos[round(np.mean(peaks))]

        x1 = peaks_pos_mean - peaks_pos_std * σ_coef
        x2 = peaks_pos_mean + peaks_pos_std * σ_coef

        if x2 > pos[-1]:
            x2 = pos[-1]

        x1_peaks = 0
        x2_peaks = -1

        for i, peak in enumerate(peaks):
            if pos[peak] >= x1:
                x1_peaks = i
                break

        for i, peak in enumerate(peaks):
            if pos[peak] > x2:
                x2_peaks = i-1
                break

        first_peak = find_first_peak_by_distance(pos, peaks[x1_peaks:x2_peaks], max_distance)

        # Compute error
        #-----------------------------------------------------------

        if scratch.has_lc(lc):
            if not first_peak is None:
                error = np.abs(scratch.pos[scratch.lc_index(lc)] - pos[first_peak]) / scratch.pos[-1] * 100
            else:
                print('First peak not found.')
                error = 100
        else:
            error = 0
        
        # Dsiplay Scalogram informations with peaks
        #-----------------------------------------------------------
        fig, ax = plt.subplots(figsize = figsize)
        
        # Display mean
        ax.set_title('Scalogram information')
        ax.grid(b = True, which = 'major', axis = 'both')
        ax.plot(pos, mean_norm, label = 'mean')
        #ax.plot(pos, std_norm, label = 'std')

        # Display peaks
        ax.scatter(pos[peaks], mean_norm[peaks], color = 'r', s = 10, marker = 'D', label = 'Maxima')

        # Diplay LC and predicted LC
        if scratch.has_lc(lc):
            plot_lc(scratch, lc, ax, 'position', label = 'cohesive spallation')
        if error < 100:
            ax.axvline(pos[first_peak], c='b', label = 'Predicted cohesive spallation')

        # Display peaks mean and selected range
        ax.axvline(pos[round(peaks_mean)], c='orange', label = 'peaks mean position')
        ax.axvspan(x1, x2, alpha=0.1, color='orange')

        ax.set_xlabel('time [s]')
        ax.margins(x=0, y=0)
        plt.legend(loc='best')
        plt.show()

        return error

def errors_overview(errors, percentage = 95, figsize = FIGSIZE, show = True):
    """
    Function to display a global overview of all prediction errors.
    This function compute also the mean and median of all errors.
    
    Arguments:
    -------------------
    - errors                Array of errors in %
    - percentage            Percentage of errors under a maximum value of error
    - figsize               Size of the figure to display
    - show                  Boolean, if true display the figure
    
    Returns:
    -------------------
    - fig                   Figure
    - ax                    Axis
    """

    nb_pred = len(errors)
    errors_sorted = np.sort(errors)
    fig, ax = plt.subplots(figsize = figsize)
    ax.set_title(f'Automatic LC prediction errors  |  Nb. of scratches : {nb_pred}  |  {percentage} % of total is under {errors_sorted[round(nb_pred / 100 * percentage) - 1]:.2f} % error')
    ax.grid(b = True, which = 'major', axis = 'both')
    ax.stem(errors, linefmt = ':', basefmt = " ", label = 'errors')
    ax.set_xlabel('Scratches [-]')
    ax.set_ylabel('Prediction error [%]')

    # Compute mean and median
    mean = np.mean(errors)
    median = np.median(errors)

    # Display mean and median
    ax.axhline(mean, c='r', label = f'mean = {mean:.2f} %')
    ax.axhline(median, c='g', label = f'median = {median:.2f} %')

    if show:
        plt.legend(loc='best')
        plt.show()

    return fig, ax

def find_first_peak_by_distance(pos, peaks, max_dist):
    """
    Function to find first peak by taking into account a maximal distance (in % of the total signal lenghth) with the next peak.
    
    Arguments:
    -------------------
    - pos       Array of position
    - peaks     Array pf peaks
    - max       Maximum value in % of the total signal lenghth
    
    Returns:
    -------------------
    - peak      Index of the first peak
    """

    nb_peaks = len(peaks)

    distances = np.zeros(nb_peaks)
    if peaks.any():
        for i in range(nb_peaks - 1):
            distances[i] = pos[peaks[i+1]] - pos[peaks[i]]

        for i, distance in enumerate(distances):
            if distance <= max_dist * pos[-1] / 100:
                return peaks[i]

    return None

def downscale_panorama(panorama, downscale_ratio):
    if len(np.shape(panorama)) == 2:
        downscaled_panorama = transform.downscale_local_mean(np.array(panorama), (downscale_ratio, downscale_ratio))
    elif len(np.shape(panorama)) == 3:
        downscaled_panorama = transform.downscale_local_mean(np.array(panorama), (downscale_ratio, downscale_ratio, 1))
    return downscaled_panorama

def display_panorama(panorama=[], scratch:'mb.Scratch'=None, div=0, downscale_ratio=1, title = False, show_lcs = False, show = True, borne=[0,-1,0,-1]):
        if len(panorama)==0:
            panorama = scratch.panorama
            div = 255

        if div == 0 and np.max(panorama) <= 1:
            div = 1
        elif div == 0 and np.max(panorama) <= 255:
            div = 255
        elif div == 0:
            div = np.max(panorama)

        image = downscale_panorama(panorama, downscale_ratio) / div
        
        fig, ax = plt.subplots(figsize = (18, 9), clear = True)
        ax.set_xmargin(0)
        ax.set_yticks([])
        ax.set_xticks([])
        plt.box(on = None)
        if title : plt.title(scratch.filename , fontsize=15, color = 'white')
        io.imshow(image[borne[0]:borne[1],borne[2]:borne[3]])

        if show_lcs:
            plot_lc_panorama(scratch, ax, len_xAxis=np.shape(image)[1], start_ind=borne[2], end_ind=borne[3])

        if show: plt.show()

        return fig, ax, image

def getImageLength(image):
    """ Function to get length in mm of an image
        -------------------
        Input parameter :
        - image : Panoramic image of scratch measure
        -------------------
        return : 
        - imgae length : total length of image in mm
        - LenPerPix : length in mm of every pixel
    """

    grayscaleImage = color.rgb2gray(image)
    height, width = np.shape(grayscaleImage)
    posx = round(width/20)
    posy = round(height*4/5)
    # print(posx, posy)
    # print(np.min(grayscaleImage[posy-4:posy+4,posx]))

    bwImage = grayscaleImage < 0.1
    # plt.imshow(bwImage, 'gray')
    # plt.show()
    diskOpeningImage = morphology.closing(bwImage,  morphology.square(4))

    # plt.imshow(diskOpeningImage, 'gray')
    # plt.show()
    i = 0
    while(True):
        if(diskOpeningImage[posy, posx+i] == 0):        
            i -= 1
            # print(i)
            break
        i += 1
        
    LenPerPix = 0.05/(i-1)
    # print(LenPerPix*width)
    return LenPerPix*width, LenPerPix

def setImageToDataLength(image, X):
    """ Function to get rezised image if the length of data is smaller
        -------------------
        Input parameter :
        - image : Panoramic image of scratch measure
        - X : Measure vector (mm) 
        -------------------
        return : 
        - image : image with same length as data
    """

    imLength, lenPerPix =  getImageLength(image)
    dataLength = (X[-1] - X[0])
    if(dataLength < imLength):
        return resizeImage(image, dataLength, lenPerPix)
    else:
        return image

def cropImage(image, dataLength, pixelPerMeter):
    h,w,p = np.shape(image)
    middlePix = w//2
    nbPix = dataLength*0.001*pixelPerMeter
    return image[:, middlePix-int(nbPix//2):middlePix+int(nbPix//2),:]

def resizeImage(image, dataLength, lenPerPix):
    """ Function to rezis image according to the length of data
        -------------------
        Input parameter :
        - image : Panoramic image of scratch measure
        - dataLength : total length of measure (mm) 
        - LenPerPix : length in mm of every pixel
        -------------------
        return : 
        - image : image resized with same length as data
    """
    h,w,p = np.shape(image)
    middlePix = w//2
    nbPix = dataLength/lenPerPix
    return image[:, middlePix-int(nbPix//2):middlePix+int(nbPix//2),:]

def list_files(directory, extend=".xlsx") :
    """ List all the .TXT files in a directory given in parameter
        -------------------
        Input parameter :
        - directory : The directory with the files to list
        -------------------
        return : 
        - file_path_list : The list of files
    """
    fileDir = directory + "/"         # specify your path here
    file_path_list = []
    valid_file_extensions = [extend]    # specify your valid extensions here
    valid_file_extensions = [item.lower() for item in valid_file_extensions]

    #create a list with all files in directory
    for file in os.listdir(fileDir):
        extension = os.path.splitext(file)[1]
        if extension.lower() not in valid_file_extensions:
            continue
        file_path_list.append(os.path.join(fileDir, file))
        
    return file_path_list

def listImages(directory):
    """ List all the images files in a directory given in parameter
        -------------------
        Input parameter :
        - directory : The directory with the images to list
        -------------------
        return : 
        - file_path_list : The list of images
    """

    #image path and valid extensions
    imageDir = directory + "/"         # specify your path here
    image_path_list = []
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"] #specify your vald extensions here
    valid_image_extensions = [item.lower() for item in valid_image_extensions]

    #create a list all files in directory and
    for file in os.listdir(imageDir):
        extension = os.path.splitext(file)[1]
        if extension.lower() not in valid_image_extensions:
            continue
        image_path_list.append(os.path.join(imageDir, file))
        
    return image_path_list

    """
    ### Function to compute the sampling frequency on a time vector
    
    #### Inputs:
    - t     the time vector
    
    #### Outputs:
    - Fs    the sampling frequency
    """
    return len(t) / (max(t)-min(t))