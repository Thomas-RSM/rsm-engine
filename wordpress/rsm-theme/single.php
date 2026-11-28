<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
while ( have_posts() ) { the_post(); ?>
	<article <?php post_class( 'section' ); ?>><div class="wrap rs-prose">
		<p class="eyebrow"><?php echo esc_html( get_the_date() ); ?></p>
		<h1><?php the_title(); ?></h1>
		<?php the_content(); ?>
		<p class="small"><?php printf( /* translators: %s: author name */ esc_html__( 'By %s', 'rsm' ), esc_html( get_the_author() ) ); ?></p>
	</div></article>
<?php }
get_footer();
