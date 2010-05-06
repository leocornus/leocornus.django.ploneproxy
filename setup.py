from setuptools import setup, find_packages
import os

product_folder = 'leocornus/django/ploneproxy'

version = open(os.path.join(product_folder, 'version.txt')).read().split('\n')[0]

setup(name='leocornus.django.ploneproxy',
      version=version,
      description="Django Application as a Proxy to Plone Sites",
      long_description=open(os.path.join(product_folder, "README.txt")).read() + "\n" +
                       open(os.path.join(product_folder, "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Zope",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        ],
      keywords='Python Plone Zope Django Proxy',
      author='Sean Chen',
      author_email='sean.chen@leocorn.com',
      url='http://plonexp.leocorn.com/xp/leocornus.django.ploneproxy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['leocornus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
