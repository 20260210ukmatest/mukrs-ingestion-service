def get_country_from_img_link(parent):
    return (img := parent.find('img')) and img.attrs['src'].split('/')[-1].split('.')[0] or None