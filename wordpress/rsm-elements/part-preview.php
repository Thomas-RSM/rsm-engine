<?php
/** Preview shell used while a header or footer part is edited in Elementor. */
if ( ! defined( 'ABSPATH' ) ) { exit; }
$slot = (int) get_option( 'rsm_part_footer' ) === get_queried_object_id() ? 'footer' : 'header';
?><!doctype html>
<html <?php language_attributes(); ?> class="no-js">
<head><meta charset="<?php bloginfo( 'charset' ); ?>"><meta name="viewport" content="width=device-width,initial-scale=1"><?php wp_head(); ?></head>
<body <?php body_class( 'rsm-part-preview' ); ?>>
<?php wp_body_open(); ?>
<<?php echo 'footer' === $slot ? 'footer class="site-footer"' : 'header class="site-header"'; ?>>
<?php while ( have_posts() ) { the_post(); the_content(); } ?>
</<?php echo 'footer' === $slot ? 'footer' : 'header'; ?>>
<?php if ( 'header' === $slot ) { echo '<main style="min-height:60vh"></main>'; } ?>
<?php wp_footer(); ?>
</body>
</html>
