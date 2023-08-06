from napari_power_spectrum import calculate_spectrum
import numpy as np
import napari
from napari.layers import Image

# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
   
def test_calculate_spectrum(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    layer = viewer.add_image(np.random.random((100, 100)))

    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = calculate_spectrum()

    # if we "call" this object, it'll execute our function
    #my_widget(viewer.layers[0])

    # read captured output and check that it's as we expected
    #captured = capsys.readouterr()
    #assert type(captured.out) == Image