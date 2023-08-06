import os
import streamlit.components.v1 as components
from dataclasses import dataclass
from typing import List
import streamlit as st

IS_RELEASE = True
if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("tab_bar", path=build_path)
else:
    _component_func = components.declare_component("tab_bar", url="http://localhost:3000")


@dataclass(frozen=True, order=True, unsafe_hash=True)
class TabBarItemData:
    id: int
    title: str
    description: str = ''
    icon: str = ''

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "icon": self.icon}


def tab_bar(data: List[TabBarItemData], default=None, return_type=str, key=None):
    data = list(map(lambda item: item.to_dict(), data))
    component_value = _component_func(data=data, selectedId=default, key=key, default=default)

    try:
        if return_type == str:
            return str(component_value)
        elif return_type == int:
            return int(component_value)
        elif return_type == float:
            return float(component_value)
    except:
        return component_value


if __name__ == '__main__':
    # test component
    st.title('tab bar')
    tab_id = tab_bar(data=[
        TabBarItemData(id=1, title="数据", icon='home'),
        TabBarItemData(id=2, title="表格", icon='gear'),
        TabBarItemData(id=3, title="small", icon='coffee'),
        TabBarItemData(id=4, title="BIG", ),
    ], default=1, return_type=int)
    st.info(f'select tab id is : **{tab_id}**')
    if tab_id == 1:
        st.button('button')
        st.markdown('---')
        st.info('tab 1 page')
    elif tab_id == 2:
        st.warning('tab 2 page')
    else:
        st.success('tab 3 page')
