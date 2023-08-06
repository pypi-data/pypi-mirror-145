from setuptools import setup

with open("./requestments.txt", "r") as fh:
    requestments = fh.read()

setup(
    name='flask-socketio-web',
    version='0.0.1',
    description='flask-socketio-web',
    author='hammer',
    author_email='liuzhuogood@foxmail.com',
    long_description="融合http ajax 与 websocket",
    long_description_content_type="text/markdown",
    packages=['src', 'src.common'],
    package_data={'src': ['README.md', 'LICENSE']},
    install_requires=requestments.split("\n")
)
