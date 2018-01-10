# 内网 dnsApi 说明文档

## 获取所有解析
获取方法

名称 | 说明
--- | ---
url | /list
请求方法 | GET

返回参数:
```
{
  "status": {
    "msg": "Get all records for Success.",
    "code": 1
  },
  "records": [
    {
      "status": "enable",         # 此记录的状态
      "domain": "7lk.com",        # 此记录的域
      "name": "git",              # 此记录的名称
      "value": "172.16.1.210",    # 此记录的解析ip
      "ttl": 60,                  # ttl 值
      "type": "A",                # 记录的类型
      "id": 45                    # 此记录的id
    },
    ... 
  ]
}
```
    
    


## 增加记录

名称 | 说明
--- | ---
请求地址 | /add/
编码 | UTF-8
请求方式 | POST
请求参数格式 | application/json

### 请求参数
|字段 | 类型 | 是否必填 | 描述|
--- | --- | --- | ---
name | string | 是 | 主机名，如www.7lk.com中的www
type | string | 是 | 解析类型 , A记录，MX记录等
value| string | 是 | 解析的ip地址
ttl  | int    | 是 | TTL 值

请求参数示例:

```
{
	"name": "yun.questionsa",  
	"type": "A",               
	"value": "192.168.1.133",  
	"ttl": 69                  
}

```

返回参数示例:
```
{
  "status": {
    "msg": "Successfully add yun.questionsa.7lk.com record.",  
    "code": 1                                                  
  },
  "record": {
    "id": 976,                  
    "name": "yun.questionsa"    
  }
}

```



## 删除记录
名称 | 说明
--- | ---
请求地址 | /del
编码 | UTF-8
请求方式 | POST
请求参数格式 | application/json
### 请求参数

字段 | 类型 | 是否必填 | 描述
--- | --- | --- | ---
id |int | 是 | list中获取的record对应的id

请求参数示例：
```
{
	"id":976
}
```

返回参数示例：
```
{
  "status": {
    "msg": "Successfully deleted  record 976.",
    "code": 1
  }
}
```


## 修改记录
名称 | 说明
--- | ---
请求地址 | /mod
编码 | UTF-8
请求方式 | POST
请求参数格式 | application/json

### 请求参数

字段 | 类型 | 是否必填 | 描述
--- | --- | --- | ---
id  | int    | 是 | 需要更新的记录id
name | string | 是 | name不允许修改
type | string | 是 |  原记录类型
value| string | 是 | 解析的ip地址
ttl  | int    | 是 | TTL 值

请求参数示例:
```
{
	"id" : 977,
	"name": "yun.questionsa",
	"type": "MX",
	"value": "192.168.1.134",
	"ttl": 600
}

```

返回参数示例:

```
{
  "status": {
    "msg": "Successfully updated yun.questionsa.7lk.com records.",
    "code": 1
  }
}
```


## 开启/禁用
名称 | 说明
--- | ---
请求地址 | /status
编码 | UTF-8
请求方式 | POST
请求参数格式 | application/json


### 请求参数

字段 | 类型 | 是否必填 | 描述
--- | --- | --- | ---
id  | int    | 是 | 需要更新的记录id
status | string | 是 | enable , disable


请求参数示例:

```
{
    "id" : 979,
    "status": "disable"
}

```

返回参数示例:
```
{
  "status": {
    "msg": "Successfully disable  record 979.",
    "code": 1
  },
  "record": {
    "status": "disable",
    "id": 979
  }
}

```
