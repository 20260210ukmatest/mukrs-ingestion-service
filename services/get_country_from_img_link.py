from bs4 import Tag

def get_country_from_img_link(parent: Tag):
    img_tag = parent.select_one('img') 
    if img_tag is None:
        return None
    src_attr = img_tag.attrs.get('src')
    if type(src_attr) is not str:
        return None
    return src_attr.split('/')[-1].split('.')[0] or None