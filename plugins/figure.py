__all__ = ['figure']

FIGURE_PATTERN = r'^~fig\((?P<fig_class>[^\s]+?)?[\s]*\n(?P<fig_img>[\s\S]+?)\n(?P<fig_caption>[\s\S]+?)\n\)~[\s]*$'
# ^~fig\(                       open figure. must be at start of line
# (?P<fig_class>[^\s]+?)?       class (final ? makes it optional)
# [\s]*\n                      look past spaces to newline
# (?P<fig_img>[\s\S]+?)\n       first line within is image
# (?P<fig_caption>[\s\S]+?)\n   second line within is caption
# \)~                           close figure
# [\s]*$                       look past spaces to newline

def parse_block_figure(block, m, state):
    img = m.group('fig_img')
    caption = m.group('fig_caption')
    figclass = m.group('fig_class')

    figindex = state.env.get('nextfigindex')
    if not figindex:
        figindex = 1
    state.env['nextfigindex'] = figindex + 1

    state.append_token({
        'type': 'block_figure',
        'children': [
            {'type': 'fig_img', 'text': img},
            {
                'type': 'fig_caption',
                'text': caption,
                'attrs': {
                    'figindex': figindex
                }
            }
        ],
        'attrs': {
            'figclass': figclass
        }
    })
    return m.end() + 1

def render_block_figure(renderer, children, figclass):
    if figclass == None:
        return '<figure>' + children + '</figure>'
    return '<figure class="figure-' + figclass + '">' + children + '</figure>'

def render_fig_img(renderer, text):
    return text

def render_fig_caption(renderer, text, figindex):
    return '<p>Figure ' + str(figindex) + ': ' + text + '</p>'

def figure(md):
    """
    A mistune plugin to support figures.

    .. figure-block:: text

        Figure is surrounded by ~fig( and )fig~, and has two lines within:
        image, and caption.

        ~fig(
        ![alt](source title)
        caption
        )~

        Optionally, you can open a figure as:

        ~fig(class

        This will add figure-[class] as a class to the figure.

    :param md: Markdown instance
    """

    md.block.register('block_figure', FIGURE_PATTERN, parse_block_figure, before='list')
    if md.renderer and md.renderer.NAME == 'html':
        md.renderer.register('block_figure', render_block_figure)
        md.renderer.register('fig_img', render_fig_img)
        md.renderer.register('fig_caption', render_fig_caption)
