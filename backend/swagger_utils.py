from drf_yasg import openapi


class RequiredQueryParam:
    _type_map = {
        int: openapi.TYPE_INTEGER,
        str: openapi.TYPE_STRING,
    }

    def __init__(self, parameters: list):
        self.params = []
        for param, param_type, description in parameters:
            self.params.append(openapi.Parameter(param,
                                                 in_=openapi.IN_QUERY,
                                                 description=description,
                                                 type=self._type_map[param_type]))

    def params(self):
        return self.params
