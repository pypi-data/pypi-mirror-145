from warnings import warn
from .pure import *


def version():
    """
    * 2021/3/14
    - [pypi_url](https://pypi.org/project/bddjango/)

    # 党史项目结束, 海南项目开始

    ## 2.1修改部分
        - 修复了AdvancedSearchView post时page_size失效的问题     # 2.1.1
        - 对`list`的数据返回格式进行了优化, 避免了自定义page_size时无效的bug
        - `BaseListView`增加`set_request_data`方法
        - 优化`distince_type_ls`和`order_type_ls`的错误提示
        - `AdvancedSearchView`增加`Q_add_ls`检索方法      # 2.1.2
        - `.pure`增加`convert_query_parameter_to_bool`函数
        - '.django'增加`update_none_to_zero_by_field_name`函数
        - 增加`AliasField`绑定字段方法      # 2.1.3
        - 按年份分布的统计方法`get_df_by_freq_and_year`       # 2.1.4
        - 修复distinct_field_ls和order_type_ls的冲突      # 2.1.5
        - BaseListView中, 加入'pk'作为默认过滤字段     # 2.1.6
        - template调整`simpleui_change_list_actions.html`样式
        - 新增`only_get_distinct_field`功能
        - 修复2.1.6版本忘记上传templates导致adminclass导入失败问题      # 2.1.7
        - 修复了`BaseListView`的list方法中`get_serializer_context`无效的问题, 在`paginate_qsls_to_dcls`加入了`context`参数       # 2.1.8
        - 在`adminclass.remove_temp_file`方法中增加描述字段`desc`, 并增加部分debug说明文字
        - 前端可以控制`base_fields`参数, 但仅适用于`auto_generate_serializer`为`True`的情况
        - 加上`auth.MyValidationError`, 修复验证模块报错bug
        - 简化部分代码: 将(获取self.key or 获取query_dc.key)的方法统一  # 2.1.9
        - 修复`_get_key_from_query_dc_or_self`的关键bug!     # 2.1.10
        - 拓展`get_MySubQuery`方法, 对`annotate`生成的字段生效      # 2.1.11
        - 在`get_abs_order_type_ls`方法中处理str类型数据
        - 自动生成wiki打包autoWiki.py        # 2.1.12

    # 2.2
        - 方法version转移到__init__.py中
        - 修改由`get_key_from_query_dc_or_self`引起的bug
        - 高级检索类增加`search_ls_dc`和`search_conf`两个参数
        - 修改由于readme.md出错导致pypi上传失败的bug	# 2.2.2
        - 去掉部分print	# 2.2.3
    """
    v = "2.2.3"     # 正式版: 2.2.3
    return v


try:
    from .django import *
except Exception as e:
    warn('导入django失败? --- ' + str(e))

try:
    from .myFIelds import AliasField        # 这个只能在这里引用, 不然`adminclass`报错
except Exception as e:
    warn('导入`AliasField`失败? --- ' + str(e))

