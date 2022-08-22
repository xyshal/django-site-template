django-site-template
====================
This is intended as a starting point for a production-worthy django site.  The idea is that you plop your django site into the appropriate directory, and then `docker-compose up` on some Internet-facing server instance.

The layout of the containers and configuration is an attempt to adhere to webdev best practices which I, as not at all a webdev, am likely failing at in some way or another, but nevertheless includes:

1. An integration test skeleton: this is a separate container that runs a small X server and runs selenium tests against the actual nginx/django site.
2. A unit test skeleton (largely just django)
3. Periodic backups
4. Unprivileged user support
