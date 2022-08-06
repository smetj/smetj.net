Title: Understanding your metrics with Xpectd.
Date: 2022-02-10 20:00
Author: smetj
Category: observability
Tags: xpectd, prometheus, traefik, metrics, observability
Slug: understanding_your_metrics_with_xpectd
Status: Hidden

![](images/understanding-metrics-with-Xpectd.png)

When we create queries and look at the resulting graphs in front of us, how do
we know that what we're seeing is actually correct? We hardly ever question
and validate the outcome.  It might be because we are confident in the tooling
so we assume its alright or perhaps because there simply is not a second
source at hand to validate the results against. In this article we cover how
to run the [Xpectd](https://github.com/smetj/xpectd) web service to generate
responses with predefined properties to create a point of reference to
validate the graphed results against.

## A service to simulate various response behavior scenarios

[Xpectd](https://github.com/smetj/xpectd) is a web service which behaves
according to a [predefined test
plan](https://github.com/smetj/Xpectd/blob/main/test_plan.yml).  One can,
among other things, define a certain endpoint to respond between a minimum and
maximum response time and define that n% of all requests must return a certain
response code. By doing so we are creating a point of reference to which we
can compare and validate the graphed results against.

## Scenario

!!! note "ᕙ(⇀‸↼‶)ᕗ"
    In this scenario Xpectd runs behind [Traefik](https://traefik.io/) and
    Traefik's metrics are scraped by [Prometheus](https://prometheus.io/). How
    to run Xpectd in some container scheduler and wire all these components
    together is out of scope of this article.

Let's setup a scenario in which we will graph the response times of our Xpectd
service by using one of Traefik's metrics named
`traefik_service_request_duration_seconds_bucket` and see whether the graphed
result meets our expectations.

### Xpectd configuration

Consider following configuration:

```yaml
scenarios:
  - endpoint: hello_world
    response:
      status: 200
      payload: Hello world!
      min_time: 0
      max_time: 0.3
    outage:
      schedule: "*/1 * * * *"
      duration: 0
      response:
        - percentage: 100
          status: 200
          payload: (╯°□°）╯︵ ┻━┻
          min_time: 2
          max_time: 3
```

We can discern the following important values:

- The Xpectd web service serves an endpoint named `/hello_world`.
- During normal operations requests return http-code `200` and response times
  are between `0` and `0.3` seconds. (Zero actually means as fast as possible
  so there will always be some framework overhead to take into account).
- The scheduled outage functionality is disabled by setting `duration` to `0`.
- When the outage scenario is activated, `100%` of all requests return
  http-code `200` with response times between `2` and `3` seconds.

### Creating Requests

Creating client requests could be as simple as:

```bash
while true;do
  curl  -w " - %{http_code} - %{time_total}\n" https://Xpectd/hello_world 2>/dev/null
done
Hello world! - 200 - 0.339863
Hello world! - 200 - 0.192286
Hello world! - 200 - 0.241460
Hello world! - 200 - 0.092470
Hello world! - 200 - 0.165882
... snip ...
```

To enable the outage scenario we can issue the following request:

```bash
curl -XPOST https://Xpectd/hello_world/enable
{"status": "enabled"}
```

After which our client receives following responses:

```bash
Hello world! - 200 - 0.169042
Hello world! - 200 - 0.271554
(╯°□°）╯︵ ┻━┻ - 200 - 2.406939
(╯°□°）╯︵ ┻━┻ - 200 - 2.396655
(╯°□°）╯︵ ┻━┻ - 200 - 2.678476
(╯°□°）╯︵ ┻━┻ - 200 - 2.994971
(╯°□°）╯︵ ┻━┻ - 200 - 2.642465
(╯°□°）╯︵ ┻━┻ - 200 - 2.899254
(╯°□°）╯︵ ┻━┻ - 200 - 2.596094
(╯°□°）╯︵ ┻━┻ - 200 - 2.209844
(╯°□°）╯︵ ┻━┻ - 200 - 2.849323
(╯°□°）╯︵ ┻━┻ - 200 - 2.369084
(╯°□°）╯︵ ┻━┻ - 200 - 2.622051
(╯°□°）╯︵ ┻━┻ - 200 - 2.615794
(╯°□°）╯︵ ┻━┻ - 200 - 2.504859
...snip...
```


### Enter Traefik, Prometheus, histograms and ... buckets

Let's assume we want to graph the request duration of a service in Prometheus
using [Traefik
metrics](https://doc.traefik.io/traefik/v1.7/configuration/metrics/). In order
to graph Xpectd's response times we select the
`traefik_service_request_duration_seconds_bucket` metric to build the
following textbook query [^1]:

```text
histogram_quantile(0.99, sum(rate(traefik_service_request_duration_seconds_bucket{}[1m])) by (le, service))
```

Which would yield (in my case) the following graph during the outage
activation where response times were set between 2 and 3 seconds:

[![](images/understanding-metrics-with-Xpectd-1.png)](images/understanding-metrics-with-Xpectd-1.png)


!!! note "(⊙＿⊙')"

    So ... we can see a P99 of `4.9` ...
    But Xpectd's response times are between `2` and `3` seconds per our configuration?
    Why?

#### Buckets

So you should realize we are dealing with [histogram
metrics](https://prometheus.io/docs/practices/histograms/#histograms-and-summaries)
which, simply said, assigns each single actual response time value to the
nearest **predefined** bucket and increments a counter for said bucket.[^2] If we
take a look at the default buckets defined by
[Traefik](https://doc.traefik.io/traefik/v1.7/configuration/metrics/) we can
see the values are `[0.1,0.3,1.2,5.0]`.

This means that all values higher than `1.2` end up in the `5.0` bucket.
Therefor, since all Xpectd's response times are deliberately configured to land
between `2` and `3` seconds they are all assigned to the `5.0` bucket which at
first glance might be puzzling but is actually correct since it tells us 99%
if all requests are below `4.9` seconds.

## Final words

It's tempting to say the P99 average response time is `4.9` seconds but that
is simply not true. In this case you should rather say 99% of all requests are
below `4.9` seconds but we lack any granularity between `1.2` and `4.9` seconds.

In this article we have seen how to use Xpectd to generate response times

If you have any questions and/or remarks you can reach out to my Twitter
handle [@smet](https://twitter.com/smetj).


## Footnotes

[^1]: [Histogram quantiles](https://prometheus.io/docs/practices/histograms/#quantiles)
[^2]: [Histograms buckets are cumulative](https://www.robustperception.io/why-are-prometheus-histograms-cumulative/)
