gnome = import('gnome')
pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()


blueprints = custom_target('blueprints',
  input: files(
  		'ui/widgets/modals/preferences.blp',
  		'ui/widgets/switch_info_row.blp',
		'ui/widgets/wrap_tags.blp',
		'ui/widgets/tag.blp',
    'ui/widgets/search_tag_autocomplet.blp',
    'ui/shortcuts-dialog.blp',
    'ui/window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('inspira',
  'inspira.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

desktop_file = i18n.merge_file(
        input: 'fr.daemonwhite.Inspira.desktop.in',
       output: 'fr.daemonwhite.Inspira.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'fr.daemonwhite.Inspira.metainfo.xml.in',
       output: 'fr.daemonwhite.Inspira.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

install_data('fr.daemonwhite.Inspira.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])


service_conf = configuration_data()
service_conf.set('bindir', get_option('prefix') / get_option('bindir'))
configure_file(
  input: 'fr.daemonwhite.Inspira.service.in',
  output: 'fr.daemonwhite.Inspira.service',
  configuration: service_conf,
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)

subdir('icons')
