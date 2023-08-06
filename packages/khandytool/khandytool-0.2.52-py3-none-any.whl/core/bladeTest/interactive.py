import random,time
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from time import sleep
# print("###"+os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# print("###"+os.path.abspath(os.path.dirname(os.getcwd())))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from loguru import logger
from pywebio.input import input, FLOAT,NUMBER,input_group,select, textarea,file_upload,checkbox,radio
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row
from pywebio import start_server,session,platform
from core.bladeTest.main import RemoteRunner,generateHtmlReport,running
from core.jmeterTool.swagger2jmeter import swagger2jmeter
from core.jmeterTool.har2jmeter import har2jmeter
from core.xmind2excel import makeCase
from core.utils import CFacker,getDateTime
from core.mqttUtil import NormalMqttGetter
from core.kafkaUtil import general_sender,continue_orderMsg,general_orderMsg,general_orderMsgWithFilter,kafkaFetchServerWithFilter,kafkaFetchServer
from functools import partial
from multiprocessing import Process
import decimal,websockets,asyncio
import json


def myapp():
    '''
    this main function for enter the whole functions of pywebio
    :return:
    '''
    session.set_env(title='testToolKit')

    select_type = select("选择你要做的操作:",["xmind转excel","混沌测试-交互式","混沌测试-直接输入(推荐)","jmeter脚本生成","假数据构造","kafka操作","mqtt操作"])
    try:
        if select_type=="xmind转excel":
            uploadXmind()
        elif select_type=="混沌测试-交互式":
            oneCheck()
        elif select_type=="混沌测试-直接输入(推荐)":
            onePageInput()
        elif select_type=="jmeter脚本生成":
            jmeterScriptGen()
        elif select_type=="假数据构造":
            myFackData()
        elif select_type=="kafka操作":
            kafkaListener()
        elif select_type=="mqtt操作":
            mqttListener()
    except Exception as e:
        put_text(e)

def jmeterScriptGen():
    '''
    this just invoke the lib for generate jmeter script
    :return:
    '''
    session.set_env(title='testToolKit')
    select_type = select("选择你要做的操作:",["swagger转jmeter脚本","har转jmeter脚本"])
    if select_type=="swagger转jmeter脚本":
        url=input('输入swagger地址：example:http://192.168.xxx.xxx:port/space_name/v2/api-docs')
        # print(url)
        location=os.path.join(sys.exec_prefix, 'jmx')+os.sep
        print(location)
        swagger2jmeter(url,location)
        file_location=None
        # location=os.path.abspath(os.path.dirname(__file__))+os.sep+'jmx'+os.sep
        print(location)
        for x,y,z in os.walk(location):
            file_location=location+"".join(z)
            break
        print(file_location)
        put_file(content=open(file_location,mode="rb").read(),name=file_location.split(os.sep)[-1],label="点击下载jmeter脚本")
        os.remove(file_location)
    elif select_type=="har转jmeter脚本":
        f = file_upload("上传har文件，可以从fidder, charlse, chrome开发者工具中导出",accept="*.har",placeholder='选择har文件')
        open('temp.har', 'wb').write(f['content'])
        har2jmeter('temp.har')
        location=os.path.abspath('.')+os.path.sep+"autoGen.jmx"
        print(location)
        put_file(content=open(location,mode="rb").read(),name="autoGen.jmx",label="点击下载jmeter脚本")
        


def uploadXmind():
    '''
    generate excel of test case from a xmind file
    :return:
    '''
    session.set_env(title='testToolKit')
    # Upload a file and save to server      
    print(os.path.abspath(os.path.dirname(__file__)))
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]

    img = open(os.path.join(curPath,'xmindStructure.jpg'), 'rb').read()  
    put_image(img)              
    f = file_upload("上传xmind文件，注意xmind节点中不要有特殊字符，空的节点使用NA标记",accept="*.xmind",placeholder='选择xmind文件')                  
    # open('asset/'+f['filename'], 'wb').write(f['content'])  
    open('temp.xmind', 'wb').write(f['content']) 
    makeCase('temp.xmind',f"{f['filename']}_testcase.xlsx")
    location=os.path.abspath('.')+os.path.sep+f"{f['filename']}_testcase.xlsx"
    put_file(content=open(location,mode="rb").read(),name=f"{f['filename']}_testcase.xlsx",label="点击下载Excel用例")





def onePageInput():
    '''
    using formated json script to generate the blade test and run it
    :return:
    '''
    session.set_env(title='testToolKit')
    put_markdown('''# 基础指令参考：
        ## blade create cpu load [flags]
                            --timeout string   设定运行时长，单位是秒，通用参数
                            --cpu-count string     指定 CPU 满载的个数
                            --cpu-list string      指定 CPU 满载的具体核，核索引从 0 开始 (0-3 or 1,3)
                            --cpu-percent string   指定 CPU 负载百分比，取值在 0-100
        ##                blade create disk burn
                            --path string      指定提升磁盘 io 的目录，会作用于其所在的磁盘上，默认值是 /
                            --read             触发提升磁盘读 IO 负载，会创建 600M 的文件用于读，销毁实验会自动删除
                            --size string      块大小, 单位是 M, 默认值是 10，一般不需要修改，除非想更大的提高 io 负载
                            --timeout string   设定运行时长，单位是秒，通用参数
                            --write            触发提升磁盘写 IO 负载，会根据块大小的值来写入一个文件，比如块大小是 10，则固定的块的数量是 100，则会创建 1000M 的文件，销毁实验会自动删除
        ##                blade create disk fill
                            --path string      需要填充的目录，默认值是 /
                            --size string      需要填充的文件大小，单位是 M，取值是整数，例如 --size 1024
                            --reserve string   保留磁盘大小，单位是MB。取值是不包含单位的正整数，例如 --reserve 1024。如果 size、percent、reserve 参数都存在，优先级是 percent > reserve > size
                            --percent string   指定磁盘使用率，取值是不带%号的正整数，例如 --percent 80
                            --retain-handle    是否保留填充
                            --timeout string   设定运行时长，单位是秒，通用参数
        ##                blade create mem load
                            --mem-percent string    内存使用率，取值是 0 到 100 的整数
                            --mode string   内存占用模式，有 ram 和 cache 两种，例如 --mode ram。ram 采用代码实现，可控制占用速率，优先推荐此模式；cache 是通过挂载tmpfs实现；默认值是 --mode cache
                            --reserve string    保留内存的大小，单位是MB，如果 mem-percent 参数存在，则优先使用 mem-percent 参数
                            --rate string 内存占用速率，单位是 MB/S，仅在 --mode ram 时生效
                            --timeout string   设定运行时长，单位是秒，通用参数
        ##                blade create network delay
                            --destination-ip string   目标 IP. 支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                            --exclude-port string     排除掉的端口，默认会忽略掉通信的对端端口，目的是保留通信可用。可以指定多个，使用逗号分隔或者连接符表示范围，例如 22,8000 或者 8000-8010。 这个参数不能与 --local-port 或者 --remote-port 参数一起使用
                            --exclude-ip string       排除受影响的 IP，支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                            --interface string        网卡设备，例如 eth0 (必要参数)
                            --local-port string       本地端口，一般是本机暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                            --offset string           延迟时间上下浮动的值, 单位是毫秒
                            --remote-port string      远程端口，一般是要访问的外部暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                            --time string             延迟时间，单位是毫秒 (必要参数)
                            --force                   强制覆盖已有的 tc 规则，请务必在明确之前的规则可覆盖的情况下使用
                            --ignore-peer-port        针对添加 --exclude-port 参数，报 ss 命令找不到的情况下使用，忽略排除端口
                            --timeout string          设定运行时长，单位是秒，通用参数
        ##                blade create network loss
                            --destination-ip string   目标 IP. 支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                            --exclude-port string     排除掉的端口，默认会忽略掉通信的对端端口，目的是保留通信可用。可以指定多个，使用逗号分隔或者连接符表示范围，例如 22,8000 或者 8000-8010。 这个参数不能与 --local-port 或者 --remote-port 参数一起使用
                            --exclude-ip string       排除受影响的 IP，支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
                            --interface string        网卡设备，例如 eth0 (必要参数)
                            --local-port string       本地端口，一般是本机暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                            --percent string          丢包百分比，取值在[0, 100]的正整数 (必要参数)
                            --remote-port string      远程端口，一般是要访问的外部暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
                            --force                   强制覆盖已有的 tc 规则，请务必在明确之前的规则可覆盖的情况下使用
                            --ignore-peer-port        针对添加 --exclude-port 参数，报 ss 命令找不到的情况下使用，忽略排除端口
                            --timeout string          设定运行时长，单位是秒，通用参数
        ##                blade create network occupy
                            --port string             指定被占用的端口，（必填项）
                            --force                   强制占用此端口，会将已使用此端口的进程杀掉
                            --timeout string          设定运行时长，单位是秒，通用参数
        ##                blade create process kill
                            --process string       进程关键词，会在整个命令行中查找
                            --process-cmd string   进程命令，只会在命令中查找
                            --count string      限制杀掉进程的数量，0 表示无限制
                            --signal string     指定杀进程的信号量，默认是 9，例如 --signal 15
                            --timeout string   设定运行时长，单位是秒，通用参数
        ##                blade create process stop
                            --process string       进程关键词，会在整个命令行中查找
                            --process-cmd string   进程命令，只会在命令中查找
                            --timeout string   设定运行时长，单位是秒，通用参数
        ##                blade create docker cpu
                            --blade-override           是否覆盖容器内已有的 chaosblade 工具，默认是 false，表示不覆盖，chaosblade 在容器内的部署路径为 /opt/chaosblade
                            --blade-tar-file string    指定本地 chaosblade-VERSION.tar.gz 工具包全路径，用于拷贝到容器内执行
                            --container-id string      目标容器 ID
                            --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
        ##                blade create docker network
                            --container-id string      目标容器 ID
                            --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
                            --image-repo string        chaosblade-tool 镜像仓库地址，默认是从 `registry.cn-hangzhou.aliyuncs.com/chaosblade`
        ##                blade create docker process
                            --blade-override           是否覆盖容器内已有的 chaosblade 工具，默认是 false，表示不覆盖，chaosblade 在容器内的部署路径为 /opt/chaosblade
                            --blade-tar-file string    指定本地 chaosblade-VERSION.tar.gz 工具包全路径，用于拷贝到容器内执行
                            --container-id string      目标容器 ID
                            --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
        ##                blade create docker container
                            --container-id string      要删除的容器 ID
                            --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
                            --force                    是否强制删除
        ''')
    json_str = textarea('请输入json串', rows=30,value=r'''{
    "data":[
      {
        "description": "主机网络限制延迟查看接口响应",
        "flag":"true", 是否运行
        "type": "docker", 类型是host 或者 docker
        "host":"192.168.xxxx.xxx",
        "port": 22,
        "user":"root",
        "passwd": "xxxxxx",
        "execCommand":"blade create network delay --time 1000 --interface eth0 --local-port 18086", 需要执行的命令
        "execCommandExpect": "success", 通常为success，可以不用改
        "dockerName": "",  如果是docker需要知道docker名称，一定要是唯一标识
        "checkCommand": "", 执行命令后的检查命令，比如CPU是否达到 70%
        "checkExpect": "", 检查的期望值
        "httpCheckCommand": { 通过http的方式进行检查，以及发送的内容，目前不支持需要登录的方式，建议手动添加token到header
          "url":"http://192.168.xxxx.xxx:18086/query",
          "method":"POST",
          "header":{},
          "cookie":{},
          "params":{"q":"show databases"},
          "json":{}
        },
        "httpExpect": "results" http检查值的返回
      },{}]}''',code={
            'mode': "json",
            'theme': 'darcula'
        })
    put_code(json_str, language='json') 
    runAndGetReport(json.loads(json_str))

    
    






def oneCheck():
    '''
    using step by step way to execute blade test
    :return:
    '''
    session.set_env(title='testToolKit')
    input_data={"data":[]}
    temp_data={}
    
    go_on=True
    while go_on:
        http_check_data={}
        type_data={}

        server_data = input_group("请输入主机信息",[
        input('本次测试描述', name="description"),
        input('输入服务器IP', name="host"),
        input('输入服务器端口', name="port", type=NUMBER),
        input('输入服务器用户名', name="user"),
        input('输入服务器密码', name="passwd"),
        ])

        r=RemoteRunner(server_data["host"],server_data["port"],server_data["user"],server_data["passwd"])
        upload = select("是否已经上传chaos文件:",["是","否"])
        if upload=="否":
            popup(title="注意",content="部署命令安装中。。。")
            r.exec_cmd("cd /opt;rm -rf chaos*")
            r.upload_file("chaosblade.tar.gz", "/opt")
            r.exec_cmd('cd /opt; mkdir chaos;tar -xzvf chaosblade.tar.gz -C ./chaos;')
            r.exec_cmd('echo "export PATH=$PATH:/opt/chaos/chaosblade-1.2.0/">>~/.bashrc')
            r.exec_cmd('source ~/.bashrc')
            r.upload_file("chaosblade.tar.gz", "/opt")

        select_type = select("选择被检查类型:",["主机","docker"])

        if select_type=="主机":
            type_data["type"]="host"
            type_data["dockerName"]=""
        elif select_type=="docker":
            type_data["type"]="docker"
            type_data["dockerName"]=input("请输入docker名称", name="dockerName")
        # else:
        #     popup(title="注意",content="类型选择有误！！！")
        #     select_type=None

        chaos_data = input_group("请输入chaos命令",[
            # textarea('基础指令参考', rows=20,name='comments',value='''基础指令参考：
            #     blade create cpu load [flags]
            #         --timeout string   设定运行时长，单位是秒，通用参数
            #         --cpu-count string     指定 CPU 满载的个数
            #         --cpu-list string      指定 CPU 满载的具体核，核索引从 0 开始 (0-3 or 1,3)
            #         --cpu-percent string   指定 CPU 负载百分比，取值在 0-100
            #     blade create disk burn
            #         --path string      指定提升磁盘 io 的目录，会作用于其所在的磁盘上，默认值是 /
            #         --read             触发提升磁盘读 IO 负载，会创建 600M 的文件用于读，销毁实验会自动删除
            #         --size string      块大小, 单位是 M, 默认值是 10，一般不需要修改，除非想更大的提高 io 负载
            #         --timeout string   设定运行时长，单位是秒，通用参数
            #         --write            触发提升磁盘写 IO 负载，会根据块大小的值来写入一个文件，比如块大小是 10，则固定的块的数量是 100，则会创建 1000M 的文件，销毁实验会自动删除
            #     blade create disk fill
            #         --path string      需要填充的目录，默认值是 /
            #         --size string      需要填充的文件大小，单位是 M，取值是整数，例如 --size 1024
            #         --reserve string   保留磁盘大小，单位是MB。取值是不包含单位的正整数，例如 --reserve 1024。如果 size、percent、reserve 参数都存在，优先级是 percent > reserve > size
            #         --percent string   指定磁盘使用率，取值是不带%号的正整数，例如 --percent 80
            #         --retain-handle    是否保留填充
            #         --timeout string   设定运行时长，单位是秒，通用参数
            #     blade create mem load
            #         --mem-percent string    内存使用率，取值是 0 到 100 的整数
            #         --mode string   内存占用模式，有 ram 和 cache 两种，例如 --mode ram。ram 采用代码实现，可控制占用速率，优先推荐此模式；cache 是通过挂载tmpfs实现；默认值是 --mode cache
            #         --reserve string    保留内存的大小，单位是MB，如果 mem-percent 参数存在，则优先使用 mem-percent 参数
            #         --rate string 内存占用速率，单位是 MB/S，仅在 --mode ram 时生效
            #         --timeout string   设定运行时长，单位是秒，通用参数
            #     blade create network delay
            #         --destination-ip string   目标 IP. 支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
            #         --exclude-port string     排除掉的端口，默认会忽略掉通信的对端端口，目的是保留通信可用。可以指定多个，使用逗号分隔或者连接符表示范围，例如 22,8000 或者 8000-8010。 这个参数不能与 --local-port 或者 --remote-port 参数一起使用
            #         --exclude-ip string       排除受影响的 IP，支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
            #         --interface string        网卡设备，例如 eth0 (必要参数)
            #         --local-port string       本地端口，一般是本机暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
            #         --offset string           延迟时间上下浮动的值, 单位是毫秒
            #         --remote-port string      远程端口，一般是要访问的外部暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
            #         --time string             延迟时间，单位是毫秒 (必要参数)
            #         --force                   强制覆盖已有的 tc 规则，请务必在明确之前的规则可覆盖的情况下使用
            #         --ignore-peer-port        针对添加 --exclude-port 参数，报 ss 命令找不到的情况下使用，忽略排除端口
            #         --timeout string          设定运行时长，单位是秒，通用参数
            #     blade create network loss
            #         --destination-ip string   目标 IP. 支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
            #         --exclude-port string     排除掉的端口，默认会忽略掉通信的对端端口，目的是保留通信可用。可以指定多个，使用逗号分隔或者连接符表示范围，例如 22,8000 或者 8000-8010。 这个参数不能与 --local-port 或者 --remote-port 参数一起使用
            #         --exclude-ip string       排除受影响的 IP，支持通过子网掩码来指定一个网段的IP地址, 例如 192.168.1.0/24. 则 192.168.1.0~192.168.1.255 都生效。你也可以指定固定的 IP，如 192.168.1.1 或者 192.168.1.1/32，也可以通过都号分隔多个参数，例如 192.168.1.1,192.168.2.1。
            #         --interface string        网卡设备，例如 eth0 (必要参数)
            #         --local-port string       本地端口，一般是本机暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
            #         --percent string          丢包百分比，取值在[0, 100]的正整数 (必要参数)
            #         --remote-port string      远程端口，一般是要访问的外部暴露服务的端口。可以指定多个，使用逗号分隔或者连接符表示范围，例如 80,8000-8080
            #         --force                   强制覆盖已有的 tc 规则，请务必在明确之前的规则可覆盖的情况下使用
            #         --ignore-peer-port        针对添加 --exclude-port 参数，报 ss 命令找不到的情况下使用，忽略排除端口
            #         --timeout string          设定运行时长，单位是秒，通用参数
            #     blade create network occupy
            #         --port string             指定被占用的端口，（必填项）
            #         --force                   强制占用此端口，会将已使用此端口的进程杀掉
            #         --timeout string          设定运行时长，单位是秒，通用参数
            #     blade create process kill
            #         --process string       进程关键词，会在整个命令行中查找
            #         --process-cmd string   进程命令，只会在命令中查找
            #         --count string      限制杀掉进程的数量，0 表示无限制
            #         --signal string     指定杀进程的信号量，默认是 9，例如 --signal 15
            #         --timeout string   设定运行时长，单位是秒，通用参数
            #     blade create process stop
            #         --process string       进程关键词，会在整个命令行中查找
            #         --process-cmd string   进程命令，只会在命令中查找
            #         --timeout string   设定运行时长，单位是秒，通用参数
            #     blade create docker cpu
            #         --blade-override           是否覆盖容器内已有的 chaosblade 工具，默认是 false，表示不覆盖，chaosblade 在容器内的部署路径为 /opt/chaosblade
            #         --blade-tar-file string    指定本地 chaosblade-VERSION.tar.gz 工具包全路径，用于拷贝到容器内执行
            #         --container-id string      目标容器 ID
            #         --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
            #     blade create docker network
            #         --container-id string      目标容器 ID
            #         --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
            #         --image-repo string        chaosblade-tool 镜像仓库地址，默认是从 `registry.cn-hangzhou.aliyuncs.com/chaosblade`
            #     blade create docker process
            #         --blade-override           是否覆盖容器内已有的 chaosblade 工具，默认是 false，表示不覆盖，chaosblade 在容器内的部署路径为 /opt/chaosblade
            #         --blade-tar-file string    指定本地 chaosblade-VERSION.tar.gz 工具包全路径，用于拷贝到容器内执行
            #         --container-id string      目标容器 ID
            #         --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
            #     blade create docker container
            #         --container-id string      要删除的容器 ID
            #         --docker-endpoint string   Docker server 地址，默认为本地的 /var/run/docker.sock
            #         --force                    是否强制删除
            #     '''),
        input("注入命令",name="execCommand"),
        input("注入命令期望返回", name="execCommandExpect",value="success"),
        ])
        
        select_res = select("选择检查方式:",["主机命令检查","http请求检查"])

        if select_res=="主机命令检查":
            check_data = input_group("host命令检查",[
            input("检查命令", name="checkCommand"),
            input("检查命令期望返回", name="checkExpect"),
            ])
            http_check_data["httpCheckCommand"]=""
        elif select_res=="http请求检查":
            
            check_data = input_group("http检查",[
            input("http检查接口地址", name="httpCheckCommand"),
            input("http method", name="httpCheckCommand"),
            input("http header", name="httpCheckCommand"),
            input("http param", name="httpCheckCommand"),
            input("http cookie", name="httpCheckCommand"),
            input("http json", name="httpCheckCommand"),
            input("http检查期望返回", name="httpExpect"),
            ])
            http_check_data["httpCheckCommand"]=check_data
        else:
            popup(title="注意",content="检查方式选择：有误！！！")

        # print(server_data['desc'], server_data['ip'],server_data['port'],server_data['username'],server_data['password'],
        # chaos_data['execCommand'], chaos_data['execCommandExpect'],check_data['checkCommand'],check_data['checkExpect'],check_data['httpCheckCommand'],check_data['httpExpect'])
        temp_data.update(server_data)
        temp_data.update(chaos_data)
        temp_data.update(check_data)
        temp_data.update(type_data)
        temp_data.update(http_check_data)
        temp_data["flag"]="true"
        input_data["data"].append(temp_data)



        popup(title="可直接忽略",content=json.dumps(input_data)) 

        go = select("是否继续输入下一个测试项:",["是","否"])
        if go=="是":
            go_on=True
        elif go=="否":
            go_on=False
            runAndGetReport(input_data)
            # popup(title="注意",content="正在运行测试。。。") 
            # url=generateHtmlReport(running(jf=input_data))
            # print(url)
            # close_popup()
            # # put_link(app='Result',new_window=True,name='Result')
            # # put_html(html=open(url,encoding='utf-8').readlines())
            # put_file(content=open(url,mode="rb").read(),name="result.html",label="点击下载简报")
            

def runAndGetReport(input_data):
    '''
    generate blade test report
    :param input_data:
    :return:
    '''
    session.set_env(title='testToolKit')
    popup(title="注意",content="正在运行测试。。。") 
    url=generateHtmlReport(running(jf=input_data))
    print(url)
    close_popup()
    # put_link(app='Result',new_window=True,name='Result')
    # put_html(html=open(url,encoding='utf-8').readlines())
    put_file(content=open(url,mode="rb").read(),name="result.html",label="点击下载简报")


def run(portNum=8899):
    '''
    running application by command
    :param portNum:
    :return:
    '''
    start_server(myapp, port=portNum)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def myFackData():
    '''
    generate the fake data by using this app, when you test
    :return:
    '''
    session.set_env(title='testToolKit')
    all_options={
    "city_suffix":"市，县",
    "country":"国家",
    "country_code":"国家编码",
    "district":"区",
    "latitude":"地理坐标(纬度)",
    "longitude":"地理坐标(经度)",
    "postcode":"邮编",
    "province":"省份 (zh_TW没有此方法)",
    "address":"详细地址",
    "street_address":"街道地址",
    "street_name":"街道名",
    "street_suffix":"街、路",
    "ssn":"生成身份证号",
    "bs":"随机公司服务名",
    "company":"随机公司名（长）",
    "company_prefix":"随机公司名（短）",
    "company_suffix":"公司性质",
    "credit_card_expire":"随机信用卡到期日",
    "credit_card_full":"生成完整信用卡信息",
    "credit_card_number":"信用卡号",
    "credit_card_provider":"信用卡类型",
    "credit_card_security_code":"信用卡安全码",
    "job":"随机职位",
    "first_name":"名",
    "first_name_female":"女性名",
    "first_name_male":"男性名",
    "first_romanized_name":"罗马名",
    "last_name":"姓",
    "last_name_female":"女姓",
    "last_name_male":"男姓",
    "last_romanized_name":"随机",
    "name":"随机生成全名",
    "name_female":"男性全名",
    "name_male":"女性全名",
    "romanized_name":"罗马名",
    "msisdn":"移动台国际用户识别码，即移动用户的ISDN号码",
    "phone_number":"随机生成手机号",
    "phonenumber_prefix":"随机生成手机号段",
    "ascii_company_email":"随机ASCII公司邮箱名",
    "ascii_email":"随机ASCII邮箱",
    "ascii_free_email":"二进制免费邮件",
    "ascii_safe_email":"二进制安全邮件",
    "company_email":"公司邮件",
    "email":"电子邮件",
    "free_email":"免费电子邮件",
    "free_email_domain":"免费电子邮件域名",
    "safe_email":"安全邮箱",
    "domain_name":"生成域名",
    "domain_word":"域词(即，不包含后缀)",
    "ipv4":"随机IP4地址",
    "ipv6":"随机IP6地址",
    "mac_address":"随机MAC地址",
    "tld":"网址域名后缀(.com,.net.cn,等等，不包括.)",
    "uri":"随机URI地址",
    "uri_extension":"网址文件后缀",
    "uri_page":"网址文件（不包含后缀）",
    "uri_path":"网址文件路径（不包含文件名）",
    "url":"随机URL地址",
    "user_name":"随机用户名",
    "image_url":"随机URL地址",
    "chrome":"随机生成Chrome的浏览器user_agent信息",
    "firefox":"随机生成FireFox的浏览器user_agent信息",
    "internet_explorer":"随机生成IE的浏览器user_agent信息",
    "opera":"随机生成Opera的浏览器user_agent信息",
    "safari":"随机生成Safari的浏览器user_agent信息",
    "linux_platform_token":"随机Linux信息",
    "user_agent":"随机user_agent信息",
    "file_extension":"随机文件扩展名",
    "file_name":"随机文件名（包含扩展名，不包含路径）",
    "file_path":"随机文件路径（包含文件名，扩展名）",
    "mime_type":"随机mime Type",
    "numerify":"三位随机数字",
    "random_digit":"0~9随机数",
    "random_digit_not_null":"1~9的随机数",
    "random_int":"随机数字，默认0~9999，可以通过设置min,max来设置",
    "random_number":"随机数字，参数digits设置生成的数字位数",
    "pyfloat":"left_digits=5 #生成的整数位数, right_digits=2 #生成的小数位数, positive=True #是否只有正数",
    "pyint":"随机Int数字（参考random_int=参数）",
    "pydecimal":"随机Decimal数字（参考pyfloat参数）",
    "pystr":"随机字符串",
    "random_element":"随机字母",
    "random_letter":"随机字母",
    "paragraph":"随机生成一个段落",
    "paragraphs":"随机生成多个段落，通过参数nb来控制段落数，返回数组",
    "sentence":"随机生成一句话",
    "sentences":"随机生成多句话，与段落类似",
    "text":"随机生成一篇文章（不要幻想着人工智能了，至今没完全看懂一句话是什么意思）",
    "word":"随机生成词语",
    "words":"随机生成多个词语，用法与段落，句子，类似",
    "binary":"随机生成二进制编码",
    "boolean":"True/False",
    "language_code":"随机生成两位语言编码",
    "locale":"随机生成语言/国际 信息",
    "md5":"随机生成MD5",
    "null_boolean":"NULL/True/False",
    "password":"随机生成密码,可选参数：length：密码长度；special_chars：是否能使用特殊字符；digits：是否包含数字；upper_case：是否包含大写字母；lower_case：是否包含小写字母",
    "sha1":"随机SHA1",
    "sha256":"随机SHA256",
    "uuid4":"随机UUID",
    "am_pm":"AM/PM",
    "century":"随机世纪",
    "date":"随机日期",
    "date_between":"随机生成指定范围内日期，参数：start_date，end_date取值：具体日期或者today,-30d,-30y类似",
    "date_between_dates":"随机生成指定范围内日期，用法同上",
    "date_object":"随机生产从1970-1-1到指定日期的随机日期。",
    "date_this_month":"当月",
    "date_this_year":"当年",
    "date_time":"随机生成指定时间（1970年1月1日至今）",
    "date_time_ad":"生成公元1年到现在的随机时间",
    "date_time_between":"用法同dates",
    "future_date":"未来日期",
    "future_datetime":"未来时间",
    "month":"随机月份",
    "month_name":"随机月份（英文）",
    "past_date":"随机生成已经过去的日期",
    "past_datetime":"随机生成已经过去的时间",
    "time":"随机24小时时间",
    "time_object":"随机24小时时间，time对象",
    "time_series":"随机TimeSeries对象",
    "timezone":"随机时区",
    "unix_time":"随机Unix时间",
    "year":"随机年份",
    "profile":"随机生成档案信息",
    "simple_profile":"随机生成简单档案信息",
    "currency_code":"货币编码",
    "color_name":"随机颜色名",
    "hex_color":"随机HEX颜色",
    "rgb_color":"随机RGB颜色",
    "safe_color_name":"随机安全色名",
    "safe_hex_color":"随机安全HEX颜色",
    "isbn10":"随机ISBN(10位)",
    "isbn13":"随机ISBN(13位)",
    "lexify":"替换所有问号?带有随机字母的事件"
    }
    

    choose=checkbox(label='从下列选项中，选择你想生成的数据：',options=all_options.values())
    # put_row([input('自定义键值：'),checkbox(options=[''])])
    restDict={}
    for one in choose:
        funcName=list(all_options.keys())[list(all_options.values()).index(one)]
        restDict[one]=CFacker().get_it(funcName)
    
    # put_text(restDict)
    put_code(json.dumps(restDict,cls=DecimalEncoder, indent=4,ensure_ascii=False), language='json',rows=20) 

def kafkaListener():
    '''
    to send kafka message or listener the kafka topic
    :return:
    '''
    session.set_env(title='testTools')

    select_type = select("选择kafka操作:",["kafka发送消息","kafka持续接收消息"])

    if select_type=="kafka发送消息":
        data = input_group("kafka连接配置",[
            input("kafka topic，必填", name="topic"),
            input("kafka 地址，如ip:port，必填", name="address"),
            input("要发送的消息，必填",name="msg"),
            input("发送频率（秒），非必填",name="interval",value="3"),
            radio(label="持续发送",name="always",inline='true',options=('是','否'),value=('否'))
            ])
        if data['always']=="否":
            general_sender(data['topic'],data['address'],data['msg'])
            put_text('发送完成')
        elif data['always']=="是":
            counter=0
            while True:
                counter=counter+1
                general_sender(data['topic'],data['address'],data['msg'])
                put_text(f"发送{counter}次, {getDateTime()}")
                sleep(int(data['interval']))
    # elif select_type=="kafka接收固定消息":
    #     data = input_group("kafka连接配置",[
    #         input("kafka topic，必填", name="topic"),
    #         input("kafka 地址，如ip:port，必填", name="address"),
    #         input("持续接收时间，必填", name="interval"),
    #         input("获取消息数量（条数），必填", name="getNum"),
    #         input("过滤方式，仅支持填json或regx，非必填", name="filter"),
    #         input("过滤表达式，json使用jmeshpath方式，regx采用abc(.*)bbb的方式，非必填", name="pattern"),
    #         input("过滤后比对关键字，过滤后的值是否等于输入的值，非必填", name="key"),
    #         ])
    #     if data['filter']=="None" or data['filter']=="":
    #         msg=general_orderMsg(topic=data['topic'],serverAndPort=data['address'],interval_ms=int(data['interval']),getNum=int(data['getNum']))
    #         put_text("\n".join(msg))
    #     else:
    #         msg=general_orderMsgWithFilter(topic=data['topic'],serverAndPort=data['address'],interval_ms=int(data['interval']),getNum=int(data['getNum']),filterFlag=data['filter'],pattern=data['pattern'],matchStr=data['key'])
    #         put_text("\n".join(msg))
    elif select_type=="kafka持续接收消息":
        # host=session.info["server_host"]
        put_text(
            "iotHub消息队列过滤，采用json方式，过滤虚拟设备号为：payload.virDevUid\n空间管理属性device_default_prop过滤，采用json方式，过滤虚拟设备号为payload.virDevUid\n空间管理状态device_default_state过滤，采用json方式，过滤实际设备号为payload.deviceId")
        data = input_group("kafka连接配置", [
            input("kafka topic，必填", name="topic",value='iotHub'),
            input("kafka 地址，如ip:port，必填", name="address",value='192.168.125.149:9092'),
            input("过滤方式，仅支持填json或regx，非必填", name="filter",value='json'),
            input("过滤表达式，json使用jmeshpath方式，regx采用abc(.*)bbb的方式，非必填", name="pattern",value="payload.name"),
            input("过滤后比对关键字，过滤后的值是否等于输入的值，非必填", name="key",value="status"),
        ])
        #仅在app中使用
        # ip = session.info["server_host"].split(":")[0]
        # portNum = random.randint(59000, 60000)
        # print(data['address'], data['topic'], data['filter'], data['pattern'], data['key'],portNum)
        # Process(target=kafkaFetchServerWithFilter, args=(0, None, data['address'], data['topic'],data['filter'],data['pattern'],data['key'],"0.0.0.0",portNum)).start()
        # htmlRaw='''
        #    <html>
        #         <head>
        #             <title>WebSocket demo</title>
        #         </head>
        #         <body>
        #         <h1>kafka消息：</h1>
        #             <script>
        #                 var ws = new WebSocket("ws://'''+str(ip)+''':'''+str(portNum)+'''/"),
        #                     messages = document.createElement('ul');
        #                 ws.onmessage = function (event) {
        #                     var messages = document.getElementsByTagName('ul')[0],
        #                         message = document.createElement('li'),
        #                         content = document.createTextNode(event.data);
        #                     message.appendChild(content);
        #                     messages.appendChild(message);
        #                 };
        #                 document.body.appendChild(messages);
        #             </script>
        #         </body>
        #     </html>
        # '''
        # path=os.path.abspath(os.path.dirname(__file__))
        # f=open(path+os.sep+"static/kafkaWebClient"+str(portNum)+".html",'w+',encoding='utf-8')
        # f.write(htmlRaw)

        # import socket
        # ip = socket.gethostbyname(socket.gethostname())

        # put_link(name='点击kafka连接，开始接收消息',url=f"http://{ip}:8899/kafka?portNum={portNum}&ip={ip}")
        for one in continue_orderMsg(data['topic'], data['address'], data['filter'], data['pattern'], data['key']):
            for a in one:
                if a is not None:
                    put_text(f"{getDateTime()} : {data['topic']} --> {a}")
                # print(a)

def mqttListener():
    session.set_env(title='testTools')

    select_type = select("选择监听的mqtt服务:",["自定义服务","本地固定服务(待定)"])
    if select_type=="自定义服务":
        data = input_group("mqtt信息",[
            input("mqtt主机，必填", name="host"),
            input("mqtt端口，必填", name="port"),
            input("mqtt topic，必填",name="topic"),
            input("mqtt用户", name="user"),
            input("mqtt密码", name="passwd"),
            ])
        NormalMqttGetter(host=data['host'], port=int(data['port']), topic=data['topic']).getClient(func=put_text)
    elif select_type == "本地固定服务(待定)":
        put_text('未暴露')
    # NormalMqttGetter(host='127.0.0.1',port=1883,topic='fifa').getClient(func=put_text)

# @session.defer_call
# def clean():
#     path=os.path.abspath(".")
#     files=os.listdir(path)
#     for i,f in enumerate(files):
#         if f.find("kafkaWebClient")>=0:
#             print(i)
#             os.remove(path+os.sep+f)


# print(session.info['server_host'])


if __name__ == '__main__':
    start_server(myapp, port=8899)
    # mqttListener()
    # print(session.info["server_host"].split(":")[0])
    # kafkaListener()
    # myFackData()
