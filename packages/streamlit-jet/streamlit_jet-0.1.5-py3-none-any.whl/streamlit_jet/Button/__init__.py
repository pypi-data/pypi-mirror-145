import os
import streamlit as st
import streamlit.components.v1 as components

__all__ = ['button']
__RELEASE = True

if not __RELEASE:
    _btn = components.declare_component(
        "btn_select",
        url="http://localhost:3001",
    )
else:
    _btn = components.declare_component(
        "btn_select",
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/build"),
    )


def button(label: str, key=None, icon: str = '', icon_left: bool = True, bs_class: str = ''):
    if icon_left:
        left, right = 'unset', 'none'
    else:
        left, right = 'none', 'unset'
    value = _btn(
        label=label,
        key=key,
        icon=icon,
        left=left,
        right=right,
        default=False,
        bs_class=bs_class if bs_class != '' else 'btn-default'
    )
    return value


if __name__ == '__main__':
    st.title('Button Example')
    sv = st.button('streamlit button')
    st.write(sv)
    st.header('boostrap button')
    v = button('streamlit style button')
    st.write(v)
    with st.container():
        st.text_input('username')
        st.text_input('password')
        button('Login', icon='right-to-bracket', icon_left=False, bs_class='btn-info w-100 m-1 mr-10')
    button('bs icon button', icon='gear', bs_class='btn-info m-1')
    button('bs icon button', icon='fa-brands fa-bootstrap')
    button('bs style button', bs_class='btn-primary')
    button('bs style button', bs_class='btn-outline-primary')
    button('bs style button', bs_class='btn-secondary')
    button('bs style button', bs_class='btn-success')
    button('bs style button', bs_class='btn-danger')
    button('bs style button', bs_class='btn-info')
    button('bs style button', bs_class='btn-dark')
