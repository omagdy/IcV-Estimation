import argparse

def input_parser():
    parser = argparse.ArgumentParser(description='Application arguments.')
    
    parser.add_argument('-px', '--pixel_spacing', action='store',
                         default=0.5, type=float, help=('Real width/height of each pixel in mm. Default: 0.5'))
    parser.add_argument('-st', '--slice_thickness', action='store',
                         default=1, type=float, help=('Thickness of each pixel in mm. Default: 1'))

    return parser
