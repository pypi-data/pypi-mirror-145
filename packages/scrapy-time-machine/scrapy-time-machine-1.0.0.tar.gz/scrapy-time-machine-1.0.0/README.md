# scrapy-time-machine

Run your spider with a previously crawled request chain.

## Why?

Lets say your spider crawls some page everyday and after some time you notice that an important information was added and you want to start saving it.

You may modify your spider and extract this information from now on, but what if you want the historical value of this data, since it was first introduced to the site?

With this extension you can save a snapshot of the site at every run to be used in the future (as long as you don't change the request chain).

## Sample project

There is a sample Scrapy project available at the [examples](examples/project/) directory.
