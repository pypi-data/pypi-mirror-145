import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-mflf',
    version='0.1.0',
    license='MIT',
    author='Andrey Novikov',
    author_email='novikov@gmail.com',
    description='Django model field list field',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andreynovikov/django-mlfl/tree/master',
    project_urls={
        'Source': 'https://github.com/andreynovikov/django-mlfl/',
        'Tracker': 'https://github.com/andreynovikov/django-mlfl/issues'
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    test_suite='tests.runtests.main'
)
