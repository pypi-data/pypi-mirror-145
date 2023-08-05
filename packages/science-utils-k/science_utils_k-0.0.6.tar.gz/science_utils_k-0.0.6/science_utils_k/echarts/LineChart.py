from re import S
from tracemalloc import start
from science_utils_k.echarts.EChart import EChart
from science_utils_k.utils import princess
import time
import os

class LineChart(EChart):

    def __init__(self, global_args=None, options=None):
        super(LineChart, self).__init__(global_args)
        if options == None:
            self.options = {
                'title': {
                    'text': 'Classification',
                },
                'tooltip': {},
                'legend': {},
                'xAxis': {
                    'name': "epoch",
                    'nameLocation': "end",
                    'data': None,
                    'axisLabel': {
                        'show': 'true'
                    }
                },
                'yAxis': {},
                'series': None
            }
        else:
            self.options = options

    def get_options(self):
        return self.options

    def set_options(self, attrs, values):
        for attr, value in zip(attrs, values):
            # print(attr)
            # print(value)
            attr = attr.split(".")
            princess.set_attr(self.options, attr, value)

    def output(self, time_stamp,type="html", log_root_path="log"):
        
        o_path = log_root_path + "/"+time_stamp
        if type == "html":
            if not os.path.exists("log"):
                os.makedirs("log")
            if time_stamp not in os.listdir("log"):
                os.makedirs(o_path)

            if "html" not in os.listdir(o_path):
                os.makedirs(o_path+"/html")
            if "js" not in os.listdir(o_path+"/html"):
                os.makedirs(o_path+"/html/js")
            # os.makedirs(o_path+"/html/js/")

            # 如果main.html已存在，从以有文件读入html。否则使用默认html模板
            if "main.html" in os.listdir(o_path+"/html"):
                echart_html = princess.echart2html(self,log_path=o_path)
            else:
                echart_html = princess.echart2html(self)
            
            # write html file
            fd = open(o_path+"/html/main.html", "w")
            fd.write(str(echart_html))
            fd.close()

            # write js file
            fd = open(o_path+"/html/js/charts_cfg.js","a")
            fd.write(princess.js_init_echart(self))
            fd.write(princess.js_init_chartOption(self))
            fd.close()
