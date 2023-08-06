import os
import streamlit as st
import streamlit.components.v1 as components
from typing import List

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


def button_bar(options, index=0, format_func=str, key=None, icons: List[str] = '', bs_classes: List[str] = '',
               align: str = None):
    key = st.type_util.to_key(key)
    opt = st.type_util.ensure_indexable(options)

    idx = _btn_select(
        options=[str(format_func(option)) for option in opt],
        default=index,
        key=key,
        icons=icons,
        bs_classes=['btn-default'] * len(options) if bs_classes == '' else bs_classes,
        align=align
    )

    return opt[idx]


if __name__ == '__main__':
    st.title('Button Bar Example')
    st.button('streamlit button 1')
    st.button('streamlit button 2')
    st.button('streamlit button 3')
    page = button_bar(
        ('add', 'remove', 'modify'),
        format_func=lambda x: x.capitalize(),
        icons=['square-plus', 'trash', 'screwdriver-wrench'],
    )
    st.write(page)
    st.title('flex-end')
    button_bar(
        ('add', 'remove', 'modify'),
        format_func=lambda x: x.capitalize(),
        icons=['square-plus', 'trash', 'screwdriver-wrench'],
        bs_classes=['btn-info', 'btn-outline-info', 'btn-primary'],
        align='flex-end'
    )
    st.title('center')
    button_bar(
        ('add', 'remove', 'modify'),
        format_func=lambda x: x.capitalize(),
        icons=['fa-brands fa-alipay', 'trash', 'screwdriver-wrench'],
        align='center'
    )
    st.title('space-around')
    button_bar(
        ('alipay', 'apple', 'bootstrap'),
        format_func=lambda x: x.capitalize(),
        icons=['fa-brands fa-alipay', 'fa-brands fa-apple', 'fa-brands fa-bootstrap'],
        align='space-around'
    )
