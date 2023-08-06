from distutils.core import setup

setup(
  name = 'ydb-function-driver',
  packages = ['ydb_function_driver'],
  version = '0.4',
  license='MIT',
  description = 'Yandex database (ydb) driver for cloud function.',
  author = 'Михаил Беляков (Michael Belyakov)',
  author_email = 'bigbelk@live.ru',
  url = 'https://github.com/yababay/ydb-function-driver',
  download_url = 'https://github.com/yababay/ydb-function-driver/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['ydb', 'cloud function', 'database driver'],
  install_requires=[
          'ydb',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)
