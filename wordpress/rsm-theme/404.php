<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header(); ?>
<section class="section"><div class="wrap rs-prose">
	<p class="eyebrow"><?php esc_html_e( 'Page not found', 'rsm' ); ?></p>
	<h1><?php esc_html_e( 'That page is not here.', 'rsm' ); ?></h1>
	<p class="lead"><?php esc_html_e( 'It may have moved, or it may not be built yet.', 'rsm' ); ?></p>
	<p><a class="btn" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Go to the home page', 'rsm' ); ?></a></p>
	<p><?php esc_html_e( 'Or start from one of these:', 'rsm' ); ?></p>
	<ul>
		<li><a href="<?php echo esc_url( home_url( '/problems/' ) ); ?>"><?php esc_html_e( 'SEO problems, explained one by one', 'rsm' ); ?></a></li>
		<li><a href="<?php echo esc_url( home_url( '/services/' ) ); ?>"><?php esc_html_e( 'Everything we do, by its common name', 'rsm' ); ?></a></li>
		<li><a href="<?php echo esc_url( home_url( '/ask/' ) ); ?>"><?php esc_html_e( 'Ask a question', 'rsm' ); ?></a></li>
		<li><a href="<?php echo esc_url( home_url( '/book/' ) ); ?>"><?php esc_html_e( 'Book a discovery call', 'rsm' ); ?></a></li>
	</ul>
</div></section>
<?php get_footer();
