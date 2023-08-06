from setuptools import setup, find_packages


setup(
    name='marfa_bi_connection',
    version='0.3',
    license='MIT',
    author="Ruslan Galimov",
    author_email='rgalimov@marfa-tech.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/NorddyM/MarfaBI',
    keywords='Marfa BI connections',
    install_requires=[
        'pymysql',
        'PyYAML',
        'sshtunnel',
        'pandas',
        'python-telegram-bot',
        'SQLAlchemy',
        'clickhouse-sqlalchemy',
        'clickhouse-driver',
        'google-cloud-bigquery',
        'slack-sdk',
        'google'
      ],

)
