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




### Django试图





### Django模板系统












