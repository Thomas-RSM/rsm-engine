<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header(); ?>
<section class="section"><div class="wrap rs-prose">
	<h1><?php if ( is_search() ) { printf( /* translators: %s: search words */ esc_html__( 'Results for "%s"', 'rsm' ), esc_html( get_search_query() ) ); } elseif ( is_archive() ) { the_archive_title(); } else { echo esc_html( get_the_title( get_option( 'page_for_posts' ) ) ?: __( 'Latest', 'rsm' ) ); } ?></h1>
	<?php if ( have_posts() ) : ?><ul class="rs-posts">
	<?php while ( have_posts() ) : the_post(); ?>
		<li class="glass"><a href="<?php the_permalink(); ?>"><span class="k"><?php echo esc_html( get_the_date() ); ?></span><h2><?php the_title(); ?></h2><p><?php echo esc_html( wp_trim_words( get_the_excerpt(), 30 ) ); ?></p></a></li>
	<?php endwhile; ?></ul><?php the_posts_pagination(); else : ?><p class="lead"><?php esc_html_e( 'Nothing here yet.', 'rsm' ); ?></p><?php endif; ?>
</div></section>
<?php get_footer();
