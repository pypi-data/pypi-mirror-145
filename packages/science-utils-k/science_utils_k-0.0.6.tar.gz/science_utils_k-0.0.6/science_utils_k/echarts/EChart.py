
from abc import abstractclassmethod, abstractmethod
from science_utils_k.utils import princess


class EChart(object):
    def __init__(self, global_args=None, options=None):
        if global_args == None:
            self.global_args = {
                "id": "chart",
                "init": {
                    "dom": "document.getElementById('chart')",
                    "theme": None,
                    'options': {
                        "width": 600,
                        "height": 500
                    }

                }
            }
        else:
            self.global_args = global_args
    def get_global_args(self):
        return self.global_args

    def set_global_args(self, attrs, values):
        for attr, value in zip(attrs, values):
            # print(attr)
            # print(value)
            attr = attr.split(".")
            princess.set_attr(self.global_args, attr, value)
    def output(type):
        pass
