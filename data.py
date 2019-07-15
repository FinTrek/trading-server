from event import MarketEvent
from datetime import date
import datetime
import calendar


class Datahandler:
    """
    Datahandler wraps exchange data and locally stored data with Market
    events and adds it to the event queue as each timeframe period elapses.

    Market events are created from either live or stored data (depending on
    if in backtesting or in live trading modes) and pushed to the event queue
    for the Strategy object to consume.
    """

    def __init__(self, exchanges, events, logger):
        self.exchanges = exchanges
        self.events = events
        self.logger = logger

    exchanges = []
    events = object
    logger = object
    live_trading = False

    def update_bars(self):
        """
        Pushes all new market events into the event queue

        """
        bars = []

        if self.live_trading:
            bars = self.get_new_bars()

        elif not self.live_trading:
            bars = self.get_historic_bars()

        for bar in bars:
            self.events.put(bar)

    def get_new_bars(self):
        """
        Return a list of market events containing new bars for all watched
        symbols from all exchanges for the just-elapsed time period.
        """
        new_bars = []

        for exchange in self.exchanges:
            for instrument in exchange.get_instruments():
                for timeframe in self.get_timeframes():
                    new_bars.append(
                        MarketEvent(
                            instrument,
                            exchange.get_last_bar(
                                timeframe, instrument),
                            exchange.get_name()))
        return new_bars

    def get_historic_bars(self):
        """
        Create market events containing "new" historic 1 min bars for all
        watched symbols
        """
        historic_bars = []

        return historic_bars

    def set_live_trading(self, live_trading):
        """Set true or false live execution flag"""

        self.set_live_trading = live_trading

    def get_timeframes(self):
        """Return a list of timeframes relevant to the just-elapsed time period.
        E.g if time has just struck UTC 10:30am the list will contain "1m",
        "3m", "5m", "m15" and "30m" strings. The first minute of a new day or
        week will add daily/weekly/monthly timeframe string. Timeframes in
        use are 1, 3, 5, 15 and 30 mins, 1, 2, 3, 4, 6, 8 and 12 hours, 1, 2
        and 3 days, weekly and monthly."""

        timestamp = datetime.datetime.utcnow()
        timeframes = ["1m"]

        # 3 minute bars
        for x in range(0, 20):
            val = x * 3
            if timestamp.minute == val:
                timeframes.append("3m")

        # 5 minute bars
        for x in range(0, 12):
            val = x * 5
            if timestamp.minute == val:
                timeframes.append("5m")

        # 15 minute bars
        for x in range(0, 4):
            val = x * 15
            if timestamp.minute == val:
                timeframes.append("15m")

        # 30 minute bars
        for x in range(0, 2):
            val = x * 30
            if timestamp.minute == val:
                timeframes.append("30m")

        # 1h hour bars
        if timestamp.minute == 0:
            timeframes.append("1h")

        # 2 hour bars
        if timestamp.minute == 0 & timestamp.hour % 2 == 0:
            timeframes.append("2h")

        # 3 hour bars
        if timestamp.minute == 0 & timestamp.hour % 3 == 0:
            timeframes.append("3h")

        # 4 hour bars
        if timestamp.minute == 0 & timestamp.hour % 4 == 0:
            timeframes.append("4h")

        # 6 hour bars
        if timestamp.minute == 0 & timestamp.hour % 6 == 0:
            timeframes.append("6h")

        # 8 hour bars
        if timestamp.minute == 0 & timestamp.hour % 8 == 0:
            timeframes.append("8h")

        # 12 hour bars
        if timestamp.minute == 0 & timestamp.hour % 12 == 0:
            timeframes.append("12h")

        # 1 day bars
        if timestamp.minute == 0 & timestamp.hour == 0:
            timeframes.append("1d")

        # 2 day bars
        if (
            timestamp.minute == 0 & timestamp.hour == 0 &
                timestamp.day % 2 == 0):
                    timeframes.append("2d")

        # 3 day bars
        if (
            timestamp.minute == 0 & timestamp.hour == 0 &
                timestamp.day % 3 == 0):
                    timeframes.append("3d")

        # weekly bars
        if (
            timestamp.minute == 0 & timestamp.hour == 0 &
                calendar.day_name[date.today().weekday()] == "Monday"):
                    timeframes.append("1w")

        return timeframes