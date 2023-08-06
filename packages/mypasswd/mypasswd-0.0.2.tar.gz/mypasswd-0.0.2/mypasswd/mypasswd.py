# -*- coding=utf-8

import sys
import logging
import fire
import stdiomask
import os
import requests
import urllib.parse

        # 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.ERROR, stream=sys.stdout)

secretctl_config_path = "/root/.secretctl.conf"

# 密码管理工具依赖的配置项
config_map = {
    "service_url":"",
    "aes_cos_path":"",
    "identity_cos_path":"",
    "secret_db_cos_path":""
}


def checkPrepare():
    if len(config_map['service_url']) == 0 or len(config_map['aes_cos_path']) == 0 or len(config_map['identity_cos_path']) == 0 or len(config_map['secret_db_cos_path']) == 0:
        print('使用前，请先使用secretctl config指令进行初始化！')   
        return False
    return True
    


def operateLocalConfig(new_config_map):
    config_file_exist = os.path.exists(secretctl_config_path)
    if config_file_exist:
        f = open(secretctl_config_path,"r")
        line = f.readline()
        while line:
            line = line.strip()
            if line.startswith("#") or len(line)==0:
                line = f.readline()
                continue
            
            items = line.split('=')
            config_key = items[0].strip()
            if config_key in config_map.keys() and len(items) == 2:
                config_map[config_key] = items[1].strip().replace("\n", "")
            line = f.readline()
        f.close()
    else:
        os.mknod(secretctl_config_path) 

    for key in new_config_map:
        if key in config_map.keys():
            config_map[key] = new_config_map[key]

    with open(secretctl_config_path,'w') as f:
        for key in config_map:
            f.write(key + "=" + config_map[key] + "\n")
        f.close()



def loadConfig(needLog):
    if needLog:
        print("|1.加载本地cos配置,本地路径：",secretctl_config_path,"            |")
    if os.path.exists(secretctl_config_path):
        f = open(secretctl_config_path,"r")
        line = f.readline()
        while line:
            line = line.strip()
            if line.startswith("#") or len(line)==0:
                line = f.readline()
                continue
            else:
                pairs = line.split("=")
                key = pairs[0].strip();
                if len(pairs) <= 1:
                    config_map[key] = ''
                else:
                    config_map[key] = pairs[1].strip()
                line = f.readline()
        f.close()
    else:
        print('请先使用secretctl init命令进行初始化！')


# secretctl工具初始化配置
def config(service_url,aes_cos_path,identity_cos_path,secret_db_cos_path):
    data = {
        "aes_cos_path":aes_cos_path,
        "identity_cos_path":identity_cos_path,
        "secret_db_cos_path":secret_db_cos_path
    }
    data['action'] = 'config'
    data['identity'] = ''
    response = requests.post(service_url,data)
    if response.status_code == 200:
        result = eval(response.text)
        if result['code'] == 0:
            data['service_url'] = service_url
            operateLocalConfig(data)  
            print('已完成secretctl本地初始化配置')
        else:
            print('配置失败，请确认COS中是否存在以下三个配置文件？')
            print('1.AES配置文件',aes_cos_path)
            print('2.身份认证文件',identity_cos_path)
            print('3.密码库文件：',secret_db_cos_path)
    else:
        print()
        print("服务地址无法正常连接，请确认[",service_url,"]是否有误？")



def post_with_dict_response(data):
    for idx in range(3):
        inputs = stdiomask.getpass(prompt='请输入身份认证码:')
        inputs = inputs.strip().replace("\n", "")
        data['identity_cos_path'] = config_map['identity_cos_path']
        data['input_identity'] = inputs
        if len(inputs) >0:
            response = requests.post(config_map['service_url'],data).text
            # print('response=',response)
            result = eval(response)
            if result['code'] == 0:
                print('认证成功')
                print('---------返回值---------')
                return [True,result]
        print('身份认证错误!')
    print('认证次数超限，退出')
    return [False,{}]

    


def info():
    if checkPrepare():
        print('----------------------------secretctl配置文件信息--------------------------------')
        print('1.本地secretctl工具配置文件地址：',secretctl_config_path)
        print('2.远程AES配置文件COS地址：',config_map['aes_cos_path'])    
        print('3.远程身份认证配置文件COS地址：',config_map['identity_cos_path'])    
        print('4.远程密码库COS文件地址：',config_map['secret_db_cos_path']) 
        print('5.远程服务器地址：',config_map['service_url'])
        print('---------------------------------------------------------------------------------')   



def listSecret():
    if checkPrepare():
        secretCosPath = config_map['secret_db_cos_path']
        data = {'secret_db_cos_path':config_map['secret_db_cos_path'],'action':'list'}
        result = post_with_dict_response(data)
        if result[0] and result[1]['code'] == 0:
            resultData = result[1]['data']
            print('ID|资源名称|账户|密码|备注')
            index = len(resultData)
            for line in resultData:
                index -= 1
                line = urllib.parse.unquote(line)
                print(line)
                if index > 0:
                    print(' ')


def search(feature):
    if checkPrepare():
        secretCosPath = config_map['secret_db_cos_path']
        data = {'secret_db_cos_path':config_map['secret_db_cos_path'],'action':'search'}
        result = post_with_dict_response(data)
        if result[0] and result[1]['code'] == 0:
            resultData = result[1]['data']
            print('ID|资源名称|账户|密码|备注')
            for line in resultData:
                if str(feature).upper() in line.upper():
                    print(line)



def addSecret(resource_name,account,password,*remark):
    if checkPrepare():
        remark2 = '-'
        if len(remark) >=1:
            remark2 = remark[0]
        
        data = {
            'secret_db_cos_path':config_map['secret_db_cos_path'],
            'action':'add',
            'resource_name':resource_name,
            'account':account,
            'password':password,
            'remark':remark2,
        }
        result = post_with_dict_response(data)
        if result[0] and result[1]['code'] == 0:
            print("[",resource_name,']添加成功')


def updateSecret(id,password):
    if checkPrepare():
        secretCosPath = config_map['secret_db_cos_path']
        data = {'secret_db_cos_path':config_map['secret_db_cos_path'],'action':'update','id':str(id),'password':password}
        result = post_with_dict_response(data)
        if result[0] and result[1]['code'] == 0:
            print('更新成功')
        else:
            print('ID[',id,']不存在，无法更新')



def getSecret(id):
    if checkPrepare():
        secretCosPath = config_map['secret_db_cos_path']
        data = {'secret_db_cos_path':config_map['secret_db_cos_path'],'action':'get','id':str(id)}
        result = post_with_dict_response(data)
        if result[0] and result[1]['code'] == 0:
            item = result[1]['data']
            print('ID|资源名称|账户|密码|备注')
            print("原密文数据：",item['encrypt_info'])
            print("解密后数据：")
            print("     序  号：",item['id'])
            print("     资源名：",item['resource_name'])
            print("     源账户：",item['account'])
            print("     源密码：",item['password'])
            print("     备  注：",item['remark'])
        else:
            print('资源ID[',id,']不存在')


if __name__ == '__main__':

    loadConfig(False)

    fire.Fire({
        'config':config,
        'add':addSecret,
        'update':updateSecret,
        'get': getSecret,
        'search':search,
        'list': listSecret,
        'info':info
    })
