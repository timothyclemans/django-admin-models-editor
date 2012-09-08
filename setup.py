from setuptools import setup, find_packages

try:
    README = open('README').read()
except:
    README = None

setup(
    name='django-admin-models-editor',
    version='0.01',
    description='Create models from the admin interface',
    long_description=README,
    license='APL',
    author='Timothy Clemans',
    author_email='timothyclemans@gmail.com',
    packages=find_packages(exclude=['sample_project']),
    zip_safe=False,
    include_package_data=True,
    classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)