from distutils.core import setup

setup(
  name = 'telegram-admin-informer',
  packages = ['telegram_admin_informer'],
  version = '0.1',
  license='MIT',
  description = 'Telegram admin informer',
  author = 'Михаил Беляков (Michael Belyakov)',
  author_email = 'bigbelk@live.ru',
  url = 'https://github.com/yababay/telegram-admin-informer',
  download_url = 'https://github.com/yababay/telegram-admin-informer/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['telegram', 'admin'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)
