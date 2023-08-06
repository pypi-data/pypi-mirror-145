from warnings import warn
from .pure import *


def version():
    """
    * 2021/3/14
    - [pypi_url](https://pypi.org/project/bddjango/)

    # 2.2
        - 方法version转移到__init__.py中
        - 修改由`get_key_from_query_dc_or_self`引起的bug
        - 高级检索类增加`search_ls_dc`和`search_conf`两个参数
        - 修改由于readme.md出错导致pypi上传失败的bug	# 2.2.2
        - 去掉部分print	# 2.2.3
        - 新增conv_to_queryset方法	# 2.2.3
        - 修复部分bug	# 2.2.4
    """
    v = "2.2.4"     # 正式版: 2.2.4
    return v


try:
    from .django import *
except Exception as e:
    warn('导入django失败? --- ' + str(e))

try:
    from .myFIelds import AliasField        # 这个只能在这里引用, 不然`adminclass`报错
except Exception as e:
    warn('导入`AliasField`失败? --- ' + str(e))

