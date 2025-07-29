import base64, requests, math

def language_list(complete_percentage_usage: list, colors: dict) -> str:
    
    list = ""
    y = 25
    count = 1

    for item in complete_percentage_usage[:5]:

        if not item:
            break
        if item:
            list += f"""
                <text x="0" y="{y-1}" fill="{colors['text_color']}" font-size="9"  font-family="Helvetica">
                    #{count}
                    <animateTransform attributeName="transform" type="translate" from="0 20" to="0 0" dur="1s" fill="freeze" />
                    <animate attributeName="opacity" from="0" to="1" dur="2s" fill="freeze" />
                </text>
                <image
                    href="{"data:"+str(item[4])+";base64,"+str(item[3])}"
                    x="15"
                    y="{y-15}"
                    width="22"
                    height="22"
                >
                    <animateTransform attributeName="transform" type="translate" from="0 20" to="0 0" dur="1s" fill="freeze" />
                    <animate attributeName="opacity" from="0" to="1" dur="1s" fill="freeze" />
                </image>
                <text x="41" y="{y}" font-size="12"  font-family="Helvetica">
                    <tspan fill="{colors['text_color']}">{item[0]}   </tspan>
                    <tspan fill="{colors['percentage_color']}" dx="5" font-weight="bold">{round(item[1])}%</tspan>
                    <animateTransform attributeName="transform" type="translate" from="0 20" to="0 0" dur="1s" fill="freeze" />
                    <animate attributeName="opacity" from="0" to="1" dur="2s" fill="freeze" />
                </text>
            """
            y += 35
            count+=1

    y = 25

    for item in complete_percentage_usage[5:10]:

        if not item:
            break
        if item:
            list += f"""
                <text x="140" y="{y-1}" fill="{colors['text_color']}" font-size="9"  font-family="Helvetica">
                    #{count}
                    <animateTransform attributeName="transform" type="translate" from="0 20" to="0 0" dur="1s" fill="freeze" />
                    <animate attributeName="opacity" from="0" to="1" dur="2s" fill="freeze" />
                </text>
                <image
                    href="{"data:"+str(item[4])+";base64,"+str(item[3])}"
                    x="155"
                    y="{y-15}"
                    width="22"
                    height="22"
                >
                    <animateTransform attributeName="transform" type="translate" from="0 20" to="0 0" dur="1s" fill="freeze" />
                    <animate attributeName="opacity" from="0" to="1" dur="1s" fill="freeze" />
                </image>
                <text x="181" y="{y}" font-size="12"  font-family="Helvetica">
                    <tspan fill="{colors['text_color']}">{item[0]}</tspan>
                    <tspan fill="{colors['percentage_color']}" dx="5" font-weight="bold">{round(item[1])}%</tspan>
                    <animateTransform attributeName="transform" type="translate" from="0 20" to="0 0" dur="1s" fill="freeze" />
                    <animate attributeName="opacity" from="0" to="1" dur="2s" fill="freeze" />
                </text>
            """
            y += 35
            count+=1

    return list


def donut_chart(data: list,size: float,r: float,stroke_width: float) -> str:
    svg = ""
    offset = 0
    per = 2 * math.pi * r
    cx = cy = size / 2

    percentages = []
    colors = []

    for i in range(len(data)):
        percentages.append(data[i][1])
        colors.append(data[i][2])

    for i, (p, color) in enumerate(zip(percentages, colors)):
        dash_length = per * (p / 100)
        dash_array = f"{dash_length:.2f} {per:.2f}"
        dash_offset = -offset
        
        svg +=  f"""
            <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-dasharray="{dash_array}" stroke-dashoffset="{dash_offset:.2f}" transform="rotate(-90 {cx} {cy})">
                <animate attributeName="stroke-dashoffset" from="0" to="{dash_offset:.2f}" dur="2s" fill="freeze" />
            </circle>
        """

        offset += dash_length

    return svg

def create_svg(percentage_usage: list, config: dict, colors: dict, complete_percentage_usage: list) -> str:
    svg = f"""
    <svg width="465" height="250" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 465 250" fill="none">
       <rect width="465" height="250" fill="{colors['background_color']}" stroke="{colors['border_color']}" stroke-width="1" stroke-opacity="1" rx="5"/>
        <g transform="translate(0, 35)">
            <text x="22" y="0" fill="{colors['title_color']}" font-size="16" font-family="Segoe UI, Helvetica" font-weight="bold">
                {config['title']}
            </text>
        </g>
        <g transform="translate(22, 52)">
        <svg x="0" y="0" width="280" height="180" viewBox="0 0 280 180">   
            
            {language_list(complete_percentage_usage, colors)}

        </svg>
       </g>
       <g transform="translate(307, 57)">
       <svg x="0" y="0" width="150" height="150" viewBox="0 0 150 150">

            <circle cx="75" cy="75" r="60" fill="none" stroke="{colors['background_color']}" stroke-width="10"/>

            {donut_chart(complete_percentage_usage,150,60,10)}

            <defs>
                <clipPath id="circleView">
                <circle cx="75" cy="75" r="50" />
                </clipPath>
            </defs>
            <image
                href="{(
                    "data:"
                    +str(requests.get(config['custom_image']).headers["Content-Type"])
                    +";base64,"
                    +str(base64.b64encode(requests.get(config['custom_image']).content).decode('utf-8'))
                ) if config['custom_image'] != "" else (
                    "data:"
                    +str(complete_percentage_usage[0][4])
                    +";base64,"
                    +str(complete_percentage_usage[0][3])
                )}"
                x="{0 if config['custom_image'] != "" else 40}"
                y="{0 if config['custom_image'] != "" else 40}"
                width="{150 if config['custom_image'] != "" else 70}"
                height="{150 if config['custom_image'] != "" else 70}"
                clip-path="url(#circleView)"
            />

       </svg>
       </g>
       <g transform="translate(307, 212)">
       <svg x="0" y="0" width="150" height="20" viewBox="0 0 150 20">
        <a xlink:href="https://github.com/CaioLr/github-used-languages" target="_blank">
            <text x="110" y="15" fill="{colors['text_color']}" font-size="5"  font-family="Helvetica">
                Made by CaioLr
            </text>
        </a>
       </svg>
       </g>
     </svg>

    """

    return svg

def get_svg(percentage_usage: list, config: dict, colors: dict) -> list[str,str]:
    
    color = {lang["name"]: lang["color"] for lang in config["languages"]}
    image = {lang["name"]: base64.b64encode(requests.get(lang["image"]).content).decode('utf-8') for lang in config["languages"]}
    content_type = {lang["name"]: requests.get(lang["image"]).headers["Content-Type"] for lang in config["languages"]}

    # list comprehension
    complete_percentage_usage = [
        (name, percent, color.get(name), image.get(name), content_type.get(name))
        for name, percent in percentage_usage
    ]

    svg_pair = (create_svg(percentage_usage, config, colors[0], complete_percentage_usage), create_svg(percentage_usage, config, colors[1], complete_percentage_usage))

    return svg_pair

