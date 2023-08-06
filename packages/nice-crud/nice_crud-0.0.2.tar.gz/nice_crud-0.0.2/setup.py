from distutils.core import setup


setup(
    name='nice_crud',
    packages=['nice_crud'],
    version='0.0.2',
    license='MIT',
    description='A simple CRUD application',
    author='amiwrpremium',
    author_email='amiwrpremiun@gmail.com',
    url='https://github.com/amiwrpremium/nice_crud',
    keywords=['crud', 'crud-app', 'crud-application'],
    install_requires=[
        'psycopg2-binary',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
