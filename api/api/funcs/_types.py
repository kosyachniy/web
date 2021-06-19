"""
Types checking functionality for the API
"""

from ..errors import ErrorSpecified, ErrorInvalid, ErrorType


def check_params(data, filters):
    """ Checking parameters """

    # TODO: Удалять другие поля (которых нет в списке)

    for i in filters:
        if i[0] in data:
            # Invalid data type
            if not isinstance(i[2], (list, tuple)):
                el_type = (i[2],)
            else:
                el_type = i[2]

            cond_type = not isinstance(data[i[0]], el_type)
            cond_iter = isinstance(data[i[0]], (tuple, list))

            try:
                cond_iter_el = cond_iter \
                    and any(not isinstance(j, i[3]) for j in data[i[0]])
            except:
                raise ErrorType(i[0])

            if cond_type or cond_iter_el:
                raise ErrorType(i[0])

            cond_null = isinstance(i[-1], bool) and i[-1] and cond_iter \
                and not data[i[0]]

            if cond_null:
                raise ErrorInvalid(i[0])

        # Not all fields are filled
        elif i[1]:
            raise ErrorSpecified(i[0])

        # Default
        else:
            data[i[0]] = None

    return data
