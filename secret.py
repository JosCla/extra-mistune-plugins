__all__ = ['secret']

SECRET_PATTERN = r'~secret\((?P<secret_text>[\s\S]+?)~,~(?P<secret_title>[\s\S]+?)\)~'
# ~secret\(                     open secret
# (?P<secret_text>[\s\S]+?)     secret render text
# ~,~                           double-tilde splitter
# (?P<secret_title>[\s\S]+?)    secret title text
# \)~                           close secret

def parse_inline_secret(inline, m, state):
    text = m.group('secret_text')
    title = m.group('secret_title')
    state.append_token({
        'type': 'inline_secret',
        'raw': text,
        'attrs': {
            'title': title
        }
    })
    return m.end()

def render_inline_secret(renderer, text, title):
    return '<span class="hidden-footnote" title="' + title + '">' + text + '</span>'

def secret(md):
    """
    A mistune plugin to support secrets.

    .. secret-inline:: text

        Inline secrets are constructed as such:

        ~secret(a~,~b)~

        This will display 'a', with a hover title of 'b'. Perfect for putting
        some sneaky commentary!
    """

    md.inline.register('inline_secret', SECRET_PATTERN, parse_inline_secret, before='link')
    if md.renderer and md.renderer.NAME == 'html':
        md.renderer.register('inline_secret', render_inline_secret)
