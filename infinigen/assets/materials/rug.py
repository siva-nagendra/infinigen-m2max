# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei
import numpy as np
from numpy.random import uniform

from infinigen.assets.materials import common
from infinigen.core.nodes import NodeWrangler, Nodes
from infinigen.core.util.color import hsv2rgba
from infinigen.core.util.random import log_uniform


def shader_rug(nw: NodeWrangler, strength=1., **kwargs):
    coord = nw.new_node(Nodes.Mapping, [nw.new_node(Nodes.TextureCoord).outputs['Object']])
    vec = nw.new_node(Nodes.MixRGB, [uniform(.8, .9), nw.new_node(Nodes.NoiseTexture, [coord]), coord])
    height = 0, 0, 0, 1
    base_scale = log_uniform(250, 500)
    for scale, thresh in zip([1, .75, .5], [1, .5, .33]):
        voronoi = nw.new_node(Nodes.VoronoiTexture, [vec], input_kwargs={'Scale': scale * base_scale}).outputs[
            0]
        height = nw.new_node(Nodes.MixRGB, [nw.math('GREATER_THAN', voronoi, thresh), voronoi, height])
    base_hue = uniform(0, 1)
    base_value = uniform(.2, .5)
    if uniform() < .2:
        base_saturation = log_uniform(.02, .05)
        front_color = hsv2rgba(base_hue, base_saturation, base_value)
        back_color = hsv2rgba(base_hue + uniform(-.01, .01), base_saturation * uniform(.9, 1.1),
                              base_value * uniform(.9, 1.1))
    else:
        base_saturation = log_uniform(.2, .4)
        front_color = hsv2rgba(base_hue, base_saturation, base_value)
        back_color = hsv2rgba(base_hue + uniform(-.01, .01), base_saturation * uniform(.9, 1.1),
                              base_value * uniform(.9, 1.1))
    color = nw.new_node(Nodes.MixRGB, [
        nw.build_float_curve(nw.musgrave(uniform(20, 50)), [(0, 1), (uniform(.3, .4), 0), (1, 0)]), front_color,
        back_color])
    roughness = nw.build_float_curve(nw.musgrave(uniform(20, 50)), [(.5, .9), (1, .8)])
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,

def apply(obj, selection=None, **kwargs):
    common.apply(obj, shader_rug, selection, **kwargs)
