#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visualize seeds where streamlines originate from
in a tractogram
"""

import argparse

from fury import window, actor
from nibabel.streamlines import detect_format, TrkFile

from scilpy.io.utils import (
    add_overwrite_arg,
    assert_inputs_exist,
    assert_outputs_exists)


def _build_args_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tractogram', help='Tractogram file')
    parser.add_argument('--dest', type=str, help='If set, save a ' +
                        'screenshot of the result at the ' +
                        'specified path')
    add_overwrite_arg(parser)
    return parser


def main():
    parser = _build_args_parser()
    args = parser.parse_args()
    assert_inputs_exist(parser, [args.tractogram])
    assert_outputs_exists(parser, args, [], [args.dest])

    tracts_format = detect_format(args.tractogram)
    if tracts_format is not TrkFile:
        raise ValueError("Invalid input streamline file format " +
                         "(must be trk): {0}".format(args.tractogram_filename))

    # Load files and data
    trk = TrkFile.load(args.tractogram)
    tractogram = trk.tractogram
    streamlines = tractogram.streamlines
    if 'seeds' not in tractogram.data_per_streamline:
        parser.error('Tractogram does not contain seeds')
    seeds = tractogram.data_per_streamline['seeds']

    # Make display objects
    streamlines_actor = actor.line(streamlines)
    points = actor.dots(seeds, color=(1., 1., 1.))

    # Add display objects to canvas
    r = window.Renderer()
    r.add(streamlines_actor)
    r.add(points)

    # Show and record if needed
    if args.dest is not None:
        window.record(r, out_path=args.dest, size=(1000, 1000))
    window.show(r)


if __name__ == '__main__':
    main()
