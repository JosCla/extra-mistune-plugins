from ..helpers import LINK_LABEL

__all__ = ['figure']

FIGURE_PATTERN = (
    r'^~fig\('
    r'(?P<fig_class>[^\s]+?)?[\s]*\n'           # figure class
    r'(?P<fig_ident>' + LINK_LABEL + r'?)\n'    # figure identifier
    r'(?P<fig_img>[\s\S]+?)\n'                  # figure image
    r'(?P<fig_caption>[\s\S]+?)\n'              # figure caption
    r'\)~[\s]*$'
)

SIMPLE_FIGURE_PATTERN = (
    r'^~simplefig\('
    r'(?P<simplefig_class>[^\s]+?)?[\s]*\n'     # figure class
    r'(?P<simplefig_img>[\s\S]+?)\n'            # figure image
    r'\)~[\s]*$'
)

FIGURE_REF_PATTERN = (
    r'~fref\('
    r'(?P<fig_ident>' + LINK_LABEL + r'?)'  # figure identifier
    r'\)'
)

def get_ident_index(ident, state):
    figidentmap = state.env.get('figidentmap')
    ident = ident.strip()

    if not figidentmap:
        figidentmap = {}
    if not ident in figidentmap:
        nextkey = len(figidentmap.keys()) + 1
        figidentmap[ident] = nextkey
        state.env['figidentmap'] = figidentmap
    
    return figidentmap.get(ident)

def parse_block_figure(block, m, state):
    ident = m.group('fig_ident')
    img = m.group('fig_img')
    caption = m.group('fig_caption')
    figclass = m.group('fig_class')

    figindex = get_ident_index(ident, state)

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

def parse_block_simplefigure(block, m, state):
    img = m.group('simplefig_img')
    figclass = m.group('simplefig_class')

    state.append_token({
        'type': 'block_simplefigure',
        'children': [
            {'type': 'fig_img', 'text': img},
        ],
        'attrs': {
            'figclass': figclass
        }
    })
    return m.end() + 1

def parse_inline_figure_ref(inline, m, state):
    ident = m.group('fig_ident')
    figindex = get_ident_index(ident, state)

    state.append_token({
        'type': 'inline_figure_ref',
        'attrs': {
            'figindex': figindex
        }
    })

    return m.end()

def render_block_figure(renderer, children, figclass):
    if figclass == None:
        return '<figure>\n' + children + '</figure>\n'
    return '<figure class="figure-' + figclass + '">\n' + children + '</figure>\n'

def render_fig_img(renderer, text):
    return text + '\n'

def render_fig_caption(renderer, text, figindex):
    return '<p>Figure ' + str(figindex) + ': ' + text + '</p>\n'

def render_inline_figure_ref(renderer, figindex):
    return 'Figure ' + str(figindex)

def figure(md):
    """
    A mistune plugin to support figures.

    .. figure-block:: text

        Figure is surrounded by ~fig( and )fig~, and has three lines within:
        identifier, image, and caption.

        ~fig(
        identifier
        ![alt](source title)
        caption
        )~

        Optionally, you can open a figure as:

        ~fig(class

        This will add figure-[class] as a class to the figure.

        When rendering the document, the caption will automatically have
        ascending "Figure #: " prepended.

    .. figure-ref:: text

        To reference a figure in text, use:

        ~fref(identifier)

        The identifier should be the same as the one provided with the figure.

        This will be replaced with "Figure #", with # matching the figure.

    :param md: Markdown instance
    """

    md.block.register('block_figure', FIGURE_PATTERN, parse_block_figure, before='list')
    md.block.register('block_simplefigure', SIMPLE_FIGURE_PATTERN, parse_block_simplefigure, before='list')
    md.inline.register('inline_figure_ref', FIGURE_REF_PATTERN, parse_inline_figure_ref, before='link')
    if md.renderer and md.renderer.NAME == 'html':
        md.renderer.register('block_simplefigure', render_block_figure)
        md.renderer.register('block_figure', render_block_figure)
        md.renderer.register('fig_img', render_fig_img)
        md.renderer.register('fig_caption', render_fig_caption)
        md.renderer.register('inline_figure_ref', render_inline_figure_ref)
