def language_list(complete_percentage_usage: list) -> str:
    
    list = ""
    y = 25
    count = 1

    for item in complete_percentage_usage[:5]:

        if not item:
            break
        if item:
            list += f"""
                <text x="0" y="{y-1}" fill="#888888" font-size="9"  font-family="Helvetica">#{count}</text>
                <image
                    href="{item[3]}"
                    x="15"
                    y="{y-15}"
                    width="22"
                    height="22"
                />
                <text x="41" y="{y}" fill="#000000" font-size="12"  font-family="Helvetica">
                    <tspan fill="#888888">{item[0]}   </tspan>
                    <tspan fill="#828282" dx="5" font-weight="bold">{round(item[1])}%</tspan>
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
                <text x="140" y="{y-1}" fill="#888888" font-size="9"  font-family="Helvetica">#{count}</text>
                <image
                    href="{item[3]}"
                    x="155"
                    y="{y-15}"
                    width="22"
                    height="22"
                />
                <text x="181" y="{y}" fill="#000000" font-size="12"  font-family="Helvetica">
                    <tspan fill="#888888">{item[0]}</tspan>
                    <tspan fill="#828282" dx="5" font-weight="bold">{round(item[1])}%</tspan>
                </text>
            """
            y += 35
            count+=1

    return list

def create_svg(percentage_usage: list, config: dict) -> str:
    
    color = {lang["name"]: lang["color"] for lang in config["languages"]}
    image = {lang["name"]: lang["image"] for lang in config["languages"]}

    # list comprehension
    complete_percentage_usage = [
        (name, percent, color.get(name), image.get(name))
        for name, percent in percentage_usage
    ]

    svg = f"""
    <svg width="465" height="250" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 465 250" fill="none">
       <rect width="465" height="250" fill="#fefeff" stroke="gray" stroke-width="1" stroke-opacity="1" rx="5"/>
        <g transform="translate(0, 35)">
            <text x="22" y="0" fill="{config['title_color']}" font-size="16" font-family="Segoe UI, Helvetica" font-weight="bold">
                {config['title']}
            </text>
        </g>
        <g transform="translate(22, 52)">
        <svg x="0" y="0" width="280" height="180" viewBox="0 0 280 180">   
            
            {language_list(complete_percentage_usage)}

        </svg>
       </g>
       <g transform="translate(307, 57)">
       <svg x="0" y="0" width="150" height="150" viewBox="0 0 150 150">

            <circle cx="75" cy="75" r="60" fill="none" stroke="black" stroke-width="10"/>

            <defs>
                <clipPath id="circleView">
                <circle cx="75" cy="75" r="50" />
                </clipPath>
            </defs>
            <image
                href="{config['custom_image'] if config['custom_image'] != "" else complete_percentage_usage[0][3]}"
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
            <text x="110" y="15" fill="#888888" font-size="5"  font-family="Helvetica">
                Made by CaioLr
            </text>
        </a>
       </svg>
       </g>
     </svg>

    """
    return svg

