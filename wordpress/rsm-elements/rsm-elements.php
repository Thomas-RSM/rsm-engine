<?php
/**
 * Plugin Name: RSM Elements
 * Description: Elementor widgets, editable header and footer templates, and search basics for the Relevant Search Media theme. Works with Elementor Free.
 * Version: 1.4.1
 * Author: Relevant Search Media
 * Requires at least: 6.4
 * Requires PHP: 7.4
 * Text Domain: rsm-elements
 * License: GPL-2.0-or-later
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
define( 'RSM_EL_VERSION', '1.4.1' );
require_once plugin_dir_path( __FILE__ ) . 'push.php';
define( 'RSM_EL_DIR', plugin_dir_path( __FILE__ ) );

/** Theme asset base (the design's CSS, scripts, fonts and data live in the theme). */
function rsm_asset( $path = '' ) { return apply_filters( 'rsm_asset_url', get_template_directory_uri() . '/assets/' ) . ltrim( $path, '/' ); }

/** Allow inline SVG pictures typed into widget fields. */
function rsm_svg( $svg ) {
	$a = array( 'class' => true, 'id' => true, 'd' => true, 'fill' => true, 'stroke' => true, 'stroke-width' => true, 'stroke-linecap' => true, 'stroke-linejoin' => true, 'stroke-dasharray' => true, 'opacity' => true, 'x' => true, 'y' => true, 'x1' => true, 'y1' => true, 'x2' => true, 'y2' => true, 'cx' => true, 'cy' => true, 'r' => true, 'rx' => true, 'ry' => true, 'width' => true, 'height' => true, 'viewbox' => true, 'transform' => true, 'offset' => true, 'stop-color' => true, 'stop-opacity' => true, 'font-family' => true, 'font-size' => true, 'font-weight' => true, 'letter-spacing' => true, 'text-anchor' => true, 'role' => true, 'aria-label' => true, 'aria-hidden' => true, 'xmlns' => true, 'href' => true, 'attributename' => true, 'values' => true, 'dur' => true, 'repeatcount' => true, 'begin' => true, 'type' => true, 'keytimes' => true, 'style' => true, 'points' => true );
	$tags = array();
	foreach ( array( 'svg', 'g', 'path', 'circle', 'ellipse', 'rect', 'line', 'polyline', 'polygon', 'text', 'tspan', 'defs', 'lineargradient', 'radialgradient', 'stop', 'animate', 'animatetransform', 'animatemotion', 'mpath', 'image', 'title' ) as $t ) { $tags[ $t ] = $a; }
	$out = wp_kses( $svg, $tags );
	// kses lowercases names; SVG used as an image is XML and case matters.
	return str_replace( array( 'viewbox=', '<lineargradient', '</lineargradient', '<radialgradient', '</radialgradient', '<animatemotion', '</animatemotion', '<animatetransform', '</animatetransform', 'attributename=', 'repeatcount=', 'keytimes=' ), array( 'viewBox=', '<linearGradient', '</linearGradient', '<radialGradient', '</radialGradient', '<animateMotion', '</animateMotion', '<animateTransform', '</animateTransform', 'attributeName=', 'repeatCount=', 'keyTimes=' ), $out );
}
function rsm_url( $v ) { $u = is_array( $v ) ? ( $v['url'] ?? '' ) : $v; return esc_url( $u ); }
function rsm_inline( $html ) { return wp_kses( $html, array( 'span' => array( 'class' => true, 'style' => true ), 'b' => array(), 'strong' => array(), 'em' => array( 'class' => true ), 'i' => array(), 'br' => array(), 'a' => array( 'href' => true, 'class' => true ) ) ); }

/* ---------- header and footer templates, editable with Elementor Free ---------- */
add_action( 'init', function () {
	register_post_type( 'rsm_part', array(
		'labels' => array( 'name' => __( 'Header & Footer', 'rsm-elements' ), 'singular_name' => __( 'Site part', 'rsm-elements' ), 'add_new_item' => __( 'Add site part', 'rsm-elements' ), 'edit_item' => __( 'Edit site part', 'rsm-elements' ) ),
		'public' => true, 'exclude_from_search' => true, 'show_in_nav_menus' => false, 'show_ui' => true, 'show_in_menu' => 'themes.php', 'show_in_rest' => true,
		'supports' => array( 'title', 'editor', 'elementor' ), 'rewrite' => array( 'slug' => 'site-part' ), 'has_archive' => false,
	) );
} );
add_filter( 'option_elementor_cpt_support', function ( $v ) { $v = is_array( $v ) ? $v : array( 'page', 'post' ); if ( ! in_array( 'rsm_part', $v, true ) ) { $v[] = 'rsm_part'; } return $v; } );
add_filter( 'default_option_elementor_cpt_support', function () { return array( 'page', 'post', 'rsm_part' ); } );
add_filter( 'wp_robots', function ( $r ) { if ( is_singular( 'rsm_part' ) ) { $r['noindex'] = true; } return $r; } );
add_filter( 'wp_sitemaps_post_types', function ( $t ) { unset( $t['rsm_part'] ); return $t; } );
add_filter( 'template_include', function ( $t ) { return is_singular( 'rsm_part' ) ? RSM_EL_DIR . 'part-preview.php' : $t; } );

function rsm_part_id( $slot ) {
	$id = (int) get_option( 'rsm_part_' . $slot );
	if ( $id && 'publish' === get_post_status( $id ) ) { return $id; }
	return 0;
}
/** Print a header or footer part. Returns false when none is set, so the theme can fall back. */
function rsm_render_part( $slot ) {
	$id = rsm_part_id( $slot );
	if ( ! $id || ! did_action( 'elementor/loaded' ) ) { return false; }
	if ( is_singular( 'rsm_part' ) && get_queried_object_id() === $id ) { return true; }
	echo \Elementor\Plugin::instance()->frontend->get_builder_content_for_display( $id ); // phpcs:ignore WordPress.Security.EscapeOutput
	return true;
}
add_filter( 'display_post_states', function ( $states, $post ) {
	foreach ( array( 'header' => __( 'Site header', 'rsm-elements' ), 'footer' => __( 'Site footer', 'rsm-elements' ) ) as $k => $l ) { if ( (int) get_option( 'rsm_part_' . $k ) === $post->ID ) { $states[] = $l; } }
	return $states;
}, 10, 2 );

/* ---------- widgets ---------- */
add_action( 'elementor/elements/categories_registered', function ( $m ) { $m->add_category( 'rsm', array( 'title' => __( 'Relevant Search Media', 'rsm-elements' ), 'icon' => 'eicon-star' ) ); } );
add_action( 'elementor/widgets/register', function ( $wm ) {
	require_once RSM_EL_DIR . 'widgets.php';
	foreach ( rsm_widget_classes() as $c ) { $wm->register( new $c() ); }
} );
add_action( 'elementor/editor/after_enqueue_styles', function () { wp_add_inline_style( 'elementor-editor', '.elementor-element .icon .rsm-ico{font-size:28px}' ); } );

/* ---------- search basics: title, description, social tags, structured data, robots, llms.txt ---------- */
function rsm_seo( $key, $post_id = 0 ) { $post_id = $post_id ? $post_id : get_queried_object_id(); return $post_id ? (string) get_post_meta( $post_id, '_rsm_' . $key, true ) : ''; }
add_filter( 'pre_get_document_title', function ( $t ) { $v = is_singular() ? rsm_seo( 'title' ) : ''; return $v ? $v : $t; } );
add_action( 'wp_head', function () {
	if ( is_singular( 'rsm_part' ) ) { return; }
	$d = is_singular() ? rsm_seo( 'description' ) : '';
	$img = is_singular() ? rsm_seo( 'image' ) : '';
	$title = wp_get_document_title();
	if ( $d ) { printf( "<meta name=\"description\" content=\"%s\">\n", esc_attr( $d ) ); }
	printf( "<meta property=\"og:type\" content=\"website\">\n<meta property=\"og:site_name\" content=\"%s\">\n<meta property=\"og:title\" content=\"%s\">\n", esc_attr( get_bloginfo( 'name' ) ), esc_attr( $title ) );
	if ( is_singular() ) { printf( "<meta property=\"og:url\" content=\"%s\">\n", esc_url( get_permalink() ) ); }
	if ( $d ) { printf( "<meta property=\"og:description\" content=\"%s\">\n<meta name=\"twitter:description\" content=\"%s\">\n", esc_attr( $d ), esc_attr( $d ) ); }
	if ( $img ) { printf( "<meta property=\"og:image\" content=\"%s\">\n<meta property=\"og:image:width\" content=\"1200\">\n<meta property=\"og:image:height\" content=\"630\">\n<meta name=\"twitter:card\" content=\"summary_large_image\">\n<meta name=\"twitter:image\" content=\"%s\">\n", esc_url( $img ), esc_url( $img ) ); }
	$graph = json_decode( (string) get_option( 'rsm_schema_graph', '' ), true );
	$graph = is_array( $graph ) ? $graph : array();
	if ( is_singular() ) {
		$home = trailingslashit( home_url() );
		$node = array( '@type' => 'WebPage', '@id' => get_permalink() . '#webpage', 'url' => get_permalink(), 'name' => $title, 'inLanguage' => get_bloginfo( 'language' ), 'datePublished' => get_the_date( 'c' ), 'dateModified' => get_the_modified_date( 'c' ), 'isPartOf' => array( '@id' => $home . '#website' ) );
		if ( $d ) { $node['description'] = $d; }
		$graph[] = $node;
	}
	$graph = apply_filters( 'rsm_schema_graph', $graph );
	if ( $graph ) { echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => array_values( $graph ) ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n"; }
}, 5 );
/** Widgets print their own structured data (questions, film) beside their markup, so it survives Elementor's output cache. */
function rsm_schema_push( $node ) {
	echo '<script type="application/ld+json">' . wp_json_encode( array_merge( array( '@context' => 'https://schema.org' ), $node ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . '</script>'; // phpcs:ignore WordPress.Security.EscapeOutput
}
add_filter( 'robots_txt', function ( $out, $public ) {
	if ( ! $public ) { return $out; }
	$out .= "\n# AI crawlers, allowed by name\n";
	foreach ( array( 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'Google-Extended', 'PerplexityBot', 'ClaudeBot', 'anthropic-ai', 'Bingbot', 'Applebot', 'Applebot-Extended', 'Meta-ExternalAgent', 'Amazonbot', 'CCBot' ) as $b ) { $out .= "User-agent: $b\nAllow: /\n"; }
	return $out;
}, 10, 2 );
add_action( 'init', function () {
	$path = wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? esc_url_raw( wp_unslash( $_SERVER['REQUEST_URI'] ) ) : '', PHP_URL_PATH );
	$base = wp_parse_url( home_url( '/' ), PHP_URL_PATH );
	if ( $path && rtrim( (string) $base, '/' ) . '/llms.txt' === $path ) {
		$txt = (string) get_option( 'rsm_llms_txt', '' );
		if ( $txt ) { status_header( 200 ); header( 'Content-Type: text/plain; charset=utf-8' ); echo str_replace( '{{home}}', untrailingslashit( home_url() ), $txt ); exit; } // phpcs:ignore WordPress.Security.EscapeOutput
	}
} );
/* Page fields for the title and description shown in search results. */
add_action( 'add_meta_boxes', function () {
	add_meta_box( 'rsm_seo', __( 'Search result title and description', 'rsm-elements' ), function ( $post ) {
		wp_nonce_field( 'rsm_seo', 'rsm_seo_nonce' );
		printf( '<p><label>%s<br><input type="text" name="rsm_seo_title" value="%s" class="widefat"></label></p>', esc_html__( 'Title (30 to 60 characters)', 'rsm-elements' ), esc_attr( rsm_seo( 'title', $post->ID ) ) );
		printf( '<p><label>%s<br><textarea name="rsm_seo_description" rows="3" class="widefat">%s</textarea></label></p>', esc_html__( 'Description (110 to 155 characters)', 'rsm-elements' ), esc_textarea( rsm_seo( 'description', $post->ID ) ) );
	}, array( 'page', 'post' ), 'normal' );
} );
add_action( 'save_post', function ( $id ) {
	if ( ! isset( $_POST['rsm_seo_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['rsm_seo_nonce'] ), 'rsm_seo' ) || ! current_user_can( 'edit_post', $id ) ) { return; }
	foreach ( array( 'title', 'description' ) as $k ) { if ( isset( $_POST[ 'rsm_seo_' . $k ] ) ) { update_post_meta( $id, '_rsm_' . $k, sanitize_text_field( wp_unslash( $_POST[ 'rsm_seo_' . $k ] ) ) ); } }
} );
