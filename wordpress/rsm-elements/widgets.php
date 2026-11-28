<?php
/**
 * RSM Elements: Elementor widgets.
 * Each widget prints the same markup the approved design uses, so the theme stylesheet and script apply unchanged,
 * and every word, link, picture and list item is a control in the Elementor panel.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

use Elementor\Controls_Manager as CM;

function rsm_widget_classes() {
	return array( 'RSM_W_Brand', 'RSM_W_Nav', 'RSM_W_Mobile_Menu', 'RSM_W_Link_List', 'RSM_W_Orbit', 'RSM_W_Stat', 'RSM_W_Chapters', 'RSM_W_Film', 'RSM_W_Engines', 'RSM_W_Lab', 'RSM_W_Console', 'RSM_W_Card', 'RSM_W_Seal', 'RSM_W_US_Map', 'RSM_W_Table', 'RSM_W_Path', 'RSM_W_Chips', 'RSM_W_Portrait', 'RSM_W_FAQ' );
}
function rsm_menu_options() { $o = array( '' => __( 'Choose a menu', 'rsm-elements' ) ); foreach ( wp_get_nav_menus() as $m ) { $o[ $m->slug ] = $m->name; } return $o; }
function rsm_data( $file ) { $p = RSM_EL_DIR . 'data/' . $file; return file_exists( $p ) ? json_decode( file_get_contents( $p ), true ) : array(); } // phpcs:ignore WordPress.WP.AlternativeFunctions

abstract class RSM_Widget extends \Elementor\Widget_Base {
	/** [ key, label, type, default, extra ] rows; type 'section' starts a new panel section, 'repeater' takes fields in extra['fields']. */
	abstract protected function fields();
	protected function style_targets() { return array( 'title' => 'h2, {{WRAPPER}} h3, {{WRAPPER}} .brand-name, {{WRAPPER}} b', 'text' => 'p, {{WRAPPER}} li, {{WRAPPER}} span.d, {{WRAPPER}} figcaption', 'accent' => '.k, {{WRAPPER}} .go, {{WRAPPER}} .more, {{WRAPPER}} .day-n, {{WRAPPER}} .mh' ); }
	public function get_categories() { return array( 'rsm' ); }
	public function get_icon() { return 'eicon-star-o'; }
	public function get_keywords() { return array( 'rsm', 'relevant search media' ); }
	protected function is_dynamic_content(): bool { return false; }

	private function add_field( $target, $f ) {
		list( $key, $label, $type ) = $f; $default = $f[3] ?? ''; $extra = $f[4] ?? array();
		$map = array( 'text' => CM::TEXT, 'textarea' => CM::TEXTAREA, 'wysiwyg' => CM::WYSIWYG, 'url' => CM::URL, 'media' => CM::MEDIA, 'code' => CM::CODE, 'number' => CM::NUMBER, 'select' => CM::SELECT, 'switch' => CM::SWITCHER, 'color' => CM::COLOR );
		$args = array( 'label' => $label, 'type' => $map[ $type ], 'default' => $default, 'label_block' => in_array( $type, array( 'text', 'textarea', 'url', 'code', 'select' ), true ) );
		if ( 'url' === $type ) { $args['default'] = array( 'url' => $default ); $args['dynamic'] = array( 'active' => true ); }
		if ( 'media' === $type ) { $args['default'] = array( 'url' => $default ); }
		if ( 'code' === $type ) { $args['language'] = 'html'; $args['rows'] = 6; }
		if ( 'switch' === $type ) { $args['return_value'] = 'yes'; }
		if ( 'textarea' === $type ) { $args['rows'] = 3; }
		$target->add_control( $key, array_merge( $args, $extra ) );
	}
	protected function register_controls() {
		$open = false; $n = 0;
		foreach ( $this->fields() as $f ) {
			if ( 'section' === $f[2] ) { if ( $open ) { $this->end_controls_section(); } $this->start_controls_section( 'sec_' . $f[0], array( 'label' => $f[1], 'tab' => CM::TAB_CONTENT ) ); $open = true; continue; }
			if ( ! $open ) { $this->start_controls_section( 'sec_content_' . ( ++$n ), array( 'label' => __( 'Content', 'rsm-elements' ), 'tab' => CM::TAB_CONTENT ) ); $open = true; }
			if ( 'repeater' === $f[2] ) {
				$rep = new \Elementor\Repeater();
				foreach ( $f[4]['fields'] as $rf ) { $this->add_field( $rep, $rf ); }
				$this->add_control( $f[0], array( 'label' => $f[1], 'type' => CM::REPEATER, 'fields' => $rep->get_controls(), 'default' => $f[3], 'title_field' => $f[4]['title'] ?? '', 'prevent_empty' => false ) );
				continue;
			}
			$this->add_field( $this, $f );
		}
		if ( $open ) { $this->end_controls_section(); }
		// Style tab: colours and type for the three kinds of text every widget uses.
		$this->start_controls_section( 'sec_style', array( 'label' => __( 'Colours and type', 'rsm-elements' ), 'tab' => CM::TAB_STYLE ) );
		$t = $this->style_targets();
		$this->add_control( 'st_title_color', array( 'label' => __( 'Heading colour', 'rsm-elements' ), 'type' => CM::COLOR, 'selectors' => array( '{{WRAPPER}} ' . $t['title'] => 'color: {{VALUE}};' ) ) );
		$this->add_group_control( \Elementor\Group_Control_Typography::get_type(), array( 'name' => 'st_title_type', 'label' => __( 'Heading type', 'rsm-elements' ), 'selector' => '{{WRAPPER}} ' . $t['title'] ) );
		$this->add_control( 'st_text_color', array( 'label' => __( 'Text colour', 'rsm-elements' ), 'type' => CM::COLOR, 'selectors' => array( '{{WRAPPER}} ' . $t['text'] => 'color: {{VALUE}};' ) ) );
		$this->add_group_control( \Elementor\Group_Control_Typography::get_type(), array( 'name' => 'st_text_type', 'label' => __( 'Text type', 'rsm-elements' ), 'selector' => '{{WRAPPER}} ' . $t['text'] ) );
		$this->add_control( 'st_accent_color', array( 'label' => __( 'Accent colour', 'rsm-elements' ), 'type' => CM::COLOR, 'selectors' => array( '{{WRAPPER}} ' . $t['accent'] => 'color: {{VALUE}};' ) ) );
		$this->end_controls_section();
	}
	protected function s() { return $this->get_settings_for_display(); }
}

/* ============================== header and footer ============================== */
class RSM_W_Brand extends RSM_Widget {
	public function get_name() { return 'rsm-brand'; }
	public function get_title() { return __( 'RSM Logo and name', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-site-logo'; }
	protected function fields() { return array(
		array( 'logo', __( 'Logo', 'rsm-elements' ), 'media', rsm_asset( 'rsm-logo-512.png' ) ),
		array( 'name', __( 'Name', 'rsm-elements' ), 'text', 'Relevant Search Media' ),
		array( 'tag', __( 'Line under the name', 'rsm-elements' ), 'text', 'Relevant search · traffic · leads' ),
		array( 'link', __( 'Link', 'rsm-elements' ), 'url', '/' ),
	); }
	protected function render() { $s = $this->s(); ?>
		<a href="<?php echo rsm_url( $s['link'] ); ?>" class="brand" aria-label="<?php echo esc_attr( $s['name'] ); ?> home"><span class="brand-disc"><img src="<?php echo rsm_url( $s['logo'] ); ?>" alt="<?php echo esc_attr( $s['name'] ); ?>" width="30" height="27"></span><span><span class="brand-name"><?php echo esc_html( $s['name'] ); ?></span><?php if ( $s['tag'] ) : ?><span class="brand-tag"><?php echo esc_html( $s['tag'] ); ?></span><?php endif; ?></span></a>
	<?php }
}

/** Reads a three-level WordPress menu: top item, column heading, link (with its description). */
function rsm_menu_tree( $slug ) {
	$items = $slug ? wp_get_nav_menu_items( $slug ) : array(); $by = array(); $tree = array();
	if ( ! $items ) { return array(); }
	foreach ( $items as $it ) { $by[ $it->ID ] = array( 'title' => $it->title, 'url' => $it->url, 'desc' => $it->description, 'classes' => implode( ' ', array_filter( (array) $it->classes ) ), 'parent' => (int) $it->menu_item_parent, 'children' => array() ); }
	foreach ( $by as $id => &$n ) { if ( $n['parent'] && isset( $by[ $n['parent'] ] ) ) { $by[ $n['parent'] ]['children'][] = &$n; } else { $tree[] = &$n; } } unset( $n );
	return $tree;
}
class RSM_W_Nav extends RSM_Widget {
	public function get_name() { return 'rsm-nav'; }
	public function get_title() { return __( 'RSM Menu with dropdowns', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-nav-menu'; }
	protected function style_targets() { return array( 'title' => 'a.top', 'text' => '.mcol a b, {{WRAPPER}} .mcol a span', 'accent' => '.mh' ); }
	protected function fields() { return array(
		array( 'menu', __( 'Menu', 'rsm-elements' ), 'select', 'rsm-main', array( 'options' => rsm_menu_options(), 'description' => __( 'Edit items under Appearance, Menus. Level 1 is the bar, level 2 the column headings, level 3 the links. Add the CSS class "wide" or "right" to a level 1 item to change how its panel opens.', 'rsm-elements' ) ) ),
		array( 'label', __( 'Name for screen readers', 'rsm-elements' ), 'text', 'Main' ),
	); }
	protected function render() { $s = $this->s(); $tree = rsm_menu_tree( $s['menu'] );
		if ( ! $tree ) { if ( \Elementor\Plugin::$instance->editor->is_edit_mode() ) { echo '<p>' . esc_html__( 'Choose a menu.', 'rsm-elements' ) . '</p>'; } return; } ?>
		<nav class="nav" aria-label="<?php echo esc_attr( $s['label'] ); ?>"><ul>
		<?php foreach ( $tree as $top ) : $cls = preg_match( '/\b(wide|right)\b/', $top['classes'], $m ) ? $m[1] : ''; ?>
			<li class="<?php echo $top['children'] ? 'has-mega' : ''; ?>"><a class="top" href="<?php echo esc_url( $top['url'] ); ?>"<?php echo $top['children'] ? ' aria-haspopup="true"' : ''; ?>><?php echo esc_html( $top['title'] ); ?></a>
			<?php if ( $top['children'] ) : ?><div class="mega <?php echo esc_attr( $cls ); ?>"><div class="mega-in">
				<?php foreach ( $top['children'] as $col ) : ?><div class="mcol"><p class="mh"><?php echo esc_html( $col['title'] ); ?></p><ul>
					<?php foreach ( $col['children'] as $l ) : ?><li><a href="<?php echo esc_url( $l['url'] ); ?>"><b><?php echo esc_html( $l['title'] ); ?></b><?php if ( $l['desc'] ) : ?><span><?php echo esc_html( $l['desc'] ); ?></span><?php endif; ?></a></li><?php endforeach; ?>
				</ul></div><?php endforeach; ?>
			</div></div><?php endif; ?></li>
		<?php endforeach; ?>
		</ul></nav>
	<?php }
}
class RSM_W_Mobile_Menu extends RSM_Widget {
	public function get_name() { return 'rsm-mobile-menu'; }
	public function get_title() { return __( 'RSM Small-screen menu', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-menu-bar'; }
	protected function fields() { return array(
		array( 'menu', __( 'Menu', 'rsm-elements' ), 'select', 'rsm-main', array( 'options' => rsm_menu_options() ) ),
		array( 'button', __( 'Button word', 'rsm-elements' ), 'text', 'Menu' ),
		array( 'overview', __( 'Word after each group name', 'rsm-elements' ), 'text', 'overview' ),
		array( 'phone_text', __( 'Phone line', 'rsm-elements' ), 'text', 'Call +1 (202) 609-6641' ),
		array( 'phone_link', __( 'Phone link', 'rsm-elements' ), 'url', 'tel:+12026096641' ),
		array( 'cta_text', __( 'Button text', 'rsm-elements' ), 'text', 'Book a discovery call' ),
		array( 'cta_link', __( 'Button link', 'rsm-elements' ), 'url', '/book/' ),
	); }
	protected function render() { $s = $this->s(); $tree = rsm_menu_tree( $s['menu'] ); ?>
		<details class="menu"><summary aria-label="<?php echo esc_attr( $s['button'] ); ?>"><span class="menu-bars" aria-hidden="true"></span><?php echo esc_html( $s['button'] ); ?></summary>
		<nav class="menu-panel" aria-label="Main, small screens">
		<?php foreach ( $tree as $top ) : ?>
			<?php if ( $top['children'] ) : ?><details class="mgroup"><summary><?php echo esc_html( $top['title'] ); ?></summary><a class="hub" href="<?php echo esc_url( $top['url'] ); ?>"><?php echo esc_html( $top['title'] . ': ' . $s['overview'] ); ?></a>
				<?php foreach ( $top['children'] as $col ) { foreach ( $col['children'] as $l ) { printf( '<a href="%s">%s</a>', esc_url( $l['url'] ), esc_html( $l['title'] ) ); } } ?></details>
			<?php else : ?><a href="<?php echo esc_url( $top['url'] ); ?>"><?php echo esc_html( $top['title'] ); ?></a><?php endif; ?>
		<?php endforeach; ?>
		<?php if ( $s['phone_text'] ) : ?><a href="<?php echo rsm_url( $s['phone_link'] ); ?>"><?php echo esc_html( $s['phone_text'] ); ?></a><?php endif; ?>
		<?php if ( $s['cta_text'] ) : ?><a class="btn" href="<?php echo rsm_url( $s['cta_link'] ); ?>"><?php echo esc_html( $s['cta_text'] ); ?></a><?php endif; ?>
		</nav></details>
	<?php }
}
class RSM_W_Link_List extends RSM_Widget {
	public function get_name() { return 'rsm-link-list'; }
	public function get_title() { return __( 'RSM Footer links', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-editor-list-ul'; }
	protected function style_targets() { return array( 'title' => '.footer-h', 'text' => 'a', 'accent' => 'a:hover' ); }
	protected function fields() { return array(
		array( 'heading', __( 'Heading', 'rsm-elements' ), 'text', '' ),
		array( 'menu', __( 'Menu', 'rsm-elements' ), 'select', '', array( 'options' => rsm_menu_options() ) ),
	); }
	protected function render() { $s = $this->s(); $items = $s['menu'] ? wp_get_nav_menu_items( $s['menu'] ) : array(); ?>
		<nav aria-label="<?php echo esc_attr( $s['heading'] ); ?>"><?php if ( $s['heading'] ) : ?><h2 class="footer-h"><?php echo esc_html( $s['heading'] ); ?></h2><?php endif; ?><ul>
		<?php foreach ( (array) $items as $it ) { printf( '<li><a href="%s">%s</a></li>', esc_url( $it->url ), esc_html( $it->title ) ); } ?>
		</ul></nav>
	<?php }
}

/* ============================== hero ============================== */
class RSM_W_Orbit extends RSM_Widget {
	public function get_name() { return 'rsm-orbit'; }
	public function get_title() { return __( 'RSM Orbit', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-globe'; }
	protected function fields() { return array(
		array( 'logo', __( 'Centre logo', 'rsm-elements' ), 'media', rsm_asset( 'rsm-logo-512.png' ) ),
		array( 'label', __( 'Description for screen readers', 'rsm-elements' ), 'textarea', 'Your business at the centre, with the places customers look for it in orbit.' ),
		array( 'tiles', __( 'Tiles (inner ring first)', 'rsm-elements' ), 'repeater', rsm_data( 'icons.json' ), array( 'title' => '{{{ name }}}', 'fields' => array(
			array( 'name', __( 'Name', 'rsm-elements' ), 'text', '' ),
			array( 'c', __( 'Glow colour', 'rsm-elements' ), 'color', '#6F8CF0' ),
			array( 'svg', __( 'Icon (SVG code, 48 by 48)', 'rsm-elements' ), 'code', '' ),
		) ) ),
	); }
	protected function render() { $s = $this->s(); $tiles = array();
		foreach ( (array) $s['tiles'] as $t ) { $tiles[] = array( 'name' => (string) $t['name'], 'c' => $t['c'] ? $t['c'] : '#6F8CF0', 'svg' => rsm_svg( (string) $t['svg'] ) ); } ?>
		<div class="orbit" id="orbit" role="img" aria-label="<?php echo esc_attr( $s['label'] ); ?>"><script type="application/json" class="orbit-data"><?php echo wp_json_encode( $tiles, JSON_HEX_TAG | JSON_HEX_AMP ); ?></script><div class="o-core" style="left:50%;top:50%;width:128px;height:128px"><img src="<?php echo rsm_url( $s['logo'] ); ?>" alt="" width="84" height="74"></div></div>
	<?php }
}
class RSM_W_Stat extends RSM_Widget {
	public function get_name() { return 'rsm-stat'; }
	public function get_title() { return __( 'RSM Figure', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-counter'; }
	protected function fields() { return array(
		array( 'number', __( 'Figure', 'rsm-elements' ), 'text', '900+' ),
		array( 'label', __( 'What it counts', 'rsm-elements' ), 'text', 'businesses served since 2020' ),
		array( 'link_text', __( 'Link text (optional)', 'rsm-elements' ), 'text', '' ),
		array( 'link', __( 'Link', 'rsm-elements' ), 'url', '' ),
	); }
	protected function render() { $s = $this->s(); ?>
		<div class="rs-stat"><b><?php echo esc_html( $s['number'] ); ?></b> <?php echo esc_html( $s['label'] ); ?><?php if ( $s['link_text'] ) : ?> · <a href="<?php echo rsm_url( $s['link'] ); ?>"><?php echo esc_html( $s['link_text'] ); ?></a><?php endif; ?></div>
	<?php }
}

/* ============================== film ============================== */
class RSM_W_Chapters extends RSM_Widget {
	public function get_name() { return 'rsm-chapters'; }
	public function get_title() { return __( 'RSM Film chapters', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-bullet-list'; }
	protected function style_targets() { return array( 'title' => '.beats button b', 'text' => '.beats button span', 'accent' => '.beats button::before' ); }
	protected function fields() { return array(
		array( 'label', __( 'Name for screen readers', 'rsm-elements' ), 'text', 'Chapters of the film' ),
		array( 'items', __( 'Chapters', 'rsm-elements' ), 'repeater', array(), array( 'title' => '{{{ title }}}', 'fields' => array(
			array( 'title', __( 'Title', 'rsm-elements' ), 'text', '' ),
			array( 'text', __( 'One line', 'rsm-elements' ), 'textarea', '' ),
			array( 'time', __( 'Starts at (seconds)', 'rsm-elements' ), 'number', 0, array( 'step' => 0.01 ) ),
		) ) ),
	); }
	protected function render() { $s = $this->s(); ?>
		<ol class="beats" id="film-transcript" aria-label="<?php echo esc_attr( $s['label'] ); ?>">
		<?php foreach ( (array) $s['items'] as $c ) { printf( '<li><button type="button" data-t="%s"><b>%s</b><span>%s</span></button></li>', esc_attr( number_format( (float) $c['time'], 2, '.', '' ) ), esc_html( $c['title'] ), esc_html( $c['text'] ) ); } ?>
		</ol>
	<?php }
}
class RSM_W_Film extends RSM_Widget {
	protected function is_dynamic_content(): bool { return true; }
	public function get_name() { return 'rsm-film'; }
	public function get_title() { return __( 'RSM Film', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-youtube'; }
	protected function fields() { return array(
		array( 'video', __( 'Film file (MP4)', 'rsm-elements' ), 'media', rsm_asset( 'film-answer.mp4' ), array( 'media_types' => array( 'video' ) ) ),
		array( 'poster', __( 'Poster image', 'rsm-elements' ), 'media', rsm_asset( 'film-answer-poster.jpg' ) ),
		array( 'captions', __( 'Captions file (.vtt address)', 'rsm-elements' ), 'text', rsm_asset( 'film-answer.vtt' ) ),
		array( 'title', __( 'Title', 'rsm-elements' ), 'text', 'Be the answer: how an engine decides who to name' ),
		array( 'caption', __( 'Line under the film', 'rsm-elements' ), 'text', '' ),
		array( 'fallback', __( 'Text when video cannot play', 'rsm-elements' ), 'text', 'Your browser does not play video. The chapters beside it tell the same story.' ),
		array( 'sound_off', __( 'Sound button', 'rsm-elements' ), 'text', 'Play with sound' ),
		array( 'sound_on', __( 'Sound button when on', 'rsm-elements' ), 'text', 'Sound on' ),
		array( 'roll', __( 'Play muted when on screen', 'rsm-elements' ), 'switch', 'yes' ),
		array( 'schema', __( 'Search engine details', 'rsm-elements' ), 'section' ),
		array( 'description', __( 'Description', 'rsm-elements' ), 'textarea', '' ),
		array( 'transcript', __( 'Transcript', 'rsm-elements' ), 'textarea', '' ),
		array( 'date', __( 'Published (YYYY-MM-DD)', 'rsm-elements' ), 'text', '' ),
		array( 'duration', __( 'Length in seconds', 'rsm-elements' ), 'number', 58 ),
	); }
	protected function render() { $s = $this->s(); $v = rsm_url( $s['video'] ); $p = rsm_url( $s['poster'] );
		if ( $s['description'] && $v ) { rsm_schema_push( array_filter( array( '@type' => 'VideoObject', 'name' => $s['title'], 'description' => $s['description'], 'thumbnailUrl' => $p, 'contentUrl' => $v, 'uploadDate' => $s['date'], 'duration' => 'PT' . (int) $s['duration'] . 'S', 'transcript' => $s['transcript'] ) ) ); } ?>
		<figure class="film"><div class="film-frame">
			<video controls muted loop playsinline preload="none" poster="<?php echo $p; // phpcs:ignore ?>" width="1280" height="720" aria-describedby="film-transcript" title="<?php echo esc_attr( $s['title'] ); ?>"<?php echo 'yes' === $s['roll'] ? ' data-roll' : ''; ?>>
				<source src="<?php echo $v; // phpcs:ignore ?>" type="video/mp4">
				<?php if ( $s['captions'] ) : ?><track kind="captions" src="<?php echo esc_url( $s['captions'] ); ?>" srclang="en" label="English"><?php endif; ?>
				<?php echo esc_html( $s['fallback'] ); ?>
			</video>
			<button type="button" class="sound" id="film-sound" aria-pressed="false" data-on="<?php echo esc_attr( $s['sound_on'] ); ?>" data-off="<?php echo esc_attr( $s['sound_off'] ); ?>"><?php echo esc_html( $s['sound_off'] ); ?></button>
		</div><?php if ( $s['caption'] ) : ?><figcaption><?php echo esc_html( $s['caption'] ); ?></figcaption><?php endif; ?></figure>
	<?php }
}

/* ============================== the equation ============================== */
function rsm_nested_icon( $svg, $x, $y, $size, $uid ) {
	$svg = rsm_svg( (string) $svg ); if ( ! $svg ) { return ''; }
	$svg = preg_replace( '/\s(width|height|x|y)="[^"]*"/', '', $svg, 4 );
	$svg = preg_replace( '/id="([^"]+)"/', 'id="$1-' . $uid . '"', $svg ); $svg = preg_replace( '/url\(#([^)]+)\)/', 'url(#$1-' . $uid . ')', $svg );
	return preg_replace( '/<svg/', '<svg x="' . $x . '" y="' . $y . '" width="' . $size . '" height="' . $size . '"', $svg, 1 );
}
class RSM_W_Engines extends RSM_Widget {
	public function get_name() { return 'rsm-engines'; }
	public function get_title() { return __( 'RSM Five engines, one answer', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-flow'; }
	protected function style_targets() { return array( 'title' => '.caption', 'text' => '.eg-hint, {{WRAPPER}} .eg-controls button', 'accent' => '.eg-lab' ); }
	protected function fields() { $ic = array(); foreach ( rsm_data( 'icons.json' ) as $i ) { $ic[ $i['name'] ] = $i['svg']; }
		$eng = array(
			array( 'name' => 'Google', 'info' => 'Google reads your pages, your links and how people use them.', 'svg' => $ic['Google'] ?? '' ),
			array( 'name' => 'Maps', 'info' => 'Maps reads your listing: categories, hours, photos and reviews.', 'svg' => $ic['Maps'] ?? '' ),
			array( 'name' => 'ChatGPT', 'info' => 'ChatGPT reads what the wider web says about you, then answers in a sentence.', 'svg' => $ic['ChatGPT'] ?? '' ),
			array( 'name' => 'Gemini', 'info' => 'Gemini reads Google’s index and your business profile together.', 'svg' => $ic['Gemini'] ?? '' ),
			array( 'name' => 'Perplexity', 'info' => 'Perplexity reads live sources and shows which ones it used.', 'svg' => $ic['Perplexity'] ?? '' ),
		);
		return array(
		array( 'q_label', __( 'Question label', 'rsm-elements' ), 'text', 'The question' ),
		array( 'question', __( 'Question', 'rsm-elements' ), 'text', 'Who should I call?' ),
		array( 'a_label', __( 'Answer label', 'rsm-elements' ), 'text', 'The answer' ),
		array( 'a_yes', __( 'Answer when the checks are strong', 'rsm-elements' ), 'text', 'You.' ),
		array( 'a_no', __( 'Answer when a check is weak', 'rsm-elements' ), 'text', 'Someone else.' ),
		array( 'logo', __( 'Logo in the answer', 'rsm-elements' ), 'media', rsm_asset( 'rsm-logo-512.png' ) ),
		array( 'caption', __( 'Line under the picture', 'rsm-elements' ), 'text', 'One question in. Five engines read it their own way. One business comes out named.' ),
		array( 'label', __( 'Description for screen readers', 'rsm-elements' ), 'text', 'One question goes to five engines, and one business is named' ),
		array( 'engines', __( 'Engines', 'rsm-elements' ), 'repeater', $eng, array( 'title' => '{{{ name }}}', 'fields' => array(
			array( 'name', __( 'Name', 'rsm-elements' ), 'text', '' ),
			array( 'info', __( 'How it reads (shown on tap)', 'rsm-elements' ), 'textarea', '' ),
			array( 'svg', __( 'Icon (SVG code, 48 by 48)', 'rsm-elements' ), 'code', '' ),
		) ) ),
		array( 'try', __( 'Try a question', 'rsm-elements' ), 'section' ),
		array( 'try_label', __( 'Label', 'rsm-elements' ), 'text', 'Try a question' ),
		array( 'examples', __( 'Example questions', 'rsm-elements' ), 'repeater', array( array( 'q' => 'Who should I call?' ), array( 'q' => 'Who fixes a burst pipe?' ), array( 'q' => 'Which roofer can I trust?' ) ), array( 'title' => '{{{ q }}}', 'fields' => array( array( 'q', __( 'Question', 'rsm-elements' ), 'text', '' ) ) ) ),
		array( 'placeholder', __( 'Text in the empty box', 'rsm-elements' ), 'text', 'Type your own' ),
		array( 'hint', __( 'Hint', 'rsm-elements' ), 'text', 'Tap an engine. The answer follows the dials below.' ),
	); }
	protected function render() { $s = $this->s(); $uid = $this->get_id(); $eng = array_values( (array) $s['engines'] ); $n = max( 1, count( $eng ) );
		$W = 1000; $H = 400; $qx = 250; $qy = 200; $ax = 750; $tx = 500; $ts = 56; $ys = array();
		for ( $i = 0; $i < $n; $i++ ) { $ys[] = 1 === $n ? 200 : round( 44 + $i * ( 312 / ( $n - 1 ) ) ); }
		$words = explode( ' ', (string) $s['question'] ); $l1 = ''; $l2 = '';
		foreach ( $words as $w ) { if ( '' === $l2 && strlen( trim( $l1 . ' ' . $w ) ) <= 14 ) { $l1 = trim( $l1 . ' ' . $w ); } else { $l2 = trim( $l2 . ' ' . $w ); } }
		$o = '<svg class="eg-wide" viewBox="0 0 ' . $W . ' ' . $H . '" role="img" aria-label="' . esc_attr( $s['label'] ) . '"><defs><linearGradient id="eg-in" x1="0" x2="1"><stop offset="0" stop-color="#A3B5F2" stop-opacity=".15"/><stop offset="1" stop-color="#A3B5F2" stop-opacity=".7"/></linearGradient><linearGradient id="eg-out" x1="0" x2="1"><stop offset="0" stop-color="#FFD98A" stop-opacity=".75"/><stop offset="1" stop-color="#F8B10F" stop-opacity=".25"/></linearGradient><radialGradient id="eg-glow"><stop offset="0" stop-color="#F8B10F" stop-opacity=".5"/><stop offset="1" stop-color="#F8B10F" stop-opacity="0"/></radialGradient><linearGradient id="eg-tile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3C5096" stop-opacity=".7"/><stop offset=".4" stop-color="#1E2A56" stop-opacity=".9"/><stop offset="1" stop-color="#0A1024"/></linearGradient></defs>';
		foreach ( $ys as $i => $y ) {
			$d1 = "M$qx $qy C " . ( $qx + 130 ) . " $qy, " . ( $tx - $ts / 2 - 110 ) . " $y, " . ( $tx - $ts / 2 - 4 ) . " $y"; $d2 = 'M' . ( $tx + $ts / 2 + 4 ) . " $y C " . ( $tx + $ts / 2 + 110 ) . " $y, " . ( $ax - 130 ) . " $qy, $ax $qy";
			$o .= '<path id="ein' . $i . '" d="' . $d1 . '" fill="none" stroke="url(#eg-in)" stroke-width="1.4"/><path class="eg-o" id="eout' . $i . '" d="' . $d2 . '" fill="none" stroke="url(#eg-out)" stroke-width="1.6"/>';
			$o .= '<circle r="3.2" fill="#DCE6FF"><animateMotion dur="3.6s" begin="' . number_format( $i * 0.55, 2 ) . 's" repeatCount="indefinite"><mpath href="#ein' . $i . '"/></animateMotion></circle><circle class="eg-o eg-spark" r="3.8" fill="#FFD98A"><animateMotion dur="3.6s" begin="' . number_format( $i * 0.55 + 1.8, 2 ) . 's" repeatCount="indefinite"><mpath href="#eout' . $i . '"/></animateMotion></circle>';
		}
		foreach ( $eng as $i => $e ) { $y = $ys[ $i ];
			$o .= '<g class="eg-tile" tabindex="0" role="button" aria-label="' . esc_attr( $e['name'] . ': ' . $e['info'] ) . '" data-info="' . esc_attr( $e['info'] ) . '"><rect x="' . ( $tx - $ts / 2 ) . '" y="' . ( $y - $ts / 2 ) . '" width="' . $ts . '" height="' . $ts . '" rx="16" fill="url(#eg-tile)" stroke="rgba(190,205,250,.45)"/>' . rsm_nested_icon( $e['svg'], $tx - 15, $y - 15, 30, $uid . $i ) . '</g>';
			$o .= '<text x="' . ( $tx + $ts / 2 + 12 ) . '" y="' . ( $y - $ts / 2 + 2 ) . '" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="1.5" fill="#B4C0E0">' . esc_html( strtoupper( $e['name'] ) ) . '</text>';
		}
		$o .= '<rect x="18" y="' . ( $qy - 66 ) . '" width="232" height="132" rx="20" fill="url(#eg-tile)" stroke="rgba(163,181,242,.4)"/><text x="40" y="' . ( $qy - 34 ) . '" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="2" fill="#A3B5F2">' . esc_html( strtoupper( $s['q_label'] ) ) . '</text><text x="40" y="' . ( $qy + 2 ) . '" font-family="Sora, sans-serif" font-size="23" font-weight="650" fill="#fff" id="eg-q1" class="eg-q1">“' . esc_html( $l1 ) . ( $l2 ? '' : '”' ) . '</text><text x="40" y="' . ( $qy + 32 ) . '" font-family="Sora, sans-serif" font-size="23" font-weight="650" fill="#fff" id="eg-q2" class="eg-q2">' . ( $l2 ? esc_html( $l2 ) . '”' : '' ) . '</text>';
		$o .= '<circle id="eg-glowc" class="eg-glowc" cx="' . ( $ax + 110 ) . '" cy="' . $qy . '" r="150" fill="url(#eg-glow)"/><rect id="eg-ansr" class="eg-ansr" x="' . $ax . '" y="' . ( $qy - 66 ) . '" width="232" height="132" rx="20" fill="url(#eg-tile)" stroke="rgba(248,177,15,.75)"/><circle cx="' . ( $ax + 50 ) . '" cy="' . $qy . '" r="28" fill="#F6EFDF" stroke="#E2AE45" stroke-width="1.5"/><image href="' . rsm_url( $s['logo'] ) . '" x="' . ( $ax + 31 ) . '" y="' . ( $qy - 17 ) . '" width="38" height="34"/><text x="' . ( $ax + 92 ) . '" y="' . ( $qy - 14 ) . '" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="2" fill="#FFD98A" id="eg-ansl" class="eg-ansl">' . esc_html( strtoupper( $s['a_label'] ) ) . '</text><text x="' . ( $ax + 92 ) . '" y="' . ( $qy + 16 ) . '" font-family="Sora, sans-serif" font-size="23" font-weight="650" fill="#fff" id="eg-ans" class="eg-ans" data-yes="' . esc_attr( $s['a_yes'] ) . '" data-no="' . esc_attr( $s['a_no'] ) . '">' . esc_html( $s['a_yes'] ) . '</text></svg>';
		/* the same picture, drawn top to bottom for phones */
		$xs = array(); for ( $i = 0; $i < $n; $i++ ) { $xs[] = 1 === $n ? 180 : round( 36 + $i * ( 288 / ( $n - 1 ) ) ); }
		$ey = 262; $t2 = 50; $ui = $uid . 'm';
		$m = '<svg class="eg-tall" viewBox="0 0 360 520" role="img" aria-label="' . esc_attr( $s['label'] ) . '"><defs><linearGradient id="eg-in-v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A3B5F2" stop-opacity=".15"/><stop offset="1" stop-color="#A3B5F2" stop-opacity=".7"/></linearGradient><linearGradient id="eg-out-v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD98A" stop-opacity=".75"/><stop offset="1" stop-color="#F8B10F" stop-opacity=".25"/></linearGradient><radialGradient id="eg-glow-v"><stop offset="0" stop-color="#F8B10F" stop-opacity=".5"/><stop offset="1" stop-color="#F8B10F" stop-opacity="0"/></radialGradient><linearGradient id="eg-tile-v" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3C5096" stop-opacity=".7"/><stop offset=".4" stop-color="#1E2A56" stop-opacity=".9"/><stop offset="1" stop-color="#0A1024"/></linearGradient></defs>';
		foreach ( $xs as $i => $x ) {
			$d1 = 'M180 114 C 180 176, ' . $x . ' 168, ' . $x . ' ' . ( $ey - $t2 / 2 - 4 ); $d2 = 'M' . $x . ' ' . ( $ey + $t2 / 2 + 24 ) . ' C ' . $x . ' 356, 180 338, 180 404';
			$m .= '<path id="einv' . $i . '" d="' . $d1 . '" fill="none" stroke="url(#eg-in-v)" stroke-width="1.4"/><path class="eg-o" id="eoutv' . $i . '" d="' . $d2 . '" fill="none" stroke="url(#eg-out-v)" stroke-width="1.6"/>';
			$m .= '<circle r="3" fill="#DCE6FF"><animateMotion dur="3.6s" begin="' . number_format( $i * 0.55, 2 ) . 's" repeatCount="indefinite"><mpath href="#einv' . $i . '"/></animateMotion></circle><circle class="eg-o eg-spark" r="3.6" fill="#FFD98A"><animateMotion dur="3.6s" begin="' . number_format( $i * 0.55 + 1.8, 2 ) . 's" repeatCount="indefinite"><mpath href="#eoutv' . $i . '"/></animateMotion></circle>';
		}
		foreach ( $eng as $i => $e ) { $x = $xs[ $i ];
			$m .= '<g class="eg-tile" tabindex="0" role="button" aria-label="' . esc_attr( $e['name'] . ': ' . $e['info'] ) . '" data-info="' . esc_attr( $e['info'] ) . '"><rect x="' . ( $x - $t2 / 2 ) . '" y="' . ( $ey - $t2 / 2 ) . '" width="' . $t2 . '" height="' . $t2 . '" rx="14" fill="url(#eg-tile-v)" stroke="rgba(190,205,250,.45)"/>' . rsm_nested_icon( $e['svg'], $x - 14, $ey - 14, 28, $ui . $i ) . '</g>';
			$m .= '<text x="' . $x . '" y="' . ( $ey + $t2 / 2 + 15 ) . '" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" letter-spacing=".4" fill="#B4C0E0">' . esc_html( strtoupper( $e['name'] ) ) . '</text>';
		}
		$m .= '<rect x="56" y="8" width="248" height="106" rx="20" fill="url(#eg-tile-v)" stroke="rgba(163,181,242,.4)"/><text x="78" y="38" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="2" fill="#A3B5F2">' . esc_html( strtoupper( $s['q_label'] ) ) . '</text><text x="78" y="70" font-family="Sora, sans-serif" font-size="22" font-weight="650" fill="#fff" class="eg-q1">“' . esc_html( $l1 ) . ( $l2 ? '' : '”' ) . '</text><text x="78" y="98" font-family="Sora, sans-serif" font-size="22" font-weight="650" fill="#fff" class="eg-q2">' . ( $l2 ? esc_html( $l2 ) . '”' : '' ) . '</text>';
		$m .= '<circle class="eg-glowc" cx="180" cy="456" r="150" fill="url(#eg-glow-v)"/><rect class="eg-ansr" x="56" y="404" width="248" height="106" rx="20" fill="url(#eg-tile-v)" stroke="rgba(248,177,15,.75)"/><circle cx="104" cy="457" r="27" fill="#F6EFDF" stroke="#E2AE45" stroke-width="1.5"/><image href="' . rsm_url( $s['logo'] ) . '" x="86" y="441" width="36" height="32"/><text x="146" y="445" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="2" fill="#FFD98A" class="eg-ansl">' . esc_html( strtoupper( $s['a_label'] ) ) . '</text><text x="146" y="474" font-family="Sora, sans-serif" font-size="22" font-weight="650" fill="#fff" class="eg-ans" data-yes="' . esc_attr( $s['a_yes'] ) . '" data-no="' . esc_attr( $s['a_no'] ) . '">' . esc_html( $s['a_yes'] ) . '</text></svg>';
		$o .= $m; ?>
		<figure class="plate engine-plate glass"><?php echo $o; // phpcs:ignore WordPress.Security.EscapeOutput ?><figcaption class="caption" id="eg-cap" aria-live="polite"><?php echo esc_html( $s['caption'] ); ?></figcaption>
			<div class="eg-controls"><span class="eg-lab"><?php echo esc_html( $s['try_label'] ); ?></span>
			<?php foreach ( array_values( (array) $s['examples'] ) as $i => $e ) { printf( '<button type="button" class="%s" data-q="%s">%s</button>', 0 === $i ? 'on' : '', esc_attr( $e['q'] ), esc_html( $e['q'] ) ); } ?>
			<label class="sr-only" for="eg-input"><?php echo esc_html( $s['placeholder'] ); ?></label><input id="eg-input" type="text" maxlength="30" placeholder="<?php echo esc_attr( $s['placeholder'] ); ?>" autocomplete="off">
			<?php if ( $s['hint'] ) : ?><span class="eg-hint"><?php echo esc_html( $s['hint'] ); ?></span><?php endif; ?></div></figure>
	<?php }
}
class RSM_W_Lab extends RSM_Widget {
	public function get_name() { return 'rsm-lab'; }
	public function get_title() { return __( 'RSM Equation instrument', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-sliders'; }
	protected function style_targets() { return array( 'title' => '.formula, {{WRAPPER}} .lt h3', 'text' => '.lt p, {{WRAPPER}} .formula-plain', 'accent' => '.lt .more' ); }
	protected function fields() { return array(
		array( 'formula', __( 'Formula (words; = and × are coloured)', 'rsm-elements' ), 'text', 'Relevance = Read × Confirm × Choose' ),
		array( 'formula_label', __( 'Formula read aloud', 'rsm-elements' ), 'text', 'Relevance equals Read times Confirm times Choose' ),
		array( 'plain', __( 'Plain sentence ({n} is the live figure)', 'rsm-elements' ), 'textarea', 'Of every 100 customers who ask, about {n} are sent to you. Fail one check and none are.' ),
		array( 'logo', __( 'Logo at the end of the line', 'rsm-elements' ), 'media', rsm_asset( 'rsm-logo-512.png' ) ),
		array( 'terms', __( 'The three checks (keep three)', 'rsm-elements' ), 'repeater', array(
			array( 'k' => 'Term one', 'name' => 'Read', 'q' => 'Can I read plainly what this business is and what it answers?', 'where_label' => 'Where the work happens:', 'where' => 'your site: facts, answers, structure, markup.', 'more' => 'How Read works', 'link' => array( 'url' => '/dsouza-equation/read/' ), 'value' => 80, 'color' => '#F8B10F', 'ask' => 'Can it read you?' ),
			array( 'k' => 'Term two', 'name' => 'Confirm', 'q' => 'Do independent sources say the same thing?', 'where_label' => 'Where the work happens:', 'where' => 'listings, reviews, mentions, profiles, press.', 'more' => 'How Confirm works', 'link' => array( 'url' => '/dsouza-equation/confirm/' ), 'value' => 70, 'color' => '#4CC0A8', 'ask' => 'Do others back you up?' ),
			array( 'k' => 'Term three', 'name' => 'Choose', 'q' => 'Do real people choose it?', 'where_label' => 'Where the work happens:', 'where' => 'clicks, calls, reviews, repeat visits.', 'more' => 'How Choose works', 'link' => array( 'url' => '/dsouza-equation/choose/' ), 'value' => 75, 'color' => '#A3B5F2', 'ask' => 'Do people pick you?' ),
		), array( 'title' => '{{{ name }}}', 'fields' => array(
			array( 'k', __( 'Small label', 'rsm-elements' ), 'text', '' ), array( 'name', __( 'Name', 'rsm-elements' ), 'text', '' ),
			array( 'ask', __( 'Question in the picture', 'rsm-elements' ), 'text', '' ),
			array( 'q', __( 'Question in the column', 'rsm-elements' ), 'textarea', '' ),
			array( 'where_label', __( 'Bold lead-in', 'rsm-elements' ), 'text', '' ), array( 'where', __( 'Where the work happens', 'rsm-elements' ), 'textarea', '' ),
			array( 'more', __( 'Link text', 'rsm-elements' ), 'text', '' ), array( 'link', __( 'Link', 'rsm-elements' ), 'url', '' ),
			array( 'value', __( 'Starting strength (0 to 100)', 'rsm-elements' ), 'number', 75, array( 'min' => 0, 'max' => 100 ) ),
			array( 'color', __( 'Colour', 'rsm-elements' ), 'color', '#F8B10F' ),
		) ) ),
		array( 'result', __( 'Result column and foot', 'rsm-elements' ), 'section' ),
		array( 'r_k', __( 'Small label', 'rsm-elements' ), 'text', 'The result' ),
		array( 'r_name', __( 'Name', 'rsm-elements' ), 'text', 'You' ),
		array( 'r_unit', __( 'Line under the figure', 'rsm-elements' ), 'text', 'in 100 sent to you' ),
		array( 'weak', __( 'Tag on the weakest check', 'rsm-elements' ), 'text', 'Raise this first' ),
		array( 'try_label', __( 'Label before the examples', 'rsm-elements' ), 'text', 'Try a case' ),
		array( 'presets', __( 'Examples', 'rsm-elements' ), 'repeater', array(
			array( 'label' => 'A fine website nobody vouches for', 'v' => '92,4,60' ), array( 'label' => 'Well known, hard to read', 'v' => '8,85,70' ), array( 'label' => 'Read and confirmed, not chosen', 'v' => '88,80,6' ), array( 'label' => 'All three', 'v' => '92,88,85' ),
		), array( 'title' => '{{{ label }}}', 'fields' => array( array( 'label', __( 'Label', 'rsm-elements' ), 'text', '' ), array( 'v', __( 'Three strengths, comma separated', 'rsm-elements' ), 'text', '80,70,75' ) ) ) ),
		array( 'caption', __( 'Small print', 'rsm-elements' ), 'text', 'An illustration, not a measurement of any site.' ),
	); }
	protected function render() { $s = $this->s(); $terms = array_slice( array_values( (array) $s['terms'] ), 0, 3 ); $uid = $this->get_id();
		$f = esc_html( $s['formula'] ); $f = str_replace( array( ' = ', ' × ' ), array( ' <span class="op">=</span> ', ' <span class="op">×</span> ' ), $f );
		$prod = 1; foreach ( $terms as $t ) { $prod *= ( (int) $t['value'] ) / 100; } $prod = (int) round( $prod * 100 );
		$plain = str_replace( '{n}', '<b data-rel2>' . $prod . '</b>', esc_html( $s['plain'] ) ); ?>
		<div class="lab glass" id="lab" data-logo="<?php echo rsm_url( $s['logo'] ); ?>" data-ask="<?php echo esc_attr( wp_json_encode( wp_list_pluck( $terms, 'ask' ) ) ); ?>" data-colors="<?php echo esc_attr( wp_json_encode( wp_list_pluck( $terms, 'color' ) ) ); ?>">
			<p class="formula" role="img" aria-label="<?php echo esc_attr( $s['formula_label'] ); ?>"><?php echo $f; // phpcs:ignore ?></p>
			<p class="formula-plain"><?php echo $plain; // phpcs:ignore ?></p>
			<canvas aria-hidden="true"></canvas>
			<div class="lab-terms">
			<?php foreach ( $terms as $i => $t ) : $id = 'd-' . $uid . '-' . $i; $c = $t['color'] ? $t['color'] : '#F8B10F'; ?>
				<div class="lt"><span class="weak" hidden data-label="<?php echo esc_attr( $s['weak'] ); ?>"></span>
					<span class="k" style="color:<?php echo esc_attr( $c ); ?>"><?php echo esc_html( $t['k'] ); ?></span>
					<h3><?php echo esc_html( $t['name'] ); ?></h3>
					<p class="q">“<?php echo esc_html( $t['q'] ); ?>”</p>
					<p><b><?php echo esc_html( $t['where_label'] ); ?></b> <?php echo esc_html( $t['where'] ); ?></p>
					<div class="dial"><label for="<?php echo esc_attr( $id ); ?>" class="sr-only"><?php echo esc_html( $t['name'] ); ?></label><input id="<?php echo esc_attr( $id ); ?>" type="range" min="0" max="100" value="<?php echo (int) $t['value']; ?>" style="--c:<?php echo esc_attr( $c ); ?>"><output for="<?php echo esc_attr( $id ); ?>"><?php echo (int) $t['value']; ?></output></div>
					<?php if ( $t['more'] ) : ?><a class="more" href="<?php echo rsm_url( $t['link'] ); ?>"><?php echo esc_html( $t['more'] ); ?></a><?php endif; ?>
				</div>
			<?php endforeach; ?>
				<div class="lt result"><span class="k" style="color:#FFD98A"><?php echo esc_html( $s['r_k'] ); ?></span><h3><?php echo esc_html( $s['r_name'] ); ?></h3><p class="lab-out"><b data-rel><?php echo (int) $prod; ?></b><span><?php echo esc_html( $s['r_unit'] ); ?></span></p><p data-say></p></div>
			</div>
			<div class="lab-foot"><span class="eg-lab"><?php echo esc_html( $s['try_label'] ); ?></span><div class="presets" aria-label="<?php echo esc_attr( $s['try_label'] ); ?>">
				<?php foreach ( (array) $s['presets'] as $p ) { printf( '<button type="button" data-v="%s">%s</button>', esc_attr( $p['v'] ), esc_html( $p['label'] ) ); } ?>
			</div></div>
			<?php if ( $s['caption'] ) : ?><p class="caption"><?php echo esc_html( $s['caption'] ); ?></p><?php endif; ?>
		</div>
	<?php }
}

/* ============================== the map of searches ============================== */
class RSM_W_Console extends RSM_Widget {
	public function get_name() { return 'rsm-console'; }
	public function get_title() { return __( 'RSM Search map console', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-search-results'; }
	protected function style_targets() { return array( 'title' => '.console-title, {{WRAPPER}} .readout .big', 'text' => '.readout .q, {{WRAPPER}} .readout .line, {{WRAPPER}} .console-foot', 'accent' => '.console-eq' ); }
	protected function fields() {
		$tr = array(); foreach ( array( 'plumbers' => 'Plumbers', 'hvac' => 'HVAC', 'roofers' => 'Roofers', 'electricians' => 'Electricians', 'dentists' => 'Dentists', 'law-firms' => 'Law firms', 'personal-injury-lawyers' => 'Personal injury lawyers', 'contractors' => 'Contractors', 'landscapers' => 'Landscapers', 'auto-repair' => 'Auto repair', 'med-spas' => 'Med spas', 'realtors' => 'Realtors', 'medical-clinics' => 'Medical clinics', 'accountants' => 'Accountants', 'cleaners' => 'Cleaners', 'painters' => 'Painters', 'pest-control' => 'Pest control', 'movers' => 'Movers', 'insurance-agents' => 'Insurance agents', 'mortgage-brokers' => 'Mortgage brokers' ) as $k => $v ) { $tr[] = array( 'slug' => $k, 'label' => $v ); }
		$ci = array(); foreach ( array( 'new-york' => 'New York', 'los-angeles' => 'Los Angeles', 'chicago' => 'Chicago', 'houston' => 'Houston', 'dallas' => 'Dallas', 'miami' => 'Miami', 'atlanta' => 'Atlanta', 'phoenix' => 'Phoenix', 'denver' => 'Denver', 'fresno' => 'Fresno' ) as $k => $v ) { $ci[] = array( 'slug' => $k, 'label' => $v ); }
		$opt = array( 'title' => '{{{ label }}}', 'fields' => array( array( 'label', __( 'Name shown', 'rsm-elements' ), 'text', '' ), array( 'slug', __( 'Data key (matches a file in the theme, assets/map)', 'rsm-elements' ), 'text', '' ) ) );
		return array(
		array( 'title', __( 'Title', 'rsm-elements' ), 'text', 'The equation, applied to you' ),
		array( 'eq', __( 'Line beside the title', 'rsm-elements' ), 'text', 'Relevance = Read × Confirm × Choose' ),
		array( 'trade_label', __( 'Trade label', 'rsm-elements' ), 'text', 'Your trade' ), array( 'city_label', __( 'City label', 'rsm-elements' ), 'text', 'Your city' ),
		array( 'trade', __( 'Trade shown first (data key)', 'rsm-elements' ), 'text', 'plumbers' ), array( 'city', __( 'City shown first (data key)', 'rsm-elements' ), 'text', 'miami' ),
		array( 'button', __( 'Button', 'rsm-elements' ), 'text', 'See the full plan' ), array( 'action', __( 'Button goes to', 'rsm-elements' ), 'url', '/your-plan/' ),
		array( 'unit', __( 'Word under the big number', 'rsm-elements' ), 'text', 'searches' ),
		array( 'say', __( 'Line above the picture ({trade} and {city} are filled in)', 'rsm-elements' ), 'textarea', 'Every light is one real search. This is how many ways {trade} in {city} look for a company like ours.' ),
		array( 'say_note', __( 'Small line beside it', 'rsm-elements' ), 'text', 'Grouped by what the person wants. Point at a light to read it.' ),
		array( 'foot', __( 'Small print', 'rsm-elements' ), 'textarea', '' ),
		array( 'r1', __( 'Read', 'rsm-elements' ), 'section' ),
		array( 'r_label', __( 'Label', 'rsm-elements' ), 'text', 'Read' ), array( 'r_note', __( 'Note', 'rsm-elements' ), 'text', 'from the map' ),
		array( 'r_q', __( 'Line ({trade} and {city} are filled in)', 'rsm-elements' ), 'textarea', 'Searches {trade} in {city} make when they look for a company like ours' ),
		array( 'r_line', __( 'Detail ({ex1}, {ex2}, {kinds})', 'rsm-elements' ), 'textarea', 'Such as “{ex1}” and “{ex2}”, across {kinds} kinds of search.' ),
		array( 'r2', __( 'Confirm', 'rsm-elements' ), 'section' ),
		array( 'c_label', __( 'Label', 'rsm-elements' ), 'text', 'Confirm' ), array( 'c_note', __( 'Note', 'rsm-elements' ), 'text', 'first run' ), array( 'c_note_other', __( 'Note for other trades', 'rsm-elements' ), 'text', 'not run yet' ),
		array( 'c_q', __( 'Line', 'rsm-elements' ), 'text', 'Who ChatGPT, Gemini and Perplexity name' ),
		array( 'c_big', __( 'Big words', 'rsm-elements' ), 'text', 'In progress' ), array( 'c_big_other', __( 'Big words for other trades', 'rsm-elements' ), 'text', 'Coming' ),
		array( 'c_line', __( 'Detail for the first trade', 'rsm-elements' ), 'textarea', 'The AI Recommendation Index is being run for plumbers in the launch cities this month. Published when it is done.' ),
		array( 'c_line_other', __( 'Detail for other trades ({trade}, {city})', 'rsm-elements' ), 'textarea', 'The Index runs trade by trade. {trade} in {city} is not published yet; ask to be told when it is.' ),
		array( 'r3', __( 'Choose', 'rsm-elements' ), 'section' ),
		array( 'h_label', __( 'Label', 'rsm-elements' ), 'text', 'Choose' ), array( 'h_note', __( 'Note', 'rsm-elements' ), 'text', 'at launch' ),
		array( 'h_q', __( 'Line ({city})', 'rsm-elements' ), 'text', 'Is your trade still open in {city}?' ), array( 'h_big', __( 'Big words', 'rsm-elements' ), 'text', 'One per city' ),
		array( 'h_line', __( 'Detail', 'rsm-elements' ), 'textarea', 'We take one business per trade per city. The Open Board goes live with the site; until then, ask on the call.' ),
		array( 'lists', __( 'Trades and cities', 'rsm-elements' ), 'section' ),
		array( 'trades', __( 'Trades', 'rsm-elements' ), 'repeater', $tr, $opt ), array( 'cities', __( 'Cities', 'rsm-elements' ), 'repeater', $ci, $opt ),
	); }
	private function tok( $text, $names ) { $h = esc_html( $text ); foreach ( $names as $k => $v ) { $h = str_replace( '{' . $k . '}', $v, $h ); } return $h; }
	protected function render() { $s = $this->s(); $tn = ''; $cn = '';
		foreach ( (array) $s['trades'] as $t ) { if ( $t['slug'] === $s['trade'] ) { $tn = $t['label']; } } foreach ( (array) $s['cities'] as $c ) { if ( $c['slug'] === $s['city'] ) { $cn = $c['label']; } }
		/* first paint carries the real figures for the default trade and city; the script takes over on change */
		$first = array( 'n' => '', 'ex' => array( '', '' ), 'k' => '' ); $cf = get_template_directory() . '/assets/console-data.json';
		if ( is_readable( $cf ) ) { $cd = json_decode( (string) file_get_contents( $cf ), true ); if ( isset( $cd[ $s['trade'] ]['c'][ $s['city'] ] ) ) { $first = array_merge( $first, $cd[ $s['trade'] ]['c'][ $s['city'] ] ); } } // phpcs:ignore WordPress.WP.AlternativeFunctions
		ob_start();
		$sp = array( 'trade' => '<span data-trade-name>' . esc_html( strtolower( $tn ) ) . '</span>', 'city' => '<span data-city-name>' . esc_html( $cn ) . '</span>', 'ex1' => '<span data-ex1>' . esc_html( $first['ex'][0] ?? '' ) . '</span>', 'ex2' => '<span data-ex2>' . esc_html( $first['ex'][1] ?? '' ) . '</span>', 'kinds' => '<span data-kinds>' . esc_html( (string) $first['k'] ) . '</span>' );
		$sel = function ( $name, $rows, $cur ) { $o = '<select name="' . $name . '" id="' . $name . '">'; foreach ( (array) $rows as $r ) { $o .= sprintf( '<option value="%s"%s>%s</option>', esc_attr( $r['slug'] ), selected( $r['slug'], $cur, false ), esc_html( $r['label'] ) ); } return $o . '</select>'; }; ?>
		<form class="console glass" action="<?php echo rsm_url( $s['action'] ); ?>" method="get" aria-labelledby="console-h" data-first="<?php echo esc_attr( $s['trade'] ); ?>" data-c="<?php echo esc_attr( wp_json_encode( array( 'note' => $s['c_note'], 'noteOther' => $s['c_note_other'], 'big' => $s['c_big'], 'bigOther' => $s['c_big_other'], 'line' => $s['c_line'], 'lineOther' => $s['c_line_other'] ) ) ); ?>">
			<div class="console-head"><h2 id="console-h" class="console-title"><?php echo esc_html( $s['title'] ); ?></h2><span class="console-eq"><?php echo esc_html( $s['eq'] ); ?></span></div>
			<div class="console-body">
				<div class="sky" id="sky"><p class="sky-say"><?php echo $this->tok( $s['say'], $sp ); // phpcs:ignore ?><span><?php echo esc_html( $s['say_note'] ); ?></span></p><canvas aria-hidden="true"></canvas><div class="sky-count" aria-hidden="true"><b data-count></b><span><?php echo esc_html( $s['unit'] ); ?></span></div><div class="sky-tip" aria-hidden="true"></div></div>
				<div class="side">
					<div class="picker"><label><?php echo esc_html( $s['trade_label'] ); ?> <?php echo $sel( 'trade', $s['trades'], $s['trade'] ); // phpcs:ignore ?></label><label><?php echo esc_html( $s['city_label'] ); ?> <?php echo $sel( 'city', $s['cities'], $s['city'] ); // phpcs:ignore ?></label><button type="submit" class="btn"><?php echo esc_html( $s['button'] ); ?></button></div>
					<div class="readout">
						<div><p class="term t-read"><?php echo esc_html( $s['r_label'] ); ?> <i><?php echo esc_html( $s['r_note'] ); ?></i></p><p class="q"><?php echo $this->tok( $s['r_q'], $sp ); // phpcs:ignore ?></p><p class="big"><span data-count></span> <?php echo esc_html( $s['unit'] ); ?></p><p class="line"><?php echo $this->tok( $s['r_line'], $sp ); // phpcs:ignore ?></p></div>
						<div><p class="term t-confirm"><?php echo esc_html( $s['c_label'] ); ?> <i data-confirm-status><?php echo esc_html( $s['c_note'] ); ?></i></p><p class="q"><?php echo esc_html( $s['c_q'] ); ?></p><p class="big" data-confirm-big><?php echo esc_html( $s['c_big'] ); ?></p><p class="line" data-confirm-line><?php echo esc_html( $s['c_line'] ); ?></p></div>
						<div><p class="term t-choose"><?php echo esc_html( $s['h_label'] ); ?> <i><?php echo esc_html( $s['h_note'] ); ?></i></p><p class="q"><?php echo $this->tok( $s['h_q'], $sp ); // phpcs:ignore ?></p><p class="big"><?php echo esc_html( $s['h_big'] ); ?></p><p class="line"><?php echo esc_html( $s['h_line'] ); ?></p></div>
					</div>
				</div>
			</div>
			<ul class="kinds" id="kinds" aria-label="Kinds of search in this map"></ul>
			<?php if ( $s['foot'] ) : ?><p class="console-foot"><?php echo esc_html( $s['foot'] ); ?></p><?php endif; ?>
		</form>
	<?php $html = ob_get_clean(); $n = $first['n'] ? number_format( (int) $first['n'] ) : ''; echo str_replace( array( '<b data-count></b>', '<span data-count></span>' ), array( '<b data-count>' . esc_html( $n ) . '</b>', '<span data-count>' . esc_html( $n ) . '</span>' ), $html ); // phpcs:ignore WordPress.Security.EscapeOutput
	}
}

/* ============================== cards ============================== */
class RSM_W_Card extends RSM_Widget {
	public function get_name() { return 'rsm-card'; }
	public function get_title() { return __( 'RSM Card', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-info-box'; }
	protected function style_targets() { return array( 'title' => 'h3', 'text' => 'p, {{WRAPPER}} .d', 'accent' => '.go, {{WRAPPER}} .k, {{WRAPPER}} .day-n, {{WRAPPER}} .tag' ); }
	protected function fields() { return array(
		array( 'variant', __( 'Kind of card', 'rsm-elements' ), 'select', 'problem', array( 'options' => array( 'problem' => __( 'Picture card', 'rsm-elements' ), 'look' => __( 'Status card', 'rsm-elements' ), 'stat' => __( 'Figure card', 'rsm-elements' ), 'clause' => __( 'Commitment', 'rsm-elements' ), 'service' => __( 'Service with icon', 'rsm-elements' ), 'day' => __( 'Day step', 'rsm-elements' ), 'cadence' => __( 'Cadence item', 'rsm-elements' ) ) ) ),
		array( 'svg', __( 'Picture or icon (SVG code)', 'rsm-elements' ), 'code', '', array( 'condition' => array( 'variant' => array( 'problem', 'service' ) ) ) ),
		array( 'number', __( 'Figure, numeral or small label', 'rsm-elements' ), 'text', '', array( 'condition' => array( 'variant' => array( 'stat', 'clause', 'day', 'cadence' ) ) ) ),
		array( 'tag', __( 'Tag or status', 'rsm-elements' ), 'text', '', array( 'condition' => array( 'variant' => array( 'problem', 'look', 'stat' ) ) ) ),
		array( 'status', __( 'Status colour', 'rsm-elements' ), 'select', 'green', array( 'options' => array( 'green' => __( 'Green', 'rsm-elements' ), 'gold' => __( 'Gold', 'rsm-elements' ) ), 'condition' => array( 'variant' => 'look' ) ) ),
		array( 'title', __( 'Title', 'rsm-elements' ), 'text', 'Title' ),
		array( 'text', __( 'Text (bold with <b>)', 'rsm-elements' ), 'textarea', '' ),
		array( 'link_text', __( 'Link text', 'rsm-elements' ), 'text', '' ),
		array( 'link', __( 'Link', 'rsm-elements' ), 'url', '' ),
		array( 'highlight', __( 'Highlight in gold', 'rsm-elements' ), 'switch', '' ),
	); }
	protected function render() { $s = $this->s(); $v = $s['variant']; $href = rsm_url( $s['link'] ); $hl = 'yes' === $s['highlight'];
		$t = '<h3>' . rsm_inline( $s['title'] ) . '</h3>'; $p = $s['text'] ? '<p>' . rsm_inline( $s['text'] ) . '</p>' : ''; $go = $s['link_text'] ? '<span class="go">' . esc_html( $s['link_text'] ) . '</span>' : '';
		$open = $href ? '<a href="' . $href . '"' : '<div'; $close = $href ? '</a>' : '</div>';
		switch ( $v ) {
			case 'look': echo '<div class="rs-one">' . $open . ' class="card glass"><span class="tag"><span class="status ' . ( 'gold' === $s['status'] ? '' : 'green' ) . '">' . esc_html( $s['tag'] ) . '</span></span>' . $t . $p . $go . $close . '</div>'; break; // phpcs:ignore
			case 'stat': echo '<div class="stats rs-one">' . $open . ' class="glass"><span class="n gold">' . esc_html( $s['number'] ) . '</span><span class="k">' . esc_html( $s['tag'] ) . '</span><span class="d">' . rsm_inline( $s['text'] ) . '</span>' . $go . $close . '</div>'; break; // phpcs:ignore
			case 'clause': echo '<div class="clauses rs-one"><div class="glass rs-clause"><span class="roman" aria-hidden="true">' . esc_html( $s['number'] ) . '</span>' . $t . $p . '</div></div>'; break; // phpcs:ignore
			case 'service': echo '<div class="services rs-one">' . $open . ' class="glass"><span class="ic">' . rsm_svg( $s['svg'] ) . '</span>' . $t . $p . $close . '</div>'; break; // phpcs:ignore
			case 'day': echo '<div class="days rs-one"><div class="glass rs-day' . ( $hl ? ' is-live' : '' ) . '"><span class="day-n">' . esc_html( $s['number'] ) . '</span>' . $t . $p . '</div></div>'; break; // phpcs:ignore
			case 'cadence': echo '<div class="cadence rs-one"><div class="rs-cad"><span class="k">' . esc_html( $s['number'] ) . '</span>' . $t . $p . '</div></div>'; break; // phpcs:ignore
			default: echo '<div class="problems rs-one">' . $open . ' class="card glass' . ( $hl ? ' feature' : '' ) . '"><div class="c-head">' . ( $s['tag'] ? '<span class="tag">' . esc_html( $s['tag'] ) . '</span>' : '' ) . $t . '</div><div class="c-body">' . rsm_svg( $s['svg'] ) . $p . $go . '</div>' . $close . '</div>'; // phpcs:ignore
		}
	}
}
class RSM_W_Seal extends RSM_Widget {
	public function get_name() { return 'rsm-seal'; }
	public function get_title() { return __( 'RSM Signature and seal', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-check-circle-o'; }
	protected function style_targets() { return array( 'title' => '.sig', 'text' => '.small', 'accent' => '.seal text' ); }
	protected function fields() { return array(
		array( 'ring', __( 'Words round the seal', 'rsm-elements' ), 'text', 'IN WRITING · SIGNED BEFORE YOU PAY · ' ),
		array( 'name', __( 'Name', 'rsm-elements' ), 'text', "Thomas D'Souza" ),
		array( 'role', __( 'Role', 'rsm-elements' ), 'text', 'Founder · in digital marketing since 2010' ),
		array( 'note', __( 'Note beside it', 'rsm-elements' ), 'textarea', '' ),
	); }
	protected function render() { $s = $this->s(); $id = 'seal-' . $this->get_id(); ?>
		<div class="signed"><svg class="seal" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="<?php echo esc_attr( $id ); ?>" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1 -92 0"/></defs><circle cx="60" cy="60" r="58" fill="none" stroke="rgba(248,177,15,.5)"/><circle cx="60" cy="60" r="35" fill="rgba(248,177,15,.10)" stroke="rgba(248,177,15,.8)"/><g class="spin"><text><textPath href="#<?php echo esc_attr( $id ); ?>"><?php echo esc_html( $s['ring'] ); ?></textPath></text></g><path d="M47 61l9 9 18-20" fill="none" stroke="#FFD98A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
		<div class="signature"><span class="sig"><?php echo esc_html( $s['name'] ); ?></span><span class="small"><?php echo esc_html( $s['role'] ); ?></span></div><?php if ( $s['note'] ) : ?><p class="small"><?php echo esc_html( $s['note'] ); ?></p><?php endif; ?></div>
	<?php }
}

/* ============================== pictures built from data ============================== */
class RSM_W_US_Map extends RSM_Widget {
	public function get_name() { return 'rsm-us-map'; }
	public function get_title() { return __( 'RSM US map of cities', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-google-maps'; }
	protected function style_targets() { return array( 'title' => '.usmap .city text', 'text' => '.caption', 'accent' => '.usmap .city.launch .pin' ); }
	protected function fields() { $c = array();
		$rows = array(
			array( 'New York', -74.0, 40.7, 'r', 1, 1 ), array( 'Los Angeles', -118.2, 34.05, 'l', 1, 1 ), array( 'Chicago', -87.6, 41.9, 'l', 1, 1 ), array( 'Houston', -95.4, 29.76, 'r', 1, 1 ), array( 'Dallas', -96.8, 32.8, 't', 1, 1 ),
			array( 'Miami', -80.2, 25.8, 'r', 1, 1 ), array( 'Atlanta', -84.4, 33.75, 'b', 1, 1 ), array( 'Phoenix', -112.1, 33.45, 'b', 1, 1 ), array( 'Denver', -105.0, 39.74, 't', 1, 1 ), array( 'Fresno', -119.8, 36.74, 'b', 1, 1 ),
			array( 'Philadelphia', -75.16, 39.95, 'r', 0, 0 ), array( 'San Antonio', -98.49, 29.42, 'l', 0, 1 ), array( 'San Diego', -117.16, 32.72, 'l', 0, 1 ), array( 'Austin', -97.74, 30.27, 'r', 0, 0 ), array( 'San Jose', -121.89, 37.34, 'r', 0, 0 ),
			array( 'Jacksonville', -81.66, 30.33, 'r', 0, 1 ), array( 'Fort Worth', -97.33, 32.76, 'l', 0, 0 ), array( 'Columbus', -82.99, 39.96, 'b', 0, 0 ), array( 'Charlotte', -80.84, 35.23, 'r', 0, 0 ), array( 'Indianapolis', -86.16, 39.77, 'b', 0, 0 ),
			array( 'San Francisco', -122.42, 37.77, 'l', 0, 1 ), array( 'Seattle', -122.33, 47.61, 'r', 0, 1 ), array( 'Washington', -77.04, 38.91, 'r', 0, 1 ), array( 'Boston', -71.06, 42.36, 'r', 0, 1 ), array( 'Nashville', -86.78, 36.16, 'l', 0, 1 ),
			array( 'Las Vegas', -115.14, 36.17, 'r', 0, 1 ), array( 'Orlando', -81.38, 28.54, 'r', 0, 0 ), array( 'Tampa', -82.46, 27.95, 'l', 0, 1 ), array( 'Detroit', -83.05, 42.33, 't', 0, 1 ), array( 'Minneapolis', -93.27, 44.98, 't', 0, 1 ),
			array( 'Portland', -122.68, 45.52, 'r', 0, 1 ), array( 'Oklahoma City', -97.52, 35.47, 't', 0, 0 ), array( 'El Paso', -106.49, 31.76, 'b', 0, 1 ), array( 'Memphis', -90.05, 35.15, 'b', 0, 0 ), array( 'Louisville', -85.76, 38.25, 'r', 0, 0 ),
			array( 'Baltimore', -76.61, 39.29, 'r', 0, 0 ), array( 'Milwaukee', -87.91, 43.04, 't', 0, 0 ), array( 'Albuquerque', -106.65, 35.08, 'r', 0, 1 ), array( 'Tucson', -110.97, 32.22, 'b', 0, 0 ), array( 'Sacramento', -121.49, 38.58, 'r', 0, 0 ),
			array( 'Kansas City', -94.58, 39.1, 't', 0, 1 ), array( 'Mesa', -111.83, 33.42, 'r', 0, 0 ), array( 'Omaha', -95.93, 41.26, 't', 0, 0 ), array( 'Raleigh', -78.64, 35.78, 'r', 0, 0 ), array( 'Colorado Springs', -104.82, 38.83, 'b', 0, 0 ),
			array( 'Long Beach', -118.19, 33.77, 'r', 0, 0 ), array( 'Virginia Beach', -75.98, 36.85, 'r', 0, 0 ), array( 'Oakland', -122.27, 37.8, 'r', 0, 0 ), array( 'Tulsa', -95.99, 36.15, 't', 0, 0 ), array( 'Frisco', -96.82, 33.15, 't', 0, 0 ),
		);
		foreach ( $rows as $r ) { $c[] = array( 'name' => $r[0], 'lon' => $r[1], 'lat' => $r[2], 'side' => $r[3], 'launch' => $r[4] ? 'yes' : '', 'show' => $r[5] ? 'yes' : '' ); }
		return array(
		array( 'caption', __( 'Line under the map', 'rsm-elements' ), 'text', 'All 50 cities in our map. The ten in gold are the launch cities, at full depth: one business per trade in each.' ),
		array( 'label', __( 'Description for screen readers', 'rsm-elements' ), 'text', 'Map of the United States with the fifty mapped cities marked and the ten launch cities highlighted' ),
		array( 'k_launch', __( 'Key: launch cities', 'rsm-elements' ), 'text', 'Launch city, full depth' ),
		array( 'k_mapped', __( 'Key: other cities', 'rsm-elements' ), 'text', 'Mapped city' ),
		array( 'cities', __( 'Cities', 'rsm-elements' ), 'repeater', $c, array( 'title' => '{{{ name }}}', 'fields' => array(
			array( 'name', __( 'Name', 'rsm-elements' ), 'text', '' ), array( 'lon', __( 'Longitude (west is negative)', 'rsm-elements' ), 'number', -100, array( 'step' => 0.01 ) ), array( 'lat', __( 'Latitude', 'rsm-elements' ), 'number', 40, array( 'step' => 0.01 ) ),
			array( 'side', __( 'Label sits', 'rsm-elements' ), 'select', 'r', array( 'options' => array( 'r' => __( 'Right', 'rsm-elements' ), 'l' => __( 'Left', 'rsm-elements' ), 't' => __( 'Above', 'rsm-elements' ), 'b' => __( 'Below', 'rsm-elements' ) ) ) ),
			array( 'launch', __( 'Launch city (gold)', 'rsm-elements' ), 'switch', 'yes' ),
			array( 'show', __( 'Show the name', 'rsm-elements' ), 'switch', 'yes' ),
		) ) ),
	); }
	protected function render() { $s = $this->s(); $o = '<svg class="usmap" viewBox="-70 -4 800 440" role="img" aria-label="' . esc_attr( $s['label'] ) . '"><g class="land">';
		foreach ( rsm_data( 'us-dots.json' ) as $d ) { $o .= '<circle cx="' . (int) $d[0] . '" cy="' . (int) $d[1] . '" r="2.1"/>'; } $o .= '</g>';
		$cities = array_values( (array) $s['cities'] ); usort( $cities, function ( $a, $b ) { return (int) ! empty( $a['launch'] ) - (int) ! empty( $b['launch'] ); } ); $li = 0;
		foreach ( $cities as $c ) { $x = round( ( (float) $c['lon'] + 125 ) * cos( deg2rad( 38 ) ) * 13.2 + 40 ); $y = round( ( 50 - (float) $c['lat'] ) * 16.6 ); $L = ! empty( $c['launch'] ); $gap = $L ? 11 : 8;
			$pos = array( 'r' => array( $x + $gap, $y + 3.5, 'start' ), 'l' => array( $x - $gap, $y + 3.5, 'end' ), 't' => array( $x, $y - $gap - 1, 'middle' ), 'b' => array( $x, $y + $gap + 9, 'middle' ) ); $p = $pos[ $c['side'] ] ?? $pos['r'];
			$o .= '<g class="city' . ( $L ? ' launch' : '' ) . '" aria-label="' . esc_attr( $c['name'] ) . '"' . ( $L ? ' style="--d:' . number_format( $li++ * 0.35, 2 ) . 's"' : '' ) . '>' . ( $L ? '<circle class="halo" cx="' . $x . '" cy="' . $y . '" r="5"/>' : '' ) . '<circle class="pin" cx="' . $x . '" cy="' . $y . '" r="' . ( $L ? '4.5' : '2.8' ) . '"/>' . ( ! empty( $c['show'] ) ? '<text x="' . $p[0] . '" y="' . $p[1] . '" text-anchor="' . $p[2] . '">' . esc_html( $c['name'] ) . '</text>' : '' ) . '</g>'; }
		$key = '<ul class="map-key"><li class="kl">' . esc_html( $s['k_launch'] ) . '</li><li class="km">' . esc_html( $s['k_mapped'] ) . '</li></ul>';
		echo '<figure class="plate glass map-plate">' . $o . '</svg><div class="map-foot">' . ( $s['caption'] ? '<figcaption class="caption">' . esc_html( $s['caption'] ) . '</figcaption>' : '' ) . $key . '</div></figure>'; // phpcs:ignore
	}
}
class RSM_W_Path extends RSM_Widget {
	public function get_name() { return 'rsm-path'; }
	public function get_title() { return __( 'RSM First fifteen days', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-time-line'; }
	protected function fields() { return array(
		array( 'label', __( 'Description for screen readers', 'rsm-elements' ), 'text', 'Five days from the first conversation to live work, then work logged every day until the first report on day fifteen' ),
		array( 's1', __( 'Day 1', 'rsm-elements' ), 'text', 'Discover' ), array( 's2', __( 'Day 2', 'rsm-elements' ), 'text', 'Market study' ), array( 's3', __( 'Day 3', 'rsm-elements' ), 'text', '413 checks' ), array( 's4', __( 'Day 4', 'rsm-elements' ), 'text', 'Growth plan' ), array( 's5', __( 'Day 5', 'rsm-elements' ), 'text', 'Live' ),
		array( 'between', __( 'Days 6 to 14', 'rsm-elements' ), 'text', 'Work shipped and logged every day' ),
		array( 'report', __( 'Day 15', 'rsm-elements' ), 'text', 'First report' ),
		array( 'day', __( 'Word for "day"', 'rsm-elements' ), 'text', 'Day' ),
	); }
	private function bez( $s, $t ) { $r = array(); for ( $k = 0; $k < 2; $k++ ) { $r[] = pow( 1 - $t, 3 ) * $s[0][ $k ] + 3 * pow( 1 - $t, 2 ) * $t * $s[1][ $k ] + 3 * ( 1 - $t ) * $t * $t * $s[2][ $k ] + pow( $t, 3 ) * $s[3][ $k ]; } return $r; }
	private function y_at( $x ) { $seg = $x <= 600 ? array( array( 100, 250 ), array( 300, 250 ), array( 420, 120 ), array( 600, 120 ) ) : array( array( 600, 120 ), array( 780, 120 ), array( 950, 78 ), array( 1120, 78 ) ); $best = null; $by = 0;
		for ( $k = 0; $k <= 400; $k++ ) { $p = $this->bez( $seg, $k / 400 ); $d = abs( $p[0] - $x ); if ( null === $best || $d < $best ) { $best = $d; $by = $p[1]; } } return $by; }
	protected function render() { $s = $this->s(); $d = 'M100 250 C 300 250, 420 120, 600 120 S 950 78, 1120 78'; $u = $this->get_id();
		$ico = array( 1 => '<path d="M-11 -9h22v14h-12l-7 6v-6h-3z"/>', 2 => '<circle cx="-2" cy="-2" r="8"/><path d="M4 4l7 7"/>', 3 => '<path d="M-10 -8l4 4 7-8M-10 4l4 4 7-8M5 -6h7M5 6h7"/>', 4 => '<rect x="-11" y="-9" width="22" height="20" rx="3"/><path d="M-11 -3h22M-5 -13v6M5 -13v6"/>', 5 => '<circle r="3" fill="#1A1200" stroke="none"/><path d="M-7 -7a10 10 0 0 0 0 14M7 -7a10 10 0 0 1 0 14M-12 -12a17 17 0 0 0 0 24M12 -12a17 17 0 0 1 0 24"/>' );
		$xs = array(); for ( $n = 1; $n <= 5; $n++ ) { $xs[ $n ] = 100 + ( $n - 1 ) * 125; } for ( $n = 6; $n <= 15; $n++ ) { $xs[ $n ] = 600 + ( $n - 5 ) * 52; }
		$o = '<svg viewBox="0 0 1220 350" role="img" aria-label="' . esc_attr( $s['label'] ) . '"><defs><linearGradient id="pg' . $u . '" x1="0" x2="1"><stop offset="0" stop-color="#6F8CF0"/><stop offset=".45" stop-color="#A3B5F2"/><stop offset=".5" stop-color="#F8B10F"/><stop offset="1" stop-color="#4CC0A8"/></linearGradient><radialGradient id="pglow' . $u . '"><stop offset="0" stop-color="#F8B10F" stop-opacity=".6"/><stop offset="1" stop-color="#F8B10F" stop-opacity="0"/></radialGradient><linearGradient id="pmed' . $u . '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4760B4"/><stop offset=".5" stop-color="#243268"/><stop offset="1" stop-color="#121A40"/></linearGradient><filter id="pblur' . $u . '" x="-10%" y="-80%" width="120%" height="260%"><feGaussianBlur stdDeviation="9"/></filter><linearGradient id="parea' . $u . '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6F8CF0" stop-opacity=".22"/><stop offset="1" stop-color="#6F8CF0" stop-opacity="0"/></linearGradient></defs>';
		$o .= '<path d="' . $d . ' L1120 300 L100 300 Z" fill="url(#parea' . $u . ')"/><path d="M100 300H1120" stroke="rgba(163,181,242,.3)" stroke-width="1.5"/>';
		for ( $n = 1; $n <= 15; $n++ ) { $big = in_array( $n, array( 1, 5, 10, 15 ), true ); $o .= '<path d="M' . $xs[ $n ] . ' 300v' . ( $big ? 10 : 6 ) . '" stroke="rgba(163,181,242,.55)" stroke-width="1.5"/>' . ( $big ? '<text x="' . $xs[ $n ] . '" y="330" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="1.5" fill="#B4C0E0">' . esc_html( strtoupper( $s['day'] ) ) . ' ' . $n . '</text>' : '' ); }
		$o .= '<path d="' . $d . '" fill="none" stroke="url(#pg' . $u . ')" stroke-width="14" stroke-linecap="round" filter="url(#pblur' . $u . ')" opacity=".7"/><path class="base" id="launch' . $u . '" d="' . $d . '" fill="none" stroke="url(#pg' . $u . ')" stroke-width="5" stroke-linecap="round"/><path class="trail-glow" d="' . $d . '" fill="none" stroke="#FFE7AE" stroke-width="12" stroke-linecap="round" filter="url(#pblur' . $u . ')" opacity="0"/><path class="trail" d="' . $d . '" fill="none" stroke="#FFF3D6" stroke-width="3" stroke-linecap="round" opacity="0"/>';
		for ( $n = 6; $n <= 14; $n++ ) { $x = $xs[ $n ]; $y = number_format( $this->y_at( $x ), 1, '.', '' ); $o .= '<g class="tick" data-x="' . $x . '"><circle cx="' . $x . '" cy="' . $y . '" r="9" fill="#121A40" stroke="#4CC0A8" stroke-width="2"/><path d="M' . ( $x - 4 ) . ' ' . $y . 'l3 3 5-6" fill="none" stroke="#8EE3D0" stroke-width="2" stroke-linecap="round"/></g>'; }
		for ( $n = 1; $n <= 5; $n++ ) { $x = $xs[ $n ]; $yy = $this->y_at( $x ); $y = number_format( $yy, 1, '.', '' ); $gold = 5 === $n; $r = $gold ? 38 : 30;
			if ( $gold ) { $o .= '<circle cx="' . $x . '" cy="' . $y . '" r="110" fill="url(#pglow' . $u . ')"/><circle cx="' . $x . '" cy="' . $y . '" r="' . $r . '" fill="none" stroke="#F8B10F" stroke-width="1.5"><animate attributeName="r" values="' . $r . ';' . ( $r + 40 ) . '" dur="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.6s" repeatCount="indefinite"/></circle>'; }
			$o .= '<g class="ms' . ( $gold ? ' ms-live' : '' ) . '" data-x="' . $x . '"><circle class="ms-ring" cx="' . $x . '" cy="' . $y . '" r="' . $r . '" fill="none" stroke="#FFD98A" stroke-width="2" opacity="0"/><circle class="ms-core" cx="' . $x . '" cy="' . $y . '" r="' . $r . '" fill="' . ( $gold ? '#F8B10F' : 'url(#pmed' . $u . ')' ) . '" stroke="' . ( $gold ? '#FFD98A' : 'rgba(190,205,250,.6)' ) . '" stroke-width="2"/><g transform="translate(' . $x . ',' . $y . ') scale(' . ( $gold ? 1.25 : 1.1 ) . ')" fill="none" stroke="' . ( $gold ? '#1A1200' : '#FFD98A' ) . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' . $ico[ $n ] . '</g>';
			$o .= '<text x="' . $x . '" y="' . number_format( $yy - $r - 14, 1, '.', '' ) . '" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="2" fill="' . ( $gold ? '#FFD98A' : '#fff' ) . '">' . esc_html( strtoupper( $s[ 's' . $n ] ) ) . '</text></g>'; }
		$x = $xs[15]; $yy = $this->y_at( $x ); $y = number_format( $yy, 1, '.', '' );
		$o .= '<g class="ms ms-report" data-x="' . $x . '"><circle class="ms-ring" cx="' . $x . '" cy="' . $y . '" r="34" fill="none" stroke="#8EE3D0" stroke-width="2" opacity="0"/><circle class="ms-core" cx="' . $x . '" cy="' . $y . '" r="34" fill="#121A40" stroke="#4CC0A8" stroke-width="2.5"/><g transform="translate(' . $x . ',' . $y . ')" fill="none" stroke="#8EE3D0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M-9 -13h13l6 6v20h-19z"/><path d="M-4 0h9M-4 6h9"/></g><text x="' . $x . '" y="' . number_format( $yy - 48, 1, '.', '' ) . '" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="2" fill="#8EE3D0">' . esc_html( strtoupper( $s['report'] ) ) . '</text></g>';
		$o .= '<text x="' . ( ( $xs[6] + $xs[14] ) / 2 ) . '" y="' . number_format( $this->y_at( $xs[10] ) + 44, 1, '.', '' ) . '" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2" fill="#B4C0E0">' . esc_html( strtoupper( $s['between'] ) ) . '</text>';
		$o .= '<g class="trav" opacity="0"><circle r="22" fill="#FFE7AE" opacity=".18"/><circle r="13" fill="#FFF3D6" opacity=".35"/><circle r="6.5" fill="#fff"/></g></svg>';
		echo '<figure class="plate path-plate rs-path-sync" data-days="' . esc_attr( wp_json_encode( array( $xs[1], $xs[2], $xs[3], $xs[4], $xs[5], $xs[15] ) ) ) . '">' . $o . '</figure>'; // phpcs:ignore
	}
}
class RSM_W_Table extends RSM_Widget {
	public function get_name() { return 'rsm-table'; }
	public function get_title() { return __( 'RSM Record table', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-table'; }
	protected function style_targets() { return array( 'title' => 'tbody th span', 'text' => 'tbody td', 'accent' => 'thead th' ); }
	protected function fields() { return array(
		array( 'caption', __( 'Table name for screen readers', 'rsm-elements' ), 'text', '' ),
		array( 'h1', __( 'Column 1 heading', 'rsm-elements' ), 'text', 'Figure' ), array( 'h2', __( 'Column 2 heading', 'rsm-elements' ), 'text', 'What it counts' ), array( 'h3', __( 'Column 3 heading', 'rsm-elements' ), 'text', 'Source' ),
		array( 'rows', __( 'Rows', 'rsm-elements' ), 'repeater', array(), array( 'title' => '{{{ a }}}', 'fields' => array( array( 'a', __( 'Figure', 'rsm-elements' ), 'text', '' ), array( 'b', __( 'What it counts', 'rsm-elements' ), 'textarea', '' ), array( 'c', __( 'Source', 'rsm-elements' ), 'textarea', '' ) ) ) ),
	); }
	protected function render() { $s = $this->s(); ?>
		<div class="record-wrap glass"><div class="table-wrap"><table class="record-table"><?php if ( $s['caption'] ) : ?><caption class="sr-only"><?php echo esc_html( $s['caption'] ); ?></caption><?php endif; ?>
		<thead><tr><th scope="col"><?php echo esc_html( $s['h1'] ); ?></th><th scope="col"><?php echo esc_html( $s['h2'] ); ?></th><th scope="col"><?php echo esc_html( $s['h3'] ); ?></th></tr></thead><tbody>
		<?php foreach ( (array) $s['rows'] as $r ) { printf( '<tr><th scope="row"><span class="gold">%s</span></th><td>%s</td><td>%s</td></tr>', esc_html( $r['a'] ), esc_html( $r['b'] ), esc_html( $r['c'] ) ); } ?>
		</tbody></table></div></div>
	<?php }
}
class RSM_W_Chips extends RSM_Widget {
	public function get_name() { return 'rsm-chips'; }
	public function get_title() { return __( 'RSM Link chips', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-tags'; }
	protected function style_targets() { return array( 'title' => 'h3', 'text' => '.chips a', 'accent' => '.chips a.more' ); }
	protected function fields() { return array(
		array( 'heading', __( 'Heading', 'rsm-elements' ), 'text', '' ),
		array( 'items', __( 'Links', 'rsm-elements' ), 'repeater', array(), array( 'title' => '{{{ label }}}', 'fields' => array( array( 'label', __( 'Text', 'rsm-elements' ), 'text', '' ), array( 'link', __( 'Link', 'rsm-elements' ), 'url', '' ), array( 'more', __( 'Show as a "see all" link', 'rsm-elements' ), 'switch', '' ) ) ) ),
	); }
	protected function render() { $s = $this->s(); ?>
		<div class="index rs-one"><div><?php if ( $s['heading'] ) : ?><h3><?php echo esc_html( $s['heading'] ); ?></h3><?php endif; ?><ul class="chips">
		<?php foreach ( (array) $s['items'] as $i ) { printf( '<li><a%s href="%s">%s</a></li>', 'yes' === $i['more'] ? ' class="more"' : '', rsm_url( $i['link'] ), esc_html( $i['label'] ) ); } // phpcs:ignore ?>
		</ul></div></div>
	<?php }
}
class RSM_W_Portrait extends RSM_Widget {
	public function get_name() { return 'rsm-portrait'; }
	public function get_title() { return __( 'RSM Portrait frame', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-person'; }
	protected function style_targets() { return array( 'title' => 'figcaption b', 'text' => 'figcaption', 'accent' => 'figcaption b' ); }
	protected function fields() { return array(
		array( 'photo', __( 'Photo (leave empty until a real one exists)', 'rsm-elements' ), 'media', '' ),
		array( 'logo', __( 'Logo shown while there is no photo', 'rsm-elements' ), 'media', rsm_asset( 'rsm-logo-512.png' ) ),
		array( 'name', __( 'Name', 'rsm-elements' ), 'text', "Thomas D'Souza" ),
		array( 'caption', __( 'Caption', 'rsm-elements' ), 'textarea', '' ),
		array( 'label', __( 'Description for screen readers', 'rsm-elements' ), 'text', '' ),
	); }
	protected function render() { $s = $this->s(); $ph = rsm_url( $s['photo'] ); ?>
		<figure class="portrait-slot<?php echo $ph ? ' has-photo' : ''; ?>" aria-label="<?php echo esc_attr( $s['label'] ); ?>"<?php echo $ph ? ' style="background:url(' . $ph . ') center/cover"' : ''; // phpcs:ignore ?>>
			<?php if ( ! $ph ) : ?><span class="brand-disc" aria-hidden="true"><img src="<?php echo rsm_url( $s['logo'] ); ?>" alt="" width="82" height="73"></span><?php endif; ?>
			<figcaption><b><?php echo esc_html( $s['name'] ); ?></b><?php echo esc_html( $s['caption'] ); ?></figcaption>
		</figure>
	<?php }
}
class RSM_W_FAQ extends RSM_Widget {
	protected function is_dynamic_content(): bool { return true; }
	public function get_name() { return 'rsm-faq'; }
	public function get_title() { return __( 'RSM Questions and answers', 'rsm-elements' ); }
	public function get_icon() { return 'eicon-help-o'; }
	protected function style_targets() { return array( 'title' => 'summary h3', 'text' => 'details p', 'accent' => 'summary::after' ); }
	protected function fields() { return array(
		array( 'items', __( 'Questions', 'rsm-elements' ), 'repeater', array(), array( 'title' => '{{{ q }}}', 'fields' => array( array( 'q', __( 'Question', 'rsm-elements' ), 'text', '' ), array( 'a', __( 'Answer (40 to 60 words; a blank line starts a new paragraph)', 'rsm-elements' ), 'textarea', '', array( 'rows' => 6 ) ) ) ) ),
		array( 'open_first', __( 'Open the first question', 'rsm-elements' ), 'switch', 'yes' ),
		array( 'schema', __( 'Tell search engines these are questions and answers', 'rsm-elements' ), 'switch', 'yes' ),
	); }
	protected function render() { $s = $this->s(); $ents = array(); echo '<div class="faq glass">';
		foreach ( array_values( (array) $s['items'] ) as $i => $it ) { $paras = array_filter( array_map( 'trim', preg_split( '/\n\s*\n/', (string) $it['a'] ) ) );
			echo '<details' . ( 0 === $i && 'yes' === $s['open_first'] ? ' open' : '' ) . '><summary><h3>' . esc_html( $it['q'] ) . '</h3></summary>'; foreach ( $paras as $p ) { echo '<p>' . esc_html( $p ) . '</p>'; } echo '</details>';
			$ents[] = array( '@type' => 'Question', 'name' => $it['q'], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => implode( ' ', $paras ) ) ); }
		echo '</div>';
		if ( 'yes' === $s['schema'] && $ents ) { rsm_schema_push( array( '@type' => 'FAQPage', 'mainEntity' => $ents ) ); }
	}
}
