from setuptools import setup

setup(
    name='flask-socketio-web',
    version='0.0.2',
    description='flask-socketio-web',
    author='hammer',
    author_email='liuzhuogood@foxmail.com',
    long_description="融合http ajax 与 websocket",
    long_description_content_type="text/markdown",
    packages=['flask_socketio_web', 'flask_socketio_web.common'],
    package_data={'flask_socketio_web': ['README.md', 'LICENSE']},
    install_requires=[
        "python-socketio",
        "flask",
        "python-engineio",
        "loguru",
    ]

)
