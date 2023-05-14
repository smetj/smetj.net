Title: Diagnostics-TK Part 1: Running diagnostic checks during incidents
Date: 2023-05-07 10:20
Modified: 2023-05-07 10:20
category: technology
Tags: observability, sre, diagnostics-tk
Slug: diagnostics-tk-part-1-running-diagnostic-checks-during-incidents
Authors: Jelle Smet

![](images/diagnostics-tk-part-1-running-diagnostic-checks-during-incidents-1.png)

# Introduction

During incidents triggered by alerting on black box monitors or *symptomatic*
metrics such as RED metrics[^1], an interesting behavior often emerges. The
responding engineers start to execute various diagnostic checks (aka
troubleshooting) to get an understanding of what exactly is happening.

There might be various reason for that but generally it boils down to
the following:

  - The observability stack doesn't contain the required data to convey
    insight into the state of all the **involved parts** hence validation
    tests need to be executed manually.
  - The observability stack contains the necessary data but it **requires
    interpretation** and therefore subject matter expertise to conclude on the
    state of some part.

Depending on the complexity of the service and the number of teams involved,
this can cause a long period of uncertainty prior to getting a grip on the
incident at hand. It impacts Mean Time To Recovery (MTTR) and it's not a
pattern which allows for iterative improvement.

## Diagnostic tests

Instead of executing these diagnostic tests manually, how can we implement
them into a solution which allows us to start the incident as well informed as
possible?

Having a list of diagnostic checks available to execute during an incident is
**always** valuable:

- On failure they point into the right direction or the root cause.
- On success they allow to concentrate efforts elsewhere.

In this article we will explore using
[Diagnostics-TK](https://github.com/smetj/diagnostics-tk) to provide answers
to the following questions:

- How can we make tests re-usable?
- How can we logically group tests together to represent larger concepts?
- How can we gradually extend these diagnostic tests and include lessons
  learned from the past?
- How can we present these checks as simple questions and answers which are
  easy to understand for everyone.
- How can we set the bar as low as possible to add new tests?
- How can we democratize access?

# Diagnostics-TK

[Diagnostics-TK](https://github.com/smetj/diagnostics-tk) is a simple,
lightweight test runner written in Python. Defining tests is done in Python
itself and not through a configuration format such as YAML or JSON on purpose.
Instead, it takes advantage of Python's properties as a language to compose
and organize the tests whilst the code remains simple enough to be understood
by everyone.

## Re-usable diagnostics tests

Diagnostics-TK expects tests defined as class methods prefixed with
`test_`[^2]. Python classes are used as a container to logically group tests
together and make them re-usable. How to group your tests together into
something which makes sense for your organization is an exercise left up to
the reader.

Let's assume we have a service called `MyCompanyService` which relies on the
availability of the Twitter and Instagram API. To keep things simple, let's
say network availability and the ability to resolve the hostname is
sufficient.

### Example

```Python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from diagnostics_tk import DiagnosticsRunner
from diagnostics_tk.tools import exec_cli


class MyCompanyServiceInstagram:
    def test_host_up(self):
        """
        """
        result, reason = exec_cli(
            f"nmap -sP api.instagram.com",
            exit_code=0,
            stdout_pattern="Host is up",
        )
        assert result, reason

    def test_hostname_resolvable(self):
        """
        """
        result, reason = exec_cli(
            f"dig api.instagram.com @1.1.1.1",
            stdout_pattern="status: NOERROR",
            timeout=5,
        )
        assert result, reason

class MyCompanyServiceTwitter:
    def test_host_up(self):
        """
        """
        result, reason = exec_cli(
            f"nmap -sP api.twitter.com",
            exit_code=0,
            stdout_pattern="Host is up",
        )
        assert result, reason

    def test_hostname_resolvable(self):
        """
        """
        result, reason = exec_cli(
            f"dig api.twitter.com @1.1.1.1",
            stdout_pattern="status: NOERROR",
            timeout=5,
        )
        assert result, reason


def main():
    with DiagnosticsRunner(name="MyCompanyService", workers=5) as runner:
        runner.register(
            "twitter",
            MyCompanyServiceTwitter(),
        )
        runner.register(
            "instagram",
            MyCompanyServiceInstagram(),
        )


if __name__ == "__main__":
    main()
```

### Result

Assuming the underlying `nmap` and `dig` command is available[^3] and all goes
well, the above code should yield following output when executed:

```text
2023-05-07 12:09:39,651 - DEBUG - Registered `twitter-api` as a test collection.
2023-05-07 12:09:39,652 - DEBUG - Registered `instagram-api` as a test collection.
2023-05-07 12:09:39,690 - INFO - MyCompanyService::MyCompanyServiceTwitter(twitter-api)::test_hostname_resolvable - OK
2023-05-07 12:09:39,690 - INFO - MyCompanyService::MyCompanyServiceInstagram(instagram-api)::test_hostname_resolvable - OK
2023-05-07 12:09:39,706 - INFO - MyCompanyService::MyCompanyServiceInstagram(instagram-api)::test_host_up - OK
2023-05-07 12:09:40,512 - INFO - MyCompanyService::MyCompanyServiceTwitter(twitter-api)::test_host_up - OK
```

Although it serves its purpose, it's not really re-usable code. Each time
there is a new `test_` to be added or a new social media service it would
result in code duplication.

Consider the following improved example:

### Example

```Python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from diagnostics_tk import DiagnosticsRunner
from diagnostics_tk.tools import exec_cli


class SocialMediaAPI:
    def __init__(self, hostname):
        self.hostname = hostname

    def test_host_up(self):
        """ """
        result, reason = exec_cli(
            f"nmap -sP {self.hostname}",
            exit_code=0,
            stdout_pattern="Host is up",
        )
        assert result, reason

    def test_hostname_resolvable(self):
        """ """
        result, reason = exec_cli(
            f"dig {self.hostname} @1.1.1.1",
            stdout_pattern="status: NOERROR",
            timeout=5,
        )
        assert result, reason


def main():
    with DiagnosticsRunner(name="MyCompanyService", workers=5) as runner:
        runner.register(
            "twitter-api",
            SocialMediaAPI(hostname="api.twitter.com"),
        )
        runner.register(
            "instagram-api",
            SocialMediaAPI(hostname="api.instagram.com"),
        )
        runner.register(
            "facebook-api",
            SocialMediaAPI(hostname="api.facebook.com"),
        )


if __name__ == "__main__":
    main()
```

The above example rewrites the individual `MyCompanyServiceTwitter` style
classes into a single generic class `MyCompanyServiceSocialMedia` which
accepts `hostname` as a variable. By using this variable in the various
underlying test cases, we can achieve the same results as our first example by
re-using a single class.  Additionally, as you can see, an social media API
test has been added to `MyCompanyService` named `facebook-api` without much
effort.

We can simplify this example even further by converting the above test class
into a distributable Python module and package[^4] which would make our test
code look even more condense:

### Example

```Python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from diagnostics_tk import DiagnosticsRunner
from mycompany_diagnostic_tests import MyCompanyServiceSocialMedia

def main():
    with DiagnosticsRunner(name="MyCompanyService", workers=5) as runner:
        runner.register(
            "twitter-api",
            MyCompanyServiceSocialMedia(hostname="api.twitter.com"),
        )
        runner.register(
            "instagram-api",
            MyCompanyServiceSocialMedia(hostname="api.instagram.com"),
        )
        runner.register(
            "facebook-api",
            MyCompanyServiceSocialMedia(hostname="api.facebook.com"),
        )

if __name__ == "__main__":
    main()
```

### Results

```text
2023-05-07 12:24:07,902 - DEBUG - Registered `twitter-api` as a test collection.
2023-05-07 12:24:07,903 - DEBUG - Registered `instagram-api` as a test collection.
2023-05-07 12:24:07,903 - DEBUG - Registered `facebook-api` as a test collection.
2023-05-07 12:24:07,943 - INFO - my_infra::MyCompanyServiceSocialMedia(instagram-api)::test_hostname_resolvable - OK
2023-05-07 12:24:07,944 - INFO - my_infra::MyCompanyServiceSocialMedia(twitter-api)::test_hostname_resolvable - OK
2023-05-07 12:24:07,963 - INFO - my_infra::MyCompanyServiceSocialMedia(facebook-api)::test_host_up - OK
2023-05-07 12:24:07,964 - INFO - my_infra::MyCompanyServiceSocialMedia(instagram-api)::test_host_up - OK
2023-05-07 12:24:07,978 - INFO - my_infra::MyCompanyServiceSocialMedia(facebook-api)::test_hostname_resolvable - OK
2023-05-07 12:24:08,761 - INFO - my_infra::MyCompanyServiceSocialMedia(twitter-api)::test_host_up - OK
```

# Final Notes

During incidents people run diagnostic tests for various reasons. Instead of
doing this ad-hoc and manually, the article explores the possibility to use
[Diagnostics-TK](https://github.com/smetj/diagnostics-tk) instead.

We have focused on how to design tests in a *re-usable* fashion by taking
advantage of how we organize code in Python. In a [series of
articles](tag/diagnostics-tk.html) we will focus on further answering the
questions and challenges outlined in the article.

If you have any feedback or suggestions, don't hesitate to get in touch on
[Twitter](https://twitter.com/smetj).

# Footnotes

[^1]: [RED metrics](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/) explained.
[^2]: Python [classes](https://docs.python.org/3/tutorial/classes.html) explained.
[^3]: This example uses `diagnostics_tk.tools.exec_cli` to execute shell
commands but you are not obliged to. You could very well write native Python
instead doing exactly the same thing.
[^4]: Python [modules](https://docs.python.org/3/tutorial/modules.html) and
[packaging](https://packaging.python.org/en/latest/) explained.
