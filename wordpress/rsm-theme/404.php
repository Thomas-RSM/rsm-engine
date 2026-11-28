<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header(); ?>
<section class="section"><div class="wrap rs-prose">
	<p class="eyebrow"><?php esc_html_e( 'Page not found', 'rsm' ); ?></p>
	<h1><?php esc_html_e( 'That page is not here.', 'rsm' ); ?></h1>
	<p class="lead"><?php esc_html_e( 'It may have moved, or it may not be built yet.', 'rsm' ); ?></p>
	<p><a class="btn" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Go to the home page', 'rsm' ); ?></a></p>
</div></section>
<?php get_footer();
