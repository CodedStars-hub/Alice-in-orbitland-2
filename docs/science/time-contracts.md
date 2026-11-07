# UTC time contracts

`UtcTimestamp(value, scale)` requires a timezone-aware Python datetime and `TimeScale.UTC`. Offset-aware inputs normalize to UTC; naive datetimes and ET scale labels are rejected. `UtcTimestamp.parse(text)` accepts the supported ISO 8601 subset `YYYY-MM-DDTHH:MM:SS[.ffffff](Z|±HH:MM)`, with at most six fractional digits and a valid numeric offset. Unknown offset `-00:00`, dates without a timestamp, leap-second labels (`:60`), invalid dates and excess precision are rejected rather than truncated. Serialization uses UTC ISO text ending in `Z`, including microseconds when present.

```json
{"value":"2026-01-01T00:00:00Z","scale":"UTC"}
```

`UtcInterval(start, end)` requires two timestamp records with start strictly before end after normalization. It represents a half-open requested interval [start, end); no timeline, duration integration or event boundary calculation is implemented.

UTC is not SPICE ephemeris time (ET). Python datetime cannot represent leap seconds, and datetime subtraction must not be used here as a leap-second-aware elapsed-time model. No elapsed SI duration or UTC/ET conversion is exposed. Future adapters must use validated SPICE mechanisms and compatible leap-second kernels. See [NAIF time subsystem](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/time.html), accessed 2026-11-07: toolkit ET uses TDB and UTC conversions require their stated time/kernel handling.

The offset normalization here is civil-time representation only. It does not establish astronomical time accuracy, leap-second coverage, or scientific temporal coverage. Out-of-range UTC normalization fails explicitly. See [ADR 0002](../adr/0002-scientific-contracts.md) and the [validation strategy](../validation/strategy.md).
