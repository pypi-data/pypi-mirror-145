from setuptools import setup

setup(
    name='DXR',
    version='0.2.5',
    packages=['Dxr_mqtt', 'Dxr_log', 'Dxr_bytes', 'Dxr_utils', 'Dxr_video'],
    install_requires=['paho-mqtt', 'pyyaml', 'grpcio', 'grpcio-tools', 'opencv-python'],
    author='luzhipeng',
    author_email='402087139@qq.com',
    license='MIT',
    url='http://pycn.me'
)
