# 自动添加当前的动态ip, 到阿里云 ECS 安全组

#coding=utf-8
import json
import re
import os
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# -*- coding: utf8 -*-
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupAttributeRequest

description = "auto added"
port_range = os.environ.get('port_range')
region_id = os.environ.get('region_id')
security_group_id = os.environ.get("security_group_id")
aliyun_ak = os.environ.get("aliyun_ak")
aliyun_sk = os.environ.get("aliyun_sk")
default_priority = 2

if not security_group_id or not aliyun_ak or not aliyun_sk:
    print("请确保在环境变量中设置安全组 ID, 阿里云 ak/sk, region_id, port_range, 再运行命令")
    exit(-1)

client = AcsClient(
    aliyun_ak,  # 此处填写你刚才创建的RAM子账号的AccessKeyId
    aliyun_sk,  # 此处填写你刚才创建的RAM子账号的AccessKeySecret
    region_id  # 此处填写你要管理的区域
)

#通过ip.cn网站获取外网ip地址
def get_now_ip():
    url="https://ifconfig.me"
    headers = { 'User-Agent': "curl/10.0","Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    response = requests.get(url,headers=headers)
    now_ip = response.content.decode("utf-8")
    print("current ip address:%s" % (now_ip))
    return (now_ip)

#根据ip和port移除规则
def remove_ip(securityGroupId, sourceCidrIp, portRange):
    request.set_action_name('RevokeSecurityGroup')
    request.add_query_param('RegionId', region_id)
    request.add_query_param('SecurityGroupId', securityGroupId)
    request.add_query_param('SourceCidrIp', sourceCidrIp)
    request.add_query_param('PortRange', portRange)
    request.add_query_param('IpProtocol', 'tcp')
    request.add_query_param('NicType', 'intranet')
    response = client.do_action_with_exception(request)

#添加指定的IP地址到安全组中:
def add_ip(securityGroupId, sourceCidrIp, portRange, priority):
    request.set_action_name('AuthorizeSecurityGroup')
    request.add_query_param('RegionId', region_id)
    request.add_query_param('SecurityGroupId', securityGroupId)
    request.add_query_param('SourceCidrIp', sourceCidrIp)
    request.add_query_param('PortRange', portRange)
    request.add_query_param('Priority', priority)
    request.add_query_param('IpProtocol', 'tcp')
    request.add_query_param('NicType', 'intranet')
    request.add_query_param("Description", description)
    response = client.do_action_with_exception(request)

print("1.query current security group...")
request = DescribeSecurityGroupAttributeRequest.DescribeSecurityGroupAttributeRequest()
request.set_SecurityGroupId(security_group_id)


response = client.do_action_with_exception(request)
responsepermissions = json.loads(response)
permissions = responsepermissions.get("Permissions").get("Permission")
print(response.decode('utf-8'))

vpcId = responsepermissions.get("VpcId")
securityGroupNameLocal = responsepermissions.get("SecurityGroupName")
securityGroupId = responsepermissions.get("SecurityGroupId")

current_ip_in_perm_list = False

print("2.detect current ip address...")
cur_ip = get_now_ip()

print("3.remove existed priority group with specified priority...")
for perm in permissions:
    
    ## 找到 指定端口, Priority = 2 的安全规则:
    if port_range == perm.get("PortRange")  and perm.get("Priority") == 2:
        # Policy:Accept SourceCidrIp:183.128.0.1/16 NicType:intranet PortRange:9100/9100 Desc:tele
        print("Policy:%s SourceCidrIp:%s NicType:%s PortRange:%s Desc:%s" % 
          (perm.get("Policy"), perm.get("SourceCidrIp"), perm.get("NicType"), 
          perm.get("PortRange"), perm.get("Description") ))
        if cur_ip != perm.get("SourceCidrIp"):
            remove_ip(securityGroupId, perm.get("SourceCidrIp"), port_range)
        else:
            current_ip_in_perm_list = True

print("current ip:%s, current ip in permission list:%s" % (cur_ip, current_ip_in_perm_list) )

print("4.add current ip address to permission list")
if not current_ip_in_perm_list:
    # add to permission list:
    add_ip(securityGroupId, cur_ip, port_range, default_priority)