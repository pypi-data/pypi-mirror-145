from setuptools import setup

with open("./README.md", "rb") as fh:
    long_description = fh.read()

setup(
    name='crawler_chrome',
    version='0.0.1',
    description='采集工具',
    author='hammer',
    author_email='liuzhuogood@foxmail.com',
    long_description=str(long_description, encoding='utf-8'),
    long_description_content_type="text/markdown",
    packages=['crawler_chrome'],
    package_data={'crawler_chrome': ['README.md', 'LICENSE']},
    install_requires=[]
)
