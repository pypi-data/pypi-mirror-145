# 基础数据rpc服务使用说明


## 安装

- pip install sense-data>=0.5.6

## 配置

- 在settings.ini中配置连接信息，比如：

```yaml
[data_rpc]
;host = 39.107.106.125
;port = 5001
host = cluster.sensedeal.wiki
port = 5100
```

## 使用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService() #调用SenseDataService方法
```

## SenseDataService方法说明：
    
- 1-实时股价，输入股票代码，输出最新的股票数据，数据形式为model

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_stock_price_tick(stock_code)
```

- 2-公司基本信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），'000045'或[]或['000045','000046']，
得到公司基本信息，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_company_info(stock_code)
```

- 3-公司别名，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到公司的别名，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_company_alias(stock_code)
```

- 4-每日股价，输入股票代码字符串，输出该股票历史信息，有三种查询方式，data_server.get_stock_price_day('000020')，
输出有史以来的所有数据，数据形式为model列表；data_server.get_stock_price_day('000020', '2018-12-2')，
输出指定某一天的数据，数据形式为model；data_server.get_stock_price_day('000020', '2018-12-2', '2019-1-4')，
输出指定时间段的数据，数据形式为model列表；

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_stock_price_day('000020')
res_1 = data_server.get_stock_price_day('000020', '2018-12-2')
res_2 = data_server.get_stock_price_day('000020', '2018-12-2', '2019-1-4')
```

- 5-子公司，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到子公司信息，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_subcompany(stock_code)
```


- 6-行业概念信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），
得到股票对应的行业概念信息，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_industry_concept(stock_code)
```


- 7-董监高信息，输入股票代码，允许的输入形式为股票字符串，或股票字符串+职位，输出懂事和监事的信息，每个人的数据形式是model，然后将对象存入列表中。

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_chairman_supervisor('000045') #输出该公司所有的董监高人员信息，
res_1 = data_server.get_chairman_supervisor('000045', '董事') #输出该公司所有的懂事人员信息
```

- 8-股东信息，输入股票代码，输出十大股东信息，每个股东的数据形式是model，然后将对象存入列表中

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_stockholder('000045')
```


- 9-返回前一个交易收盘日期，无参数，返回值形如'2019-1-28 03:00:00'的时间戳，是int型数据，李军用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_trade_date()
```


- 10-返回四大板块（深市主板、沪市主板、创业板和中小板）的股票涨跌幅，无参数，输出板块涨跌幅model，暂时不用了

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_market_rise_fall()
```


- 11-返回60左右个行业的股票涨跌幅数据，无参数，输出涨跌幅model，暂时不用了

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_industry_rise_fall()
```


- 12-返回股市中概念板块的涨跌幅数据，无参数，输出涨跌幅model，暂时不用了

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_concept_rise_fall()
```

- 13-给个实体名字（人名，子公司名）查询其在相关上市公司扮演的角色信息，输出形式为model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_entity_role('重庆富桂电子有限公司')
```


- 14-输入股票代码，返回风觅个股质押财务信息

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_financial_info(stock_code)
```


- 15-输入股票代码，返回总股本，子龙用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_total_shares(stock_code)
```

- 16-返回stock_codes中所有公司名，子龙用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_company_name()
```

- 17-输入文章标题，通过正则（新大洲控股|000571|新大洲A|新大洲），找到股票代码，广彬用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_title_code(stock_code)
```

- 18-输入股票代码，返回实控人信息，子龙用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_actual_control_person(stock_code)
```

- 19-输入实体识别的名字，返回该实体下对应的公司信息

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
entity_name = '石化油服'
data_server = SenseDataService()
res = data_server.get_origin_info_by_name(entity_name)

res_example = [
    {
        "other_name":"石化油服",
        "company_full_name":"中石化石油工程技术服务股份有限公司",
        "company_name":"中石化油服",
        "company_code":"10004315",
        "stock_code":"01033",
        "plate":"港股-H股"
    },
    {
        "other_name":"石化油服",
        "company_full_name":"中石化石油工程技术服务股份有限公司",
        "company_name":"石化油服",
        "company_code":"10004315",
        "stock_code":"600871",
        "plate":"上证主板-A股"
    }
]
```

- 20-输入股票代码，返回该股票代码对应的公司所有人员和相关公司与该公司的关系

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_company_role_info(stock_code)
res_example = {
    "stock_code":"600871",
    "plate":"上证主板-A股",
    "company_name":"石化油服",
    "company_full_name":"中石化石油工程技术服务股份有限公司",
    "person":{
        "刘中云":{
            "name":"刘中云",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "董事长",
                "法定代表人",
                "董事"
            ]
        },
        "魏然":{
            "name":"魏然",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非执行董事"
            ]
        }
    },
    "company":{
        "华美孚泰油气增产技术服务有限责任公司":{
            "name":"华美孚泰油气增产技术服务有限责任公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "合营企业",
                "合营企业"
            ]
        },
        "中石化石油工程技术服务股份有限公司":{
            "name":"中石化石油工程技术服务股份有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "上证主板-A股"
            ]
        }
    }
}
```


- 23-输入实体识别的名字，返回该实体下对应的多市场信息，广彬用的数据结构

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
entity_name = '石化油服'
data_server = SenseDataService()
res = data_server.get_multi_market_info_by_name(entity_name)

res_example = {
    "company_code":"10004315",
    "other_name":"石化油服",
    "company_full_name":"中石化石油工程技术服务股份有限公司",
    "plate":[
        "上证主板-A股",
        "港股-H股"
    ],
    "plate_value":{
        "港股-H股":{
            "stock_code":"01033",
            "company_name":"中石化油服"
        },
        "上证主板-A股":{
            "stock_code":"600871",
            "company_name":"石化油服"
        }
    }
}

```

- 24-输入实体识别的名字，返回该实体下对应的主市场信息，广彬用的数据结构

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
entity_name = '石化油服'
data_server = SenseDataService()
res = data_server.get_main_market_info_by_name(entity_name)

res_example = {'other_name': '石化油服', 'company_full_name': '中石化石油工程技术服务股份有限公司', 
'company_code': '10004315', 'stock_code': '600871', 'plate': '上证主板-A股', 
'company_name': '石化油服'}
```


- 25-输入股票代码，返回市场信息，广彬用的数据结构

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '600871'
data_server = SenseDataService()
res = data_server.get_market_info_by_stock_code(stock_code)

res_example = {'company_code': 10004315, 'company_full_name': '中石化石油工程技术服务股份有限公司', 
'company_name': '石化油服', 'plate': '上证主板-A股', 'stock_code': '600871', 
'time_stamp': 1572520699}
```








