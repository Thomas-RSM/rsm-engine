<?php
/**
 * Push: lets a signed-in administrator send pages, header, footer, menus and extra styles
 * to the site over the REST API. Administrators only. Nothing here is public.
 *
 * @package rsm-elements
 */

defined( 'ABSPATH' ) || exit;

function rsm_push_find( $type, $key ) {
	$q = get_posts( array( 'post_type' => $type, 'post_status' => 'any', 'meta_key' => '_rsm_import_key', 'meta_value' => $key, 'posts_per_page' => 1, 'fields' => 'ids', 'no_found_rows' => true ) ); // phpcs:ignore WordPress.DB.SlowDBQuery
	return $q ? (int) $q[0] : 0;
}
function rsm_push_tokens( $json ) {
	$json = strtr( $json, array( '{{home}}' => untrailingslashit( home_url() ), '{{assets}}' => untrailingslashit( get_template_directory_uri() . '/assets' ) ) );
	return preg_replace_callback( '/\{\{(media|mediaid):([a-z0-9_-]+)\}\}/', function ( $m ) {
		$id = rsm_push_find( 'attachment', $m[2] );
		if ( 'mediaid' === $m[1] ) { return (string) $id; }
		return $id ? str_replace( '/', '\/', wp_get_attachment_url( $id ) ) : '';
	}, $json );
}
function rsm_push_doc( $type, $doc, $overwrite ) {
	$key = sanitize_key( $doc['key'] ?? ( $doc['slug'] ?? '' ) );
	if ( ! $key || empty( $doc['title'] ) || ! isset( $doc['data'] ) || ! is_array( $doc['data'] ) ) { return array( 0, 'invalid' ); }
	$id = rsm_push_find( $type, $key );
	if ( ! $id && 'page' === $type && ! empty( $doc['slug'] ) ) { $p = get_page_by_path( sanitize_title( $doc['slug'] ) ); if ( $p && ! get_post_meta( $p->ID, '_rsm_import_key', true ) && ! empty( $doc['adopt'] ) ) { $id = (int) $p->ID; } }
	if ( $id && ! $overwrite ) { return array( $id, 'kept' ); }
	$args = array( 'post_type' => $type, 'post_title' => sanitize_text_field( $doc['title'] ), 'post_name' => sanitize_title( $doc['slug'] ?? $key ), 'post_status' => in_array( $doc['status'] ?? 'publish', array( 'publish', 'draft', 'private' ), true ) ? ( $doc['status'] ?? 'publish' ) : 'publish', 'post_content' => '' );
	if ( 'page' === $type && ! empty( $doc['parent'] ) ) { $pp = get_page_by_path( sanitize_text_field( $doc['parent'] ) ); if ( $pp ) { $args['post_parent'] = (int) $pp->ID; } }
	if ( $id ) { $args['ID'] = $id; wp_update_post( $args ); $state = 'updated'; } else { $id = wp_insert_post( $args ); $state = 'created'; }
	if ( is_wp_error( $id ) || ! $id ) { return array( 0, 'failed' ); }
	update_post_meta( $id, '_rsm_import_key', $key );
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $id, '_elementor_template_type', 'page' === $type ? 'wp-page' : 'wp-post' );
	update_post_meta( $id, '_elementor_version', defined( 'ELEMENTOR_VERSION' ) ? ELEMENTOR_VERSION : '3.0.0' );
	update_post_meta( $id, '_elementor_data', wp_slash( rsm_push_tokens( wp_json_encode( $doc['data'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) ) ) );
	delete_post_meta( $id, '_elementor_css' ); delete_post_meta( $id, '_elementor_element_cache' );
	foreach ( (array) ( $doc['seo'] ?? array() ) as $k => $v ) { update_post_meta( $id, '_rsm_' . sanitize_key( $k ), sanitize_text_field( rsm_push_tokens( (string) $v ) ) ); }
	return array( $id, $state );
}
function rsm_push_menu_items( $menu_id, $items, $parent = 0 ) {
	foreach ( (array) $items as $it ) {
		$url = (string) ( $it['url'] ?? '#' ); if ( 0 === strpos( $url, '/' ) ) { $url = home_url( $url ); }
		$id = wp_update_nav_menu_item( $menu_id, 0, array( 'menu-item-title' => wp_kses_post( $it['title'] ?? '' ), 'menu-item-url' => esc_url_raw( $url ), 'menu-item-description' => sanitize_text_field( $it['description'] ?? '' ), 'menu-item-classes' => sanitize_text_field( $it['classes'] ?? '' ), 'menu-item-parent-id' => $parent, 'menu-item-type' => 'custom', 'menu-item-status' => 'publish' ) );
		if ( ! is_wp_error( $id ) && ! empty( $it['children'] ) ) { rsm_push_menu_items( $menu_id, $it['children'], $id ); }
	}
}

add_action( 'rest_api_init', function () {
	$admin = function () { return current_user_can( 'manage_options' ); };

	register_rest_route( 'rsm/v1', '/state', array( 'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function () {
		$out = array( 'version' => RSM_EL_VERSION, 'theme' => wp_get_theme()->get( 'Version' ), 'front' => (int) get_option( 'page_on_front' ), 'docs' => array(), 'menus' => array(), 'css_bytes' => strlen( (string) get_option( 'rsm_extra_css', '' ) ) );
		foreach ( get_posts( array( 'post_type' => array( 'page', 'rsm_part' ), 'post_status' => 'any', 'posts_per_page' => 500 ) ) as $p ) {
			$out['docs'][] = array( 'id' => $p->ID, 'type' => $p->post_type, 'slug' => $p->post_name, 'status' => $p->post_status, 'key' => get_post_meta( $p->ID, '_rsm_import_key', true ), 'modified' => $p->post_modified_gmt, 'url' => get_permalink( $p ) );
		}
		foreach ( wp_get_nav_menus() as $m ) { $out['menus'][] = array( 'slug' => $m->slug, 'items' => (int) $m->count ); }
		return $out;
	} ) );

	register_rest_route( 'rsm/v1', '/push', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( WP_REST_Request $req ) {
		$b = $req->get_json_params(); if ( ! is_array( $b ) ) { return new WP_Error( 'rsm_bad_body', 'JSON body expected.', array( 'status' => 400 ) ); }
		if ( ! class_exists( '\Elementor\Plugin' ) ) { return new WP_Error( 'rsm_no_elementor', 'Elementor is not active.', array( 'status' => 409 ) ); }
		$over = ! empty( $b['overwrite'] ); $log = array();
		foreach ( (array) ( $b['parts'] ?? array() ) as $slot => $doc ) { $slot = sanitize_key( $slot ); list( $id, $st ) = rsm_push_doc( 'rsm_part', $doc, $over ); if ( $id ) { update_option( 'rsm_part_' . $slot, $id ); } $log[] = array( 'part' => $slot, 'id' => $id, 'state' => $st ); }
		foreach ( (array) ( $b['pages'] ?? array() ) as $doc ) { list( $id, $st ) = rsm_push_doc( 'page', $doc, $over );
			if ( $id && ! empty( $doc['front'] ) ) { update_option( 'show_on_front', 'page' ); update_option( 'page_on_front', $id ); }
			if ( $id && ! empty( $doc['posts_page'] ) ) { update_option( 'page_for_posts', $id ); }
			$log[] = array( 'page' => $doc['slug'] ?? '', 'id' => $id, 'state' => $st, 'url' => $id ? get_permalink( $id ) : '' ); }
		foreach ( (array) ( $b['menus'] ?? array() ) as $menu ) {
			$slug = sanitize_title( $menu['slug'] ?? '' ); if ( ! $slug ) { continue; }
			$obj = wp_get_nav_menu_object( $slug );
			if ( $obj ) { foreach ( (array) wp_get_nav_menu_items( $obj->term_id ) as $it ) { wp_delete_post( $it->ID, true ); } $mid = $obj->term_id; }
			else { $mid = wp_create_nav_menu( sanitize_text_field( $menu['name'] ?? $slug ) ); if ( is_wp_error( $mid ) ) { $log[] = array( 'menu' => $slug, 'state' => 'failed' ); continue; } wp_update_term( $mid, 'nav_menu', array( 'slug' => $slug ) ); }
			rsm_push_menu_items( $mid, $menu['items'] ?? array() ); $log[] = array( 'menu' => $slug, 'state' => 'written' );
		}
		if ( isset( $b['css'] ) ) { update_option( 'rsm_extra_css', wp_strip_all_tags( (string) $b['css'] ), false ); $log[] = array( 'css' => strlen( (string) $b['css'] ) ); }
		if ( isset( $b['schema_graph'] ) && is_array( $b['schema_graph'] ) ) { update_option( 'rsm_schema_graph', rsm_push_tokens( wp_json_encode( $b['schema_graph'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) ) ); $log[] = array( 'schema' => 'written' ); }
		if ( isset( $b['llms'] ) ) { update_option( 'rsm_llms_txt', sanitize_textarea_field( (string) $b['llms'] ) ); $log[] = array( 'llms' => 'written' ); }
		foreach ( (array) ( $b['trash'] ?? array() ) as $key ) { $id = rsm_push_find( 'page', sanitize_key( $key ) ); if ( $id ) { wp_trash_post( $id ); $log[] = array( 'trashed' => $key ); } }
		\Elementor\Plugin::$instance->files_manager->clear_cache();
		do_action( 'litespeed_purge_all' );
		return array( 'ok' => true, 'log' => $log );
	} ) );
} );

/* Styles sent with a push, added after the theme's own. */
add_action( 'wp_enqueue_scripts', function () {
	$css = (string) get_option( 'rsm_extra_css', '' );
	if ( '' === $css ) { return; }
	wp_register_style( 'rsm-extra', false, array(), RSM_EL_VERSION ); wp_enqueue_style( 'rsm-extra' ); wp_add_inline_style( 'rsm-extra', $css );
}, 30 );
