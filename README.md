# My tools
=====

> 都是一些自己些的小脚本的集合，在工作生活上有所帮助,目前偶的工具是

## 1.jekyll博客助手 
a blog.py python写的本地自动化推更jekyll blog脚本，想法是能不能一条命令写博客呢？用Python处理一下，改成类似命令行基本形式。

基本格式如下:
```
yg@ASUS:~$ bk


Usage:
 blog.py [options[-n|-d|-l|-m]] post_name
 blog.py [options[--pull|--push|--new|--del|--lookup|--mod|--watch]] argv 


Options:

 -n,--new    write a new post
 -l,--lookup    lookup post
 -d,--del    del a post 
 -m,--mod    mod a post
 --pull    pull blog on github
 --push    blog to github
 --watch    build and running jekyll in localhost 
 --install    install jekyll in localhost


all post 

----------Posts Name-----------------------Creat Time-------
NO.1 learn-jekyll-book			    2014-04-05
NO.2 Ruijie_Switch_setup			    2014-05-02
NO.3      Akuai_play			    2014-05-04
NO.4       Web-books			    2014-07-28
NO.5           wsshd			    2014-04-14
NO.6        wiki-cdn			    2014-04-27
NO.7        git-push			    2014-04-17
NO.8    markdown-use			    2014-04-07
NO.9    jekyll-tools			    2014-04-06
--------------------------------------------------------------


```
search blog 

```
yg@ASUS:~$ bk -l book
lookup the post!
----------Posts Name-----------------------Creat Time-------
NO.1 learn-jekyll-book			    2014-04-05
NO.2       Web-books			    2014-07-28
--------------------------------------------------------------
```
## 2.端口扫描器 

* scan.py 用Python写的测试端口扫描的小工具，其中部分还调用了namp工具。力求使用简单方便扫描。

```
yg@ASUS:~$ scan.py -h
------------------------欢迎使用Simple PortScaner------------------- 
基本格式: scan.py [option]..[-T | -S | -F | -p port | -h |]  ip
例如:     scan.py -T -p 21,22,23,80,3389 172.18.15.254
          scan.py -T www.baidu.com
参数含义:
    -T 使用TCP Connect 来扫描端口
    -S 使用SYN 半扫描法来扫描端口
    -F 使用FIN 结束法来扫描IP端口
    -P 扫描1-5000的所有端口，不能和-p混用
    -p 指定端口
    -h 获取帮助

yg@ASUS:~$ scan.py -T 192.168.1.1 
    主机不在线 无法扫描!
yg@ASUS:~$ scan.py -T 192.168.0.1 
    使用TCP三次握手方法扫描IP: 192.168.0.1
    192.168.0.1:80 is open

---------------------------------------------------------------------


```


