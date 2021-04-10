from random import randint

from IChaosGame import Shape


# TEMPLATE FOR MAKING A NEW RULE
# def sample_rule(shape: Shape = None,
#                              last_point: tuple = None,
#                              last_vertex: int = None,
#                              getinfo=False):
#     if getinfo == 'name':
#         return "name of the rule"
#     if getinfo == 'description':
#         return 'description of the rule'
#
#     # Randomly choose a vertex
#     chosen_vertex = randint(0, shape.number_of_points - 1)
#
#     # Chosen vertex x & y coordinates
#     shape_x_cords_list, shape_y_cords_list = shape.get_point_cords()
#     cv_x = shape_x_cords_list[chosen_vertex]
#     cv_y = shape_y_cords_list[chosen_vertex]
#
#     # Last point x & y coordinates
#     lp_x = last_point[0]
#     lp_y = last_point[1]
#
#     # Do something to get new point
#     new_x = (cv_x + lp_x) / 2
#     new_y = (cv_y + lp_y) / 2
#     new_point = (new_x, new_y)
#
#     return new_point, chosen_vertex


def classic_chaos_game_rules(shape: Shape = None,
                             last_point: tuple = None,
                             last_vertex: int = None,
                             getinfo=False):
    if getinfo == 'name':
        return "Classic"
    if getinfo == 'description':
        return 'From a point, pick a random vertex and move towards it halfway, ' \
               'this will become the new point, and then repeat'

    # Randomly choose a vertex
    chosen_vertex = randint(0, shape.number_of_points - 1)

    # Chosen vertex x & y coordinates
    shape_x_cords_list, shape_y_cords_list = shape.get_point_cords()
    cv_x = shape_x_cords_list[chosen_vertex]
    cv_y = shape_y_cords_list[chosen_vertex]

    # Last point x & y coordinates
    lp_x = last_point[0]
    lp_y = last_point[1]

    new_x = (cv_x + lp_x) / 2
    new_y = (cv_y + lp_y) / 2
    new_point = (new_x, new_y)

    return new_point, chosen_vertex


def no_same_vertex_rules(shape: Shape = None,
                         last_point: tuple = None,
                         last_vertex: int = None,
                         getinfo=False):
    if getinfo == 'name':
        return "No Same Vertex"
    elif getinfo == 'description':
        return "Like Classical but can't choose the same vertex twice"

    # Randomly choose a vertex
    chosen_vertex = last_vertex
    while chosen_vertex == last_vertex:
        chosen_vertex = randint(0, shape.number_of_points - 1)

    # Chosen vertex x & y coordinates
    shape_x_cords_list, shape_y_cords_list = shape.get_point_cords()
    cv_x = shape_x_cords_list[chosen_vertex]
    cv_y = shape_y_cords_list[chosen_vertex]

    # Last point x & y coordinates
    lp_x = last_point[0]
    lp_y = last_point[1]

    new_x = (cv_x + lp_x) / 2
    new_y = (cv_y + lp_y) / 2
    new_point = (new_x, new_y)

    return new_point, chosen_vertex


def no_clockwise_rule(shape: Shape = None,
                      last_point: tuple = None,
                      last_vertex: int = None,
                      getinfo=False):
    if getinfo == 'name':
        return "No Clockwise"
    if getinfo == 'description':
        return 'Like Classical but the chosen vertex cannot be one place away (clockwise) ' \
               'from the previously chosen vertex'

    # Randomly choose a vertex
    while True:
        chosen_vertex = randint(0, shape.number_of_points - 1)
        if last_vertex is None or not chosen_vertex == (last_vertex + 1) % shape.number_of_points:
            break

    # Chosen vertex x & y coordinates
    shape_x_cords_list, shape_y_cords_list = shape.get_point_cords()
    cv_x = shape_x_cords_list[chosen_vertex]
    cv_y = shape_y_cords_list[chosen_vertex]

    # Last point x & y coordinates
    lp_x = last_point[0]
    lp_y = last_point[1]

    # Do something to get new point
    new_x = (cv_x + lp_x) / 2
    new_y = (cv_y + lp_y) / 2
    new_point = (new_x, new_y)

    return new_point, chosen_vertex


def no_counter_clockwise_rule(shape: Shape = None,
                      last_point: tuple = None,
                      last_vertex: int = None,
                      getinfo=False):
    if getinfo == 'name':
        return "No Counter Clockwise"
    if getinfo == 'description':
        return 'Like Classical but the chosen vertex cannot be one place away (counter-clockwise) ' \
               'from the previously chosen vertex'

    # Randomly choose a vertex
    while True:
        chosen_vertex = randint(0, shape.number_of_points - 1)
        if last_vertex is None or not chosen_vertex == (last_vertex - 1) % shape.number_of_points:
            break

    # Chosen vertex x & y coordinates
    shape_x_cords_list, shape_y_cords_list = shape.get_point_cords()
    cv_x = shape_x_cords_list[chosen_vertex]
    cv_y = shape_y_cords_list[chosen_vertex]

    # Last point x & y coordinates
    lp_x = last_point[0]
    lp_y = last_point[1]

    # Do something to get new point
    new_x = (cv_x + lp_x) / 2
    new_y = (cv_y + lp_y) / 2
    new_point = (new_x, new_y)

    return new_point, chosen_vertex


def no_opposite(shape: Shape = None,
                last_point: tuple = None,
                last_vertex: int = None,
                getinfo=False):
    if getinfo == 'name':
        return "No Opposite"
    if getinfo == 'description':
        return 'Like Classical but the chosen vertex cannot be the opposite ' \
               'from the previously chosen vertex'

    # Randomly choose a vertex
    while True:
        chosen_vertex = randint(0, shape.number_of_points - 1)
        if last_vertex is None or not chosen_vertex == (last_vertex + shape.number_of_points//2) % shape.number_of_points:
            break

    # Chosen vertex x & y coordinates
    shape_x_cords_list, shape_y_cords_list = shape.get_point_cords()
    cv_x = shape_x_cords_list[chosen_vertex]
    cv_y = shape_y_cords_list[chosen_vertex]

    # Last point x & y coordinates
    lp_x = last_point[0]
    lp_y = last_point[1]

    # Do something to get new point
    new_x = (cv_x + lp_x) / 2
    new_y = (cv_y + lp_y) / 2
    new_point = (new_x, new_y)

    return new_point, chosen_vertex


def no_neighbor_if_chosen_twice(shape: Shape = None,
                                last_point: tuple = None,
                                last_vertex: int = None,
                                getinfo=False):
    if getinfo == 'name':
        return "No Neighbor"
    if getinfo == 'description':
        return 'Like Classical but the chosen vertex cannot neighbor the previously ' \
               'chosen vertex if the two previously chosen vertices are the same'

    # Randomly choose a vertex
    if isinstance(last_vertex, list):
        while True:
            chosen_vertex = randint(0, shape.number_of_points - 1)
            if not (chosen_vertex == (last_vertex[0] + 1) % shape.number_of_points or
                    chosen_vertex == (last_vertex[0] - 1) % shape.number_of_points):
                break
    else:
        chosen_vertex = randint(0, shape.number_of_points - 1)

    # Chosen vertex x & y coordinates
    shape_x_cords_list, shape_y_cords_list = shape.get_point_cords()
    cv_x = shape_x_cords_list[chosen_vertex]
    cv_y = shape_y_cords_list[chosen_vertex]

    # Last point x & y coordinates
    lp_x = last_point[0]
    lp_y = last_point[1]

    # Do something to get new point
    new_x = (cv_x + lp_x) / 2
    new_y = (cv_y + lp_y) / 2
    new_point = (new_x, new_y)

    if chosen_vertex == last_vertex or (isinstance(last_vertex, list) and last_vertex[0] == chosen_vertex):
        chosen_vertex = [chosen_vertex]

    return new_point, chosen_vertex
