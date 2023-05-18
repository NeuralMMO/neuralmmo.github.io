# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Neural MMO'
copyright = '2023, Joseph Suarez'
author = 'Joseph Suarez'
release = '2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'myst_parser',
        'sphinx_design',
        'sphinx.ext.autodoc', 
        ]

myst_enable_extensions = ['colon_fence']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']

text = '#f1f1f1'
background = '#061a1a'
foreground = '#000000'
highlight = '#00bbbb'
muted = '#005050'


html_theme_options = {
    "light_css_variables": {
        "color-foreground-primary": "black",
        "color-foreground-secondary": muted,
        "color-foreground-muted": muted,
        "color-foreground-border": "#878787",
        "color-background-primary": "white",
        "color-background-secondary": "#bbcccc",
        "color-background-hover": "#efeff4ff",
        "color-background-hover--transparent": "#efeff400",
        "color-background-border": muted,
        "color-background-item": "#ccc",
        "color-announcement-background": "#000000dd",
        "color-announcement-text": "#eeebee",
        "color-brand-primary": "black",
        "color-brand-content": "black",
        "color-inline-code-background": "#f8f9fb",
        "color-highlighted-background": "#ddeeff",
        "color-guilabel-background": "#ddeeff80",
        "color-guilabel-border": "#bedaf580",
        "color-card-background": "#bbcccc",
    },
    "dark_css_variables": {
        "color-problematic": "#ee5151",
        "color-foreground-primary": text, # Text
        "color-foreground-secondary": highlight, # Some icons
        "color-foreground-muted": highlight, #Some headings and icons
        "color-foreground-border": "#666666",
        "color-background-primary": background, # Main Background
        "color-background-secondary": foreground, # Sidebar
        "color-background-hover": "#1e2124ff",
        "color-background-hover--transparent": "#1e212400",
        "color-background-border": "#303335", # Sidebar border
        "color-background-item": "#444",
        "color-announcement-background": "#000000dd",
        "color-announcement-text": "#eeebee",
        "color-brand-primary": highlight, # Sidebar Items
        "color-brand-content": highlight, # Embedded Links
        "color-highlighted-background": "#083563",
        "color-guilabel-background": "#08356380",
        "color-guilabel-border": "#13395f80",
        "color-admonition-background": "#18181a",
        "color-card-border": "#1a1c1e",
        "color-card-background": foreground,
        "color-card-marginals-background": "#1e2124ff",
        "color-inline-code-background": "#00000000", # Download background
    }
}

pygments_dark_style = "monokai"