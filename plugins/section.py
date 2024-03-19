__all__ = ['section']

SECTION_START_PATTERN = r'^~sec$'
SECTION_END_PATTERN = r'^sec~$'

def parse_inline_section_start(inline, m, state):
    state.append_token({
        'type': 'inline_section_start'
    })

    return m.end()

def parse_inline_section_end(inline, m, state):
    state.append_token({
        'type': 'inline_section_end'
    })

    return m.end()

def render_inline_section_start(renderer):
    return '<section>\n'

def render_inline_section_end(renderer):
    return '</section>\n'

def section(md):
    """
    A mistune plugin to support sections.

    .. inline-section-start:: text
        ~sec

    .. inline-section-end:: text
        sec~
    """

    md.inline.register('inline_section_start', SECTION_START_PATTERN, parse_inline_section_start, before='link')
    md.inline.register('inline_section_end', SECTION_END_PATTERN, parse_inline_section_end, before='link')
    if md.renderer and md.renderer.NAME == 'html':
        md.renderer.register('inline_section_start', render_inline_section_start)
        md.renderer.register('inline_section_end', render_inline_section_end)
