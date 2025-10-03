pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'inspira'

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('NAME', meson.project_name())
conf.set('devel', get_option('devel'))
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

conf.set('URI', uri)
conf.set('URI_PATH', uri_path)

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
