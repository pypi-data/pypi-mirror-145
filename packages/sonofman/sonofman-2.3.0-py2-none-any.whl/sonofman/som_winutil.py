#!/usr/bin/env python3

import textwrap
import sonofman.som_unicurses as u


class WinUtil:
    """
    Windows utils
    Don't change value of variables, use methods to do it
    """
    def __init__(self, win_ref, win_lines, win_cols, win_top_border_lines, win_bottom_border_lines, colors):
        self.win_ref = win_ref
        self.win_lines = win_lines
        self.win_cols = win_cols
        self.win_top_border_lines = win_top_border_lines
        self.win_bottom_border_lines = win_bottom_border_lines
        self.s_line_pos = 0
        self.s_lines_max = 0
        self.s_lst = []
        self.colors = colors

    """
    Get attributes, code color associated to a color key
    """
    def get_color(self, color_key):
        attr = u.A_NORMAL
        code_color = None

        color_item = self.colors[color_key].split("#")
        if len(color_item) == 2:
            attr = color_item[0]
            if len(attr) > 0:
                attr = attr.replace("A_", "u.A_")
                attr = eval(attr)
            else:
                attr = u.A_NORMAL

            code_color = color_item[1]
            if len(code_color) > 0:
                code_color = code_color.replace("COLOR", "")
                code_color = eval("u.color_pair({0})".format(code_color))
            else:
                code_color = None
        return attr, code_color

    def move(self, step):
        """
        param step: +1, -1, 0=set to 0
        :return True: move possible, False: stop refreshing
        """
        if step == 0:
            self.s_line_pos = 0
        else:
            new_line_pos = self.s_line_pos + (step * self.win_lines)
            if new_line_pos > self.s_lines_max:
                return False
            elif new_line_pos < 0:
                self.s_line_pos = 0
            else:
                self.s_line_pos = new_line_pos
        return True

    @staticmethod
    def wrap_string(string, width):
        # noinspection PyBroadException
        try:
            wrapper = textwrap.TextWrapper(width=width-1, replace_whitespace=False)
            lst_wrapped = []
            for r in string:
                ref = r[1]
                lst = r[0].replace("§", "\n").splitlines()
                for i in lst:
                    if i == "":
                        jitem = ["", ""]
                        lst_wrapped.append(jitem)
                    else:
                        lf = wrapper.wrap(i)
                        bbname = ""
                        for j in lf:
                            jitem = [j, ref]
                            if ref == ['', '']:
                                if len(j) >= 2:
                                    new_bbname = j[0:2]
                                    if new_bbname in ('k|', 'l|', 'v|', 'd|', 'a|', 'o|', 's|', '2|'):
                                        bbname = new_bbname
                                    if bbname in ('k|', 'l|', 'v|', 'd|', 'a|', 'o|', 's|', '2|') and not(jitem[0].startswith(bbname)):
                                        jitem[0] = "{0}{1}".format(bbname, jitem[0])
                            lst_wrapped.append(jitem)
            return lst_wrapped
        except Exception:
            pass
            # TODO: was here: print_ex(ex)

    def position_in_list_by_cy(self, cy):
        """
        Screen cursor position (cy) of selection is different of real position in list
        """
        return self.s_line_pos + cy - self.win_top_border_lines

    def fill_window(self, string, from_line_nr):
        # noinspection PyBroadException
        try:
            if string is not None:
                self.s_lst = self.wrap_string(string, self.win_cols)
                self.s_lines_max = len(self.s_lst) - 1
                self.s_line_pos = from_line_nr

            if len(self.s_lst) == 0:
                return

            u.wclear(self.win_ref)
            x = y = 0
            to_line_nr = from_line_nr + self.win_lines
            # use_attr = True     # was: if len(_tbbName) > 1 else False
            for i in range(from_line_nr, to_line_nr):
                text = self.s_lst[i][0]
                ref = self.s_lst[i][1]
                bbname = ref[1] if len(ref) == 2 else ""
                if bbname == "":
                    if text.startswith("k|"):
                        bbname = "k"
                        text = text[2:]
                    elif text.startswith("v|"):
                        bbname = "v"
                        text = text[2:]
                    elif text.startswith("l|"):
                        bbname = "l"
                        text = text[2:]
                    elif text.startswith("d|"):
                        bbname = "d"
                        text = text[2:]
                    elif text.startswith("a|"):
                        bbname = "a"
                        text = text[2:]
                    elif text.startswith("o|"):
                        bbname = "o"
                        text = text[2:]
                    elif text.startswith("s|"):
                        bbname = "s"
                        text = text[2:]
                    elif text.startswith("2|"):
                        bbname = "2"
                        text = text[2:]
                elif text.startswith("{0}|".format(bbname)):
                    text = text[2:]

                attr = u.A_NORMAL
                code_color = None
                if len(text) > 0:
                    # noinspection PyBroadException
                    try:
                        if bbname in ("k", "v", "l", "d", "a", "o", "s", "2"):
                            attr, code_color = self.get_color(bbname)

                        if text[0] == "#":
                            text = text[1:]
                            attr = u.A_REVERSE
                        elif text[0:4] == "_HB_":
                            text = text[4:]
                            attr = u.A_UNDERLINE + u.A_BOLD
                        elif text[0:2] == "__":
                            attr = u.A_BOLD
                        elif text[0:2] == "~~":
                            self.s_lst[i] = "-" * self.win_cols
                            text = self.s_lst[i]
                    except Exception:
                        attr = u.A_NORMAL

                if not(code_color is None):
                    u.mvwaddstr(self.win_ref, y, x, text, attr + code_color)
                else:
                    u.mvwaddstr(self.win_ref, y, x, text, attr)
                y += 1

            u.wrefresh(self.win_ref)
        except Exception:
            pass
            # TODO: print_ex(ex) ?
