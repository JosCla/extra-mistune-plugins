__all__ = ['section']

SECTION_START_PATTERN = r'^~sec$'
SECTION_END_PATTERN = r'^sec~$'

def parse_block_section_start(block, m, state):
    state.append_token({
        'type': 'block_section_start'
    })

    return m.end()

def parse_block_section_end(block, m, state):
    state.append_token({
        'type': 'block_section_end'
    })

    return m.end()

def render_block_section_start(renderer):
    return '<section>\n'

def render_block_section_end(renderer):
    return '</section>\n'

def section(md):
    """
    A mistune plugin to support sections.

    .. block-section-start:: text
        ~sec

    .. block-section-end:: text
        sec~
    """

    md.block.register('block_section_start', SECTION_START_PATTERN, parse_block_section_start, before='list')
    md.block.register('block_section_end', SECTION_END_PATTERN, parse_block_section_end, before='list')
    if md.renderer and md.renderer.NAME == 'html':
        md.renderer.register('block_section_start', render_block_section_start)
        md.renderer.register('block_section_end', render_block_section_end)
