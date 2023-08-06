Summary
-------

Exporting prometheus metrics.

This cube provides a pyramid tween that will, when active, collect the metrics
configured in the settings pyramid.ini and expose them on route `/metrics`.

Configuration
-------------

Include the metrics you want in pyramid.ini:

```
prometheus.pyramid.http_requests = True
prometheus.pyramid.current_requests = True
prometheus.pyramid.slow_routes = True
prometheus.pyramid.time_routes = True
prometheus.pyramid.count_routes = True

prometheus.cubicweb.sql.time = Histogram
prometheus.cubicweb.rql.time = Histogram
...
```

