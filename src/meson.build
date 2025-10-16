configure_file(
  input: 'inspira.py',
  output: 'inspira',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

configure_file(
  input: 'config.in',
  output: 'config.py',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

inspira_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]


install_data(inspira_sources, install_dir: moduledir)
install_subdir('core', install_dir: moduledir)
install_subdir('apis', install_dir: moduledir)
install_subdir('items', install_dir: moduledir)
install_subdir('utils', install_dir: moduledir)
install_subdir('widgets', install_dir: moduledir)
