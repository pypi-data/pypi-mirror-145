from setuptools import setup, find_packages

setup(
    name='marfa_bi_connection',
    version='0.3.2',
    license='MIT',
    author="Ruslan Galimov",
    author_email='rgalimov@marfa-tech.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/NorddyM/MarfaBI',
    keywords='Marfa BI connections',
    install_requires=[
        'PyMySQL==1.0.2',
        'PyYAML==6.0',
        'sshtunnel==0.4.0',
        'pandas==1.4.1',
        'python-telegram-bot==13.11',
        'SQLAlchemy==1.4.34',
        'clickhouse-sqlalchemy==0.2.0',
        'clickhouse-driver==0.2.3',
        'google-cloud-bigquery==2.34.2',
        'slack-sdk==3.15.2',
        'google==3.0.0',
        'cryptography==36.0.1'
      ]
)
