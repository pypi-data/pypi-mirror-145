from distutils.core import setup

setup(
  name = 'abstract-telegram-processor',
  packages = ['abstract_telegram_processor'],
  version = '0.3',
  license='MIT',
  description = 'Abstract telegram processor.',
  author = 'Михаил Беляков (Michael Belyakov)',
  author_email = 'bigbelk@live.ru',
  url = 'https://github.com/yababay/abstract-telegram-processor',
  download_url = 'https://github.com/yababay/abstract-telegram-processor/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Telegram', 'bot', 'command'],
  install_requires=[
    'emoji',
    'yc-event-to-json',
    'telegram-admin-informer'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)
