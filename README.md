![banner_scylla](https://user-images.githubusercontent.com/2396817/40580477-f15a15b8-6136-11e8-9f4b-1f012e90712c.png)
===

Scylla 是一款高质量的免费代理 IP 池工具，仅支持 Python 3.6。特性如下：
features:

- 自动化的代理 IP 爬取与验证
- 易用的 JSON API
- 简单但美观的 web 用户界面，基于 TypeScript 和 React（例如，代理的地理分布）
- 最少仅用 **一条命令** 即可启动
- Simple HTTP 转发代理服务
- 最少仅用一行代码即可与 [Scrapy] 和 [requests] 进行集成
- 无头浏览器（headless browser crawling）爬虫

对于偏好中文的用户，请阅读 [中文文档](https://scylla.wildcat.io/zh/latest/)。For those who prefer to use Chinese, please read the [Chinese Documentation](https://scylla.wildcat.io/zh/latest/).

快速开始
===========

安装
------------

### Docker 安装（推荐）

```bash
docker run -d -p 8899:8899 -p 8081:8081 -v /var/www/scylla:/var/www/scylla --name scylla wildcat/scylla:latest
```

### 使用 pip 直接安装

```bash
pip install scylla
scylla --help
scylla # Run the crawler and web server for JSON API
```

### 从源代码安装

```bash
git clone https://github.com/imWildCat/scylla.git
cd scylla

pip install -r requirements.txt

npm install # or yarn install
make assets-build

python -m scylla
```

##### Windows用户在安装 sanic 时假如遇到 uvloop does not support Windows at the moment:

```bash
export SANIC_NO_UVLOOP=true
export SANIC_NO_UJSON=true
pip3 install sanic
```
如果仍是失败，你需要从源码安装sanic。

使用
-----
这里以服务运行在本地（`localhost`）为例，使用口号 `8899`。 注意：首次运行本项目时，您可能需要等待 1～2 分钟以爬取一定量的代理 IP。

### JSON API

#### 代理 IP 列表

```bash
http://localhost:8899/api/v1/proxies
```

可选 URL 参数：

| 参数        |  默认值        | 说明                                                         |
| ----------- | ------------- | ------------------------------------------------------------ |
| `page`      | `1`           | The page number                                              |
| `limit`     | `20`          | The number of proxies shown on each page                     |
| `anonymous` | `any`         | Show anonymous proxies or not. Possible values：`true`, only anonymous proxies; `false`, only transparent proxies |
| `https`     | `any`         | Show HTTPS proxies or not. Possible values：`true`, only HTTPS proxies; `false`, only HTTP proxies |
| `countries` | None          | Filter proxies for specific countries. Format example: ``US``, or multi-countries: `US,GB` |

结果样例：

```json
{
    "proxies": [{
        "id": 599,
        "ip": "91.229.222.163",
        "port": 53281,
        "is_valid": true,
        "created_at": 1527590947,
        "updated_at": 1527593751,
        "latency": 23.0,
        "stability": 0.1,
        "is_anonymous": true,
        "is_https": true,
        "attempts": 1,
        "https_attempts": 0,
        "location": "54.0451,-0.8053",
        "organization": "AS57099 Boundless Networks Limited",
        "region": "England",
        "country": "GB",
        "city": "Malton"
    }, {
        "id": 75,
        "ip": "75.151.213.85",
        "port": 8080,
        "is_valid": true,
        "created_at": 1527590676,
        "updated_at": 1527593702,
        "latency": 268.0,
        "stability": 0.3,
        "is_anonymous": true,
        "is_https": true,
        "attempts": 1,
        "https_attempts": 0,
        "location": "32.3706,-90.1755",
        "organization": "AS7922 Comcast Cable Communications, LLC",
        "region": "Mississippi",
        "country": "US",
        "city": "Jackson"
    },
    ...
    ],
    "count": 1025,
    "per_page": 20,
    "page": 1,
    "total_page": 52
}
```

#### 系统统计

```bash
http://localhost:8899/api/v1/stats
```

结果样例：

```json
{
    "median": 181.2566407083,
    "valid_count": 1780,
    "total_count": 9528,
    "mean": 174.3290085201
}
```

### HTTP 正向代理服务器

默认情况下，Scylla 会在端口 `8081` 启动一个 HTTP 正向代理服务器（Forward Proxy Server）。 这个服务器会从数据库中选择一个刚更新过的代理，并将其用作正向代理。 每当发出 HTTP 请求时，代理服务器将随机选择一个代理。

注意：目前不支持 HTTPS 请求。

使用此代理服务器的 “`curl`” 示例如下：
```bash
curl http://api.ipify.org -x http://127.0.0.1:8081
```

你也可以在 [requests][] 中使用这个特性：

```python
requests.get('http://api.ipify.org', proxies={'http': 'http://127.0.0.1:8081'})
```

### Web 界面
打开 `http://localhost:8899` 即可访问本项目的 Web 界面。

#### 代理 IP 列表

```
http://localhost:8899/
```

截图：
![screenshot-proxy-list](https://user-images.githubusercontent.com/2396817/40653600-946eae6e-6333-11e8-8bbd-9d2f347c5461.png)

#### 代理 IP 全球分布

```
http://localhost:8899/#/geo
```

截图：

![screenshot-geo-distribution](https://user-images.githubusercontent.com/2396817/40653599-9458b6b8-6333-11e8-8e6e-1d90271fc083.png)

API 文档
=================
请阅读 [模块索引](https://scylla.wildcat.io/en/latest/py-modindex.html)。

开发路线图
=======
请查看 [Projects](https://github.com/imWildCat/scylla/projects)。

测试
=======

如需在本地运行测试，命令如下：
```bash
pip install -r tests/requirements-test.txt
pytest tests/
```

项目命名
======================
[Scylla](http://prisonbreak.wikia.com/wiki/Scylla)，或被称为“锡拉”（中文里），源自于美剧[《越狱》](https://en.wikipedia.org/wiki/Prison_Break)中的一组记忆芯片的名字。本项目以此命名，是为了致敬这部美剧。

捐助
========

[捐助Scylla的原作者](https://github.com/imWildCat/scylla#paypal)

协议
=======
Apache License 2.0. 如需了解详情，请阅读 [LICENSE](https://github.com/imWildCat/scylla/blob/master/LICENSE) 这个文件。

