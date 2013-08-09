# encoding: utf-8
# Copyright 2009, EveryBlock
# This code is released under the GPL.

from django import template
register = template.Library()

try:
    from django.template.defaulttags import verbatim
    # if verbatim is available, we don't need to redeclare them
except ImportError:
    # compatibility with Django < 1.5


    @register.tag(name="verbatim")
    def raw(parser, token):
        # Whatever is between {% verbatim %} and {% endverbatim %}
        # will be preserved as
        # verbatim, unrendered template code.
        text = []
        parse_until = 'endverbatim'
        tag_mapping = {
            template.TOKEN_TEXT: ('', ''),
            template.TOKEN_VAR: ('{{', '}}'),
            template.TOKEN_BLOCK: ('{%', '%}'),
            template.TOKEN_COMMENT: ('{#', '#}'),
        }
        # By the time this template tag is called, the template
        # system has already lexed the template into tokens.
        # Here, we loop over the tokens until
        # {% endverbatim %} and parse them to TextNodes.
        # We have to add the start and
        # end bits (e.g. "{{" for variables) because those 
        # have already been stripped off in a previous
        # part of the template-parsing process.
        while parser.tokens:
            token = parser.next_token()
            if token.token_type == template.TOKEN_BLOCK and \
                    token.contents == parse_until:
                return template.TextNode(u''.join(text))
            start, end = tag_mapping[token.token_type]
            if token.contents.startswith('='):
                text.append(u'%s%s %s' % (start, token.contents, end))
            else:
                text.append(u'%s %s %s' % (start, token.contents, end))
        parser.unclosed_block_tag(parse_until)

