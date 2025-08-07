<div align="center">

# Github Used Languages
  
Customized GitHub Used Languages dynamic image to use in your README profile.

![caiolr](https://github.com/user-attachments/assets/d1fa92d5-8115-4246-ba1c-fa23150be29c)

</div>

The idea behind this project is to create a customizable chart that measures the usage of programming languages and/or tools from github profiles. You have a lot of control over what to include, **from choosing which languages or tools to display, to defining the relevant file extensions, names, images, colors and more.**

## How to use

You can use it with the link `https://github-used-languages.vercel.app/your-github-username` (changing the `your-github-username` to your username) that returns a SVG image, with the default configuration.

In your README github, add the following code:
```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-used-languages.vercel.app/your-github-username?theme=dark">
  <img alt="Most Used Languages'" src="https://github-used-languages.vercel.app/your-github-username">
</picture>
```
***With the picture and the prefers-color-scheme checkup, github will change automatically to light or dark mode by the github preferences of who enter in your profile.***

#### Parameters

- **theme:** By default the image is on light mode, but by sending the the value `dark` in this parameter, it will return the SVG with the colors defined for the dark mode in the current configuration (Any other values will returns the light mode SVG).
- **config:** This parameter expects the path of the custom configuration JSON file, based on the repository with the same same of your profile (If the path is not found, the default configuration will be used).

## How to customize

The customization happens using the `config` parameter.

To start the customization is necessary to follow these steps:
1. Copy the default configuration file in default_config.json file (you can access clicking here).
2. Create a JSON file with that information, in your repository with the same name as your username.
3. Add the path of the configuration file to your request to the endpoint using the config parameter, as the following example:
```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-used-languages.vercel.app/your-github-username?theme=dark&config=config.json">
  <img alt="Most Used Languages'" src="https://github-used-languages.vercel.app/your-github-username?config=config.json">
</picture>
```
4. Edit the JSON as your wish.

**Here’s where your creativity comes into play**, you can send a custom image to be in the center of the donut chart in the `custom_image` field, also your are able to edit all the words and colors used.

This also includes the programing languages, enabling you to disable, add and edit (including the images).



```
{
    "title": "🏆 Most Used Languages 🏆",
    "custom_image": "",
    "colors_light_theme" : {
        "title_color": "#828282",
        "text_color" : "#888888",
        "percentage_color": "#828282",
        "background_color": "#fefeff",
        "border_color": "#808080"
    },
    "colors_dark_theme": {
        "title_color": "#E0E0E0",
        "text_color": "#CCCCCC",
        "percentage_color": "#BBBBBB",
        "background_color": "#20202a",
        "border_color": "#101010"
    },
    "disable_languages": [
        "HTML"
    ],
    "languages": [
        {
            "name": "Python",
            "extensions": ["py", "pyw", "pyc", "pyo", "pyd", "ipynb"],
            "color": "#3572A5",
            "image": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg"
        },
...
```
## Percentage Calculation

*The percentage is calculated based on the total file size and the number of repositories in which each language appears, using weights of 0.6 and 0.4 respectively. The language is determined by the file extension.*
