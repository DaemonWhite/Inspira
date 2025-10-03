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

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
