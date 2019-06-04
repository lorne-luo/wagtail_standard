Getting started
===============

1. Clone project 
2. `cd example`
3. Setup virtualenv `/bin/bash ./shell.sh setupenv`
4. Run server `/bin/bash ./shell.sh runserver`
5. That's it. Your server URL will be at localhost:8000
6. Some settings value can be change by creating .env file in your project root. Example. You may want to change BASE_URL and DATABASE_URL when settings up your local.

Wagtail Packages 
========
## wagtailstreamform 3.5
- Form Builder that can be added via StreamField.
https://wagtailstreamforms.readthedocs.io/en/latest/index.html

## wagtailmenus 2.13
-  Help define, manage and render menu in wagtail admin.
https://wagtailmenus.readthedocs.io/en/stable/rendering_menus/custom_templates.html#custom-templates

## wagtail-condensedinlinepanel
- Recomended to use with wagtailmenu for a better user expirence with menu editing. 
Feature are:
- Fast, react-based UI which hides away forms that aren't being used
- Drag and drop reordering
- Add a new item at any point
https://pypi.org/project/wagtail-condensedinlinepanel/


See docs/ for more 
