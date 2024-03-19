__all__ = ['secret']

SECRET_PATTERN = (
    r'~secret\('
    r'(?P<secret_text>[\s\S]+?)'    # secret render text
    r'~,~'
    r'(?P<secret_title>[\s\S]+?)'   # secret hover text
    r'\)~'
)

NOTE_PATTERN = (
    r'~note\('
    r'(?P<note_text>[\s\S]+?)'  # render text
    r'~,~'
    r'(?P<note_title>[\s\S]+?)' # hover text
    r'\)~'
)

def parse_inline_note(inline, m, state):
    text = m.group('note_text')
    title = m.group('note_title')

    parse_inline_generalnote(inline, state, text, title, False)

    return m.end()

def parse_inline_secret(inline, m, state):
    text = m.group('secret_text')
    title = m.group('secret_title')

    parse_inline_generalnote(inline, state, text, title, True)

    return m.end()

def parse_inline_generalnote(inline, state, text, title, isHidden):
    new_state = state.copy()
    new_state.src = text
    children = inline.render(new_state)

    state.append_token({
        'type': 'inline_note',
        'children': children,
        'attrs': {
            'title': title,
            'isHidden': isHidden
        }
    })

def render_inline_generalnote(renderer, children, title, isHidden):
    if isHidden:
        return '<span class="hidden-note" title="' + title + '">' + children + '</span>'
    else:
        return '<span class="note" title="' + title + '">' + children + '</span>'

def secret(md):
    """
    A mistune plugin to support secrets.

    .. secret-inline:: text

        Inline secrets are constructed as such:

        ~secret(a~,~b)~

        This will display 'a', with a hover title of 'b'. Perfect for putting
        some sneaky commentary!

    .. note-inline:: text

        Inline notes are constructed as such:

        ~note(a~,~b)~

        It's the same as the secret, but will be given a different class.
    """

    md.inline.register('inline_note', NOTE_PATTERN, parse_inline_note, before='link')
    md.inline.register('inline_secret', SECRET_PATTERN, parse_inline_secret, before='link')
    if md.renderer and md.renderer.NAME == 'html':
        md.renderer.register('inline_note', render_inline_generalnote)
