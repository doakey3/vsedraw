from .distance_formula import distance_formula


def get_curve_length(curve):
    """
    Get the total length of a curve
    """
    lengths = []
    points = curve.data.splines.active.points

    for i in range(len(points) - 1):
        p1 = [points[i].co.x, points[i].co.y]
        p2 = [points[i + 1].co.x, points[i + 1].co.y]
        length = distance_formula(p1, p2)
        lengths.append(length)

    return sum(lengths)
