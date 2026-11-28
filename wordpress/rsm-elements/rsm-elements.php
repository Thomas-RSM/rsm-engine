<?php
/**
 * Plugin Name: RSM Elements
 * Description: Elementor widgets, editable header and footer templates, and search basics for the Relevant Search Media theme. Works with Elementor Free.
 * Version: 1.7.0
 * Author: Relevant Search Media
 * Requires at least: 6.4
 * Requires PHP: 7.4
 * Text Domain: rsm-elements
 * License: GPL-2.0-or-later
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
define( 'RSM_EL_VERSION', '1.7.0' );
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
}, 5 );

/** Dates a page shows and declares: set per page, never the moment WordPress happened to save it. */
function rsm_page_date( $which, $id = 0 ) { $id = $id ? $id : get_the_ID(); $v = (string) get_post_meta( $id, '_rsm_' . $which, true );
	if ( preg_match( '/^\d{4}-\d{2}-\d{2}$/', $v ) ) { return $v; } return 'published' === $which ? get_the_date( 'Y-m-d', $id ) : get_the_modified_date( 'Y-m-d', $id ); }

/** Widgets hand their structured data here; the footer prints everything as one block. */
function rsm_schema_push( $node ) { if ( ! isset( $GLOBALS['rsm_nodes'] ) ) { $GLOBALS['rsm_nodes'] = array(); } $GLOBALS['rsm_nodes'][] = $node; }
add_action( 'wp_footer', function () {
	if ( is_admin() || is_feed() ) { return; }
	$graph = json_decode( (string) get_option( 'rsm_schema_graph', '' ), true ); $graph = is_array( $graph ) ? $graph : array();
	if ( is_singular() ) { $home = trailingslashit( home_url() ); $d = rsm_seo( 'description' ); $img = rsm_seo( 'image' );
		$node = array( '@type' => 'WebPage', '@id' => get_permalink() . '#webpage', 'url' => get_permalink(), 'name' => wp_get_document_title(), 'inLanguage' => 'en-US', 'datePublished' => rsm_page_date( 'published' ), 'dateModified' => rsm_page_date( 'reviewed' ), 'isPartOf' => array( '@id' => $home . '#website' ), 'about' => array( '@id' => $home . '#organization' ) );
		if ( $d ) { $node['description'] = $d; } if ( $img ) { $node['primaryImageOfPage'] = array( '@type' => 'ImageObject', 'url' => $img ); }
		$person = null; foreach ( $graph as $g ) { if ( isset( $g['@type'] ) && 'Person' === $g['@type'] && ! empty( $g['@id'] ) ) { $person = $g['@id']; } }
		if ( $person ) { $node['author'] = array( '@id' => $person ); $node['reviewedBy'] = array( '@id' => $person ); }
		if ( ! is_front_page() ) { $items = array( array( '@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => $home ) ); $pos = 2;
			foreach ( array_reverse( get_post_ancestors( get_the_ID() ) ) as $aid ) { $items[] = array( '@type' => 'ListItem', 'position' => $pos++, 'name' => get_the_title( $aid ), 'item' => get_permalink( $aid ) ); }
			$items[] = array( '@type' => 'ListItem', 'position' => $pos, 'name' => get_the_title(), 'item' => get_permalink() );
			$node['breadcrumb'] = array( '@id' => get_permalink() . '#breadcrumb' ); $graph[] = array( '@type' => 'BreadcrumbList', '@id' => get_permalink() . '#breadcrumb', 'itemListElement' => $items ); }
		$graph[] = $node;
	}
	foreach ( (array) ( $GLOBALS['rsm_nodes'] ?? array() ) as $n ) { $graph[] = $n; }
	$graph = apply_filters( 'rsm_schema_graph', $graph );
	if ( $graph ) { echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => array_values( $graph ) ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n"; }
}, 5 );

/* ---------- one sitemap, ours: every indexable page, its real review date and its images ---------- */
add_filter( 'wp_sitemaps_enabled', '__return_false' );
function rsm_sitemap_xml() {
	$o = '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
	$front = (int) get_option( 'page_on_front' );
	foreach ( get_posts( array( 'post_type' => array( 'page', 'post' ), 'post_status' => 'publish', 'posts_per_page' => 2000, 'orderby' => 'menu_order title', 'order' => 'ASC' ) ) as $p ) {
		if ( get_post_meta( $p->ID, '_rsm_noindex', true ) ) { continue; }
		$o .= '<url><loc>' . esc_url( get_permalink( $p ) ) . '</loc><lastmod>' . esc_html( rsm_page_date( 'reviewed', $p->ID ) ) . '</lastmod>';
		$imgs = array_filter( array_unique( array_merge( array( (string) get_post_meta( $p->ID, '_rsm_image', true ) ), (array) json_decode( (string) get_post_meta( $p->ID, '_rsm_images', true ), true ) ) ) );
		if ( $p->ID === $front ) { $logo = wp_get_attachment_url( (int) get_theme_mod( 'custom_logo' ) ); if ( $logo ) { $imgs[] = $logo; } } $imgs = array_unique( $imgs );
		foreach ( $imgs as $i ) { $o .= '<image:image><image:loc>' . esc_url( $i ) . '</image:loc></image:image>'; }
		$o .= "</url>\n";
	}
	return $o . '</urlset>';
}
add_action( 'init', function () {
	$path = wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? esc_url_raw( wp_unslash( $_SERVER['REQUEST_URI'] ) ) : '', PHP_URL_PATH );
	$base = rtrim( (string) wp_parse_url( home_url( '/' ), PHP_URL_PATH ), '/' );
	if ( $path && in_array( $path, array( $base . '/sitemap.xml', $base . '/wp-sitemap.xml' ), true ) ) { status_header( 200 ); header( 'Content-Type: application/xml; charset=utf-8' ); header( 'X-Robots-Tag: noindex' ); echo rsm_sitemap_xml(); exit; } // phpcs:ignore
}, 1 );

/* ---------- llms.txt: ours, even where a host plugin writes its own file ---------- */
function rsm_llms_text() { $txt = (string) get_option( 'rsm_llms_txt', '' ); if ( '' === $txt ) { return ''; }
	if ( false !== strpos( $txt, '{{pages}}' ) ) { $rows = array(); $front = (int) get_option( 'page_on_front' );
		foreach ( get_posts( array( 'post_type' => array( 'page', 'post' ), 'post_status' => 'publish', 'posts_per_page' => 2000, 'orderby' => 'menu_order title', 'order' => 'ASC' ) ) as $p ) { if ( get_post_meta( $p->ID, '_rsm_noindex', true ) ) { continue; }
			$d = (string) get_post_meta( $p->ID, '_rsm_description', true ); $rows[ $p->ID === $front ? 0 : $p->ID ] = '- [' . wp_strip_all_tags( get_the_title( $p ) ) . '](' . get_permalink( $p ) . ')' . ( $d ? ': ' . $d : '' ); }
		ksort( $rows ); $txt = str_replace( '{{pages}}', implode( "\n", $rows ), $txt ); }
	return str_replace( '{{home}}', untrailingslashit( home_url() ), $txt ); }
function rsm_llms_sync() { $txt = rsm_llms_text(); if ( '' === $txt ) { return; } $f = ABSPATH . 'llms.txt';
	if ( file_exists( $f ) && is_writable( $f ) && file_get_contents( $f ) !== $txt ) { file_put_contents( $f, $txt ); } // phpcs:ignore WordPress.WP.AlternativeFunctions
}
add_action( 'save_post', 'rsm_llms_sync', 9999 ); add_action( 'rsm_after_push', 'rsm_llms_sync' ); add_action( 'admin_init', 'rsm_llms_sync' ); add_action( 'shutdown', function () { if ( wp_doing_cron() ) { rsm_llms_sync(); } } );

add_filter( 'robots_txt', function ( $out, $public ) {
	if ( ! $public ) { return $out; }
	$out .= "\n# AI crawlers, allowed by name\n";
	$out = preg_replace( '/^Sitemap:.*$/mi', '', $out ) . "\nSitemap: " . home_url( '/sitemap.xml' ) . "\n";
	foreach ( array( 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'Google-Extended', 'PerplexityBot', 'ClaudeBot', 'anthropic-ai', 'Bingbot', 'Applebot', 'Applebot-Extended', 'Meta-ExternalAgent', 'Amazonbot', 'CCBot' ) as $b ) { $out .= "User-agent: $b\nAllow: /\n"; }
	return $out;
}, 10, 2 );
add_action( 'init', function () {
	$path = wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? esc_url_raw( wp_unslash( $_SERVER['REQUEST_URI'] ) ) : '', PHP_URL_PATH );
	$base = wp_parse_url( home_url( '/' ), PHP_URL_PATH );
	if ( $path && rtrim( (string) $base, '/' ) . '/llms.txt' === $path ) {
		$txt = rsm_llms_text();
		if ( $txt ) { status_header( 200 ); header( 'Content-Type: text/plain; charset=utf-8' ); echo $txt; exit; } // phpcs:ignore WordPress.Security.EscapeOutput
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
