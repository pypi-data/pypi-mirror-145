luckdog  新版本已经出来了

luckdog是类似于postman的接口访问工具。

#######################################################################

Last update time: 2020-04-20 
By： 8034.com

#######################################################################

更新日志：
2022-04-02  增加断言

#######################################################################

    ## 打包 检查
    python setup.py check 
    ## 打包 生成
    python setup.py sdist
    ## 上传
    twine upload -u uu -p DD dist/*
    ## 使用
    pip install luckdog 
    ## 更新
    pip install --upgrade luckdog
    ## 卸载
    pip uninstall -y luckdog 
#######################################################################

## MANIFEST.in 

    include pat1 pat2 ...   #include all files matching any of the listed patterns

    exclude pat1 pat2 ...   #exclude all files matching any of the listed patterns

    recursive-include dir pat1 pat2 ...  #include all files under dir matching any of the listed patterns

    recursive-exclude dir pat1 pat2 ... #exclude all files under dir matching any of the listed patterns

    global-include pat1 pat2 ...    #include all files anywhere in the source tree 
    matching — & any of the listed patterns

    global-exclude pat1 pat2 ...    #exclude all files anywhere in the source tree matching — & any of the listed patterns

    prune dir   #exclude all files under dir

    graft dir   #include all files under dir
