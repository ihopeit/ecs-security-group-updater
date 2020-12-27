
# 自动化的阿里云安全组设置工具, 自动添加当前机器的外网 IP 到安全组

## 功能
1.自动删除指定端口、指定优先级(默认为2)的安全规则中的 IP
2.自动添加当前机器外网IP (当前网络的外网IP, 比如办公网络, 或者家里的网络) 到安全组

## 使用示例
例如, 允许 当前机器的外网 IP 访问 安全组的 80端口:
机器分组在北京, 

export port_range = '80/80'
export region_id = 'cn-beijing'
export security_group_id = "bj-xxxxxx"
export aliyun_ak = "xxxxx"
export aliyun_sk = "yyyyy"

python3 update_security_group.py