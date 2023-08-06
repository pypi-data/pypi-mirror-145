import re
import markdown as md


RE_ASIDE = re.compile(r'^', flags=re.MULTILINE)


def _repl_aside(match: re.Match):
    pass


def aside(document: str):
    """Notation for asides.
    
    Marquedown:
        ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
        How could I possibly be expected
        to handle school on a day like this?
        ''''''''''''''''''''''''''''''''''''''

        | How could I possibly be expected
        | to handle school on a day like this?

    HTML:
        <aside>

        </aside>
    """