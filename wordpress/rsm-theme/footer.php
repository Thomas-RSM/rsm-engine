<?php if ( ! defined( 'ABSPATH' ) ) { exit; } ?>
</main>
<footer class="site-footer">
<?php if ( ! rsm_site_part( 'footer' ) ) : ?>
	<div class="wrap"><div class="footer-bottom"><span>&copy; <?php echo esc_html( gmdate( 'Y' ) . ' ' . get_bloginfo( 'name' ) ); ?></span></div></div>
<?php endif; ?>
</footer>
<?php wp_footer(); ?>
</body>
</html>
