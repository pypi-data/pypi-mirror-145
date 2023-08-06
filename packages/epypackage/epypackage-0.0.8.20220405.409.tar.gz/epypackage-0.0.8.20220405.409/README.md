由于没学会git合并~~~

在原模块上进行添加pyefun

修改 code version

两个打包命令二选一
py -m build
python setup.py sdist

有坑 要先上传测试 在上传正式 要不然不知道为什么找不到模块
要是报错升级下
pip install pyOpenSSL ndg-httpsclient pyasn1

py -m twine upload --repository testpypi dist/*
py -m twine upload --repository pypi dist/*

上传完成后等待一下在安装 更新不及时

pip install epypackage==0.0.7.20220330.537