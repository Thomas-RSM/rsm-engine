<?php
/**
 * Relevant Search Media theme.
 * The design lives in assets/site.css and assets/site.js. Page content lives in Elementor, never in these files.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
define( 'RSM_THEME_VERSION', '1.0.0' );

add_action( 'after_setup_theme', function () {
	load_theme_textdomain( 'rsm', get_template_directory() . '/languages' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
	add_theme_support( 'custom-logo' );
	add_theme_support( 'responsive-embeds' );
	register_nav_menus( array( 'primary' => __( 'Main menu', 'rsm' ) ) );
	$GLOBALS['content_width'] = 1296;
} );

add_action( 'wp_enqueue_scripts', function () {
	$uri = get_template_directory_uri() . '/assets/'; $dir = get_template_directory() . '/assets/';
	wp_enqueue_style( 'rsm-site', $uri . 'site.css', array(), filemtime( $dir . 'site.css' ) );
	wp_enqueue_style( 'rsm-wp', $uri . 'wp.css', array( 'rsm-site' ), filemtime( $dir . 'wp.css' ) );
	wp_enqueue_script( 'rsm-site', $uri . 'site.js', array(), filemtime( $dir . 'site.js' ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
	wp_add_inline_script( 'rsm-site', 'window.RSM_BASE=' . wp_json_encode( $uri ) . ';', 'before' );
}, 20 );
/* The header and footer are drawn after the head has closed; load their layout styles in the head so nothing jumps. */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! function_exists( 'rsm_part_id' ) || ! class_exists( '\Elementor\Core\Files\CSS\Post' ) ) { return; }
	foreach ( array( 'header', 'footer' ) as $slot ) { $id = (int) rsm_part_id( $slot ); if ( $id ) { \Elementor\Core\Files\CSS\Post::create( $id )->enqueue(); } }
}, 30 );
add_action( 'wp_head', function () {
	$uri = get_template_directory_uri() . '/assets/fonts/';
	foreach ( array( 'sora.woff2', 'jakarta.woff2' ) as $f ) { printf( "<link rel=\"preload\" href=\"%s\" as=\"font\" type=\"font/woff2\" crossorigin>\n", esc_url( $uri . $f ) ); }
	echo "<meta name=\"theme-color\" content=\"#0B1033\">\n";
}, 1 );
add_filter( 'body_class', function ( $c ) { $c[] = 'rsm'; return $c; } );
add_action( 'elementor/theme/register_locations', '__return_false' );

/** Header or footer built in Elementor (RSM Elements plugin); a plain fallback if it is missing. */
function rsm_site_part( $slot ) { return function_exists( 'rsm_render_part' ) && rsm_render_part( $slot ); }

require get_template_directory() . '/inc/setup.php';
