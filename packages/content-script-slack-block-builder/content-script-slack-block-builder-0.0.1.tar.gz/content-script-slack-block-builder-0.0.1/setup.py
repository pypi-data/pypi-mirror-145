import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import setup


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')
setup(
    name='content-script-slack-block-builder',
    version='0.0.1',
    cmdclass={
        "register": register,
        "upload": upload,
    },
    url='https://int.repositories.cloud.sap/artifactory/api/pypi/io-contentpypi-internal',
    author='c5324466',
    author_email='archna.singh@sap.com',
)

# setup(
#     name='content-script-slack-block-builder',
#     version='',
#     packages=['conf', 'tests', 'tests.unittests', 'tests.unittests.block_builder', 'modules'],
#     url='https://int.repositories.cloud.sap/artifactory/api/pypi/io-contentpypi-internal',
#     license='',
#     author='c5324466',
#     author_email='archna.singh@sap.com',
#     description=''
# )
