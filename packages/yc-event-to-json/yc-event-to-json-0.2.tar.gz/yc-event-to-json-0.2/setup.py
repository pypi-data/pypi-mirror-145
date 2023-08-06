from distutils.core import setup

setup(
  name = 'yc-event-to-json',
  packages = ['yc_event_to_json'],
  version = '0.2',
  license='MIT',
  description = 'Yandex Cloud event to json convertor.',
  author = 'Михаил Беляков (Michael Belyakov)',
  author_email = 'bigbelk@live.ru',
  url = 'https://github.com/yababay/yc-event-to-json',
  download_url = 'https://github.com/yababay/yc-event-to-json/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['yc', 'yandex cloud function', 'json', 'post request'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)
