# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:23:36 2019

@author: daukes
"""

import yaml
import numpy
import matplotlib.pyplot as plt
import os
import shapely.geometry as sg
from foldable_robotics.layer import Layer
import foldable_robotics.layer
import foldable_robotics.dxf

class obj(object):
    pass
    
def objectify(var):
    if isinstance(var,dict):
        new_var = obj()
        for key,value in var.items():
            setattr(new_var,key,objectify(value))
        return new_var
    elif isinstance(var,list):
        new_var = [objectify(item) for item in var]
        return new_var
    else: 
        return var    
        
class Component(object):
    pass

class Face(object):
    pass

def create_loops(filename,prescale):
#    plt.figure()
    with open(filename) as f:
        data1 = yaml.load(f,Loader=yaml.FullLoader)
    data = objectify(data1)
    global_transform = numpy.array(data.transform)
    components = []
    for component in data.components:
        new_component = Component()
        local_transform = numpy.array(component.transform)
        T = local_transform.dot(global_transform)
        faces = []
        for face in component.faces:
            new_face = Face()
            loops = []
            for loop in face.loops:
                loop = numpy.array(loop)
                loop_a = numpy.hstack([loop,numpy.ones((len(loop),1))])
                loop_t = loop_a.dot(T)
                loop_t*=prescale
                loop_out = loop_t[:,:2].tolist()
                loops.append(loop_out)
#                plt.fill(loop_t[:,0],loop_t[:,1])
            new_face.loops = loops
            faces.append(new_face)
        new_component.faces = faces
        components.append(new_component)
    return components

def component_to_layer(component):
    faces = []
    for face in component.faces:
        loops = []
        for loop in face.loops:
            loops.append(Layer(sg.Polygon(loop)))
        if not not loops:
            face_new = loops.pop(0)            
            for item in loops:
                face_new^=item
            faces.append(face_new)
    if not not faces:
        component_new = faces.pop(0)
        for item in faces:
            component_new|=item
        return component_new
            
def get_joints(*layers,tolerance=1e-5):
    segments = []
    errors = []
    
    
    
    for ll,layer1 in enumerate(layers):
        segments_a = layer1.get_segments()
        for mm,layer2 in enumerate(layers[ll+1:]):
            segments_b = layer2.get_segments()
            for sega in segments_a:
                for segb in segments_b:
                    ni1 = foldable_robotics.geometry.slope_intercept(*sega)
                    ni2 = foldable_robotics.geometry.slope_intercept(*segb)
                    e1 = foldable_robotics.geometry.length(numpy.array(ni1[0])-numpy.array(ni2[0]))
                    e2 = foldable_robotics.geometry.length(numpy.array(ni1[0])+numpy.array(ni2[0]))
                    error = min(e1,e2)
                    
                    e3 = foldable_robotics.geometry.length(numpy.array(ni1[1])-numpy.array(ni2[1]))
                    e4 = foldable_robotics.geometry.length(numpy.array(ni1[1])+numpy.array(ni2[1]))
                    error += min(e3,e4)
            
                    errors.append(error)
                    if error<tolerance:
            
                        interiors = foldable_robotics.geometry.colinear_segment_interior_points(sega,segb,tolerance=tolerance)
                        # print(interiors)
                        
                        if not not interiors:
                            segments.append(interiors)
    return segments

def length(segment):
    segment = numpy.array(segment)
    v = segment[1]-segment[0]
    l=((v**2).sum())**.5
    return l

# def filter_segments(segments,round_digits):
#     lengths = [length(item) for item in segments]
#     segments = [item for item,l in zip(segments,lengths) if l>(10**(-round_digits))]
#     return segments

def create_layered_dxf(elements,filename):
    import ezdxf
    dwg = ezdxf.new('R2010')
    msp = dwg.modelspace()

    import foldable_robotics.dxf

    for info,items in elements:
#        items = element.pop('items')
        
        layer = dwg.layers.new(**info)
        for item in items.get_paths():
            msp.add_lwpolyline(item,dxfattribs={'layer': info['name']})
        
    dwg.saveas(filename)     

def process(input_filename,output_file_name,prescale,round_digits,body_prebuffer=-.001,joint_tolerance=1e-5):

    components = create_loops(input_filename,prescale)
    layers_orig = [component_to_layer(item) for item in components]
    
    body_layers= [item.buffer(body_prebuffer) for item in layers_orig]
    body_layer = Layer()
    body_layer = body_layer.unary_union(*body_layers)
    
    body_layer.plot(new=True)
    
    segments = foldable_robotics.solidworks_support.get_joints(*layers_orig,tolerance=joint_tolerance)
    
    linestrings = [sg.LineString(item) for item in segments]
    joints = Layer(*linestrings)
    joints.plot()
    
    elements = []
    elements.append(({'name':'body','dxfattribs':{'color': foldable_robotics.dxf.to_index[0xff0000]}},body_layer))
    elements.append(({'name':'joints','dxfattribs':{'color': foldable_robotics.dxf.to_index[0x0000ff]}},joints))
    
    foldable_robotics.solidworks_support.create_layered_dxf(elements,output_file_name)
    
    return body_layer,joints,components
       
    
if __name__=='__main__':
    user_path = os.path.abspath(os.path.expanduser('~'))
    # folder = os.path.join(user_path,'C:/Users/danaukes/projects/papers_2019_foldable_textbook/_cad/spherical_example')

    # folder=r'C:\Users\danaukes\Dropbox (Personal)\projects\2020-12-06 Knife holder'
    # filename='knife_holder - Sheet1_Drawing View1.yaml'

    # folder = r'C:\Users\danaukes\Dropbox (Personal)\projects\2019-12-27 silverware'
    # filename = 're-assembled - Sheet1_Drawing View1.yaml'

    folder = r'C:\Users\danaukes\Desktop\test1'
    filename = 'fivebar - Sheet1_Drawing View1.yaml'

    filename_simple = os.path.splitext(filename)[0]
    full_path = os.path.normpath(os.path.join(folder,filename))
    
    # output_file_name = os.path.join(user_path,'desktop','design.dxf')
    output_file_name = os.path.join(folder,filename_simple+'.dxf')
    
    
    round_digits = 2
    a,b,c = process(full_path,output_file_name,1,round_digits)

    for item in c:
        component_to_layer(item).plot(new=True)
        
    a.plot(new=True)