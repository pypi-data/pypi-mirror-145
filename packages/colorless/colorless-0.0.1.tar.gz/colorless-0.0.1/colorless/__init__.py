import requests
from bs4 import BeautifulSoup
import colorsys

def rgb_to_hex(rgb):
    """
    >>> rgb_to_hex((255, 255, 195))
    'ffffc3'
    """
    return '%02x%02x%02x' % rgb


def apply_formatting(col, hex_colors):
    for hex_color in hex_colors:
        if col.name == hex_color:
            return [f'background-color: {hex_color}' for c in col.values]


def display_hex_colors(hex_colors):
    """Display list of colors in jupyter notebook.
    >>> hex_list = ['#FFFFFF', '#F0F0F0', '#FCF0D8', '#fdd8a7', '#fdc38d', '#fca16c']
    >>> display_hex_colors(hex_list)
    """
    import pandas as pd
    hex_colors = [c.upper() for c in hex_colors]
    df = pd.DataFrame(hex_colors).T
    df.columns = hex_colors
    df.iloc[0,0:len(hex_colors)] = "<br><br><br>"
    display(df.style.apply(lambda x: apply_formatting(x, hex_colors)).hide_index())


def slurp(url, encoding='utf8'):
    response = requests.get(url)
    bsoup = BeautifulSoup(response.content.decode(encoding), features="lxml")
    return bsoup


def wiki_colors(with_links=False):
    a_to_f = 'https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F'
    g_to_m = 'https://en.wikipedia.org/wiki/List_of_colors:_G%E2%80%93M'
    n_to_z = 'https://en.wikipedia.org/wiki/List_of_colors:_N%E2%80%93Z'

    colors = {}

    for url in [a_to_f, g_to_m, n_to_z]:
        bsoup = slurp(url)
        headers = []
        table = bsoup.find('table')
        for tr in table.find_all('tr'):
            if 'id' in tr.attrs:
                continue
            if not tr.find('th').find('a') and not headers:
                headers = [th.text.strip() for th in tr.find_all('th')]
                continue
            # Row data.
            row = {h:td.text.strip() for h, td in zip(headers[1:], tr.find_all('td'))}
            # Row header.
            name = tr.find('th').text.strip()
            row['href'] = tr.find('th').find('a').attrs['href']
            row['name'] = name
            colors[name] = row

    for n, c in colors.items():
        new_color = {}
        new_color['name'] = c['name']
        # Parse rgb
        rgb = [c['Red (RGB)'], c['Green (RGB)'], c['Blue (RGB)']]
        new_color['rgb'] = tuple(int(s.strip('%')) for s in rgb)
        # Parse hsv
        #new_color['hsv'] = c['Hue (HSL/HSV)'], c['Satur. (HSV)'], c['Value (HSV)']
        #new_color['hsl'] = c['Hue (HSL/HSV)'], c['Satur. (HSL)'], c['Light (HSL)']
        #new_color['hex'] = c['Hex (RGB)']
        if with_links:
            new_color['wiki_url'] = "https://en.wikipedia.org" + c['href']
        colors[n] = new_color
    return colors


def novact_colors(url="http://www.novact.info/id40.html"):
    colors = {}
    bsoup = slurp(url)
    table = bsoup.find('tbody')
    headers = table.find_all('tr')[0].get_text('\t').replace('\n', ' ').split('\t')
    for tr in table.find_all('tr')[1:]:
        n, h, r = tr.get_text('\t').replace('\n', ' ').split('\t')
        n = ' '.join(n.split())
        h = ' '.join(h.split())
        r = ' '.join(r.split())
        colors[n] = dict(zip(headers, (n,h,r)))

    for n, c in colors.items():
        new_color = {}
        new_color['name'] = c['Name']
        new_color['rgb'] = tuple(int(i) for i in c['RGB'].split(','))
        colors[n] = new_color
    return colors


def html_colors(url='https://htmlcolorcodes.com/colors/'):
    bsoup = slurp(url)
    colors = {}
    for i, tr in enumerate(bsoup.find_all('tr')):
        try:
            _, color_name, color_hex, color_rgb = [td.text.strip() for td in tr.find_all('td')]
            colors[color_name] = {'name':color_name , 'hex': color_hex, 'rgb': color_rgb}
        except ValueError:
            continue
    for n, c in colors.items():
        new_color = {}
        new_color['name'] = c['name']
        new_color['rgb'] = tuple(int(i) for i in c['rgb'][4:-1].split(','))
        colors[n] = new_color
    return colors
