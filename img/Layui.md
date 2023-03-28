
<!-- TOC -->
* [前端UI框架：Layui](#uilayui)
  * [1、Layui介绍](#1layui)
  * [2、Layui基本使用](#2layui)
  * [3、管理后台布局](#3)
    * [3.1 导航栏](#31-)
    * [3.2 管理后台布局与修改](#32-)
    * [3.3 字体图标](#33-)
    * [3.4 主题颜色](#34-)
  * [5、栅格系统](#5)
  * [6、卡片面板](#6)
  * [7、按钮](#7)
  * [8、表单](#8)
  * [9、上传文件](#9)
  * [10、数据表格](#10)
    * [10.1 分页](#101-)
    * [10.2 表格工具栏](#102-)
    * [10.3 表格查询](#103-)
      * [搜索关键字查询](#)
      * [选择框查询](#)
    * [10.4 数据表格内容美化](#104-)
  * [11、弹出层](#11)
<!-- TOC -->


# 前端UI框架：Layui

![](https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/layui.png)

## 1、Layui介绍

layui（谐音：类UI)是一个前端UI框架，遵循原生 HTML/CSS/JS 的书写与组织形式，使用门槛低，拿来即用，给不熟悉前端的工程师带来福音。

同类产品：Bootstrap、EasyUI

官网（www.layui.com）已下线，全面迁移到公共代码平台。

Github地址：https://github.com/sentsin/layui

Gitee地址：https://gitee.com/sentsin/layui.git

文档目前还未迁移，可先参考镜像站点：[http://](http://layui-doc.pearadmin.com/)[layui-doc.pearadmin.com](http://layui-doc.pearadmin.com/)

## 2、Layui基本使用

1、下载压缩包

```
  ├─css //css目录
  │  │─modules //模块 css 目录（一般如果模块相对较大，我们会单独提取，如下：）
  │  │  ├─laydate
  │  │  └─layer
  │  └─layui.css //核心样式文件
  ├─font  //字体图标目录
  └─layui.js //核心库
```

2、将layui目录放到django项目的static静态目录下

3、html导入layui.css和layui.js

```
<link rel="stylesheet" href="/static/layui/css/layui.css">
<script src="/static/layui/layui.js"></script>
```

4、使用layui

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
    <link rel="stylesheet" href="/static/layui/css/layui.css">
    <script src="/static/layui/layui.js"></script>
</head>
<body>
<h1>首页</h1>

<script>
layui.use(['layer', 'form'], function(){  // 导入js模块
  var layer = layui.layer   // 为了方便使用，将模块赋予变量
  ,form = layui.form;  

  layer.msg('Hello World');
});
</script>

</body>
</html>
```

## 3、管理后台布局

### 3.1 导航栏

![https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/nav-style.png](https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/nav-style.png)

顶部导航：一般用于官网

侧栏导航：一般用于管理后台

### 3.2 管理后台布局与修改

管理后台布局代码：

```
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>layout 管理系统大布局 - Layui</title>
  <link rel="stylesheet" href="./layui/css/layui.css">
</head>
<body>
<div class="layui-layout layui-layout-admin">
  <div class="layui-header">
    <div class="layui-logo layui-hide-xs layui-bg-black">layout demo</div>
    <!-- 头部区域（可配合layui 已有的水平导航） -->
    <ul class="layui-nav layui-layout-left">
      <!-- 移动端显示 -->
      <li class="layui-nav-item layui-show-xs-inline-block layui-hide-sm" lay-header-event="menuLeft">
        <i class="layui-icon layui-icon-spread-left"></i>
      </li>
      
      <li class="layui-nav-item layui-hide-xs"><a href="">nav 1</a></li>
      <li class="layui-nav-item layui-hide-xs"><a href="">nav 2</a></li>
      <li class="layui-nav-item layui-hide-xs"><a href="">nav 3</a></li>
      <li class="layui-nav-item">
        <a href="javascript:;">nav groups</a>
        <dl class="layui-nav-child">
          <dd><a href="">menu 11</a></dd>
          <dd><a href="">menu 22</a></dd>
          <dd><a href="">menu 33</a></dd>
        </dl>
      </li>
    </ul>
    <ul class="layui-nav layui-layout-right">
      <li class="layui-nav-item layui-hide layui-show-md-inline-block">
        <a href="javascript:;">
          <img src="//tva1.sinaimg.cn/crop.0.0.118.118.180/5db11ff4gw1e77d3nqrv8j203b03cweg.jpg" class="layui-nav-img">
          tester
        </a>
        <dl class="layui-nav-child">
          <dd><a href="">Your Profile</a></dd>
          <dd><a href="">Settings</a></dd>
          <dd><a href="">Sign out</a></dd>
        </dl>
      </li>
      <li class="layui-nav-item" lay-header-event="menuRight" lay-unselect>
        <a href="javascript:;">
          <i class="layui-icon layui-icon-more-vertical"></i>
        </a>
      </li>
    </ul>
  </div>
  
  <div class="layui-side layui-bg-black">
    <div class="layui-side-scroll">
      <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
      <ul class="layui-nav layui-nav-tree" lay-filter="test">
        <li class="layui-nav-item layui-nav-itemed">
          <a class="" href="javascript:;">menu group 1</a>
          <dl class="layui-nav-child">
            <dd><a href="javascript:;">menu 1</a></dd>
            <dd><a href="javascript:;">menu 2</a></dd>
            <dd><a href="javascript:;">menu 3</a></dd>
            <dd><a href="">the links</a></dd>
          </dl>
        </li>
        <li class="layui-nav-item">
          <a href="javascript:;">menu group 2</a>
          <dl class="layui-nav-child">
            <dd><a href="javascript:;">list 1</a></dd>
            <dd><a href="javascript:;">list 2</a></dd>
            <dd><a href="">超链接</a></dd>
          </dl>
        </li>
        <li class="layui-nav-item"><a href="javascript:;">click menu item</a></li>
        <li class="layui-nav-item"><a href="">the links</a></li>
      </ul>
    </div>
  </div>
  
  <div class="layui-body">
    <!-- 内容主体区域 -->
    <div style="padding: 15px;">内容主体区域。记得修改 layui.css 和 js 的路径</div>
  </div>
  
  <div class="layui-footer">
    <!-- 底部固定区域 -->
    底部固定区域
  </div>
</div>
<script src="./layui/layui.js"></script>
<script>
//JS 
layui.use(['element', 'layer', 'util'], function(){
  var element = layui.element
  ,layer = layui.layer
  ,util = layui.util
  ,$ = layui.$;
  
  //头部事件
  util.event('lay-header-event', {
    //左侧菜单事件
    menuLeft: function(othis){
      layer.msg('展开左侧菜单的操作', {icon: 0});
    }
    ,menuRight: function(){
      layer.open({
        type: 1
        ,content: '<div style="padding: 15px;">处理右侧面板的操作</div>'
        ,area: ['260px', '100%']
        ,offset: 'rt' //右上角
        ,anim: 5
        ,shadeClose: true
      });
    }
  });
  
});
</script>
</body>
</html>
```

1、获取后端布局代码，这个作为母版

2、头部区域只保留一个li，用于存放设置命名空间

3、修改涉及文字

4、创建四个页面

5、导航栏展开和选中效果

```
菜单展开类样式：layui-nav-itemed
子菜单选中类样式：layui-this
```

### 3.3 字体图标

可以给导航栏前面添加字体图标，美化效果：

```
<a class="" href="javascript:;"><i class="layui-icon layui-icon-template-1">&nbsp;&nbsp;</i>Kubernetes</a>
```

### 3.4 主题颜色

顶部背景：

```
<div class="layui-header layui-bg-cyan">
```

侧栏背景：

```
<div class="layui-logo layui-hide-xs layui-bg-cyan">DevOps管理平台</div>
<div class="layui-side-scroll layui-bg-cyan">
<ul class="layui-nav layui-nav-tree layui-bg-cyan"  lay-filter="test">
```

## 5、栅格系统

栅格也叫网格系统，是一种平面设计的方法和风格。以规则的网格阵列来指导和规范网页中的版面布局。

将容器进行了 12 等分，预设了 4*12 种 CSS 排列类，它们在移动设备、平板、桌面中/大尺寸四种不同的屏幕下发挥着各自的作用。

栅格布局规则：

| 1.   | 采用 *layui-row* 来定义行，如：<div class="layui-row"></div> |
| ---- | ------------------------------------------------------------ |
| 2.   | 采用类似 *layui-col-md** 这样的预设类来定义一组列（column），且放在行（row）内。其中：变量*md* 代表的是不同屏幕下的标记（可选值见下文）变量代表的是该列所占用的12等分数（如6/12），可选值为 1 - 12如果多个列的“等分数值”总和等于12，则刚好满行排列。如果大于12，多余的列将自动另起一行。 |
| 3.   | 列可以同时出现最多四种不同的组合，分别是：*xs*（超小屏幕，如手机）、*sm*（小屏幕，如平板）、*md*（桌面中等屏幕）、*lg*（桌面大型屏幕），以呈现更加动态灵活的布局。 |
| 4.   | 可对列追加类似 *layui-col-space5*、 *layui-col-md-offset3* 这样的预设类来定义列的间距和偏移。 |
| 5.   | 最后，在列（column）元素中放入你自己的任意元素填充内容，完成布局！ |

示例：

![image-20211126104258831](C:\Users\lizhenliang\AppData\Roaming\Typora\typora-user-images\image-20211126104258831.png)

```
<div class="layui-container">  
  常规布局（以中型屏幕桌面为例）：
  <div class="layui-row">
    <div class="layui-col-md9">
      你的内容 9/12
    </div>
    <div class="layui-col-md3">
      你的内容 3/12
    </div>
  </div>
</div>
```

样式行类：layui-row

样式列类：layui-col-md* 

列间距类：layui-col-space*，支持列之间为 1px-30px 区间的所有双数间隔，以及 1px、5px、15px、25px 的单数间隔。

------

**栅格嵌套**

可以对栅格进行无穷层次的嵌套，这更加增强了栅格的表现能力。而嵌套的使用非常简单。在列元素（layui-col-md）中插入一个行元素（layui-row），即可完成嵌套。下面是一个简单的例子：

```
<div class="layui-row layui-col-space5">
  <div class="layui-col-md5">
    <div class="layui-row grid-demo">
      <div class="layui-col-md3">
        内部列
      </div>
      <div class="layui-col-md9">
        内部列
      </div>
      <div class="layui-col-md12">
        内部列
      </div>
    </div>
  </div>
  <div class="layui-col-md7">
    <div class="layui-row grid-demo grid-demo-bg1">
      <div class="layui-col-md12">
        内部列
      </div>
      <div class="layui-col-md9">
        内部列
      </div>
      <div class="layui-col-md3">
        内部列
      </div>
    </div>
  </div>
</div>
```

## 6、卡片面板

卡片式面板面板通常用于非白色背景色的主体内，从而衬托出边框投影的效果。主要用于美化显示。

```
<div class="layui-card">
  <div class="layui-card-header">卡片面板</div>
  <div class="layui-card-body">
		内容区
  </div>
</div>
```

注：如果网页采用的是默认的白色背景，不建议使用卡片面板，因为无法衬托出效果。

## 7、按钮

```
<!-- 基础按钮 -->
<button type="button" class="layui-btn">一个标准的按钮</button>
<a href="http://www.ctnrs.com" class="layui-btn">一个可跳转的按钮</a>
<div class="layui-btn">一个按钮</div>
<!-- 不同主题按钮 --> <br>
<button type="button" class="layui-btn layui-btn-primary">原始按钮</button>
<button type="button" class="layui-btn">默认按钮</button>
<button type="button" class="layui-btn layui-btn-normal">百搭按钮</button>
<button type="button" class="layui-btn layui-btn-warm">暖色按钮</button>
<button type="button" class="layui-btn layui-btn-danger">警告按钮</button>
<button type="button" class="layui-btn layui-btn-disabled">禁用按钮</button>
<!-- 按钮尺寸 -->  <br>
<button type="button" class="layui-btn layui-btn-primary layui-btn-lg">大型按钮</button>
<button type="button" class="layui-btn layui-btn-primary">默认按钮</button>
<button type="button" class="layui-btn layui-btn-primary layui-btn-sm">小型按钮</button>
<button type="button" class="layui-btn layui-btn-primary layui-btn-xs">迷你按钮</button>
<!-- 圆角按钮 --> <br>
<button type="button" class="layui-btn layui-btn-primary layui-btn-radius">原始按钮</button>
<button type="button" class="layui-btn layui-btn-radius">默认按钮</button>
<button type="button" class="layui-btn layui-btn-normal layui-btn-radius">百搭按钮</button>
<button type="button" class="layui-btn layui-btn-warm layui-btn-radius">暖色按钮</button>
<button type="button" class="layui-btn layui-btn-danger layui-btn-radius">警告按钮</button>
<button type="button" class="layui-btn layui-btn-disabled layui-btn-radius">禁用按钮</button>

<!-- 图标按钮 --> <br>
<button type="button" class="layui-btn">
    <i class="layui-icon layui-icon-addition">增加</i>
</button>
<button type="button" class="layui-btn">
    <i class="layui-icon layui-icon-subtraction">删除</i>
</button>
```

## 8、表单

表单基本区块结构：

```
<form action="" class="layui-form">
    <div class="layui-form-item">
      <label class="layui-form-label">标签区域</label>
      <div class="layui-input-block" >
             表单元素区域
      </div>
    </div>
</form>
```

示例代码：

```
<form class="layui-form" action="">
  <div class="layui-form-item">
    <label class="layui-form-label">输入框</label>
    <div class="layui-input-block">
      <input type="text" name="title" required  lay-verify="required" placeholder="请输入标题" autocomplete="off" class="layui-input">
    </div>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">密码框</label>
    <div class="layui-input-inline">
      <input type="password" name="password" required lay-verify="required" placeholder="请输入密码" autocomplete="off" class="layui-input">
    </div>
    <div class="layui-form-mid layui-word-aux">辅助文字</div>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">选择框</label>
    <div class="layui-input-block">
      <select name="city" lay-verify="required">
        <option value=""></option>
        <option value="0">北京</option>
        <option value="1">上海</option>
        <option value="2">广州</option>
        <option value="3">深圳</option>
        <option value="4">杭州</option>
      </select>
    </div>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">复选框</label>
    <div class="layui-input-block">
      <input type="checkbox" name="like[write]" title="写作">
      <input type="checkbox" name="like[read]" title="阅读" checked>
      <input type="checkbox" name="like[dai]" title="发呆">
    </div>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">开关</label>
    <div class="layui-input-block">
      <input type="checkbox" name="switch" lay-skin="switch">
    </div>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">单选框</label>
    <div class="layui-input-block">
      <input type="radio" name="sex" value="男" title="男">
      <input type="radio" name="sex" value="女" title="女" checked>
    </div>
  </div>
  <div class="layui-form-item layui-form-text">
    <label class="layui-form-label">文本域</label>
    <div class="layui-input-block">
      <textarea name="desc" placeholder="请输入内容" class="layui-textarea"></textarea>
    </div>
  </div>
  <div class="layui-form-item">
    <div class="layui-input-block">
      <button class="layui-btn" lay-submit lay-filter="formDemo">立即提交</button>
      <button type="reset" class="layui-btn layui-btn-primary">重置</button>
    </div>
  </div>
</form>
 
<script>
//Demo
layui.use('form', function(){
  var form = layui.form;
  
  //监听提交
  form.on('submit(formDemo)', function(data){
    layer.msg(JSON.stringify(data.field)); 
    return false;
  });
});
</script>  
```

- lay-filter="formDemo"： 类似于ID，选择一个事件标识

- data.field：表单数据及csrf_token都保存到里面
- lay-submit：表单的提交事件是需要通过带有lay-submit属性的按钮来触发的

------

form.on语法：form.on('event(过滤器值)', callback);

form模块在 layui 事件机制中注册了专属事件，类似于js onclick：

| event    | 描述                       |
| :------- | :------------------------- |
| select   | 触发select下拉选择事件     |
| checkbox | 触发checkbox复选框勾选事件 |
| switch   | 触发checkbox复选框开关事件 |
| radio    | 触发radio单选框事件        |
| submit   | 触发表单提交事件           |

**使用ajax将表单数据提交到服务端接口：**

```
<script>
layui.use(['form','layer'], function(){
  var form = layui.form;
  var layer = layui.layer;
  //监听提交
  form.on('submit(formBtn)', function(data){
    console.log(data.field);
    // 可以通过form自带提交事件或者通过AJAX
    $.ajax({
        type: "POST",
        url: "/myapp/user/",
        data: data.field,
        success: function (result) {
            if (result.code == "0"){
                layer.msg(result.msg, {icon: 6})
            } else {
                layer.msg(result.msg, {icon: 5})
            }
        },
        error: function () {
            layer.msg("服务器接口异常！", {icon: 5})
        }
    });
  });
});
</script>
```

## 9、上传文件

上述示例使用ajax提交data.field所有表单数据，但无法同时提交文件。如果按照之前讲的ajax原始方式提交又感觉太繁琐。

layui可以通过上传模块upload.render实现。

在上述示例中添加一个上传文件按钮（表单项）：

```
<div class="layui-form-item">
    <label class="layui-form-label">上传头像</label>
    <div class="layui-input-block">
        <button type="button" class="layui-btn" id="test1"><i class="layui-icon"></i>上传文件</button>
    </div>
</div>
 
<button class="layui-btn" lay-submit lay-filter="formDemo" id="uploadBtn">立即提交</button>
```



```
<script>
layui.use(['form','layer','upload'], function(){
  var form = layui.form;
  var layer = layui.layer;
  var $ = layui.jquery
  ,upload = layui.upload;
    
  upload.render({
    elem: '#test1'  // 选择元素
    ,url: '/myapp/user/' // 服务端上传接口
    ,auto: false  // 是否选完文件后自动上传
    ,bindAction: '#uploadBtn' // 绑定提交表单按钮，一般配合auto: false使用
    ,accept: 'file' // 指定允许上传时效验的文件类型
    ,size: 10240 //限制文件大小，单位 KB
    ,exts: 'jpg|txt' //允许上传的文件后缀，一般结合accept设置
    // 上传前回调
    ,before: function () {
          // 兴趣爱好多选保存到数组中
          var like = [];
          $("input[name='like']:checked").each(function () {
              like.push($(this).val());
          });
          this.data = {
              csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
              username: $('input[name="username"]').val(),
              password: $('input[name="password"]').val(),
              city: $('select[name="city"]').val(),
              like: like,  // 'like': ['协作,阅读'],
              status: $('input[name="status"]').val(),
              sex: $('input[name="sex"]:checked').val(),
              desc: $('textarea[name="desc"]').val(),
          };
      }
    ,done: function(res){  // 上传完后回调，服务端以json格式返回数据
        if (res.code == "0") {
            layer.msg(res.msg, {icon: 6});
        } else {
            layer.msg(res.msg, {icon: 5});
        }
    }
    ,error: function (res) {
       layer.msg("服务器接口异常！", {icon:5})
    }
  });
});
</script>
```

回调函数：

- choose 选择文件后的回调函数
- before 文件提交上传前的回调
- done 执行上传请求后的回调
- error 执行上传请求出现异常的回调

服务端代码（保存文件）：

```
        file_obj = request.FILES.get('file')
        try:
            import os
            file_path = os.path.join('upload', file_obj.name)
            with open(file_path, mode='wb') as f:
                for i in file_obj.chunks():
                    f.write(i)
            code = 0
            msg = "上传成功."
        except Exception as e:
            code = 1
            msg = "上传失败！"
```

## 10、数据表格

表格是呈现数据的主流方式。

table 模块对表格进行一些列功能和动态化数据操作，涵盖了日常业务所涉及的几乎全部需求。支持固定表头、固定行、固定列左/列右，支持拖拽改变列宽度，支持排序，支持多级表头，支持单元格的自定义模板，支持对表格重载（比如搜索、条件筛选等），支持复选框，支持分页，支持单元格编辑等等一些列功能。

创建一个table实例最简单的方式是，在页面放置一个元素 *<table id="demo"></table>*，然后通过 *table.render()* 方法指定该容器，

示例：

```
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>table模块快速使用</title>
  <link rel="stylesheet" href="/layui/css/layui.css" media="all">
  <script src="/layui/layui.js"></script>
</head>
<body>
 
<table id="demo" lay-filter="test"></table>
 
<script>
layui.use('table', function(){
  var table = layui.table;
    
  table.render({
    elem: '#demo' // 选择table元素
    ,url: '/user_data/' //数据接口
    ,page: true //开启分页
    ,cols: [[ //表头
      {field: 'id', title: 'ID',  sort: true, fixed: 'left'}
      ,{field: 'username', title: '用户名'}
      ,{field: 'sex', title: '性别'}
      ,{field: 'email', title: '邮箱'}
    ]]
  });
});
</script>
</body>
</html>
```
服务端数据接口代码：

```
def user_data(request):
    if request.method == "GET":
        user = []  # [{},{},{}]
        # 正常通过ORM获取
        for id in range(1, 100):
            import random
            name = random.sample(['龙', '妹', '东', '西', '南', '北'], 1)  # 返回列表
            name = '阿' + str(name[0])
            sex = random.sample(['男', '女'], 1)
            sex = sex[0]
            email = str(id) + '@aliangedu.com'
            row = {'id': id, 'username': name, 'sex': sex, 'email': email}
            user.append(row)
        msg = "获取用户数据成功！"
        data = {'code': 0, 'data': user, 'msg': msg}
        return JsonResponse(data) # 如果传递不是一个字典，需要设置safe=False
```

数据接口返回的JSON数据格式：

```
{
    "code": 0,
    "data": [{}, {}],
    "msg": "",
    "count": 1000  
}
```
table模块支持的常用参数：

| 参数           | 类型               | 说明                                                         | 示例值              |
| :------------- | :----------------- | :----------------------------------------------------------- | :------------------ |
| elem           | String/DOM         | 指定原始 table 容器的选择器或 DOM，方法渲染方式必填          | "#demo"             |
| cols           | Array              | 设置表头。值是一个二维数组。方法渲染方式必填                 |                     |
| url（等）      | -                  | 异步数据接口相关参数。其中 url 参数为必填项                  |                     |
| toolbar        | String/DOM/Boolean | 开启表格头部工具栏区域，该参数支持四种类型值：toolbar: '#toolbarDemo' *//指向自定义工具栏模板选择器*toolbar: '<div>xxx</div>' *//直接传入工具栏模板字符*toolbar: true *//仅开启工具栏，不显示左侧模板*toolbar: 'default' *//让工具栏左侧显示默认的内置模板*注意： 1. 该参数为 layui 2.4.0 开始新增。 2. 若需要“列显示隐藏”、“导出”、“打印”等功能，则必须开启该参数 | false               |
| defaultToolbar | Array              | 该参数可自由配置头部工具栏右侧的图标按钮                     |                     |
| done           | Function           | 数据渲染完的回调。你可以借此做一些其它的操作                 |                     |
| error          | Function           | 数据请求失败的回调，返回两个参数：错误对象、内容 layui 2.6.0 新增 | -                   |
| data           | Array              | 直接赋值数据。既适用于只展示一页数据，也非常适用于对一段已知数据进行多页展示。 | [{}, {}, {}, {}, …] |
| totalRow       | Boolean/String     | 是否开启合计行区域                                           | false               |
| page           | Boolean/Object     | 开启分页（默认：false）。支持传入一个对象，里面可包含 [laypage](http://layui-doc.pearadmin.com/doc/modules/laypage.html) 组件所有支持的参数（jump、elem除外） | {theme: '#c00'}     |
| limit          | Number             | 每页显示的条数（默认 10）。值需对应 limits 参数的选项。 注意：*优先级低于 page 参数中的 limit 参数* | 30                  |
| limits         | Array              | 每页条数的选择项，默认：[10,20,30,40,50,60,70,80,90]。 注意：*优先级低于 page 参数中的 limits 参数* | [30,60,90]          |
| title          | String             | 定义 table 的大标题（在文件导出等地方会用到）                | "用户表"            |
| text           | Object             | 自定义文本，如空数据时的异常提示等。                         |                     |
| id             | String             | 设定容器唯一 id。id 是对表格的数据操作方法上是必要的传递条件，它是表格容器的索引，你在下文诸多地方都将会见识它的存在。  另外，若该参数未设置，则默认从 *<table id="test"></table>* 中的 id 属性值中获取。 | test                |

**cols 表头参数**

| 参数    | 类型          | 说明                                                         | 示例值                                  |
| :------ | :------------ | :----------------------------------------------------------- | :-------------------------------------- |
| field   | String        | 设定字段名。非常重要，且是表格数据列的唯一标识               | username                                |
| title   | String        | 设定标题名称                                                 | 用户名                                  |
| width   | Number/String | 设定列宽，若不填写，则自动分配；若填写，则支持值为：数字、百分比。 请结合实际情况，对不同列做不同设定。 | 200 30%                                 |
| type    | String        | 设定列类型。可选值有：normal（常规列，无需设定）checkbox（复选框列）radio（单选框列，layui 2.4.0 新增）numbers（序号列）space（空列） | 任意一个可选值                          |
| fixed   | String        | 固定列。可选值有：*left*（固定在左）、*right*（固定在右）。一旦设定，对应的列将会被固定在左或右，不随滚动条而滚动。 注意：*如果是固定在左，该列必须放在表头最前面；如果是固定在右，该列必须放在表头最后面。* | left（同 true） right                   |
| hide    | Boolean       | 是否初始隐藏列，默认：false。layui 2.4.0 新增                | true                                    |
| sort    | Boolean       | 是否允许排序（默认：false）。如果设置 true，则在对应的表头显示排序icon，从而对列开启排序功能。 | true                                    |
| edit    | String        | 单元格编辑类型（默认不开启）目前只支持：*text*（输入框）     | text                                    |
| style   | String        | 自定义单元格样式。即传入 CSS 样式                            | background-color: #5FB878; color: #fff; |
| align   | String        | 单元格排列方式。可选值有：*left*（默认）、*center*（居中）、*right*（居右） | center                                  |
| templet | String        | 自定义列模板，模板遵循 laytpl语法。这是一个非常实用的功能，你可借助它实现逻辑处理，以及将原始数据转化成其它格式，如时间戳转化为日期字符等 |                                         |
| toolbar | String        | 绑定工具条模板。可在每行对应的列中出现一些自定义的操作性按钮 |                                         |

### 10.1 分页

如果数据接口返回几百条记录的话，如果一次性显示的话表格会很多行，用户体验不佳。因此，一般会进行分页显示，例如一页显示10条记录，共十页。用户可以自行翻阅，记录少，清晰显示。

table.render 默认会自动传递两个参数：?page=1&limit=30（该参数可通过 request 自定义）

- page 代表当前第几页
- limit 代表每页数据条数

服务端数据接口根据这两个参数返回指定数量数据：

```#
page = int(request.GET.get('page'))
limit = int(request.GET.get('limit'))
# data = data[0:10]
start = (page - 1) * limit  # 切片的起始值
end = page * limit  # 切片的末值
data = data[start:end] # 返回指定数据范围
```

服务端数据接口：

```
if request.method == "GET":
    # 模拟数据
    user = []
    for id in range(1, 100):
        import random
        name = random.sample(['龙', '妹', '东', '西', '南', '北'], 1)  # 返回列表
        name = '阿'+str(name[0])
        sex = random.sample(['男', '女'], 1)
        sex = sex[0]
        email = str(id) + '@aliangedu.com'
        row = {'id': id, 'username': name, 'sex': sex, 'email': email}
		user.append(row)

	count = len(user)  # 要在切片之前获取总数

    page = int(request.GET.get('page', 1))   # 当前页，第几页
    limit = int(request.GET.get('limit'))  # 当前页数量，在table.render参数配置，默认10
    start = (page - 1) * limit  # 获取上一页的最后一个数
    end = page * limit  # 当前页最后一个数
    data = user[start:end]
   
    code = '0'
    msg = "获取数据成功."
    user = {'code': code, 'msg': msg, 'count': count, 'data': data }
    return JsonResponse(user)
```

### 10.2 表格工具栏

```
<table class="layui-hide" id="test" lay-filter="test"></table>

<!--  头部工具栏，左侧 -->
<script type="text/html" id="toolbarDemo">
  <div class="layui-btn-container">
    <button class="layui-btn layui-btn-sm" lay-event="getCheckData">获取选中行数据</button>
    <button class="layui-btn layui-btn-sm" lay-event="getCheckLength">获取选中数目</button>
    <button class="layui-btn layui-btn-sm" lay-event="isAll">验证是否全选</button>
  </div>
</script>

<!--  行工具 -->
<script type="text/html" id="barDemo">
  <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
  <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
</script>

<script>
    layui.use(['table','upload'], function(){
        // Layui 的模块
          var layer = layui.layer;
          var $ = layui.jquery;
          var table = layui.table;

          table.render({
              elem: '#test'
              ,url:'/user'
              ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
              ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
                title: '提示'
                ,layEvent: 'LAYTABLE_TIPS'
                ,icon: 'layui-icon-tips'
              }]
              ,title: '用户数据表'
              ,cols: [[
                {type: 'checkbox', fixed: 'left'}
                ,{field:'id', title:'ID', width: 80}
                ,{field:'username', title:'用户名', sort:true}
                ,{field:'sex', title:'性别'}
                ,{field:'city', title:'城市'}
                ,{fixed: 'right', title:'操作', toolbar: '#barDemo', width:200}
              ]]
              ,page: true
            });

        //头工具栏事件
        table.on('toolbar(test)', function(obj){
          var checkStatus = table.checkStatus(obj.config.id);
          switch(obj.event){
            case 'getCheckData':
              var data = checkStatus.data;
              layer.alert(JSON.stringify(data));
            break;
            case 'getCheckLength':
              var data = checkStatus.data;
              layer.msg('选中了：'+ data.length + ' 个');
            break;
            case 'isAll':
              layer.msg(checkStatus.isAll ? '全选': '未全选');
            break;

            //自定义头工具栏右侧图标 - 提示
            case 'LAYTABLE_TIPS':
              layer.alert('这是工具栏右侧自定义的一个图标按钮');
            break;
          };
        });

        //监听行工具事件
        table.on('tool(test)', function(obj){
          var data = obj.data;
          console.log(data);
          //console.log(obj)
          var csrf_token = $('[name="csrfmiddlewaretoken"]').val();
          if(obj.event === 'del'){
            layer.confirm('真的删除行么？', function(index){
              var post_data = {'id': data.id};
              console.log(post_data);
              $.ajax({
                 type: "DELETE",
                  url: "/user",
                  data: post_data,
                  headers: {'X-CSRFToken': csrf_token},  // 放到请求头，django也会验证这字段
                  success: function (result) {
                      if (result.code == '0') {
                          obj.del();  // 临时删除当前页面记录
                          layer.msg(result.msg)
                      } else {
                          layer.msg(result.msg)
                      }
                  },
                  error: function () {
                      layer.msg("服务器接口异常！")
                  }
              });

              layer.close(index);
            });
          } else if(obj.event === 'edit'){
            layer.prompt({
              formType: 2
              ,value: data.city
            }, function(value, index){
              obj.update({
                city: value
              });
              // 将当前记录ID、修改的字段和值传递到后端
              console.log(value);
              var post_data = {'id': data.id, 'city': value};
              $.ajax({
                 type: "PUT",
                  url: "/user",
                  data: post_data,
                  headers: {'X-CSRFToken': csrf_token},  // 另一种方式，放到请求头，django也会验证这字段
                  success: function (result) {
                      if (result.code == '0') {
                          obj.del();  // 临时删除当前页面记录
                          layer.msg(result.msg)
                      } else {
                          layer.msg(result.msg)
                      }
                  },
                  error: function () {
                      layer.msg("服务器接口异常！")
                  }
              });
              layer.close(index);
            });
          } else if(obj.event === 'record') {
              layer.msg("这是记录按钮功能测试。")
          }
        });
    });
</script>
```

**编辑和删除操作实现**

监听行工具事件函数第一个参数obj是当前行所有数据，可以console.log(obj)查看。

既然能拿到该行数据，实现删除就简单多了，只需要把这行ID或者其他列值传递给服务端即可。

实现思路：

- 删除按钮，前端ajax DELETE提交当前行ID到服务端接口
- 编辑按钮，以修改邮箱为例，前端ajax PUT 提交当前行ID和弹出框输入的信息到服务端接口
- 回调：根据不同状态，使用layer提示框
- 服务端一个函数视图实现增删改查，即GET/POST/PUT/DELETE

常见HTTP操作方法：

| **HTTP**方法 | **数据处理** | **说明**                                       |
| ------------ | ------------ | ---------------------------------------------- |
| POST         | 新增         | 新增一个没有id的资源                           |
| GET          | 获取         | 取得一个资源                                   |
| PUT          | 更新         | 更新一个资源。或新增一个含id资源(如果id不存在) |
| DELETE       | 删除         | 删除一个资源                                   |

前端代码示例：

```
<table class="layui-hide" id="demo" lay-filter="test"></table>

<!--  头部工具栏，左侧 -->
<script type="text/html" id="toolbarDemo">
  <div class="layui-btn-container">
    <button class="layui-btn layui-btn-sm" lay-event="getCheckData">获取选中行数据</button>
    <button class="layui-btn layui-btn-sm" lay-event="getCheckLength">获取选中数目</button>
    <button class="layui-btn layui-btn-sm" lay-event="isAll">验证是否全选</button>
  </div>
</script>

<!--  行工具 -->
<script type="text/html" id="barDemo">
  <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
  <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
</script>

<script>
layui.use(['table', 'layer'], function(){
  var table = layui.table;
  var layer = layui.layer;

  table.render({
    elem: '#demo'      // 选择元素
    ,url:'/myapp/user'   // JSON数据接口
    ,toolbar: '#toolbarDemo' // 开启左侧头部工具栏
    ,defaultToolbar: ['filter', 'exports', 'print', { // 启动右侧头部工具栏
      title: '提示'
      ,layEvent: 'LAYTABLE_TIPS'
      ,icon: 'layui-icon-tips'
    }]
    ,title: '用户数据表'
    ,cols: [[   // field 是JSON数据接口的键，必须要与JSON数据一致。title是列名称
      {type: 'checkbox', fixed: 'left'}  // 选中
      ,{field:'id', title:'ID', width:80, fixed: 'left', unresize: true, sort: true}
      ,{field:'username', title:'用户名', width:120, edit: 'text'}
      ,{field:'email', title:'邮箱',edit: 'text', templet: function(res){
        return '<em>'+ res.email +'</em>'
      }}
      ,{field:'sex', title:'性别', width:80, edit: 'text', sort: true}
      ,{fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
    ]]
    ,page: true  // 开启分页
  });

  //头工具栏事件，左侧
  table.on('toolbar(test)', function(obj){    // 这个test是lay-filter的值
    var checkStatus = table.checkStatus(obj.config.id);
    switch(obj.event){
      case 'getCheckData':
        var data = checkStatus.data;
        layer.alert(JSON.stringify(data));
      break;
      case 'getCheckLength':
        var data = checkStatus.data;
        layer.msg('选中了：'+ data.length + ' 个');
      break;
      case 'isAll':
        layer.msg(checkStatus.isAll ? '全选': '未全选');
      break;

      //自定义头工具栏右侧图标 - 提示
      case 'LAYTABLE_TIPS':
        layer.alert('这是工具栏右侧自定义的一个图标按钮');
      break;
    };
  });

  //监听行工具事件
  table.on('tool(test)', function(obj){
    var data = obj.data;
    console.log(data);
    if(obj.event === 'del'){
      layer.confirm('真的删除行么', function(index){
        // obj.del();  // 删除当前页面数据，届时ajax将数据id传服务端进行删除数据库
        // 这里是一个ajax请求
        var csrf_token = $("[name='csrfmiddlewaretoken']").val();
        var post_data = {'id': data.id, 'csrfmiddlewaretoken': csrf_token};
        $.ajax({
            type: "DELETE",
            url: "/myapp/user/",
            data: post_data,
            headers:{'X-CSRFToken': csrf_token},
            success: function (result) {
                if(result.code == '0'){
                    obj.del();  // 删除当前页面数据，届时ajax将数据id传服务端进行删除数据库
                    layer.msg(result.msg, {icon: 6,time: 1000})  // icon 6 微笑，time弹出时间，默认3秒，单位毫秒
                } else {
                    layer.msg(result.msg, {icon: 5})  // icon 5 哭泣
                }
            },
            error: function () {
                layer.msg("服务器接口异常！", {icon: 5})
            }
        });
        layer.close(index);  // 关闭layer层
      });
    } else if(obj.event === 'edit'){
      layer.prompt({
        formType: 2
        ,value: data.email   // 输入框的默认显示当前行email
      }, function(value, index){     // 函数第一个参数value是弹出框输入的值，第二个参数index是当前行ID
        var csrf_token = $("[name='csrfmiddlewaretoken']").val();
        var post_data = {'id': index, 'email': value};
        $.ajax({
            type: "PUT",
            url: "/myapp/user/",
            data: post_data,
            headers:{'X-CSRFToken': csrf_token},
            success: function (result) {
                if(result.code == '0'){
                    obj.update({
                      email: value
                    });
                    layer.msg(result.msg, {icon: 6,time: 1000})  // icon 6 微笑，time弹出时间，默认3秒，单位毫秒
                } else {
                    layer.msg(result.msg, {icon: 5})  // icon 5 哭泣
                }
            },
            error: function () {
                layer.msg("服务器接口异常！", {icon: 5})
            }
        });
        layer.close(index);
      });
    }
  });
});
</script>

```

服务端数据接口代码：

```
from django.http import QueryDict
 
def user(request):
    code = ""
    msg = ""
    # 模拟数据
    user = []
    for id in range(1, 100):
        import random
        name = random.sample(['龙', '妹', '东', '西', '南', '北'], 1)  # 返回列表
        name = '阿'+str(name[0])
        sex = random.sample(['男', '女'], 1)
        sex = sex[0]
        email = str(id) + '@aliangedu.com'
        row = {'id': id, 'username': name, 'sex': sex, 'email': email}
		user.append(row)
    if request.method == "GET":
        # 查询
        code = '0'
        msg = "获取数据成功."
        user = {'code': code, 'msg': msg, 'data': data }
        return JsonResponse(user)
    elif request.method == "POST":
        # 新增
        pass
    elif request.method == "PUT":
        # 更新
        PUT = QueryDict(request.body)    # 由于PUT和DELETE并没有像GET那种封装好的字典结果，需要我们手动处理request.body获取参数
        id = PUT.get('id')
        email = PUT.get('email')
        print(id,email)

        code = 0
        msg = "更新成功."
        result = {'code': code, 'msg': msg}
        return JsonResponse(result)
    elif request.method == "DELETE":
        # 删除
        DELETE = QueryDict(request.body)
        id = DELETE.get('id')
        print(id)
        
        code = 0
        msg = "删除成功."
        result = {'code': code, 'msg': msg}
        return JsonResponse(result)
    else:
        # 其他HTTP方法不允许
        code = "1"
        msg = "Method Not Allowed"
        result = {'code':code, 'msg': msg}
        return JsonResponse(result)
```

### 10.3 表格查询

#### 搜索关键字查询

思路：

1. 在已有的左侧位置创建input搜索框和button按钮
2. 使用jquery绑定按钮事件并获取input输入框值
3. 使用table.reload重载表格
4. 服务端接受url传参，根据搜索关键字返回数据

**1、增加搜索框**

```
<!--  头部工具栏，左侧 -->
<script type="text/html" id="toolbarDemo">

    <a href="#" class="layui-btn" style="float: left;margin-right: 50px">创建</a>
    <input type="text" name="username" lay-verify="title" placeholder="请输入用户名" class="layui-input" style="width: 150px;float: left">
    <button class="layui-btn" id="searchBtn" style="float: left">搜索</button>

</script>
```

**2、给表格设置ID**

```
table.render({
elem: '#id'
,cols: [] //设置表头
,url: '/api/data' //设置异步接口
,id: 'TT'
}); 
```

**3、监听搜索按钮事件与表格重载**

表格重载其实就是重新从后端获取数据，刷新表格。

在layui.use函数里增加：

```
$(document).on('click','#searchBtn', function () {
    var input_val = $('.layui-input').val();
// var input_val = $("input[name='username']").val();
    table.reload('TT', {
        where: {   //设定异步数据接口的额外参数，任意设置
            key: input_val
        },
        page: {
            curr: 1  //重新从第 1 页开始
        }
    })
})
```

**4、服务端数据接口**

```
def user(request):
    code = ""
    msg = ""
    if request.method == "GET":
        # 模拟数据
        user = []
        for id in range(1, 100):
            import random
            name = random.sample(['龙', '妹', '东', '西', '南', '北'], 1)  # 返回列表
            name = '阿'+str(name[0])
            sex = random.sample(['男', '女'], 1)
            sex = sex[0]
            email = str(id) + '@ctnrs.com'
            row = {'id': id, 'username': name, 'sex': sex, 'email': email}

            # 根据查询关键字返回数据（如果请求带搜索关键字，那这个条件在生成数据时就应该包含进去）
            search_key = request.GET.get("key", None)
            if search_key:
                if search_key == name:   # == 换成 in 则为模糊查询
                    user.append(row)
            else:
                user.append(row)

        # 分页
        page = int(request.GET.get('page', 1))   # 当前页，第几页
        limit = int(request.GET.get('limit'))  # 当前页数量，在table.render参数配置，默认10
        start = (page - 1) * limit  # 获取上一页的最后一个数
        end = page * limit
        data = user[start:end]

        code = '0'
        msg = "获取数据成功."
        count = len(user)
        user = {'code': code, 'msg': msg, 'count': count, 'data': data }
        return JsonResponse(user)
```

#### 选择框查询

与上面思路一样。增加选择框，根据已有的信息选择，这里是性别为例。

**1、增加选择框**

```
<!--  头部工具栏，左侧 -->
<script type="text/html" id="toolbarDemo">

    <a href="#" class="layui-btn" style="float: left;margin-right: 50px">创建</a>

    <label class="layui-form-label" style="width: 100px">性别</label>
    <div class="layui-input-inline" style="float: left;margin-right: 50px">
        <select name="sex" lay-verify="required" lay-search="" lay-filter="sex">
              <option value="">直接选择或搜索选择</option>
              {% for i in user_sex %}
              <option value="{{ i }}">{{ i }}</option>
              {% endfor %}
        </select>
    </div>

    <input type="text" name="username" lay-verify="title" placeholder="请输入用户名" class="layui-input" style="width: 150px;float: left">
    <button class="layui-btn" id="searchBtn" style="float: left">搜索</button>

</script>
```

**2、表单（选择框）事件监听**

```
form.on('select(sex)', function (data) {
    var select_val = data.value;
    table.reload('TT', {
        where: {   //设定异步数据接口的额外参数，任意设置
            sex: select_val
        },
        page: {
            curr: 1  //重新从第 1 页开始
        }
    });
})
```

3、服务端数据接口

在页面函数视图：

```
def index(request):
    user_sex = ['男','女']
    return render(request, 'index.html', {'user_sex': user_sex})
```

在接口函数视图：

```
def user(request):
    code = ""
    msg = ""
    if request.method == "GET":
        # 模拟数据
        user = []
        search_key = request.GET.get("key", None)
        select_sex = request.GET.get('sex', None)
        for id in range(1, 100):
            import random
            name = random.sample(['龙', '妹', '东', '西', '南', '北'], 1)  # 返回列表
            name = '阿'+str(name[0])
            sex = random.sample(['男', '女'], 1)
            sex = sex[0]
            email = str(id) + '@ctnrs.com'
            row = {'id': id, 'username': name, 'sex': sex, 'email': email}

            # 根据查询关键字返回数据（如果请求带搜索关键字，那这个条件在生成数据时就应该包含进去）
            if search_key and select_sex:   # 如果两个条件都满足
                if search_key == name and select_sex == sex:
                    user.append(row)
            elif search_key:     # 满足一个条件
                if search_key == name:
                    user.append(row)
            elif select_sex:
                if select_sex == sex:
                    user.append(row)
            else:  # 默认打开页面都不满足上面条件
                user.append(row)

        # 分页
        page = int(request.GET.get('page', 1))   # 当前页，第几页
        limit = int(request.GET.get('limit'))  # 当前页数量，在table.render参数配置，默认10
        start = (page - 1) * limit  # 获取上一页的最后一个数
        end = page * limit
        data = user[start:end]

        code = '0'
        msg = "获取数据成功."
        count = len(user)
        user = {'code': code, 'msg': msg, 'count': count, 'data': data }
        return JsonResponse(user)
```

### 10.4 数据表格内容美化

在默认情况下，单元格的内容是完全按照数据接口返回的content原样输出的，如果你想对某列的单元格添加链接等其它元素，你可以借助该参数来轻松实现。这是一个非常实用且强大的功能，你的表格内容会因此而丰富多样。

代码示例：

```
table.render({
  cols: [[
    {field:'title', title: '文章标题', width: 200
      ,templet: function(d){
        return 'ID：'+ d.id +'，标题：<span style="color: #c00;">'+ d.title +'</span>'
      }
    }
    ,{field:'id', title:'ID', width:100}
  ]]
});   
```

或者定义函数

```
// 数据表格指定函数
,{field:'sex', title:'性别', templet: sexFormat}

// 定义处理表格内容函数
function sexFormat(d) {
    if(d.sex == "女") {
        return '<span style="color: red">' + d.sex + '<span>'
    } else {
        return '<span style="color: blue">' + d.sex + '<span>'
    }
}
```

## 11、弹出层

layer几种类型：

- layer.msg：提示框
- layer.open：又支持几种常用类型
  - 0：信息框，默认，输出一个文本

  - 1：页面层，输出一段HTML内容

  - 2：内嵌层，加载网址

提示框：

```
layer.msg('提示框', {icon: 6});
```

信息框：

```
<button type="submit" class="layui-btn" id="btn">弹出</button>

<script>
layui.use(['layer'], function () {
    var layer = layui.layer;
    var $ = layui.jquery;

    $(document).on('click','#btn',function () {
        layer.open({
          type: 0,
          content: '<span style="color: red">这是一个普通的文本<span>' // 字符串或者HTML
        });
    });
})
</script>
```

页面层：

```
<button type="submit" class="layui-btn" id="btn">弹出</button>

<script>
layui.use(['layer'], function () {
    var layer = layui.layer;
    var $ = layui.jquery;

    $(document).on('click','#btn',function () { 
        layer.open({
          type: 1,
          content: $('#test')
        });
    });
})
</script>
```

内嵌层：

```
<script>
    layui.use(['layer'], function(){
          // Layui 的模块
          var layer = layui.layer;
          var $ = layui.jquery;
          $('#btn').click(function () {
              layer.open({
                  type: 2,  // 层类型
                  title: ['弹窗名称', 'font-size:18px;'],
                  area: ['60%', '40%'], // 或者是像素
                  content: 'http://www.baidu.com'
                });
          })
    });
</script>
```

