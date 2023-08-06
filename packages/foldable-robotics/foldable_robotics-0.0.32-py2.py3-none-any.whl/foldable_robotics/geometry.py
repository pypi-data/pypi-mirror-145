# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""
import numpy
import math


def close_to(a,b,tolerance=1e-5):
    result = ((a-b)**2)**.5
    return result < tolerance

def distance(p1,p2):
    p1 = numpy.array(p1)
    p2 = numpy.array(p2)
    v = p2-p1
    return(length(v))

def length(v1):
    '''
    finds the length of a vector
    
    :param v1: the vector
    :type v1: tuple or list of floats
    :rtype: float
    '''
    v1 = numpy.array(v1).flatten()
    l = (v1.dot(v1))**.5
    return l
    
def inner_angle(v1,v2):
    '''
    finds the interior angle between two vectors
    
    :param v1: the first vector
    :type v1: tuple or list of floats
    :param v2: the second vector
    :type v2: tuple or list of floats
    :rtype: float
    '''
    v1 = numpy.array(v1).flatten()
    l1 = length(v1)
    v2 = numpy.array(v2).flatten()
    l2 = length(v2)
    cost = numpy.dot(v1,v2)/l1/l2
    t = math.acos(cost)
    return t
    
def total_angle(v1,v2,v3=None):
    '''
    finds the interior angle between two vectors
    
    :param v1: the first vector
    :type v1: tuple or list of floats
    :param v2: the second vector
    :type v2: tuple or list of floats
    :rtype: float
    '''

    v1 = numpy.array(v1).flatten()
    if len(v1)==2:
        v1 = numpy.r_[v1,0]
        v3 = numpy.array([0,0,1])

        v2 = numpy.array(v2).flatten()
    if len(v2)==2:
        v2 = numpy.r_[v2,0]
        v3 = numpy.array([0,0,1])

    costheta = numpy.dot(v1,v2)
    sintheta  = numpy.cross(v1,v2)
    l_sintheta = length(sintheta)
    neg = sintheta.dot(v3)
    if neg<0:
        neg = -1
    else:
        neg=1
    theta = math.atan2(neg*l_sintheta,costheta)
    return theta    

def heal_polylines(lines, tolerance=1e-3):
    polylines=[]
    while len(lines)>0:
        polyline = []
        polyline.append(lines.pop(0))
        finding = True
        while finding:
            finding = False
            for ii in range(len(lines)):
                item = lines[ii]
                if distance(polyline[-1][1],item[0])<tolerance:
                    polyline.append(item)
                    lines.pop(ii)
                    finding = True
                    break
                elif  distance(polyline[-1][1],item[-1])<tolerance:
                    polyline.append(item[::-1])
                    lines.pop(ii)
                    finding = True
                    break
        polyline2 = numpy.array([item[0] for item in polyline]+[polyline[-1][-1]])
        # polyline = numpy.array([item for segment in polyline for item in segment])
        polylines.append(polyline2)
        print(len(lines))
    return polylines
    

# def vec_error(v1,v2):
#     v1 = numpy.r_[v1]
#     v2 = numpy.r_[v2]
#     error = (v1-v2)**2
#     error = error.sum()
#     error = error**.5
#     return error

def slope_intercept(p1,p2):
    
    if len(p1)==2:
        p1 = numpy.r_[p1,0]
    else:
        p1 = numpy.r_[p1]
    if len(p2)==2:
        p2 = numpy.r_[p2,0]
    else:
        p2 = numpy.r_[p2]
    
    v = p2-p1
    l = (v.dot(v))**.5
    n = v/l
    p = numpy.cross(p1,n)
    i = numpy.cross(p,n)
    
    return tuple(n[:2]),tuple(i[:2])

def interior(seg,p):
    pA1,pA2 = seg
    pA1 = numpy.r_[pA1]
    pA2 = numpy.r_[pA2]
    p = numpy.r_[p]


    vA = pA2-pA1
    lA = length(vA)
    v = p-pA1
    l = length(v)

    if lA==0:
        return-1,lA

    if l==0:
        return l,lA
    
    nA = vA/lA
    n = v/l
    d = nA.dot(n)
    n *=d
    l *=d
    return l,lA

def colinear_segment_interior_points(segA,segB,tolerance=1e-5):
    '''
    
    requires that you check slope and intercept first

    Parameters
    ----------
    (pA1,pA2) : TYPE
        DESCRIPTION.
    (pB1,pB2) : TYPE
        DESCRIPTION.

    Returns
    -------
    interior : TYPE
        DESCRIPTION.

    '''
    (pA1,pA2) = segA
    (pB1,pB2) = segB

    lB1,lA = interior(segA,pB1)
    lB2,lA = interior(segA,pB2)
    
    interiors = []
    
    if lB1<tolerance or close_to(lB1,0,tolerance):
        if lB2<tolerance or close_to(lB2,0,tolerance):
            pass
        elif lB2<lA-tolerance:
            interiors = [pA1,pB2]
        else: #lB>lA
            interiors = [pA1,pA2]
      
    elif lB1<lA-tolerance:
        if lB2<tolerance or close_to(lB2,0,tolerance):
            interiors = [pA1,pB1]
        elif lB2<lA-tolerance:
            interiors = [pB1,pB2]
        else: #lB>lA
            interiors = [pB1,pA2]

    else:
        if lB2<tolerance or close_to(lB2,0,tolerance):
            interiors = [pA1,pA2]
        elif lB2<lA-tolerance:
            interiors = [pB2,pA2]
        else: #lB>lA
            pass
        
    return interiors

if __name__=='__main__':
    a = [(0,0),(1,1),(1,0),(0,0)]
    # a = numpy.array(a)
    # a = numpy.hstack((a,a[:,0:1]*0))

    
    for p1,p2 in zip(a[:-1],a[1:]):
        n,i = slope_intercept(p1,p2)
        print('n:',n,'i:',i)
    

