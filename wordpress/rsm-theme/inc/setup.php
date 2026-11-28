<?php
/**
 * RSM Setup: one screen that installs the two required plugins and imports the whole website.
 * Appearance > RSM Setup.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

function rsm_setup_plugins() {
	return array(
		'elementor'    => array( 'name' => 'Elementor', 'file' => 'elementor/elementor.php', 'source' => 'wordpress.org' ),
		'rsm-elements' => array( 'name' => 'RSM Elements', 'file' => 'rsm-elements/rsm-elements.php', 'source' => get_template_directory() . '/plugins/rsm-elements.zip' ),
	);
}
function rsm_setup_plugin_state( $file ) {
	if ( ! function_exists( 'is_plugin_active' ) ) { require_once ABSPATH . 'wp-admin/includes/plugin.php'; }
	if ( is_plugin_active( $file ) ) { return 'active'; }
	return file_exists( WP_PLUGIN_DIR . '/' . $file ) ? 'installed' : 'missing';
}
function rsm_setup_ready() { foreach ( rsm_setup_plugins() as $p ) { if ( 'active' !== rsm_setup_plugin_state( $p['file'] ) ) { return false; } } return true; }

add_action( 'admin_menu', function () {
	add_theme_page( __( 'RSM Setup', 'rsm' ), __( 'RSM Setup', 'rsm' ), 'manage_options', 'rsm-setup', 'rsm_setup_screen' );
} );
add_action( 'after_switch_theme', function () { set_transient( 'rsm_setup_notice', 1, WEEK_IN_SECONDS ); } );
add_action( 'admin_notices', function () {
	$scr = get_current_screen();
	if ( ! current_user_can( 'manage_options' ) || ( $scr && 'appearance_page_rsm-setup' === $scr->id ) || get_option( 'rsm_import_done' ) ) { return; }
	printf( '<div class="notice notice-info"><p><strong>%s</strong> %s <a class="button button-primary" href="%s">%s</a></p></div>', esc_html__( 'Relevant Search Media theme:', 'rsm' ), esc_html__( 'two clicks to finish. Install the plugins, then import the website.', 'rsm' ), esc_url( admin_url( 'themes.php?page=rsm-setup' ) ), esc_html__( 'Open RSM Setup', 'rsm' ) );
} );

/* ---------- step 1: plugins ---------- */
add_action( 'admin_post_rsm_install_plugins', function () {
	if ( ! current_user_can( 'install_plugins' ) || ! current_user_can( 'activate_plugins' ) ) { wp_die( esc_html__( 'You are not allowed to install plugins.', 'rsm' ) ); }
	check_admin_referer( 'rsm_install_plugins' );
	require_once ABSPATH . 'wp-admin/includes/plugin.php'; require_once ABSPATH . 'wp-admin/includes/file.php'; require_once ABSPATH . 'wp-admin/includes/misc.php';
	require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php'; require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
	$log = array();
	foreach ( rsm_setup_plugins() as $slug => $p ) {
		$state = rsm_setup_plugin_state( $p['file'] );
		if ( 'missing' === $state ) {
			$src = $p['source'];
			if ( 'wordpress.org' === $src ) { $api = plugins_api( 'plugin_information', array( 'slug' => $slug, 'fields' => array( 'sections' => false ) ) ); if ( is_wp_error( $api ) ) { $log[] = $p['name'] . ': ' . $api->get_error_message(); continue; } $src = $api->download_link; }
			$skin = new Automatic_Upgrader_Skin(); $up = new Plugin_Upgrader( $skin ); $r = $up->install( $src );
			if ( is_wp_error( $r ) || ! $r ) { $why = is_wp_error( $r ) ? $r->get_error_message() : wp_strip_all_tags( (string) ( function ( $m ) { return end( $m ); } )( $skin->get_upgrade_messages() ) ); $log[] = $p['name'] . ': ' . ( $why ? $why : __( 'could not be installed.', 'rsm' ) ) . ' ' . __( 'You can also install it from Plugins, Add New, then come back here.', 'rsm' ); continue; }
			wp_clean_plugins_cache();
		}
		if ( 'active' !== rsm_setup_plugin_state( $p['file'] ) ) { $r = activate_plugin( $p['file'] ); if ( is_wp_error( $r ) ) { $log[] = $p['name'] . ': ' . $r->get_error_message(); } }
	}
	// Elementor sends a new site to its own welcome screens on the next admin page; come back here instead.
	delete_transient( 'elementor_activation_redirect' ); delete_option( 'elementor_onboarding_pending' );
	set_transient( 'rsm_setup_log', $log ? $log : array( __( 'Plugins are installed and active.', 'rsm' ) ), 60 );
	wp_safe_redirect( admin_url( 'themes.php?page=rsm-setup' ) ); exit;
} );

/* ---------- step 2: import ---------- */
add_action( 'admin_post_rsm_import', function () {
	if ( ! current_user_can( 'manage_options' ) ) { wp_die( esc_html__( 'You are not allowed to import.', 'rsm' ) ); }
	check_admin_referer( 'rsm_import' );
	$log = rsm_import_site( ! empty( $_POST['reset'] ) );
	set_transient( 'rsm_setup_log', $log, 60 );
	wp_safe_redirect( admin_url( 'themes.php?page=rsm-setup' ) ); exit;
} );

function rsm_import_find( $type, $key ) {
	$q = get_posts( array( 'post_type' => $type, 'post_status' => 'any', 'meta_key' => '_rsm_import_key', 'meta_value' => $key, 'posts_per_page' => 1, 'fields' => 'ids', 'no_found_rows' => true ) ); // phpcs:ignore WordPress.DB.SlowDBQuery
	return $q ? (int) $q[0] : 0;
}
function rsm_import_media( $m ) {
	$id = rsm_import_find( 'attachment', $m['key'] );
	if ( $id && get_attached_file( $id ) && file_exists( get_attached_file( $id ) ) ) { return array( $id, false ); }
	$path = get_template_directory() . '/assets/' . $m['file'];
	if ( ! file_exists( $path ) ) { return array( 0, false ); }
	require_once ABSPATH . 'wp-admin/includes/image.php'; require_once ABSPATH . 'wp-admin/includes/file.php'; require_once ABSPATH . 'wp-admin/includes/media.php';
	$up = wp_upload_bits( basename( $path ), null, file_get_contents( $path ) ); // phpcs:ignore WordPress.WP.AlternativeFunctions
	if ( ! empty( $up['error'] ) ) { return array( 0, false ); }
	$type = wp_check_filetype( $up['file'] );
	$id = wp_insert_attachment( array( 'post_mime_type' => $type['type'], 'post_title' => $m['title'], 'post_status' => 'inherit' ), $up['file'] );
	if ( is_wp_error( $id ) || ! $id ) { return array( 0, false ); }
	wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $up['file'] ) );
	update_post_meta( $id, '_rsm_import_key', $m['key'] );
	if ( ! empty( $m['alt'] ) ) { update_post_meta( $id, '_wp_attachment_image_alt', $m['alt'] ); }
	return array( $id, true );
}
function rsm_import_menu_items( $menu_id, $items, $parent = 0 ) {
	$n = 0;
	foreach ( $items as $it ) {
		$url = $it['url']; if ( 0 === strpos( $url, '/' ) ) { $url = home_url( $url ); }
		$id = wp_update_nav_menu_item( $menu_id, 0, array( 'menu-item-title' => $it['title'], 'menu-item-url' => $url, 'menu-item-description' => $it['description'] ?? '', 'menu-item-classes' => $it['classes'] ?? '', 'menu-item-parent-id' => $parent, 'menu-item-type' => 'custom', 'menu-item-status' => 'publish' ) );
		if ( is_wp_error( $id ) ) { continue; }
		$n++;
		if ( ! empty( $it['children'] ) ) { $n += rsm_import_menu_items( $menu_id, $it['children'], $id ); }
	}
	return $n;
}
function rsm_import_doc( $type, $doc, $reset, $tokens ) {
	$id = rsm_import_find( $type, $doc['key'] );
	if ( $id && ! $reset ) { return array( $id, 'kept' ); }
	$json = strtr( wp_json_encode( $doc['data'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ), $tokens );
	$args = array( 'post_type' => $type, 'post_title' => $doc['title'], 'post_name' => $doc['slug'], 'post_status' => 'publish', 'post_content' => '' );
	if ( $id ) { $args['ID'] = $id; wp_update_post( $args ); $state = 'reset'; } else { $id = wp_insert_post( $args ); $state = 'created'; }
	if ( is_wp_error( $id ) || ! $id ) { return array( 0, 'failed' ); }
	update_post_meta( $id, '_rsm_import_key', $doc['key'] );
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $id, '_elementor_template_type', 'page' === $type ? 'wp-page' : 'wp-post' );
	update_post_meta( $id, '_elementor_version', defined( 'ELEMENTOR_VERSION' ) ? ELEMENTOR_VERSION : '3.0.0' );
	update_post_meta( $id, '_elementor_data', wp_slash( $json ) );
	delete_post_meta( $id, '_elementor_css' ); delete_post_meta( $id, '_elementor_element_cache' );
	foreach ( (array) ( $doc['seo'] ?? array() ) as $k => $v ) { update_post_meta( $id, '_rsm_' . $k, strtr( $v, $tokens ) ); }
	return array( $id, $state );
}
/** Imports everything. Safe to run again: anything already imported is kept, never duplicated. */
function rsm_import_site( $reset = false ) {
	$log = array();
	if ( ! rsm_setup_ready() ) { return array( __( 'Install and activate the two plugins first.', 'rsm' ) ); }
	$site = json_decode( file_get_contents( get_template_directory() . '/import/site.json' ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions
	if ( ! is_array( $site ) ) { return array( __( 'The import file is missing or damaged.', 'rsm' ) ); }
	if ( function_exists( 'set_time_limit' ) ) { @set_time_limit( 300 ); } // phpcs:ignore

	// 1. media
	$tokens = array( '{{home}}' => untrailingslashit( home_url() ), '{{assets}}' => untrailingslashit( get_template_directory_uri() . '/assets' ) ); $new = 0;
	foreach ( $site['media'] as $m ) { list( $id, $made ) = rsm_import_media( $m ); if ( $made ) { $new++; }
		$tokens[ '{{media:' . $m['key'] . '}}' ] = $id ? wp_get_attachment_url( $id ) : get_template_directory_uri() . '/assets/' . $m['file']; $tokens[ '{{mediaid:' . $m['key'] . '}}' ] = (string) $id; }
	$log[] = sprintf( /* translators: 1: new files, 2: total */ __( 'Media: %1$d added, %2$d in total.', 'rsm' ), $new, count( $site['media'] ) );

	// 2. menus
	$made = 0;
	foreach ( $site['menus'] as $menu ) {
		$obj = wp_get_nav_menu_object( $menu['slug'] );
		if ( $obj && ! $reset ) { continue; }
		if ( $obj ) { foreach ( (array) wp_get_nav_menu_items( $obj->term_id ) as $it ) { wp_delete_post( $it->ID, true ); } $mid = $obj->term_id; } else { $mid = wp_create_nav_menu( $menu['name'] ); if ( is_wp_error( $mid ) ) { continue; } wp_update_term( $mid, 'nav_menu', array( 'slug' => $menu['slug'] ) ); }
		rsm_import_menu_items( $mid, $menu['items'] ); $made++;
		if ( ! empty( $menu['location'] ) ) { $loc = get_theme_mod( 'nav_menu_locations', array() ); $loc[ $menu['location'] ] = $mid; set_theme_mod( 'nav_menu_locations', $loc ); }
	}
	$log[] = sprintf( /* translators: 1: menus written, 2: total */ __( 'Menus: %1$d written, %2$d in total.', 'rsm' ), $made, count( $site['menus'] ) );

	// 3. Elementor settings, colours and type
	foreach ( $site['options'] as $k => $v ) { update_option( $k, $v ); }
	$kit_id = (int) \Elementor\Plugin::$instance->kits_manager->get_active_id();
	if ( ! $kit_id || 'publish' !== get_post_status( $kit_id ) ) { $kit_id = (int) \Elementor\Core\Kits\Manager::create_default_kit(); update_option( 'elementor_active_kit', $kit_id ); }
	if ( $kit_id ) { $cur = get_post_meta( $kit_id, '_elementor_page_settings', true ); $cur = is_array( $cur ) ? $cur : array(); if ( $reset || empty( $cur['rsm_kit'] ) ) { update_post_meta( $kit_id, '_elementor_page_settings', array_merge( $cur, $site['kit'], array( 'rsm_kit' => '1' ) ) ); $log[] = __( 'Global colours, type and page width set.', 'rsm' ); } }

	// 4. header and footer
	foreach ( $site['parts'] as $slot => $doc ) { list( $id, $state ) = rsm_import_doc( 'rsm_part', $doc, $reset, $tokens ); if ( $id ) { update_option( 'rsm_part_' . $slot, $id ); } $log[] = sprintf( '%s: %s.', $doc['title'], $state ); }

	// 5. pages
	foreach ( $site['pages'] as $doc ) { list( $id, $state ) = rsm_import_doc( 'page', $doc, $reset, $tokens ); $log[] = sprintf( '%s: %s.', $doc['title'], $state );
		if ( $id && ! empty( $doc['front'] ) ) { update_option( 'show_on_front', 'page' ); update_option( 'page_on_front', $id ); }
		if ( $id && ! empty( $doc['posts_page'] ) ) { update_option( 'page_for_posts', $id ); } }

	// 6. site settings
	if ( $reset || ! get_option( 'rsm_import_done' ) ) {
		update_option( 'rsm_schema_graph', strtr( wp_json_encode( $site['schema_graph'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ), $tokens ) );
		update_option( 'rsm_llms_txt', $site['llms'] );
		if ( ! get_option( 'permalink_structure' ) ) { global $wp_rewrite; $wp_rewrite->set_permalink_structure( '/%postname%/' ); }
		if ( ! empty( $tokens['{{mediaid:logo}}'] ) ) { set_theme_mod( 'custom_logo', (int) $tokens['{{mediaid:logo}}'] ); update_option( 'site_icon', (int) $tokens['{{mediaid:logo}}'] ); }
	}
	flush_rewrite_rules();
	\Elementor\Plugin::$instance->files_manager->clear_cache();
	update_option( 'rsm_import_done', time() );
	$log[] = __( 'Done. The website is ready.', 'rsm' );
	return $log;
}

/* ---------- the screen ---------- */
function rsm_setup_screen() {
	$ready = rsm_setup_ready(); $done = (int) get_option( 'rsm_import_done' ); $log = get_transient( 'rsm_setup_log' ); delete_transient( 'rsm_setup_log' );
	$labels = array( 'active' => __( 'Active', 'rsm' ), 'installed' => __( 'Installed, not active', 'rsm' ), 'missing' => __( 'Not installed', 'rsm' ) ); ?>
	<div class="wrap" style="max-width:860px">
		<h1><?php esc_html_e( 'Relevant Search Media: setup', 'rsm' ); ?></h1>
		<p><?php esc_html_e( 'Two steps. After the second one the whole website is in place: every page, the header and footer, the menus, the media and the settings.', 'rsm' ); ?></p>
		<?php if ( $log ) : ?><div class="notice notice-success inline"><ul style="margin:.6em 0 .6em 1.2em;list-style:disc"><?php foreach ( (array) $log as $l ) { echo '<li>' . esc_html( $l ) . '</li>'; } ?></ul></div><?php endif; ?>

		<div class="card" style="max-width:none"><h2>1. <?php esc_html_e( 'Required plugins', 'rsm' ); ?></h2>
			<table class="widefat striped" style="margin:10px 0"><tbody>
			<?php foreach ( rsm_setup_plugins() as $p ) : $st = rsm_setup_plugin_state( $p['file'] ); ?><tr><td><strong><?php echo esc_html( $p['name'] ); ?></strong></td><td><?php echo esc_html( 'wordpress.org' === $p['source'] ? __( 'Free, from WordPress.org', 'rsm' ) : __( 'Bundled with this theme', 'rsm' ) ); ?></td><td id="rsm-state-<?php echo esc_attr( sanitize_title( $p['name'] ) ); ?>"><?php echo esc_html( $labels[ $st ] ); ?></td></tr><?php endforeach; ?>
			</tbody></table>
			<?php if ( ! $ready ) : ?><form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>"><?php wp_nonce_field( 'rsm_install_plugins' ); ?><input type="hidden" name="action" value="rsm_install_plugins"><button class="button button-primary button-hero" id="rsm-install"><?php esc_html_e( 'Install and activate both', 'rsm' ); ?></button></form>
			<?php else : ?><p><span class="dashicons dashicons-yes-alt" style="color:#00a32a"></span> <?php esc_html_e( 'Both plugins are active.', 'rsm' ); ?></p><?php endif; ?>
		</div>

		<div class="card" style="max-width:none"><h2>2. <?php esc_html_e( 'Import the website', 'rsm' ); ?></h2>
			<p><?php esc_html_e( 'Creates the pages, header, footer, menus and media, sets the home page, and applies the colours and type. Running it again never makes duplicates: anything already imported is left as you have edited it.', 'rsm' ); ?></p>
			<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>"><?php wp_nonce_field( 'rsm_import' ); ?><input type="hidden" name="action" value="rsm_import">
				<?php if ( $done ) : ?><p><label><input type="checkbox" name="reset" value="1"> <?php esc_html_e( 'Put everything back to the original design (overwrites my edits to the imported pages, header, footer and menus)', 'rsm' ); ?></label></p><?php endif; ?>
				<button class="button button-primary button-hero" id="rsm-import" <?php disabled( ! $ready ); ?>><?php echo esc_html( $done ? __( 'Run the import again', 'rsm' ) : __( 'Import the website', 'rsm' ) ); ?></button>
			</form>
			<?php if ( $done ) : ?><p style="margin-top:14px"><span class="dashicons dashicons-yes-alt" style="color:#00a32a"></span> <?php printf( /* translators: %s: date */ esc_html__( 'Last import: %s.', 'rsm' ), esc_html( wp_date( get_option( 'date_format' ) . ' ' . get_option( 'time_format' ), $done ) ) ); ?>
				<a class="button" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'View the site', 'rsm' ); ?></a>
				<a class="button" href="<?php echo esc_url( admin_url( 'edit.php?post_type=page' ) ); ?>"><?php esc_html_e( 'Edit pages', 'rsm' ); ?></a>
				<a class="button" href="<?php echo esc_url( admin_url( 'edit.php?post_type=rsm_part' ) ); ?>"><?php esc_html_e( 'Edit header and footer', 'rsm' ); ?></a></p><?php endif; ?>
		</div>
	</div>
<?php }
