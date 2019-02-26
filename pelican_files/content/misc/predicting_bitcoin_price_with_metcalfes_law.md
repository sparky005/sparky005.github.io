Title: Now with more HTTPS!
Date: 2018-08-02
Modified: 2018-08-02
Authors: Adil Sadik
Tags: misc

In light of [Chrome's recent push to mark all HTTP pages insecure](https://www.theregister.co.uk/2018/02/08/google_chrome_http_shame/) (as well as some admonishment from a buddy at work) this site now enforces HTTPS. Github pages added support for [HTTPS on custom domains in May](https://blog.github.com/2018-05-01-github-pages-custom-domains-https/), so the only outstanding issue was to have [Pelican](https://github.com/getpelican/pelican) generate an HTTPS-only version of the site (to prevent mixed content.)

Turns out, doing that is really easy. All you have to do is change your SITEURL from this
```
 SITEURL = 'http://mysite.com'
```
to this
```
 SITEURL = 'https://mysite.com'
```

Yup. That *s* is all it takes. Regenerate, push, and you're good to go!
