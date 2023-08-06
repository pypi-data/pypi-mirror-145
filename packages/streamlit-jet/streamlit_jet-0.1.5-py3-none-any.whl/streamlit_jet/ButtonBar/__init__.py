import os
import streamlit as st
import streamlit.components.v1 as components
from typing import List, Iterable, Union

__all__ = ['button_bar']
__RELEASE = True

if not __RELEASE:
    _btn_select = components.declare_component(
        "btn_select",
        url="http://localhost:3001",
    )

else:
    _btn_select = components.declare_component(
        "btn_select",
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/build"),
    )


def button_bar(options: Iterable[str],
               index=0,
               format_func=str,
               key=None,
               btn_icons: Union[str, List[str]] = None,
               btn_classes: Union[str, List[str]] = None,
               classes: str = None):
    """按钮栏

    :param options: 选项
    :param index: 默认索引,为None时表示无默认索引,返回None
    :param format_func: 选项格式化函数
    :param key: 组件key
    :param btn_icons: 按钮图标，为list时需要与options等长
    :param btn_classes: 按钮bootstrap类，为list时需要与options等长
    :param classes: 按钮栏的bootstrap类
    """
    n = len(options)
    if isinstance(btn_icons, list):
        if len(btn_icons) != n:
            raise ValueError('btn_icons length not equal options')
    elif isinstance(btn_icons, str):
        btn_icons = [btn_icons] * n
    else:
        btn_icons = ''
    if isinstance(btn_classes, list):
        if len(btn_classes) != n:
            raise ValueError('btn_icons length not equal options')
    elif isinstance(btn_classes, str):
        btn_classes = [btn_classes] * n
    else:
        btn_classes = ['btn-default'] * len(options)
    if classes is None:
        classes = ''

    key = st.type_util.to_key(key)
    opt = st.type_util.ensure_indexable(options)

    idx = _btn_select(
        options=[str(format_func(option)) for option in opt],
        default=index,  # must set as default in frontend
        key=key,
        btn_icons=btn_icons,
        btn_classes=btn_classes,
        classes=classes
    )
    if idx is None:
        return None
    else:
        return opt[idx]


if __name__ == '__main__':
    st.title('Button Bar Example')
    st.header('streamlit button')
    st.button('streamlit button 1')
    st.button('streamlit button 2')
    st.button('streamlit button 3')
    st.header('bootstrap button bar')
    v = button_bar(('new', 'stop'))
    st.write(v)
    button_bar(('new', 'stop'), btn_icons=['plus', 'stop'], index=1)
    a=button_bar(('new', 'stop','del'), btn_icons=['plus', 'stop','trash'],
                 btn_classes=['btn-info', 'btn-danger','btn-warning'],index=None)
    st.write(a)
    button_bar(('new', 'stop'), btn_icons=['plus', 'stop'], classes='justify-content-center')
    button_bar(('new', 'stop'), btn_icons=['plus', 'stop'], classes='justify-content-end')
    # button_bar(('new', 'stop'), btn_icons=['plus', 'stop'], classes='justify-content-between')
