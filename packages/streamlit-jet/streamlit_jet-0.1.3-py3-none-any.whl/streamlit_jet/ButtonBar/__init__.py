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

    _btn_select_nav = components.declare_component(
        "btn_select_nav",
        url="http://localhost:3001",
    )
else:
    _btn_select = components.declare_component(
        "btn_select",
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/build"),
    )

    _btn_select_nav = components.declare_component(
        "btn_select_nav",
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/build"),
    )


def button_bar(options, index=0, format_func=str, nav=False, key=None, icons: List[str] = '', align: str = None):
    key = st.type_util.to_key(key)
    opt = st.type_util.ensure_indexable(options)

    if nav:
        st.markdown(
            """
                <style>
                iframe[title="st_btn_select.btn_select_nav"] {
                    position: fixed;
                    top: 0;
                    z-index: 1;
                }
                </style>
            """,
            unsafe_allow_html=True,
        )

        idx = _btn_select_nav(
            options=[str(format_func(option)) for option in opt],
            default=index,
            nav=nav,
            key=key,
            icons=icons,
            align=align
        )
    else:
        idx = _btn_select(
            options=[str(format_func(option)) for option in opt],
            default=index,
            nav=nav,
            key=key,
            icons=icons,
            align=align
        )

    return opt[idx]


if __name__ == '__main__':
    st.title('Button Bar Example')
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
        align='flex-end'
    )
    st.title('center')
    button_bar(
        ('add', 'remove', 'modify'),
        format_func=lambda x: x.capitalize(),
        icons=['square-plus', 'trash', 'screwdriver-wrench'],
        align='center'
    )
    st.title('space-around')
    button_bar(
        ('add', 'remove', 'modify'),
        format_func=lambda x: x.capitalize(),
        icons=['square-plus', 'trash', 'screwdriver-wrench'],
        align='space-around'
    )
