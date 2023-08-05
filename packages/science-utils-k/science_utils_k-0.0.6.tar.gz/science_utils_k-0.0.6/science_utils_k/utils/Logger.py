import os
import time
from turtle import fd


class Logger(object):
    #time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) # 创建时间
    @staticmethod
    def log2terminal(*s, tofile=False,log_root_path="log",time_stamp=None):
        str_content=""
        for x in s:
            str_content += str(x) 
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        print(current_time,":",str_content)
        if tofile:
            Logger.log2file(s,time_stamp=time_stamp,log_root_path=log_root_path)
    
    @staticmethod
    def log2file(*s,time_stamp, log_root_path="log"):
        str_content=""

        # 拼接内容
        for x in s:
            str_content += str(x)

        if not os.path.exists("log"):
            os.mkdir("log")
        if time_stamp not in os.listdir("log"):
            os.makedirs(log_root_path+"/"+time_stamp)

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        log_content = current_time+": "+str_content+"\n"

        # write
        fd = open(log_root_path+"/"+time_stamp+"/log.txt", "a")
        fd.write(log_content)
        fd.close()

    @staticmethod
    def save_hyperparameter(hyperparameter, filepath='log/hyperparameter.txt'):
        fd = open(filepath, "w")

        # write
        for key in hyperparameter.keys(): 
            parameter = "%s : %s\n" %(key, str(hyperparameter[key]))
            fd.write(parameter)
        fd.close()


