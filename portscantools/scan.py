#!/usr/bin/env python
#-*-coding:utf-*-

import threading
import time
import socket
import getopt,sys
import commands

###########这里放全局变量

opts = None #用来接受长短参数
argv = None #用来接受IP地址
    
one_ip = "127.0.0.1" #接受单一IP扫描,默认扫描本机子IP
more_ip = [] #要扫描的IP段，如果多个IP，放到列表中

Tcp_flags = False #为真就是用三次握手方式扫描
Syn_flags = False #为真就是用SYN半开扫描法
Fin_flags = False #为真就是用FIN扫描方法

Port_here = [] #用户指定扫描的端口在这里    
Port_list = [20,21,22,23,25,80,3389,113,443,544,445,1723]
All_Port_flags = False

#########这里是功能类

#用TCP三次握手方法扫描
class Connect_Scan(threading.Thread): #The timer class is derived from the class threading.Thread
    """
    扫描一个IP用一个线程,传入的参数值是IP，和开始端口和结束端口
    """
    def __init__(self,ipaddr="127.0.0.1",port_start=20,port_stop=9000):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.ipaddr =  ipaddr
        self.port_start = port_start
        self.port_stop = port_stop
        #如果用户指定端口 那么就用指定扫描，如果不指定，就用默认
        if not Port_here == []:
            self.port_list = Port_here
        else: 
            self.port_list = Port_list
 
    def run(self): #Overwrite run() method, put what you want the thread do here
        #这个范围内的IP
        self.one_scan(self.ipaddr)
 
    def ip_hanld(self):
        x = self.ipaddr_start.split(".")
        y = self.ipaddr_stop.split(".")
        num =int(y[3]) - int(x[3])
        return  num
   

    def stop(self):
        self.thread_stop = True

    def one_scan(self,the_ip):
        #只扫描一个IP
        #是扫描一个范围段还是扫描list里面的端口
        if All_Port_flags == True:
            way = range(1,10001)
        else:
            way = self.port_list
        for port in way:
            yy = socket.socket()
            yy.settimeout(10)
            try:
                yy.connect(( the_ip,int(port) ))
                print "%s:%s" % (the_ip,port)
                yy.close()
            except Exception:
                yy.close()
#用SYN方法来扫描
class Syn_Scan(threading.Thread):
    def __init__(self,one_ip):
        threading.Thread.__init__(self)
        self.port_list = Port_list
        self.one_ip = one_ip
 
    def run(self):
        self.scan(one_ip,self.port_list)
    def scan(self,ip,port):
        #result_tuple是（状态码，输出字符串)
        #没有指定扫描端口的情况
        if Port_here == []:
            result_tuple = commands.getstatusoutput("sudo nmap -sS " + one_ip)
        else:
            #把端口["21","22"]变成字符串 "21,22"
            port = ",".join(Port_here)
            result_tuple = commands.getstatusoutput("sudo nmap -sS -p"+ port + "  "+ one_ip)
        #把输出字符从提取出来
        result_str = result_tuple[1]
        #分割到list
        result_list = result_str.split("\n")
        #如果resule_tuple为0，说明正确执行
        if result_tuple[0] == 0 and Port_here == []:
            for hang in result_list[6:-1]:
                #输出端口显示哪一行
                if not hang =="":
                    if "open" in hang:
                        #输出格式为127.0.0.1:20
                        print one_ip +":"+ hang.split("/")[0]
        else:
            for hang in result_list[5:-1]:
                if not hang == "":
                    #到这里已经输出了结果，接下来处理结构
                    if "open" in hang:
                        print one_ip + ":" + hang.split("/")[0]
                         
        


#用Fin方法扫描
class Fin_Scan(threading.Thread):
    def __init__(self,one_ip):
        threading.Thread.__init__(self)
        self.port_list = Port_list
        self.one_ip = one_ip
 
    def run(self):
        self.scan(one_ip,self.port_list)
    def scan(self,ip,port):
        #result_tuple是（状态码，输出字符串)
        #没有指定扫描端口的情况
        if Port_here == []:
            result_tuple = commands.getstatusoutput("sudo nmap -sF " + one_ip)
        else:
            #把端口["21","22"]变成字符串 "21,22"
            port = ",".join(Port_here)
            result_tuple = commands.getstatusoutput("sudo nmap -sF -p"+ port + "  "+ one_ip)
        #把输出字符从提取出来
        result_str = result_tuple[1]
        #分割到list
        result_list = result_str.split("\n")
        #如果resule_tuple为0，说明正确执行
        if result_tuple[0] == 0 and Port_here == []:
            for hang in result_list[6:-1]:
                #输出端口显示哪一行
                if not hang =="":
                    if "open" in hang:
                        #输出格式为127.0.0.1:20
                        print one_ip +":"+ hang.split("/")[0]
        else:
            for hang in result_list[5:-1]:
                if not hang == "":
                    #到这里已经输出了结果，接下来处理结构
                    if "open" in hang:
                        print one_ip + ":" + hang.split("/")[0]
         
def test():

    """
    这里处理使用哪一种方法来扫描
    """
    global one_ip
    online = None
    online_flags = None
    if not one_ip == None: 
        #判断IP是否在线
        online = commands.getstatusoutput("ping -c1 "+ one_ip + "")
        #oneline_flags 如果ping通这个值是0
        online_flags = online[0]
    #根据标志位来判断用哪种方法扫描
    #第一种，使用connect来扫描
    if Tcp_flags == True:
        if online_flags == 0:
            print  "使用TCP三次握手方法扫描IP:",one_ip
            t = Connect_Scan(one_ip,20,8000)
            t.start()
        else:
            print "主机不在线 无法扫描!"
    #第二种，用SYN方法来扫描
    if Syn_flags == True:
        if online_flags == 0:
            print "使用SYN半扫描法扫描IP:",one_ip
            t = Syn_Scan(one_ip)
            t.start()
    if Fin_flags == True:
        if online_flags == 0:
            print "使用FIN方法扫描IP:",one_ip
            t = Fin_Scan(one_ip)
            t.start()

 
def use_help():
    print "------------------------欢迎使用Simple PortScaner------------------- "
    print "基本格式: scan.py [option]..[-T | -S | -F | -p port | -h |]  ip"
    print "例如:     scan.py -T -p 21,22,23,80,3389 172.18.15.254"
    print "          scan.py -T www.baidu.com"
    print "参数含义:"
    print "    -T 使用TCP Connect 来扫描端口"
    print "    -S 使用SYN 半扫描法来扫描端口"
    print "    -F 使用FIN 结束法来扫描IP端口"
    print "    -P 扫描1-5000的所有端口，不能和-p混用"
    print "    -p 指定端口"
    print "    -h 获取帮助"
    print "---------------------------------------------------------------------" 
    exit()

def get_opt():
    global opts,argv,one_ip,more_ip
    global Tcp_flags,Syn_flags,Fin_flags,Port_here,All_Port_flags
    try:
        #opt是参数，出来应该是[("-h",)("-T",),("-S",),("-F"),("-p","端口范围如20-200"),("--help")]
        #argv就是剩下的参数 就是不带-t的其他参数["11","b"]
        opts,argv = getopt.getopt(sys.argv[1:],"hTSFPp:",["help","port="])
    except Exception:
        print "参数不存在，请输入-h查询命令"
        use_help()
    #如果输入了参数就不为空
    #长度参数在这里,这里负责接受是用哪种方式扫描IP，可以是-T -S -F
    if not opts == None:
        #把参数取出来
        for ways,s in opts:
            if ways == "-T":
                Tcp_flags = True
            if ways == "-S":
                Syn_flags = True
            if ways == "-F":
                Fin_flags = True
            if ways == "-P":
                All_Port_flags = True
            if ways == "-h" or ways == "--help":
                use_help()
            if ways == "-p" or ways == "--port":
                if "," in s:
                    Port_here = s.split(",")
                else:
                    Port_here.append(s)
                    #print Port_here
        #用户忘记输入了-T -S -F
        if Tcp_flags == False and Syn_flags == False and Fin_flags == False: 
            #默认用TCP connect方式扫描
            Tcp_flags =True

    #正常参数在这里输出,这里负责接受IP地址或者IP段
    if not argv == None:
        yuming_list = ["www","com","cn","me","net","org","vps","blog"]
        for canshu in argv :
            #从这里分析出来是一个段还是一个IP 
            #第一种情况是一个范围 如 172.18.15.1-254
            if "-" in canshu:
                print "这是一个IP范围"
                more_ip.append(canshu)
                print more_ip
            elif "/" in canshu:
                print "这个一个子网"
                more_ip.append(canshu)
                print more_ip
            #判断是不是域名
            for yuming in yuming_list:
                if yuming in canshu:
                    #判断肯定是域名
                    x = socket.getaddrinfo(canshu,None)
                    one_ip = x[0][4][0]
                    return 0
            else:
                one_ip = canshu 





if __name__ == "__main__":
    #分析参数
    get_opt()
    #决定用什么方法扫描就看这里了
    test()
