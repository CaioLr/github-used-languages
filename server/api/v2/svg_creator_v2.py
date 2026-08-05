import base64
import math

import requests

from .ascii_transformer import image_to_ascii


def language_list(complete_percentage_usage: list, colors: dict) -> str:

    list = ""
    y = 10
    count = 1

    for item in complete_percentage_usage[:5]:

        if not item:
            break
        if item:
            list += f"""
                <text x="25" y="{y-1}" fill="{colors['percentage_color']}" font-size="9"  font-family="monospace">
                    #{count}
                </text>
                <text x="40" y="{y}" font-size="12"  font-family="monospace">
                    <tspan fill="{colors['terminal_color']}">{item[0]}   </tspan>
                    <tspan fill="{colors['percentage_color']}" dx="5" font-weight="bold">{round(item[1])}%</tspan>
                </text>
            """
            y += 20
            count+=1

    y = 10

    for item in complete_percentage_usage[5:10]:

        if not item:
            break
        if item:
            list += f"""
                <text x="165" y="{y-1}" fill="{colors['percentage_color']}" font-size="9"  font-family="monospace">
                    #{count}
                </text>
                <text x="185" y="{y}" font-size="12"  font-family="monospace">
                    <tspan fill="{colors['terminal_color']}">{item[0]}</tspan>
                    <tspan fill="{colors['percentage_color']}" dx="5" font-weight="bold">{round(item[1])}%</tspan>
                </text>
            """
            y += 20
            count+=1

    return list

def custom_info(config: dict, colors: dict) -> list[int|str]:
    if 'custom_info' in config['v2'] and config['v2']['custom_info'] is not None:
        y =0
        svg_text = ""

        for key, value in config['v2']['custom_info'].items():
            svg_text += f"""
            <text x="22" y="{y}" font-size="12" font-family="monospace">
                <tspan fill="{colors['terminal_color']}">{key}:</tspan>
                <tspan fill="{colors['text_color']}">{value}</tspan>
            </text>
            """
            y+= 15

        y+= 75

        return [y, svg_text]

    return [55,""]

def horizontal_stacked_bar(
    data: list
) -> str:

    width: int = 250
    height: int = 4
    rx: float = 4.0

    svg = f'<svg x="22" y="120" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="overflow: hidden; border-radius: {rx}px;">\n'
    offset_x = 0

    for item in data:
        percentage = item[1]
        color = item[2]

        rect_width = width * (percentage / 100)

        final_x = offset_x

        svg += f"""  <rect x="{final_x}" y="0" width="{rect_width:.2f}" height="{height}" fill="{color}">
    <animate attributeName="width" from="0" to="{rect_width:.2f}" dur="1.5s" calcMode="spline" keySplines="0.4 0 0.2 1" fill="freeze" />
    </rect>\n"""

        offset_x += rect_width

    svg += "</svg>"
    return svg

def create_svg(percentage_usage: list, config: dict, colors: dict, complete_percentage_usage: list, ascii_type: str, ascii_size: int|None) -> str:

    custom_info_result = custom_info(config, colors)
    y = custom_info_result[0]
    svg_text = custom_info_result[1]

    if ascii_size is None:
        ascii_size = 50

    if config['custom_image'] != "":
        ascii_art = image_to_ascii(config['custom_image'],colors['background_color'], ascii_type, ascii_size)
    else:
        ascii_art = image_to_ascii(complete_percentage_usage[0][3],colors['background_color'], ascii_type, ascii_size)

    ascii_art = ascii_art.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    svg = f"""
    <svg width="550" height="300" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 550 300" fill="none">
       <rect width="550" height="300" fill="{colors['background_color']}" stroke="{colors['border_color']}" stroke-width="1" stroke-opacity="1" rx="5"/>
       <g transform="translate(0, 15)">
            <text
                x="22"
                y="12"
                font-size="12"
                font-family="monospace"
            >
                <tspan fill="{colors['terminal_color']}">
                    {config['v2']['v2_terminal_user']}@{config['v2']['v2_terminal_hostname']}:
                </tspan>
                <tspan fill="{colors['title_color']}">
                    neofetch
                </tspan>
            </text>
       </g>

        <g transform="translate(20, 45)">
            <svg x="0" y="0" width="200" height="200" viewBox="0 0 200 200">
                <defs>
                    <clipPath id="circleView">
                    <circle cx="100" cy="100" r="100" />
                    </clipPath>
                </defs>
                <image x="0" y="0" width="200" href="{ascii_art}" clip-path="url(#circleView)"/>
            </svg>
        </g>

        <g transform="translate(225, 55)">
            {svg_text}
        </g>

        <g transform="translate(225, {y})">
            <text x="22" y="0" fill="{colors['title_color']}" font-size="12" font-family="monospace">Most Used Languages</text>
            <svg x="0" y="15" width="280" height="180" viewBox="0 0 280 180">

                {language_list(complete_percentage_usage, colors)}


            </svg>

            {horizontal_stacked_bar(complete_percentage_usage)}

        </g>





     </svg>

    """

    return svg

def get_svg(percentage_usage: list, config: dict, colors: dict, ascii_type: str, ascii_size: int|None) -> list[str,str]:

    color = {lang["name"]: lang["color"] for lang in config["languages"]}
    image = {lang["name"]: base64.b64encode(requests.get(lang["image"]).content).decode('utf-8') for lang in config["languages"]}
    content_type = {lang["name"]: requests.get(lang["image"]).headers["Content-Type"] for lang in config["languages"]}

    # list comprehension
    complete_percentage_usage = [
        (name, percent, color.get(name), image.get(name), content_type.get(name))
        for name, percent in percentage_usage
    ]

    svg_pair = (create_svg(percentage_usage, config, colors[0], complete_percentage_usage, ascii_type, ascii_size), create_svg(percentage_usage, config, colors[1], complete_percentage_usage, ascii_type, ascii_size))

    return svg_pair
