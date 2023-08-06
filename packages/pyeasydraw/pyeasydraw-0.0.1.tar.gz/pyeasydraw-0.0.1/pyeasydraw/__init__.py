"""
最好用IDLE进行测试（可以输出红色），
只要指定内容、长（width）、宽（height），就可已输出了。

版权
名字：郭若垚
邮箱：yao1127@aliyun.com
****************************
测试：
>>> import pyeasydraw
>>> a = pyeasydraw.Art()
>>> a.run()
**********
**********
**********
**********
**********
**********
**********
**********
**********
**********
"""
import random # 随机
import sys # 用红色输出
import ctypes # 设置cmd颜色

__version__ = "0.0.2"
__all__ = ["Art","new_line"]
class Art:
        def __init__(self, height=10, width=10, string: (str, tuple) = "*", end: str = " ", stochastic=False, red=False, stochastic_color=False,raw_color=False,cmd_color=7,autoresetcmdcolor=True):
                self.HANDLE = ctypes.windll.kernel32.GetStdHandle(-11) #输出Handle
                self.height = height # 高度
                self.width = width # 宽度
                self.string = string # 输出内容
                self.end = end # 末尾
                self.stochastic = stochastic # 是否随机
                self.red = red #是否是红色
                self.stochastic_color = stochastic_color # 是否随机颜色
                self.raw_color = raw_color # 有规律的颜色
                self.cmd_color = cmd_color # 控制台的颜色
                self.autoresetcmdcolor = autoresetcmdcolor # 设置自动重置颜色
                self.data = {
			"Height": height, 
			"Width": width,
                        "String": string, 
			"End": end, 
			"Stochastic": stochastic, 
			"Red": red,
                        "Stochastic_color": stochastic_color,
                        "Raw_color":raw_color,
                        "Cmd_color":cmd_color,
                        "Autoresetcmdcolor":autoresetcmdcolor
                             } # 用来存放数据

        def run(self,use_cmd_color=False):
                """
进行输出程序
                """
                for a in range(self.height): # 从高度开始
                        for x in range(self.width): # 再从宽开始
                                if self.stochastic:  # 如果是随机
                                        g = random.choice(self.string) # 随机抽选
                                elif type(self.string) == tuple:
                                        g = self.string[x % len(self.string)] # 按顺序输出
                                else:
                                        g = self.string # 就选这个
                                if use_cmd_color:
                                        ctypes.windll.kernel32.SetConsoleTextAttribute(self.HANDLE,self.cmd_color) # 设置颜色
                                        print(g, end=str(self.end)) # 输出
                                elif self.stochastic_color:  # 如果是随机颜色
                                        w = random.choice([0,1]) # 随机选颜色
                                        if w == True: # 如果是红色
                                                sys.stderr.write(str(g)+str(self.end)) # 用错误（红色）输出
                                        else:
                                                print(str(g), end=str(self.end)) # 用print（蓝色）输出
                                                                
                                elif self.red: # 如果是红色
                                        sys.stderr.write(str(g)+str(self.end)) # 用错误（红色）输出
                                elif self.raw_color:
                                        if x % 2 == 0:
                                                print(str(g), end=str(self.end)) # 用print（蓝色）输出
                                        else:
                                                sys.stderr.write(str(g)+str(self.end)) # 用错误（红色）输出
                                else:
                                        # 用print（蓝色）输出
                                        print(str(g), end=str(self.end))

                        print("") #换一行
                if self.autoresetcmdcolor:
                        self.reset_cmd_color() # 重置颜色
        def set_data(self):
                """
把参数设置为data中的参数
                """
                #用data设定参数
                self.height = self.data["Height"]
                self.width = self.data["Width"]
                self.string = self.data["String"]
                self.end = self.data["End"]
                self.stochastic = self.data["Stochastic"]
                self.red = self.data["Red"]
                self.stochastic_color = self.data["Stochastic_color"]
                self.raw_color = self.data["Raw_color"]
                self.cmd_color = self.data["Cmd_color"]

        def reset_data(self):
                """
把data设置为参数中的参数
                """
                #把参数改为data
                self.data["Height"] = self.height
                self.data["Width"] = self.width
                self.data["String"] = self.string
                self.data["End"] = self.end
                self.data["Stochastic"] = self.stochastic
                self.data["Red"] = self.red
                self.data["Stochastic_color"] = self.stochastic_color
                self.data["Raw_color"] = self.raw_color
                self.data["Cmd_color"] = self.cmd_color
        def show_cmd_color(self):
                """
测试输出颜色
                """
                print("Color Unicode Is "+str(self.cmd_color)) # 输出数值
                ctypes.windll.kernel32.SetConsoleTextAttribute(self.HANDLE,self.cmd_color) # 设置颜色
                print("OK") # 输出测试
                if self.autoresetcmdcolor:
                        self.reset_cmd_color() # 重置
        def reset_cmd_color(self):
                """
重置颜色
                """
                ctypes.windll.kernel32.SetConsoleTextAttribute(self.HANDLE,7) # 先设置为白色
                print(end="") # 输出（空格）
def new_line(string="*",width=20, red=False, space=True,cmd_color=7):
    """
换一行执行新的程序
    """    
    a = Art(red=red) # 一个art
    if space:
        a.end = " "
    else:
        a.end = ""
    a.string = string # 设置字
    a.width = width # 设置宽
    a.height = 1 # 设置高
    a.cmd_color = cmd_color # 设置cmd颜色
    a.run(True) # 运行
def main():
    r = Art(10,10)
    r.run()
    #new_line()				
if __name__ == "__main__":
	main()
