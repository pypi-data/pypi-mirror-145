import cv2
import numpy as np

import dito.core


# often-used constants
sqrt_05 = np.sqrt(0.5)


def draw_circle(image, center, radius, color, thickness, line_type, start_angle=None, end_angle=None):
    """
    TODO: fix round corners when using start_angle/end_angle and thickness != cv2.FILLED
    """
    if (start_angle is None) and (end_angle is None):
        cv2.circle(img=image, center=dito.core.tir(center), radius=radius, color=color, thickness=thickness, lineType=line_type)
    else:
        if start_angle is None:
            start_angle = 0.0
        if end_angle is None:
            end_angle = 360.0
        cv2.ellipse(img=image, center=dito.core.tir(center), axes=(radius, radius), angle=0.0, startAngle=start_angle, endAngle=end_angle, color=color, thickness=thickness, lineType=line_type)


def draw_ring(image, center, radius1, radius2, color, thickness, line_type, start_angle=None, end_angle=None):
    if thickness == cv2.FILLED:
        # draw circle outline with thickness equal to the radius difference
        circle_radius = (radius1 + radius2) // 2
        circle_thickness = abs(radius1 - radius2)
        draw_circle(image=image, center=center, radius=circle_radius, color=color, thickness=circle_thickness, line_type=line_type, start_angle=start_angle, end_angle=end_angle)
    else:
        # draw two circles
        draw_circle(image=image, center=center, radius=radius1, color=color, thickness=thickness, line_type=line_type, start_angle=start_angle, end_angle=end_angle)
        draw_circle(image=image, center=center, radius=radius2, color=color, thickness=thickness, line_type=line_type, start_angle=start_angle, end_angle=end_angle)


def draw_polygon(image, points, color, thickness, line_type):
    points_int = np.round(np.array(points)).astype(np.int32)
    if thickness == cv2.FILLED:
        cv2.fillPoly(img=image, pts=[points_int], color=color, lineType=line_type)
    else:
        cv2.polylines(img=image, pts=[points_int], isClosed=True, color=color, thickness=thickness, lineType=line_type)


def draw_regular_polygon(image, point_count, position, radius, color, thickness, line_type, angle_offset=0.0):
    (x, y) = position
    points = []
    for angle in np.linspace(start=0.0, stop=2.0 * np.pi, num=point_count, endpoint=False):
        points.append([
            radius * np.cos(angle + angle_offset) + x,
            radius * np.sin(angle + angle_offset) + y,
        ])
    draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)


def draw_regular_star(image, point_count, position, radius_outer, radius_inner, color, thickness, line_type, angle_offset=0.0):
    (x, y) = position
    points = []
    for (n_point, angle) in enumerate(np.linspace(start=0.0, stop=2.0 * np.pi, num=2 * point_count, endpoint=False)):
        radius = radius_outer if (n_point % 2) == 0 else radius_inner
        points.append([
            radius * np.cos(angle + angle_offset) + x,
            radius * np.sin(angle + angle_offset) + y,
        ])
    draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)


def draw_regular_skeleton(image, point_count, position, radius, color, thickness, line_type, angle_offset=0.0):
    thickness = 1 if thickness == cv2.FILLED else thickness
    (x, y) = position
    for angle in np.linspace(start=0.0, stop=2.0 * np.pi, num=point_count, endpoint=False):
        cv2.line(img=image, pt1=dito.core.tir(x, y), pt2=dito.core.tir(radius * np.cos(angle + angle_offset) + x, radius * np.sin(angle + angle_offset) + y), color=color, thickness=thickness, lineType=line_type)


def draw_symbol(image, symbol, position, radius=4, color=None, thickness=1, line_type=cv2.LINE_AA):
    # handle arguments
    (x, y) = position
    if color is None:
        if dito.core.is_color(image=image):
            color = (0, 255, 0)
        else:
            color = (255,)

    if symbol in ("circle", "o"):
        cv2.circle(img=image, center=dito.core.tir(x, y), radius=radius, color=color, thickness=thickness, lineType=line_type)

    elif symbol in ("cross", "x"):
        thickness = 1 if thickness == cv2.FILLED else thickness
        sqrt_one_over_radius = sqrt_05 * radius
        cv2.line(img=image, pt1=dito.core.tir(x - sqrt_one_over_radius, y - sqrt_one_over_radius), pt2=dito.core.tir(x + sqrt_one_over_radius, y + sqrt_one_over_radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=dito.core.tir(x + sqrt_one_over_radius, y - sqrt_one_over_radius), pt2=dito.core.tir(x - sqrt_one_over_radius, y + sqrt_one_over_radius), color=color, thickness=thickness, lineType=line_type)

    elif symbol in ("diamond", "D"):
        points = [
            (x, y - radius),
            (x + radius, y),
            (x, y + radius),
            (x - radius, y),
        ]
        draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)

    elif symbol in ("diamond_thin", "d"):
        points = [
            (x, y - radius),
            (x + 0.67 * radius, y),
            (x, y + radius),
            (x - 0.67 * radius, y),
        ]
        draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)

    elif symbol in ("hexagon", "6"):
        draw_regular_polygon(image=image, point_count=6, position=position, radius=radius, color=color, thickness=thickness, line_type=line_type, angle_offset=1.5 * np.pi)

    elif symbol in ("pentagon", "5"):
        draw_regular_polygon(image=image, point_count=5, position=position, radius=radius, color=color, thickness=thickness, line_type=line_type, angle_offset=1.5 * np.pi)

    elif symbol in ("plus", "+"):
        thickness = 1 if thickness == cv2.FILLED else thickness
        cv2.line(img=image, pt1=dito.core.tir(x - radius, y), pt2=dito.core.tir(x + radius, y), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=dito.core.tir(x, y - radius), pt2=dito.core.tir(x, y + radius), color=color, thickness=thickness, lineType=line_type)

    elif symbol in ("skeleton_5",):
        draw_regular_skeleton(image=image, point_count=5, position=position, radius=radius, color=color, thickness=thickness, line_type=line_type, angle_offset=1.5 * np.pi)

    elif symbol in ("skeleton_6",):
        draw_regular_skeleton(image=image, point_count=6, position=position, radius=radius, color=color, thickness=thickness, line_type=line_type, angle_offset=0.5 * np.pi)

    elif symbol in ("square", "4"):
        cv2.rectangle(img=image, pt1=dito.core.tir(x - radius, y - radius), pt2=dito.core.tir(x + radius, y + radius), color=color, thickness=thickness, lineType=line_type)

    elif symbol in ("star_4",):
        draw_regular_star(image=image, point_count=4, position=position, radius_outer=radius, radius_inner=0.5 * radius, color=color, thickness=thickness, line_type=line_type, angle_offset=1.5 * np.pi)

    elif symbol in ("star_5", "*"):
        draw_regular_star(image=image, point_count=5, position=position, radius_outer=radius, radius_inner=0.5 * radius, color=color, thickness=thickness, line_type=line_type, angle_offset=1.5 * np.pi)

    elif symbol in ("star_6",):
        draw_regular_star(image=image, point_count=6, position=position, radius_outer=radius, radius_inner=0.5 * radius, color=color, thickness=thickness, line_type=line_type, angle_offset=0.5 * np.pi)

    elif symbol in ("star_12",):
        draw_regular_star(image=image, point_count=12, position=position, radius_outer=radius, radius_inner=0.5 * radius, color=color, thickness=thickness, line_type=line_type, angle_offset=0.5 * np.pi)

    elif symbol in ("triangle_up", "^"):
        points = [
            (x, y - radius),
            (x + radius, y + sqrt_05 * radius),
            (x - radius, y + sqrt_05 * radius),
        ]
        draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)

    elif symbol in ("triangle_down", "v"):
        points = [
            (x + radius, y - sqrt_05 * radius),
            (x - radius, y - sqrt_05 * radius),
            (x, y + radius),
        ]
        draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)

    elif symbol in ("triangle_left", "<"):
        points = [
            (x + sqrt_05 * radius, y - radius),
            (x - radius, y),
            (x + sqrt_05 * radius, y + radius),
        ]
        draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)

    elif symbol in ("triangle_right", ">"):
        points = [
            (x - sqrt_05 * radius, y - radius),
            (x + radius, y),
            (x - sqrt_05 * radius, y + radius),
        ]
        draw_polygon(image=image, points=points, color=color, thickness=thickness, line_type=line_type)

    elif symbol in ("y_up",):
        thickness = 1 if thickness == cv2.FILLED else thickness
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x, y - radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x + sqrt_05 * radius, y + sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x - sqrt_05 * radius, y + sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)

    elif symbol in ("y_down", "Y"):
        thickness = 1 if thickness == cv2.FILLED else thickness
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x + sqrt_05 * radius, y - sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x - sqrt_05 * radius, y - sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x, y + radius), color=color, thickness=thickness, lineType=line_type)

    elif symbol in ("y_left",):
        thickness = 1 if thickness == cv2.FILLED else thickness
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x - radius, y), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x + sqrt_05 * radius, y - sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x + sqrt_05 * radius, y + sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)

    elif symbol in ("y_right",):
        thickness = 1 if thickness == cv2.FILLED else thickness
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x - sqrt_05 * radius, y - sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x - sqrt_05 * radius, y + sqrt_05 * radius), color=color, thickness=thickness, lineType=line_type)
        cv2.line(img=image, pt1=(x, y), pt2=dito.core.tir(x + radius, y), color=color, thickness=thickness, lineType=line_type)

    else:
        raise ValueError("Unknown symbol '{}'".format(symbol))
