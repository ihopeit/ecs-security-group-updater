
# 自动化的阿里云安全组设置工具, 自动添加当前机器的外网 IP 到安全组

## 功能
* 1.自动删除指定端口、指定优先级(默认为2)的安全规则中的 IP
* 2.自动添加当前机器外网IP (当前网络的外网IP, 比如办公网络, 或者家里的网络) 到安全组

## 场景
* 1.由于安全的原因, 服务仅允许来自办公网络的访问,比如公司内部的知识库, 内部的项目管理,OA系统等;
* 2.特定的代理服务器, 仅允许来自办公/家庭网络的机器访问, 而所在的网络的出口 IP 是自动获取的, 会自动更新;

## 使用示例
例如, 替换掉以下命令中的变量, 允许当前机器的外网 IP 访问 安全组的 80端口(机器分组在北京):

```
export port_range='80/80'
export region_id='cn-beijing'
export security_group_id="bj-xxxxxx"
export aliyun_ak="xxxxx"
export aliyun_sk="yyyyy"

python3 update_security_group.py
```