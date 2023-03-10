



# 基础知识

## Django入门与进阶
### Django基本使用
#### Django是什么
```text
Django是python的一个主流web框架，提供一站式解决方案，开发成本低，内建ORM、数据管理后台、登录认证、表单、RESTAPI等功能，适合中大型项目开发

其他web框架
·flask（轻量级）
·Tornado（异步）

官网：https://www.djangoproject.com
```

#### 开发环境准备

| 软件         | 安装方式                      |
|------------|---------------------------|
| Django3.0  | pip install django==3.0.5 |
| pycharm社区版 | 官方网站下载安装                  |
| pymysql    | pip install pymysql       |
| mysql5.7   | docker-compose.yaml方式安装   |
| python3.8  | 官方网站下载安装                  |

#### 创建项目
```text
1、创建项目
django-admin startprojet youproject
2、创建应用
python manage.py startapp youapp
3、运行项目
python manage.py runserver 0.0.0.0:8888
```

#### 牛刀小试

```python
# 安装Django
C:\Users\Administrator\PycharmProjects\牛刀小试\venv\Scripts\pip.exe install Django
# 创建项目
PS C:\Users\Administrator\PycharmProjects\牛刀小试> C:\Users\Administrator\PycharmProjects\牛刀小试\venv\Scripts\django-admin.exe startproject app .
# 创建应用
PS C:\Users\Administrator\PycharmProjects\牛刀小试> C:\Users\Administrator\PycharmProjects\牛刀小试\venv\Scripts\python.exe .\manage.py startapp myapp
# 编写urls.py
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index)
]
# 添加试图
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("首页")

# 运行项目
C:\Users\Administrator\PycharmProjects\牛刀小试\venv\Scripts\python.exe .\manage.py runserver 127.0.0.1:80
        
```

![image-20230217204553810](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230217204553810.png)



#### 牛刀小试第二个页面：网页展示日志文件

```python
# 设置模板路径（settings.py）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],

# 添加url路由(app/urls.py)
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('logs/', views.logs),
]
# 添加试图（myapp/views.py）
def logs(request):
    import os
    # 获取当前文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(current_dir + "\\access.log") as f:
        result = f.read()
    return render(request, "logs.html", {"result": result})

# 创建HTML模板（项目路径下新建templates目录，该目录下新建logs.html）
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>日志</title>
</head>
<body>
<h1>Nginx访问日志</h1>
<pre>{{ result }}</pre>
</body>
</html>
# 将access.log放到myapp中
```

![image-20230217214027135](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230217214027135.png)

![image-20230217211524349](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230217211524349.png)

![image-20230217211048903](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230217211048903.png)

优化前端展示

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>日志</title>
</head>
<body>
<h1>Nginx访问日志</h1>
<div style="background-color: black; color: white">
    <span style="font-size: 15px"><pre>{{ result }}</pre></span>
</div>
</body>
</html>
```

![image-20230217212357714](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230217212357714.png)



#### Django工作流程

![1940786-20200606155652721-1371452217](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\1940786-20200606155652721-1371452217-1676640850195.png)

### Django路由系统



#### URL路由系统是什么

```text
简而言之，路由系统就是URL路径和视图函数的一个对应关系，也可以称为转发器。
```

![image-20230217215008860](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230217215008860.png)

#### URL配置

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('logs/', views.logs),
]
```

参数解释

```text
urlpatterns：一个列表，每一个path()函数是一个元素，对应一个视图
参数：
	• regex：一个字符串或者正则表达式，匹配URL
	• view：对应一个函数视图或者类视图（as_view()的结果），必须返回一个HttpResponse对象，Django将这个对象转换成一个HTTP响应
	• kwargs：可选，字典形式数据传递给对应视图
	• name：可选，URL名称
```

示例

```python
# 创建urls.py(在myapp目录下创建)
from django.urls import path
from myapp import views
urlpatterns = [
    path('hello/', views.hello),
    path('logs/', views.logs),
]

# 创建hello函数（myapp/views.py）
def hello(request):
    return HttpResponse("Hello Django")

# 项目路径下urls.py
from django.contrib import admin
from django.urls import path, include
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('logs/', views.logs),
    path('myapp/', include('myapp.urls')),
]
# 访问 http://127.0.0.1/myapp/hello/
```

![image-20230217215744165](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230217215744165.png)

#### URL正则表达式

URL路径也可以使用正则表达式匹配，re_path()替代path()

示例：博客文章归档访问形式

```python
# urls.py
from django.urls import re_path
from devops import views
urlpatterns = [
    re_path('articles/2023/$', views.specified_2023),
    re_path('^articles/([0-9]{4})/$', views.year_archive),
    re_path('^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    re_path('^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
# views.py
def specified_2023(request):
	return HttpResponse("指定2023年 文章列表")
def year_archive(request, year):
	return HttpResponse("%s年 文章列表" % year)
def month_archive(request, year, month):
	return HttpResponse("%s年/%s月 文章列表" % (year, month))
def article_detail(request, year, month, id):
	return HttpResponse("%s年/%s月 文章ID: %s" %(year, month, id))

```



#### URL名称

```html
之前
<a href="/hello">你好</a>
之后
<a href="{% url 'hello' %}">你好</a>
```




### Django试图

#### Django内置函数

![image-20230219182514216](C:\Users\Administrator\PycharmProjects\k8s-dashboard\img\image-20230219182514216.png)

#### HttpRequest对象

##### 常用属性

Django会建立一个包含请求源数据的HttpRequest对象，当Django加载对应的视图时，HttpRequest 对象将作为函数视图的第一个参数（request），每个视图负责返回一个HttpResponse对象。

例如：

```python
def index(request):
    return HttpResponse("首页")
```



| 属性            | 描述                                                    |
| --------------- | ------------------------------------------------------- |
| request.scheme  | 表示请求协议的字符串（http或https）                     |
| request.body    | 原始HTTP请求正文                                        |
| request.path    | 一个字符串，请求页面的完整路径，不包含域名              |
| request.method  | 一个字符串，请求的HTTP方法，比如GET/POST等              |
| request.GET     | GET请求所有参数，返回QueryDict类型，类似于字典          |
| request.POST    | POST请求所有参数，返回QueryDict类型                     |
| request.COOKIES | 以字典格式返回Cookie                                    |
| request.session | 可读写的类似于字典的对象，表示当前的会话                |
| request.FILES   | 所有上传的文件                                          |
| request.META    | 返回字典，包含所有的HTTP请求头。比如客户端IP，Referer等 |

##### 常用方法

| 方法                    | 描述                                        |
| ----------------------- | ------------------------------------------- |
| request.get_host()      | 服务器主机地址和端口                        |
| request.get_port()      | 服务器端口                                  |
| request.get_full_path() | 请求页面完整路径和查询参数                  |
| request.get_raw_uri()   | 请求页面URL所有信息，包括主机名、路径和参数 |

##### 接收URL参数

URL参数形式：http://www.aliangedu.cn/demo/?id=1&value=100

```python
def url_args(request):
    args1 = request.GET['a']
    args2 = request.GET['b']
return HttpResponse(int(args1) + int(args2))
```

##### QueryDict对象

request.GET和request.POST返回的都是一个QueryDict对象，类似于字典。

```python
def index(request):
    req = request.GET
    print(type(req))
return HttpResponse("首页")
```

| 方法                     | 描述                                          |
| ------------------------ | --------------------------------------------- |
| req.get(key,default)     | 返回key的值，如果key不存在返回default         |
| req.items()              | 返回迭代器，键值                              |
| req.values()             | 返回迭代器，所有键的值                        |
| req.keys()               | 返回所有键                                    |
| req.getlist(key,deafult) | 返回key的值作为列表，如果key不存在返回default |
| req.lists()              | 返回迭代器，所有键的值作为列表                |
| req.dict()               | 返回字典                                      |

##### 示例

一：表单GET提交搜索页面

二：表单POST提交登录页面

三：上传文件，例如修改头像



#### HttpResponse函数

HttpResponse函数：给浏览器返回数据。 

语法：HTTPResponse(content=响应体，content_type=响应体数据类型，status=状态码)

示例：返回HTML内容

```python
from django.http import HttpResponse
def hello(request):
    return HttpResponse("<h1>Hello Django!</h1>")
```

示例：设置响应头

```python
from django.http import HttpResponse
def hello(request):
	res = HttpResponse("Hello APP!")
    res['name'] = '测试'
    res.status_code = 302
```



##### render函数

render指定模板，返回一个渲染后的HttpResponse对象。 

语法：render(request, template_name, context=None, content_type=None, status=None, using=None)

- request：固定参数，django封装的请求
-  template_name：返回html模板 
-  context：传入模板中的内容，用于渲染模板，默认空字典

示例：

```python
from django.shortcuts import render
from datetime import datetime
def current_datetime(request):
    now = datetime.now()
    return render(request, 'demo/html', {'datetime': now})
```



##### redirect函数

redirect函数：重定向，发起第二次请求 语法：redirect(to, *args, **kwargs)

参数可以是： 

- 一个视图 
- 一个绝对的或者相对的URL 
- 一个模型，对象是重定向的URL

示例：

```python
from django.shortcuts import redirect
def test_redirect(request):
    return redirect('https://www.baidu.com')
```

##### StreamingHttpResponse函数

StreamingHttpResponse函数：流式响应可迭代对象

##### StreamingHttpResponse函数

示例：下载文件 

URL路由

```python
re_path('^download/$', views.download),
re_path(r'^down_file/(?P<filename>.*)$', views.down_file, name="down_file")
```

视图

```python
from django.http import StreamingHttpResponse
import os
def download(request):
    file_list = os.listdir('upload')
	return render(request, "download.html", {'file_list': file_list})

def down_file(request, filename):
    file_path = os.path.join('upload', filename)
    response = StreamingHttpResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=%s'
    %(os.path.basename(file_path))
	return response
```

模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>文件列表</title>
</head>
<body>
    {% for i in file_list %}
    <p><a href="{% url 'down_file' i %}">{{ i }}</a></p>
    {% endfor %}
</body>
</html>
```

##### FileResponse函数

FileResponse函数：如果提供文件下载建议方法

示例：下载文件

```python
def down_file(request, filename):
    file_path = os.path.join('upload', filename)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=%s'
    %(os.path.basename(file_path))
	return response
```

##### JsonResponse函数

JsonResponse函数：响应一个JSON对象

示例：下载文件

```python
from django.http import JsonResponse
def test_response(request):
    res = {‘foo’: ‘bar’}
	return JsonResponse(res)
```



### Django模板系统

#### 模板是什么

Django模板系统：用于自动渲染一个文本文件，一般用于HTML页面。模板引擎渲 染的最终HTML内容返回给客户端浏览器。

 模板文件有两部分组成：

-  静态部分，例如html、css、js 
-  动态部分，django模板语言，类似于jinja语法

#### 变量

变量定义：在函数视图render中的context传入，类似于字典对象。 

变量在模板中引用，格式：{{ key }} 

示例：

```python
def hello(request):
    user = {'name': '阿良', 'property': {'sex': '男', 'age': 30}}
	return render(request, 'user.html', {'user': user})
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>用户信息</title>
</head>
<body>
传递过来的字典: {{ user }}<br>
姓名: {{ user.name }}<br>
性别: {{ user.property.sex }}<br>
年龄: {{ user.property.age }}<br>
</body>
</html>

```

**设置全局变量**

1、在项目目下创建contexts.py文件

```python
def user(request):
    username = request.session.get('username')
    return {'username': username}
```



2、在settings.py文件中添加你的上下文处理器

3、```<h3>欢迎：{{ username }}</h3>```



#### 标签

**if条件判断**

判定给定的条件是否满足（True或False），根据判断的结果决定执行的语句。 

语法： 

```html
{% if <表达式> %}
    <内容块> 
{% elif <表达式> %} 
    <内容块> 
{% else %} 
    <内容块> 
{% endif %}
```

**操作符号**

| 类型       | 操作符                                              |
| ---------- | --------------------------------------------------- |
| 比较操作符 | == 等于; !=不等于;>大于;<小于;>=大于等于;<=小于等于 |
| 逻辑操作符 | and 与; or 或                                       |
| 成员操作符 | not 逻辑否定; in 包含在内                           |

**循环**

for循环：一般用于遍历数据类型的元素进行处理，例如列表。

 语法： 

```html
{% for <变量> in <序列> %} 
    <内容块> 
{% endfor %}
```

**forloop变量**

forloop是在{% for %}标签中生成的变量，用于获取当前循环进展信息.

| 变量                | 描述                                        |
| ------------------- | ------------------------------------------- |
| forloop.counter     | 循环计数器，当前循环的索引从1开始           |
| forloop.counter0    | 循环计数器，当前循环的索引从0开始           |
| forloop.revcounter  | 当前循环倒数计数，最后一次循环为1，反向计数 |
| forloop.revcounter0 | 当前循环倒数计数，最后一次循环为0，反向计数 |
| forloop.first       | 当前循环为第一个循环时，该变量为True        |
| forloop.last        | 当前循环为最后一个循环时，该变量为True      |
| forloop.parentloop  | 再嵌套循环中，指向当前循环的上级循环        |

**for empty**

for...empty 当循环的序列为空时，执行empty下面的内容。

 语法： 

```html
{% for <变量> in <序列> %} 
    <遍历> 
{% empty %} 
    <代码块> 
{% endfor %}
```



#### 常用过滤器

过滤器：在变量被显示前修改值的一种方法。

语法：{{ value | 过滤器:参数 }}

| 过滤器         | 说明                                                         | 示例                                                         |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| add            | 将两个值转换为整数相加                                       | {{ 11 \| add:"6" }} 结果 17                                  |
| cut            | 切除字符。从给定字符串中删除arg的所有值。                    | {{ "hello world" \| cut:"w" }} 结果 hello orld               |
| default        | 如果值的计算结果为 False，则使用给定的默认值。否则，使用该值。 | {{ "" \| default:"hello world" }} 结果 hello world           |
| first          | 返回第一个元素                                               | {{ "hello world" \| first }} 结果 h                          |
| last           | 返回最后一个元素                                             | {{ "hello world" \| last }} 结果 d                           |
| join           | 使用字符串连接列表，如Python的 str.join(list)                | {{ abc \| join:"," }} 结果 1,2,3 # abc = [1,2,3]             |
| length         | 返回值的长度。这适用于字符串和列表                           | {{ "hello world" \| length }} 结果 11                        |
| lower          | 将字 符串转换为小写                                          | {{ "AAA" \| lower }} 结果 aaa                                |
| upper          | 将字符串转换为大写                                           | {{ "aaa" \| upper }} 结果 AAA                                |
| slice          | 切片, 类似于Python中的切片操作                               | {{ "hello world" \| slice:"2:" }} 结果 llo world             |
| title          | 所有单词首字母大写                                           | {{ "aaa" \| title }} 结果 Aaa                                |
| truncatechars  | 如果长度大于指定的字符数，则截断字符串。截断的字符串将以可 翻译的省略号序列（“...”）结束 | {{ "hello world" \| truncatechars:2 }} 结果 h…               |
| filesizeformat | 将该值格式化为“人类可读”文件大小（即 ‘13 KB‘， ‘4.1 MB‘，‘102 bytes‘ 等）。 | {{ 10000 \| filesizeformat }} 结果 9.8 KB                    |
| floatformat    | 当不带参数时，将一个浮点数舍入到小数点后一位，但前提是要显 示一个小数部分。 | {{ 1.33333333 \| floatformat }} 结果 1.3 floatformat:2 指定保留的小数位数 |



##### 自定义过滤器

1、在app下创建templatetags目录，并且该app必须在 INSTALLED_APPS中进行安装

2、自定义过滤器函数

```python
from django.template import Library
    register = Library() # 注册过滤器对象
    @register.filter # 通过装饰注册自定义过滤器
    def func(n):
    return n / 2
```

3、在模板中使用

```html
{% load filters %} # 开头
{{ 123 | func }} 
```



#### 注释

注释：

{# 注释内容 #}

#### 模板继承

模板继承主要是为了提高代码重用，减轻开发人员的工作量。 

典型应用：网站的头部、尾部信息。 

1、定义一个基础模板，也称为母板，这个页面存放整个网站共用的内容 templates/base.html 

2、在子模板继承这个母版 {% extends ‘base.html’ %} 

3、在基础模板预留子模板差异化内容 {% block 名称 %} 预留区域 {% endblock %}

 4、在子模板里同样语法引用并填充预留区域内容

#### 模板导入

模板导入：导入一个模板（一般是某个网页功能）到当前模板

将一个功能创建为模板：

```html
# templates/hello.html
<style>
    .hello {
    background-color: red;
    }
</style>
<div class="hello">
    子模板
</div>

```

模板导入：

```html
{% extends 'base.html' %}
{% block title %}首页{% endblock %}
{% block context %}
	<h1>这是首页！</h1>
	{% include "hello.html" %}
{% endblock %}
```



#### 引用静态文件

- STATICFILES_DIRS：告诉Django哪个目录是“静态文件的文件夹”
-  STATIC_ROOT：指出浏览器访问静态文件“根路径”

1、在settings.py配置

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'
```

2、在模板文件引用静态文件

```html
<link rel="stylesheet" href="/static/main.css">
或者
{% load static %} # 在模板文件开头
<link rel="stylesheet" href="{% static 'main.css' %}">
```

