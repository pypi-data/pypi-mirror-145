# -*-coding=utf-8 -*-
__author__  = "8034.com"
__date__    = "2020-05-28"

import os
import subprocess

class SYSCMD(object):

    def cmd(self, command):
        print("EXCE COMMAND:\t" + command)
        code = os.system(command)
        print("RETRUN:\t" , code)
        pass


    def os_popen(self, command):
        print("EXCE COMMAND:\t" + command)
        with os.popen(command, 'r') as f:
            text = f.read()
        print("RETRUN:\t" , text)
        return text

    def proc_call(self, command):
        print("EXCE COMMAND:\t" + command)
        code = subprocess.call(command)
        print("RETRUN:\t" , code)
        return code 

    def proc_popen(self, command):
        print("EXCE COMMAND:\t" + command)

        proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        # proc.pid    # 查看子进程ID
        # proc.stdout # 查看子进程 标准输出
        # proc.poll() # 查看子进程状态
        # proc.wait() # 等待子进程结束
        # proc.communicate(input=None)  # 向子进程发送文字输入
        # proc.send_signal(subprocess.signal.CTRL_C_EVENT) # 向子进程发送信号
        # proc.terminate()              # 停止子进程=发送SIGTERM信号
        # proc.kill()       # 杀死子进程=发送SIGKILL信号
        # proc.stdin        # 查看子进程 标准输入
        # proc.stderr       # 查看子进程 标准错误
        # proc.returncode   # 子程序的返回值

        print("RETRUN:\t" , proc.returncode)
        return proc 
    pass

sys_cmd = SYSCMD()

proc = sys_cmd.proc_popen("echo %PATH%") 
print(proc.pid)
print(proc.stdout.readlines())
print(proc.poll)

# sys_cmd.cmd("echo %PATH%")