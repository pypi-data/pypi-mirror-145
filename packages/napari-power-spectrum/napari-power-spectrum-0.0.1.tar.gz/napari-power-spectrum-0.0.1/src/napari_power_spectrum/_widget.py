from magicgui import magic_factory
import numpy as np
from numpy.fft import ifft2, fft2, fftshift
import napari
from napari.layers import Image

@magic_factory(call_button = "Calculate Power Spectrum")
def calculate_spectrum(viewer: "napari.Viewer", image: Image,
                       entire_stack: bool = False)->Image:
    stack = image.data
    current_step = viewer.dims.current_step
    epsilon = 1e-6
    if entire_stack:
        ps = np.log((np.abs(fftshift(fft2(stack))))**2+epsilon)
        im_name = 'Spectrum ' + image.name
    else:
        im = stack[current_step[0:-2]]
        ps = np.log((np.abs(fftshift(fft2(im))))**2+epsilon)
        im_name = f'Spectrum {image.name} frame_{current_step[0]}'
        
    return Image(ps, name = im_name)