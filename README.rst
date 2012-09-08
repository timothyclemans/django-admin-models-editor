Overview
========

This app aims to let admins create and edit models within the admin interface.
It is not ready for production use.

.. image:: https://raw.github.com/timothyclemans/django-admin-models-editor/master/screenshot.png

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

Author
======

Timothy Clemans <timothy.clemans@gmail.com>