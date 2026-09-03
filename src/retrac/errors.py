# Copyright (c) 2026 Martial Systems LLC


class GateError(RuntimeError):
    """Stage hard gate failed."""


class ClaimBanError(GateError):
    """Report text hit a banned claim."""


class FetchError(GateError):
    """IDEM XLSX empty, or a train-era receiver has no coordinates."""


class SplitError(GateError):
    """Confirmation leaked into train or facility set J."""


class FigureCapError(GateError):
    """This tree stops at two figures."""


class ArchiveError(GateError):
    """Live Re-TRAC login used as the science lock."""
