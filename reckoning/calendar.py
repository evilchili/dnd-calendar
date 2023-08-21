"""
A Telisaran calendaring tool.
"""
from . import telisaran

from rich import print
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel


class TelisaranCalendar:
    """
    The Telisaran Calendar

    Syfdag kindle fate’s first light
    Mimdag have a secret might
    Wodag have the strength to fight
    Thordag curse the wrong, avenge the right
    Freydag love fair beauty’s sight

        – Dwarven nursery rhyme
    """

    def __init__(self, today=None, start=None, end=None):

        self.today = today
        if not self.today:
            self.today = telisaran.today

        self._end = end or self.today

        if start:
            self._start = start
        else:
            self._start = telisaran.datetime(
                year=self._end.year.year,
                season=self._end.season.season_of_year,
                day=1
            )

    def _season(self, season, long=False):
        if long:
            headers = season.day_names
            title = f"Season of the {season.name}, Year {season.year}"
        else:
            headers = [n[0:2] for n in season.day_names]
            title = season.name.upper()
        table = Table(*headers, title=title)
        row = []
        for day in season.days:
            if season == self.today.season and day.day_of_season == self.today.day.number:
                row.append(f"[bold]{day.day_of_season:02d}[/bold]")
            else:
                row.append(f"{day.day_of_season:02d}")
            if day.day_of_span == telisaran.Span.length_in_days:
                table.add_row(*row)
                row = []
        return table

    @property
    def season(self):
        return self._season(self._start.season, long=True)

    @property
    def calendar(self):
        return Panel(Columns(
            [self._season(season) for season in telisaran.today.year.seasons],
            equal=True,
            expand=True,
        ), title="The Telisaran Calendar", highlight=True, width=120)

    @property
    def yesterday(self):
        try:
            return self.today - telisaran.Day.length_in_seconds
        except telisaran.InvalidDayError:
            return "Mortals cannot go back before the beginning of time."

    @property
    def tomorrow(self):
        return self.today + telisaran.Day.length_in_seconds

    def __repr__(self):
        return "The Telisaran Calendar"


def main():
    print(TelisaranCalendar().calendar)
    print(TelisaranCalendar().season)


if __name__ == '__main__':
    main()
