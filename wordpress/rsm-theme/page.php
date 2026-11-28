<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
while ( have_posts() ) { the_post();
	$built = did_action( 'elementor/loaded' ) && \Elementor\Plugin::$instance->documents->get( get_the_ID() ) && \Elementor\Plugin::$instance->documents->get( get_the_ID() )->is_built_with_elementor();
	if ( $built ) { the_content(); } else { ?>
		<section class="section"><div class="wrap rs-prose"><h1><?php the_title(); ?></h1><?php the_content(); ?></div></section>
	<?php }
}
get_footer();
