import setuptools


with open('README.md', 'r', encoding='utf-8') as fn:
    long_description = fn.read()

requires = [
    'requests',
    'rauth',
    'pandas',
    'python-dotenv'
]

setuptools.setup(
    name='dtm_pyapi',
    version='0.0.12',
    author='Kevin A. Nakasaki',
    author_email='kevin.nakasaki@gmail.com',
    description='Consumindo APIs facilmente com Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kevinnakasaki/pyAPI',
    projec_urls={
        'Bug Tracker': 'https://github.com/kevinnakasaki/pyAPI/issues'
    },
    license='MIT',
    packages=['dtm_pyapi'],
    install_requires=requires,
    scripts=['setup_ini.py']
)