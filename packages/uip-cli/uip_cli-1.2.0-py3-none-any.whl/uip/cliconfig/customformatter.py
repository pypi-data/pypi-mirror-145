import textwrap

import argparse


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    """
    Custom Help Formatter that 

    Parameters
    ----------
    argparse : [type]
        [description]
    """

    def _format_action_invocation(self, action):
        """
        By default, argparse formats argument as:
        -u USERID, --userid USERID

        The changes below will change the format to:
        -u --userid USERID
        """
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s' % option_string)
                parts[-1] += ' %s' % args_string
            return ' '.join(parts)

    def _format_action(self, action):
        """
        By default, argparse only adds a newline for the help
        description after an argument if it goes over a certain 
        character limit. For example:
        -u --userid USERID     username used to login

        will now be formatted as:
        -u --userid USERID
                                username used to login
        """
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2,
                            self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, '', action_width, action_header
            action_header = '%*s%-*s  ' % tup
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup
            indent_first = help_position

        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)
            help_text = self._whitespace_matcher.sub(' ', help_text).strip()
            help_lines = textwrap.wrap(help_text, width=help_width)

            if not action_header.endswith('\n') and action.option_strings:
                # adding ' ' results in a newline
                help_lines.insert(0, ' ')

            parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            for line in help_lines[1:]:
                parts.append('%*s%s\n' % (help_position, '', line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        return self._join_parts(parts)
