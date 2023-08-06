import re
import setuptools

with open('emma/__init__.py') as init:
    text = init.read()
    match = re.search(r"__version__ = '(.+)'", text)
    version = match.group(1)

setuptools.setup(
    name='emma',
    version=version,
    description='Emma -- Productivity analysis tool.',
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='https://grantjenks.com/docs/emma/',
    project_urls={
        'Documentation': 'https://grantjenks.com/docs/emma/',
        'Source': 'https://github.com/grantjenks/emma',
        'Tracker': 'https://github.com/grantjenks/emma/issues',
    },
    license='Apache 2.0',
    packages=['emma'],
    python_requires='>=3',
    install_requires=[
        'appdirs',
        'django==3.2.*',
        'gunicorn',
        'pandas',
        'pillow',
        'plotly',
        'rumps',
        # 'rumps @ git+https://github.com/jaredks/rumps.git@018cabce9175aed3a77b747dc50118cd65a5374d',
    ],
    entry_points = {
        'console_scripts': ['emma=emma.__main__:main'],
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
