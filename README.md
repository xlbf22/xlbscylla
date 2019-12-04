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
![图片](data:image/gif;base64,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)
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

