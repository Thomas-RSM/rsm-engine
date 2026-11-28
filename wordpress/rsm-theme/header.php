<?php if ( ! defined( 'ABSPATH' ) ) { exit; } ?><!doctype html>
<html <?php language_attributes(); ?> class="no-js">
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip" href="#main"><?php esc_html_e( 'Skip to content', 'rsm' ); ?></a>
<header class="site-header">
<?php if ( ! rsm_site_part( 'header' ) ) : ?>
	<div class="wrap masthead"><a class="brand" href="<?php echo esc_url( home_url( '/' ) ); ?>"><span><span class="brand-name"><?php bloginfo( 'name' ); ?></span></span></a>
	<?php wp_nav_menu( array( 'theme_location' => 'primary', 'container' => 'nav', 'container_class' => 'nav', 'depth' => 1, 'fallback_cb' => false ) ); ?></div>
<?php endif; ?>
</header>
<main id="main">
