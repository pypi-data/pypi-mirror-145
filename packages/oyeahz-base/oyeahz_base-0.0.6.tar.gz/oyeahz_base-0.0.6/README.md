# oyeahz_base
##简介
基础组件
##配置项目
###步骤1
1、创建一个目录，作为发布项目的名称，即你的包名

2、目录里创建一个py文件 \_\_init__.py，内容name = "your pkg name"

3、目录里创建对外输出的python文件

4、拷贝一份setup.py文件，并修改关键参数

        1、name就是模块名
        2、version就是版本号
        3、packages数组填模块名，上传到仓库的配置主要是这个
        
5、拷贝一份.gitignore和deploy.sh
        
####步骤2
1、python3 -m pip install setuptools wheel twine

2、python setup.py sdist bdist_wheel

3、如果报错 pip3 install wheel , pip3 install twine

4、python3 -m twine upload dist/*

####步骤3
升级发布的话直接修改setup.py里的version后sh deploy.sh