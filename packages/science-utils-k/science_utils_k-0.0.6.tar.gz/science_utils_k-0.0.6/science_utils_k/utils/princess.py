# 公主（举）包
from bs4 import BeautifulSoup


def set_attr(options: dict, attr: list, value: any) -> str:
    i = 0
    for x in attr:
        if i == 0:
            exec_str = "options['%s']" % x
            i += 1
        else:
            exec_str += "['%s']" % x

    exec_str += " = %s" % value
    print(exec_str)
    exec(exec_str)
    # print(options)
    return exec_str


def load_html(file_path=None):
    html_temp = '<!DOCTYPE html>\
<html>\
\
<head>\
    <meta charset="utf-8" />\
    <meta http-equiv="X-UA-Compatible" content="IE=edge">\
    <meta name="viewport" content="width=device-width, initial-scale=1">\
    <title></title>\
\
    <!-- ZUI Javascript 依赖 jQuery -->\
    <script src="https://cdn.staticfile.org/echarts/4.3.0/echarts.min.js"></script>\
</head>\
\
<body>\
    <div class="container"></div>\
</body>\
<script src="js/charts_cfg.js"></script>\
\
</html>'
    if file_path == None:
        return BeautifulSoup(html_temp, features="lxml")
    else:
        return BeautifulSoup(open(file_path),features="lxml")

def load_data(data) -> str:
    return str(data)


def load_data_from_file(path: str, args_name: list, split=","):
    pass


def js_init_echart(chart):
    global_args = chart.get_global_args()
    options = chart.get_options()
    i = 0
    for arg in global_args["init"]:
        if i == 0:
            init_js = "var %s = echarts.init(\n\
                %s=%s,   \n \
            " % (
                global_args["id"],
                arg,
                global_args["init"][arg] ,
            )
            i = 1
        else:

            init_js += "%s = %s,\n" % (
                arg,
                global_args["init"][arg]if global_args["init"][arg] != None else "null",
            )
    init_js += ");\n"
    print(init_js)
    return init_js


def js_init_chartOption(chart):
    global_args = chart.get_global_args()
    options = chart.get_options()
    options_js = "%s.setOption(%s)" % (
        global_args["id"],
        options
    )
    options_js +=";\n"
    return options_js


def echart2html(chart,log_path=None):
    # echart_container = '&lt;div id="%s" style="float: left;"></div>' % chart.get_global_args()["id"]
    if log_path == None:
        soup = load_html()
    else:
        soup = load_html(file_path=log_path+"/html/main.html")
    echart_container = soup.new_tag("div", id=chart.get_global_args()["id"],style="float: left;")
    soup.div.append(echart_container)
    return soup.prettify()

# soup = load_html().prettify
# print(soup)
