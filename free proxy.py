import requests
import re
import threading
from lxml import etree
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def get_66ip():
    ip_port_list=[]
    print('开始抓取66代理...')
    for i in range(34):
        try:
            r=requests.get('http://www.66ip.cn/areaindex_{}/1.html'.format(str(i+1)))
            r.encoding='utf-8'
            html=etree.HTML(r.text)
            ip_list = html.xpath('//table[@bordercolor="#6699ff"]/tr/td[1]/text()')[1:]
            port_list= html.xpath('//table[@bordercolor="#6699ff"]/tr/td[2]/text()')[1:]
            for i in range(len(ip_list)):
                ip_port_list.append("{}:{}".format(ip_list[i],port_list[i]))
        except:
            pass
    print('66代理抓取结束')
    return ip_port_list

def get_89ip():
    print('开始抓取89代理...')
    try:
        r=requests.get('http://api.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp=')
        r.encoding = 'utf-8'
        res=re.findall(r';\n</script>(.+?)更好',r.text,re.S)[0]
        ip_port_list=res.replace('\n','').split('<br>')[0:-1]
        print('89代理抓取结束')
        return ip_port_list
    except:
        print('89代理抓取失败')
        return []

def check_proxy(fenlist,):
    for ip_port in fenlist:
        proxy = {
            'https': ip_port
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        try:
            r = requests.get('http://www.baidu.com', headers=headers, proxies=proxy, timeout=timeout)
            if r.status_code == 200:
                print('【{}】{}----验证成功'.format(threading.current_thread().name,ip_port))
                ok_list.append(ip_port)
        except:
            print('【{}】{}----超时'.format(threading.current_thread().name,ip_port))

def output():
    if output_type == '1':
        temp_1='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ProxifierProfile version="101" platform="MacOSX" product_id="2" product_minver="200">
    <Options>
        <Resolve>
            <AutoModeDetection enabled="false"/>
            <ViaProxy enabled="false">
                <TryLocalDnsFirst enabled="false"/>
            </ViaProxy>
            <ExclusionList ExcludeSimpleHostnames="true" ExcludeLocalhost="true" ExcludeSelfHostname="true" ExcludeLocalDomain="true">localhost;%SimpleHostnames%;%ComputerName%;*.local;
</ExclusionList>
        </Resolve>
        <Encryption mode="basic"/>
        <HttpProxiesSupport enabled="true"/>
        <HandleDirectConnections enabled="false"/>
        <ConnectionLoopDetection enabled="true"/>
        <ProcessServices enabled="true"/>
        <ProcessOtherUsers enabled="true"/>
    </Options>
    <ProxyList>
        '''
        temp_2=''
        temp_3='''
        </ProxyList>
    <ChainList/>
    <RuleList>
        <Rule enabled="true">
            <Name>Localhost</Name>
            <Targets>localhost; 127.0.0.1; ::1; %ComputerName%</Targets>
            <Action type="Direct"/>
        </Rule>
        <Rule enabled="true">
            <Name>Default</Name>
            <Action type="Proxy">1</Action>
        </Rule>
    </RuleList>
</ProxifierProfile>
        '''
        for g in range(len(ok_list)):
            ip_port_temp=ok_list[g].split(':')
            ip=ip_port_temp[0]
            port=ip_port_temp[1]
            temp_2+='''
            <Proxy id="{}" type="HTTPS">
                <Address>{}</Address>
                <Port>{}</Port>
                <Options>0</Options>
            </Proxy>\n
            '''.format(str(g+100),ip,port)
        with open('ok.ppx', 'a') as s:
            s.write(temp_1+temp_2+temp_3)
        print('验证完毕，结果位于根目录下的ok.ppx')
    elif output_type == '2':
        for i in ok_list:
            with open('ok.txt', 'a') as s:
                s.write(i + '\n')
        print('验证完毕，结果位于根目录下的ok.txt')


print('''
  ______               _____                     
 |  ____|             |  __ \                    
 | |__ _ __ ___  ___  | |__) | __ _____  ___   _ 
 |  __| '__/ _ \/ _ \ |  ___/ '__/ _ \ \/ / | | |
 | |  | | |  __/  __/ | |   | | | (_) >  <| |_| |
 |_|  |_|  \___|\___| |_|   |_|  \___/_/\_\\__, |
                                            __/ |
                                           |___/ 
''')
print('-------------------------------')
print('1.在线抓取   2.本地获取')
check_type=input('请选择：')
print('-------------------------------')
nocheck_list=[]
if check_type=='2':
    try:
        with open('ip.txt', 'r', encoding='utf-8') as f:
            nocheck_list = f.read().split('\n')
    except:
        print('错误，请确保ip.txt位于根目录，一行一条ip:port')
        exit()
elif check_type=='1':
    nocheck_list=get_66ip()+get_89ip()
else:
    print('输个编号都输不对，告辞！')
    exit()
print('-------------------------------')
print('输入验证线程数，建议1-10')
try:
    xc=int(input('线程数：'))
except:
    xc=0
    print('输个数字都不会，告辞！')
    exit()
print('-------------------------------')
try:
    print('请选择超时时间(秒)，建议3-6秒')
    timeout=int(input('超时时间：'))
except:
    timeout=0
    print('输个数字都不会，告辞！')
    exit()
print('-------------------------------')
print('请选择输出方式：1.Proxifier配置文件   2.[ip:port]文本输出')
output_type=input('请选择：')
if output_type != '1' and output_type != '2':
    print('输个编号都输不对，告辞！')
    exit()
print('-------------------------------')
print('共获取{}条代理，开始验证存活...'.format(len(nocheck_list)))
fenlist=[]
templist = [[] for i in range(xc)]
for i, e in enumerate(nocheck_list):
    templist[i % xc].append(e)
for i in templist:
    fenlist.append(i)
ok_list=[]
print('主线程开始')
thread_list = [threading.Thread(target=check_proxy, args=(fenlist[i],)) for i in range(len(fenlist))]
for t in thread_list:
    t.start()
for t in thread_list:
    t.join()
print('主线程结束')
print('-------------------------------')
output()
print('-------------------------------')