def create_svg(percentage_usage: dict, config: dict) -> str:
    
    svg = f"""
    <svg width="465" height="250" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 465 250" fill="none">
       <rect width="465" height="250" fill="white" stroke="gray" stroke-width="1" stroke-opacity="1" rx="5"/>
        <g transform="translate(22, 32)">
            <text x="0" y="0" fill="#000000" font-size="20"  font-family="Roboto">
                {config['title']}
            </text>
        </g>
        <g transform="translate(22, 52)">
        <svg x="0" y="0" width="280" height="180" viewBox="0 0 280 180">
            <text x="0" y="20" fill="#000000" font-size="8"  font-family="Roboto">
                #1
            </text>        
            
            <text x="10" y="20" fill="#000000" font-size="12"  font-family="Roboto">
                {config['title']}
            </text>
        </svg>
       </g>
       <g transform="translate(307, 52)">
       <svg x="0" y="0" width="150" height="150" viewBox="0 0 150 150">

            <text x="0" y="20" fill="#000000" font-size="20"  font-family="Roboto">
                {config['title']}
            </text>

       </svg>
       </g>
       <g transform="translate(307, 212)">
       <svg x="0" y="0" width="150" height="20" viewBox="0 0 150 20">
        <a xlink:href="https://github.com/CaioLr/github-used-languages" target="_blank">
            <text x="110" y="15" fill="#000000" font-size="5"  font-family="Roboto">
                Made by CaioLr
            </text>
        </a>
       </svg>
       </g>
     </svg>

    """
    return svg

