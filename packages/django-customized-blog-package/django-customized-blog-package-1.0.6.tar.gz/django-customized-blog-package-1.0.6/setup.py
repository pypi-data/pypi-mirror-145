from setuptools import setup


setup(
    name='django-customized-blog-package',
    version='1.0.6',
    description='This package is based on the blog project. It provides all the functionality required for a blog project',
    long_description_content_type='text/x-rst',
    url='https://github.com/AyanNandaGoswami/BlogModule.git',
    author='Ayan Nanda Goswami',
    author_email='ayan02472@gmail.com',
    maintainer='Ayan Nanda Goswami',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='django customized blog package',
    project_urls={
        'Documentation': 'https://blog-module-community.herokuapp.com/',
        'Source': 'https://github.com/AyanNandaGoswami/BlogModule.git',
        'Tracker': 'https://github.com/AyanNandaGoswami/BlogModule/issues',
    },
    install_requires=['Django', 'django-ckeditor', 'django-taggit', 'djangorestframework', 'Pillow', 'random2',
                      ' colorama'],
    python_requires='>=3',
)
