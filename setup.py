from setuptools import setup

setup(
    name='umedsmsclient',
    version='1.0.0',
    description='A Python client library for sending and scheduling sms messages via Fire Text Sms API',
    author='Hasitha Widanagamachchi',
    author_email='haztha@gmail.com',
    packages=['umedsmsclient'],
    install_requires=[
        'requests',
    ],
)