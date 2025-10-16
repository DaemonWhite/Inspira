project('inspira',
          version: '0.1.0',
    meson_version: '>= 1.0.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')

uri_base = ['fr', 'daemonwhite','Inspira']

if get_option('devel')
	uri_base += ['devel']
endif

uri = '.'.join(uri_base)
uri_path = '/' + '/'.join(uri_base)

message('URI: ' + uri)

pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'inspira'

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('PYTHON_VERSION', python.find_installation('python3').language_version())
conf.set('VERSION', meson.project_version())
conf.set('NAME', meson.project_name())
conf.set('devel', get_option('devel'))
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

conf.set('URI', uri)
conf.set('URI_PATH', uri_path)

subdir('data')
subdir('src')
subdir('po')

if host_machine.system() == 'windows'
  subdir('build_aux/windows')
endif

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
