#!/usr/bin/env python
#-*-coding:utf-8-*-
import os
import sys
import platform
import time
import getopt
"""

"""
SUDO_PASSWD = "1"
BLOG_PATH = "/home/yg/yanggan.me/yanggan.github.io"

class InitJekyll:
    
    def __init__(self):
        pass
    
    def GetVersion(self):
        """
        获取系统版本
        """ 
        os_type = platform.linux_distribution()[0]
        #可能为centos,redhat,ubuntu,fedora,elementary
        all_os = ["centos","redhat","ubuntu","fedora","elementary"]
        for i in all_os:
            if i in os_type:
                return i 
            
        return "unkown"

    def Install_Jekyll(self):
        """
        通过软件中心安装必须本地软件
        """
        version = self.GetVersion()
        if version == 'ubuntu' or version == "elementary":
            print "first: install ruby........."        
            x = os.system(" sudo apt-get install -y ruby1.9.1-dev gedit ")
            if (x == 0):
                print "Sec step: install jekyll........"
                y = os.system(" sudo gem install  rake rdoc rdiscount jekyll")
            else: 
                print "install ruby error ! and error code: %d" %  x
            if not (y == 0):
                print "gem install rake,rdoc,rdiscount,jekyll error! error code: %d :" % y
                
    def Build_Jekyll(self,path=None ):
        """
        调试环境
        """
        if path == None: 
            path = BLOG_PATH
        if os.system("jekyll build --watch -s " + path + " & ")  == 0:
            print "auto build blog now....."

    def Serve_Jekyll(self,path=None):
        """
        运行本地服务器
        """
        if path == None:
            path = BLOG_PATH
        self.Build_Jekyll()
        print "running localhost service :http://0.0.0.0:4000"
        os.system("jekyll serve -s " + path + " 2>> ./jekyll_log & ")
        os.system("chromium-browser 0.0.0.0:4000 &")
    

class WriteMan:
    
    def __init__(self):
        pass
    def New_post(self,name):
        """
        新建文章
        """
        #判断目录在不在,不存在就创建他
        links = None
        if BLOG_PATH[-1] == "/":
            links = None
        else:
            links = "/"
        #path为博文路径
        path = BLOG_PATH + links + "_posts/"
        print path
        if os.path.isdir(path) == False :
            print "no _posts the dir.it will auto mkdir it "
            os.mkdir(path)
         
        #判断文章在不在，在就提示用户不用新建

        # 清空这个目录地下的带~或者.swp的文件
        os.system("rm -fv "+ path + "*.md~" )
        os.system("rm -fv "+ path + "*.swp")  
        #读取这个目录下的文件名字到list中
        exist_flags = 0
        posts_list = os.listdir(path)
        for p in posts_list:
            if name in p:
                print "you want to creat blog has exist!"
                print  p
                exist_flags = 1
                break            
        #文章不存在，现在新建 
        if exist_flags == 0:
            print "creat blog now"
            #文章名称为
            day = time.strftime(("%Y-%m-%d-"))
            post_name = day + name + ".md"
            
            #创建这个文件
            f = open(path + post_name,"w")

            #写入开头信息例如 layout,title
            title_message = "title: "  + post_name +"\n"
            tags_message = "tags: news\n"
            cate_message = "categories: news\n"
            head_message = ["---\n","layout: post\n",title_message,tags_message,cate_message,"---\n"]
            #以每行的方式写入文件 
            f.writelines(head_message)
            f.close()
        self.Mod_post(name)
 
    def Lookup_post(self,post_name=None):
        """
        查的功能
        """
        #默认情况下查询所有文章
        if post_name == None:
            post_name = "ALL"
        links = None;
        if BLOG_PATH[-1] == "/":
            links = None
        else:
            links = "/"
        #文章的路径
        path = BLOG_PATH + links + "_posts/"
        #获得这个目录下的所有文章list,并且打印出来
        posts_list = os.listdir(path)
        #删除所有.～的文章 
        os.system("rm -fv "+ path + "*.md~" )
        os.system("rm -fv "+ path + "*.swp")
        #打印格式  
        print "----------%s-----------------------%s-------" % ("Posts Name","Creat Time")
        i = 0
        return_lists = []
        for p in posts_list:
            if post_name == "ALL":
                i = i + 1
                print "NO.%s %15s\t\t\t%14s" % (str(i),p[11:-3],p[0:10])
            elif post_name in p : 
                i = i + 1
                print "NO.%s %15s\t\t\t%14s" % (str(i),p[11:-3],p[0:10])
                return_lists.append( path+p )
        if i == 0:
            print "sorry no this posts!"
        print "--------------------------------------------------------------" 
        if return_lists != [] :
            return tuple( return_lists )
    
    def Del_post(self,del_name=None):
        """
        删除功能
        """ 
        if del_name == None:
            print "please input your want to del posts! "
        del_path = self.Lookup_post(del_name)
        if del_path != None :
            print "here is your posts: \n" + str(del_path)
            print "!!!!!!!!!!do you want to delete it ?!!!!!!!!!!"
            answer = raw_input("y/n? >>> ")
            if answer == "y":
                print "del..."
                for f in del_path:
                    os.remove(f)
                    print "sucess del this post!"
                    self.Lookup_post("ALL")    
        else:
            print "can not find this post!"
            self.Lookup_post("ALL")

    def Mod_post(self,mod_name=None):
        """
        修改文章的功能 
        """
        if mod_name == None:
            print "no post need to mod! exit now.."
            sys.exit()
        mod_path = self.Lookup_post(mod_name)
        print mod_path
        for f in mod_path:
            os.system("gedit " + f + " &")
    def Rename_post(self,rename=None):
        """
        重命名文章名字
        """
        pass

class ArgvMan:
        #输入或者不输入就默认弹出提示界面
    def __init__(self,argvs=sys.argv[1:]):
        self.argvs = argvs
        self.blog = WriteMan()
    def usage(self):
        print "\n\nUsage:\n blog.py [options[-n|-d|-l|-m]] post_name"
        print " blog.py [options[--pull|--push|--new|--del|--lookup|--mod|--watch]] argv "
        print "\n\nOptions:\n"
        print " -n,--new    write a new post\n -l,--lookup    lookup post\n -d,--del    del a post \n -m,--mod    mod a post"
        print " --pull    pull blog on github\n --push    blog to github\n --watch    build and running jekyll in localhost "
        print " --install    install jekyll in localhost\n\n\n "

    #处理参数的函数
    def opt_analyze(self):
        try:
            options,args = getopt.getopt(sys.argv[1:],"l:d:n:m:h",["help","pull","push","new=","lookup=","del=","mod="])
        except getopt.GetoptError():
            self.usage()
            sys.exit()
        print args
        return (options,args)

    #分析出参数后应该处理的函数
    def opt_handle(self):
        #分析并且处理命令
        if len(self.argvs) == 0:
            self.usage()
            self.blog.Lookup_post("ALL")
            sys.exit()
        #把命令行参数提取出来
        options,args = self.opt_analyze()
        #对应用户不同命令和不同处理方法
        for name,value in options:
            if name in ("-h","--help"):
                self.usage()
            if name in ("-n","--new"):
                print "new a post" 
                self.blog.New_post(value)
                break
            if name in ("-l","--lookup"):
                print "lookup the post!"
                self.blog.Lookup_post(value)
                break
            if name in ("-d","--del"):
                print "del the post"
                self.blog.Del_post(value)
                break
            if name in ("-m","--mod"):
                print "mod the post"
                self.blog.Mod_post(value)
                break
            if name in ("--push"):
                print "push blog"
                break
            if name in ("--pull"):
                print "pull bolg"
                break
            else:
                pass
        return 0

#执行函数
if __name__ == '__main__':
    # 这里算程序的入口了
    main_start = ArgvMan()
    main_start.opt_handle()
