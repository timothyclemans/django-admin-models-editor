Overview
========

This lets you create models within the admin interface.

.. image:: https://raw.github.com/timothyclemans/django-admin-models-editor/master/screenshot.png
.. image:: https://raw.github.com/timothyclemans/django-admin-models-editor/master/screenshot_of_adding_choices.png

Install
=======

1. Run ``setup.py`` or add ``admin_models_editor`` to your PYTHONPATH.

2. Add ``admin_models_editor`` to ``INSTALLED_APPS`` in your ``settings.py``

3. Add ``from admin_models_editor.admin_auto_register import autoregister`` and 
``autoregister(INSTALLED_APPS)`` to settings.py

4. Run ``python manage.py admin_models_editor_install_templates`` or add 
``os.path.join(BASE_DIR, "../admin_models_editor/templates"),`` to ``TEMPLATE_DIRS``
to settings.py and add ``import os`` and ``BASE_DIR = os.getcwd()`` to settings.py

5. Enable admin

6. Add ``url(r'^admin/create_model/', 'admin_models_editor.views.create_model'),`` to urls.py

To enable simple mode, replaces Null & Blank checkboxes with one Required checkbox, add
``ADMIN_MODELS_EDITOR_SIMPLE_MODE = True`` to ``settings.py``

Author
======

Timothy Clemans <timothy.clemans@gmail.com>

To do
=====

* Update the form based on changes to the code
  * Change model name if model name changed in code DONE
  * Change field names if field names changed in code DONE
* Make models editable
* Make a graphical interface, see http://gaesql.appspot.com/ and http://code.google.com/p/uml-to-django/