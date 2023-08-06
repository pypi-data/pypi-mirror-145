from potion.objects import *
from potion.api import *
from potion import Request
import os


class NotionPage:
    def __init__(self, auth, page_id=None, parent: Parent = None):
        self.req = Request.from_token(authorization=auth)
        self.auth = auth
        if page_id is None:
            assert parent is not None
            res = self.req.post(page_create(), data=Page(parent=parent, properties=Properties()))
            if isinstance(res, Page):
                page_id = res.id
            else:
                assert False, res.to_json(2)

        else:
            res = self.req.get(page_retrieve(page_id))
            assert isinstance(res, Page), res.to_json(2)
        self.page_id = page_id
        print(page_id)
        self.page_object = res
        self.blocks = {}

        self.properties = []
        self.children = []
        self.multi_select_property = defaultdict(set)

    def flush_property(self):
        for property_name, values in self.multi_select_property.items():
            self.properties.append(prop.MultiSelect(property_name, selects=[
                prop.Select(None, name=v) for v in values
            ]))

        page = Page(properties=Properties(*self.properties))
        res = self.req.patch(
            url=page_update(self.page_id),
            data=page
        )
        self.properties.clear()
        if isinstance(res, NotionError):
            print(res)
        return res

    def flush_children(self):
        page = Page(children=self.children)
        res = self.req.patch(
            url=block_children_append(self.page_id),
            data=page
        )
        self.children.clear()
        if isinstance(res, NotionError):
            print(res)
        return res

    def append_code(self, code, language='python', usage=None):
        self.children.append(block.Code(rich_text=[rich.Text(code)], language=language))

    def set_title(self, property_name, value):
        self.properties.append(prop.Title(property_name,
                                          rich_text=[rich.Text(content=value)]))

    def set_text(self, property_name, value):
        self.properties.append(RichTextProp(property_name,
                                            rich_text=[rich.Text(content=value)]))

    def set_duration(self, property_name: str, start: datetime = None, end: datetime = None):
        self.properties.append(Date(property_name, start=start, end=end))

    def set_checkbox(self, property_name: str, checkbox=True):
        self.properties.append(prop.CheckBox(property_name, checkbox))

    def set_number(self, property_name: str, number):
        self.properties.append(prop.Number(property_name, number))

    def add_option(self, property_name, value):
        self.multi_select_property[property_name].add(value)
        self.properties.append(prop.MultiSelect(pname=property_name, selects=[
            prop.Select(None, name=value)
        ]))

    def remove_option(self, property_name, value):
        if value in self.multi_select_property[property_name]:
            self.multi_select_property[property_name].remove(value)
