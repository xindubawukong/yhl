### 使用方法

1. 安装`mongnodb`, `pymongo`, `django==1.11` 等依赖库

2. `mongod --dbpath + 数据库路径` 新建一个mongodb数据库
3. 运行`python mongo_initial.py` 初始化数据库
4. 运行`python manage.py runserver 8000`，在`127.0.0.1:8000`端口即可访问网页
5. 点击左上角选择文件（如`IMPFCS`目录下的`flow_layer`文件），再点击上传文件
6. 选择右上角的`Flow Layer`或`Control Layer`即可查看图片
7. 点击下方绿色按钮可实现放大、缩小、下载等功能



### 注意事项

- 由于我没有搞懂这个网页要展示的东西怎么用，只是简单修改了一下，暂时没有动拖拽功能的代码，没有测试能否拖拽
- 当时王钦学长给的测试文件里`flow_layer`文件似乎不全，不能显示control layer。具体数据上传格式还要咨询一下他。





丁相允

2018.10.11

