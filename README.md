# ProjectCloud

[TOC]

## introduce

这是一个color网络架构下的简单网盘系统。

## schedule

- 2021.2.24 目前只包含前端几个页面以及一些简单的按钮逻辑。

dev分支修改了文件目录结构，PageUI将作为一个python包，SourceCode将包含源文件，其中color文件还需要进一步拆分（作为git练手，现阶段版本会多次提交）。

### 原color文件拆分

两部分，一是前后端分离，二是item缺少对应结构。

前后端分离基本结构是对于每个耗时操作编写对应线程类，通过参数传递和锁由子线程完成，完成后返回信号。

耗时操作：

- 撤销通告包 selectItem
- 撤销本地缓存 selectItem
- 删除item window.ui.treeWidget
- 双击items显示信息 
- 添加文件 window.ui.treeWidget
- 注册单个文件
- 注册多个文件
- 注册过程本体
- 获取单个文件数据
- 获取多个文件数据
- 获取数据本体
- 导入其他配置文件
- 保存配置文件
- 读取配置文件

不耗时操作：

- 打开仓库
- 打开命令行
- 打开视频页面
- 显示右键菜单栏
- 单击items选中
- 主窗体关闭事件

### 界面设计

#### 需求

1. 主界面网盘功能：添加（默认注册一条龙），下载，切换模式。
2. 注册子窗体指定路径等详细操作。

### 拆分model/view中遇到问题

一、使用qfilesystemmodel没法添加文件自定义属性，使用提供的函数修改也不行

二、使用qstandarditemmodel暂时无法和三个view联动

三、自己实现model如何重载data函数以应对三个view

采用一个data多个model、一个model一个view的方式实现