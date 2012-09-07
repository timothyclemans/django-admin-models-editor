Overview
========

This app aims to let admins create and edit models within the admin interface.
It is not ready for production use.

Install
=======

1. Run ``setup.py`` or add ``admin_models_editor`` to your PYTHONPATH.
2. Add ``admin_models_editor`` to ``INSTALLED_APPS`` in your ``settings.py``
3. Add ``from admin_models_editor.admin_auto_register import autoregister
autoregister(INSTALLED_APPS)`` to settings.py
4. Run ``python manage.py admin_models_editor_install_templates``


Author
======

Timothy Clemans <timothy.clemans@gmail.com>