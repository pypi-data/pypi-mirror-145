#!/anaconda3/envs/xxx/bin python3.7
# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: main.py
# @Author: oupeng
# @Time: 9月 23, 2021
# ---
import json
import time

from fabric import Connection,SerialGroup
from loguru import logger
from requests import session
from copy import deepcopy
import csv
logger.add('执行日志.txt',rotation="10MB",encoding='utf-8',enqueue=True)
import pytest

class RemoteRunner(object):
    '''
    run command in remote host
    '''
    def __init__(self, host, port, user, passwd):
        '''

        :param host:
        :param port:
        :param user:
        :param passwd:
        result will be store in instance res variables
        '''
        self.host = host
        self.port = port
        self.user = user
        self.passwd = {"password": passwd}
        self.conn = Connection(host=self.host, user=self.user, port=self.port, connect_kwargs=self.passwd)
        self.res=""
        self.uid=None
        self.containerList=[]
        self.commandList=[]

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.conn.close()

    def upload_file(self, localFilePath, remoteFilePath):
        '''
        :param localFilePath:
        :param remoteFilePath:
        :return:
        '''
        # logger.info(f"localFilePath: {localFilePath}")
        # logger.info(f"remoteFilePath: {remoteFilePath}")
        logger.info(f"localFilePath: {localFilePath}, remoteFilePath: {remoteFilePath}")
        self.conn.put(local=localFilePath, remote=remoteFilePath)
        return self

    def download_file(self, localFilePath, remoteFilePath):
        '''

        :param localFilePath:
        :param remoteFilePath:
        :return:
        '''
        logger.info(f"localFilePath: {localFilePath}, remoteFilePath: {remoteFilePath}")
        # logger.info(f"remoteFilePath: {remoteFilePath}")
        self.conn.get(remote=remoteFilePath, local=localFilePath)
        return self


    def get_chaos_id(self):
        if "success" in self.res.stdout.strip():
            id=json.loads(self.res.stdout.strip())['result']
            print(f"###############{id}")
            self.uid=id
        return self

    def exec_cmd(self, cmd):
        '''
        :param cmd: command in running on the host
        :return:
        '''
        logger.info(f"exec cmd: {cmd}")
        res = self.conn.run(cmd)
        # logger.info(f'cmd stdout is: {res.stdout.strip()}')
        # logger.error(f'cmd stdout is: {res.stderr.strip()}')
        self.res=res
        self.get_chaos_id()
        return self

    def exec_on_multi(self,*hosts,cmd):
        '''

        :param hosts: host list,contain lots of host
        :param cmd: command in running on the host
        :return:
        '''
        logger.info(f"hosts: {hosts}")
        logger.info(f"multi cmd: {cmd}")
        res=SerialGroup(hosts).run(cmd)
        # logger.info(f'cmd stdout is: {res.stdout.strip()}')
        # logger.error(f'cmd stdout is: {res.stderr.strip()}')
        self.res=res
        self.get_chaos_id()
        return self

    def exec_check_by_cmd(self,cmd,expect):
        '''

        :param cmd: command
        :param expect: command expect str
        :return:
        '''
        logger.info(f"check cmd is: {cmd}")
        self.exec_cmd(cmd)
        stdout = self.res.stdout.strip()
        logger.info(f"checking: result is: {stdout}, expect is: {expect}")
        assert expect in stdout
        # if expect in stdout:
        #     return True
        # else:
        #     return False

    def exec_check_contain(self,expect):
        '''
        :param expect: expect str
        :return:
        '''
        stdout=self.res.stdout.strip()
        logger.info(f"checking: result is: {stdout}, expect is: {expect}")
        assert expect in stdout
        # if expect in stdout:
        #     # logger.info(f"expect: {expect}")
        #     # logger.info(f"stdout: {stdout}")
        #     return True
        # return False

    def exec_check_equal(self,expect):
        '''

        :param expect: expect str, exactly same
        :return:
        '''
        stdout=self.res.stdout.strip()
        logger.info(f"checking: result is: {stdout}, expect is: {expect}")
        assert expect==stdout
        # if expect == stdout:
        #     # logger.info(f"expect: {expect}")
        #     # logger.info(f"stdout: {stdout}")
        #     return True
        # return False

    def exec_check_request_alive(self,url,method,data="",json="",*kwargs):
        '''
        check service is available using return code 200
        :param url:
        :param method:
        :param data:
        :param json:
        :param kwargs:
        :return:
        '''
        resp=None
        if method.lower() == 'post':
            resp = session().post(url, data, json)
        elif method.lower() == 'get':
            resp = session().post(url, data, json)
        assert resp.status_code==200
        # if resp.status_code==200:
        #     return True
        # else:
        #     return False


    def exec_check_request_response(self,url,method,data="",json="",expect="",*kwargs):
        '''
        check service ok, using response code by contain
        :param url:
        :param method:
        :param data:
        :param json:
        :param expect:
        :param kwargs:
        :return:
        '''
        resp = None
        if method.lower() == 'post':
            resp = session().post(url, data, json)
        elif method.lower() == 'get':
            resp = session().post(url, data, json)
        assert expect in resp.text 
        # if expect in resp.text:
        #     return True
        # else:
        #     return False

    def prepare_blade(self):
        '''
        :return: blade binaries will be placed in /opt/chaos/chaosblade-1.2.0/, and add blade in path
        '''
        self.exec_cmd("cd /opt;rm -rf chaos*")
        self.upload_file("chaosblade.tar.gz", "/opt")
        self.exec_cmd('cd /opt; mkdir chaos;tar -xzvf chaosblade.tar.gz -C ./chaos;')
        self.exec_cmd('echo "export PATH=$PATH:/opt/chaos/chaosblade-1.2.0/">>~/.bashrc')
        return self

    def get_docker_id(self):
        '''
        get docker id
        :return:
        '''
        res=self.conn.run("docker ps|awk '{if (NR>2) {print $1}}'")
        self.containerList=deepcopy(res.stdout.strip().split('\n'))
        logger.info(f"container list is: {self.containerList}")
        return self
        # print(type(self.containerList))
        # return self.containerList

    def run_docker_cmd_by_dockerName(self,cmd,uniq_docker_name):
        '''
        run docker command by name
        :param cmd:
        :param uniq_docker_name:
        :return:
        '''
        docker_id=self.conn.run("docker ps|grep "+uniq_docker_name+"|awk '{print $1}'").stdout.strip()
        logger.info(f"docker_id is: {docker_id}")
        logger.info(f"docker command: {cmd} --container-id {docker_id} will be execute")
        self.res=self.conn.run(f"{cmd} --container-id {docker_id}")
        self.get_chaos_id()
        return self

    def run_docker_cmd_by_dockerId(self,cmd,docker_id):
        '''
        run docker command by id
        :param cmd:
        :param docker_id:
        :return:
        '''
        # docker_id=self.conn.run("docker ps|grep "+uniq_docker_name+"|awk '{print $1}'").stdout.strip()
        logger.info(f"docker command: {cmd} --container-id {docker_id} will be execute")
        self.res=self.conn.run(f"{cmd} --container-id {docker_id}")
        self.get_chaos_id()
        return self

    def run_docker_cmd(self,cmd):
        '''
        run docker commmand directly by writed case
        :param cmd:
        :return:
        '''
        # docker_id=self.conn.run("docker ps|grep "+uniq_docker_name+"|awk '{print $1}'").stdout.strip()
        logger.info(f"docker command: {cmd} will be execute")
        self.res=self.conn.run(f"{cmd}")
        self.get_chaos_id()
        return self

    def destroy_chaos(self):
        logger.info(f"id: {self.uid} will destroy")
        self.conn.run(f"blade destroy {self.uid}")

    # def __getattribute__(self, *args, **kwargs):
    #     # print(self.__class__.__name__)
    #     # print(f'args: {args}')
    #     # print(f'kwargs: {kwargs}')
    #     if args[0] == 'executeCmd':
    #         print("#"*20)
    #     return object.__getattribute__(self, *args, **kwargs)

def requestStringParser(url_str,loginRequire="no",checkResponse="no"):
    '''
     url_str=http://mobile.abc.org/sfsf~post~urlparams~jsonparms~headers
     http://http://192.168.118.168:21368/api-dev/terminus-security/account/login~post~ ~{"loginName":"$loginName","password":"$loginPass","businessCode":"terminus","loginType":"ACCOUNT","ticket":"7c9db59cdc189b5d56ba21bf20e355fcc30c0049","rightCode":"dfdf"}~{"Content-Type": "application/json;charset=UTF-8"}
    '''
    url,method,params,jsonstr,headers=url_str.split('~')
    logger.info(f'url is {url}')
    logger.info(f'method is {method}')
    logger.info(f'params is {params}')
    logger.info(f'jsonstr is {jsonstr}')
    logger.info(f'headers is {headers}')
    requestFuncStr=f"session().{method}(url='{url}',data={params},json={jsonstr})"
    session().request(url=url,method=method,params=params,data=jsonstr,headers=json.loads(headers))
    print(requestFuncStr)

def running():
    logger.info(f'--' * 100)
    f=open("config2.json",encoding='utf-8')
    jf=json.load(f)
    for one in jf['data']:
        # print(one)
    # f = open("cmdCase.csv")
    # for one in csv.DictReader(f):
        logger.info(f'@@@data is@@@\n:{one}')
        if one['flag'] == "true":
            logger.info(f'+++++++Executing is+++++++ \n:{one}')
            if one['httpCheck'] == "":
                if one['dockerName'] != "":
                    r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'], passwd=one['passwd'])
                    r.run_docker_cmd_by_dockerName(one['execCommand'], one['dockerName']).exec_check_contain(
                        one['execCommandExpect'])
                    time.sleep(2)
                    r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
                    time.sleep(10)
                    r.destroy_chaos()
                else:
                    if "docker" in one['execCommand']:
                        r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'],
                                         passwd=one['passwd'])
                        r.run_docker_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
                        time.sleep(2)
                        r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
                        time.sleep(10)
                        r.destroy_chaos()
                    else:
                        r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'],
                                         passwd=one['passwd'])
                        r.exec_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
                        time.sleep(2)
                        r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
                        time.sleep(10)
                        r.destroy_chaos()


def blade_run():
    logger.info(f'--' * 100)
    f = open("cmdCase.csv")
    for one in csv.DictReader(f):
        logger.info(f'@@@data is@@@\n:{one}')
        if one['flag'] == "true":
            logger.info(f'+++++++Executing is+++++++ \n:{one}')
            if one['httpCheck'] == "":
                if one['dockerName'] != "":
                    r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'], passwd=one['passwd'])
                    r.run_docker_cmd_by_dockerName(one['execCommand'], one['dockerName']).exec_check_contain(
                        one['execCommandExpect'])
                    time.sleep(2)
                    r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
                    time.sleep(10)
                    r.destroy_chaos()
                else:
                    if "docker" in one['execCommand']:
                        r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'], passwd=one['passwd'])
                        r.run_docker_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
                        time.sleep(2)
                        r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
                        time.sleep(10)
                        r.destroy_chaos()
                    else:
                        r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'], passwd=one['passwd'])
                        r.exec_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
                        time.sleep(2)
                        r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
                        time.sleep(10)
                        r.destroy_chaos()
            # else:
            #     if one['dockerName'] != "":
            #         r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'], passwd=one['passwd'])
            #         r.run_docker_cmd_by_dockerName(one['execCommand'], one['dockerName']).exec_check_contain(
            #             one['execCommandExpect'])
            #         time.sleep(2)
            #         r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
            #         time.sleep(10)
            #         r.destroy_chaos()
            #     else:
            #         if "docker" in one['execCommand']:
            #             r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'], passwd=one['passwd'])
            #             r.run_docker_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
            #             time.sleep(2)
            #             r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
            #             time.sleep(10)
            #             r.destroy_chaos()
            #         else:
            #             r = RemoteRunner(host=one['host'], port=int(one['port']), user=one['user'], passwd=one['passwd'])
            #             r.exec_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
            #             time.sleep(2)
            #             r.exec_check_by_cmd(one['checkCommand'], one['exepect'])
            #             time.sleep(10)
            #             r.destroy_chaos()

        logger.info(f'+++++++Executing Done+++++++\n\n\n')

if __name__ == "__main__":
    # blade_run()
    # requestStringParser('http://192.168.118.168:xxx/api-dev/terminus-security/account/login~post~ ~{"loginName":"admin","password":"admin","businessCode":"xxx","loginType":"ACCOUNT","ticket":"7c9db59cdc189b5d56ba21bf20e355fsssssss","rightCode":"ssssss"}~{"Content-Type": "application/json;charset=UTF-8"}')
    running()