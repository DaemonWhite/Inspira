gnome = import('gnome')
pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()



blueprint_file = [
	'ui/widgets/modals/preferences.blp',
  	'ui/widgets/infos_image.blp',
  	'ui/widgets/notif_button.blp',
  	'ui/widgets/overlay_picture.blp',
  'ui/widgets/search_tag_autocomplet.blp',
  'ui/widgets/states_row.blp',
  'ui/widgets/state_progress_row.blp',
  'ui/widgets/switch_info_row.blp',
  	'ui/widgets/tag.blp',
  'ui/widgets/wrap_tags.blp',
  'ui/window.blp',
]

ui_pref = ''

if host_machine.system() == 'windows'
  blueprint_file += ['ui/help-overlay.blp']
  ui_pref = '<file preprocess="xml-stripblanks" alias="gtk/help-overlay.ui">ui/help-overlay.ui</file>'
else
	blueprint_file += ['ui/shortcuts-dialog.blp']
  ui_pref = '<file preprocess="xml-stripblanks" alias="shortcuts-dialog.ui">ui/shortcuts-dialog.ui</file>'
  warning('MSYS 2 Not support Libadwaita 1.8 Disable preference page')
endif

conf.set('UI_PREF', ui_pref)

blueprints = custom_target('blueprints',
  input: files(blueprint_file),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gresource = configure_file(
  input: 'inspira.gresource.xml.in',
  output: 'inspira.gresource.xml',
  configuration: conf,
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)

gnome.compile_resources('inspira',
  gresource,
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

desktop_file_generated = configure_file(
  input: 'fr.daemonwhite.Inspira.desktop.in',
  output: uri + '.desktop.in',
  configuration: conf,
)

desktop_file = i18n.merge_file(
        input: desktop_file_generated,
       output: uri + '.desktop',
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

configure_file(
  input: 'fr.daemonwhite.Inspira.gschema.xml.in',
  output: uri + '.gschema.xml',
  configuration: conf,
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas',
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])


service_conf = configuration_data()
service_conf.set('bindir', get_option('prefix') / get_option('bindir'))
service_conf.set('URI', uri)
configure_file(
  input: 'fr.daemonwhite.Inspira.service.in',
  output: uri + '.service',
  configuration: service_conf,
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)

subdir('icons')