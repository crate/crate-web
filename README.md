# crate-web

**Crate.IO Website**

[https://crate.io](https://crate.io)

This is the developement setup for the crate.io website.
It uses the static website generator tool [Cactus](https://github.com/koenbok/Cactus)
to generate HTML pages.

## Development Setup

    $ git clone git@github.com:crate/crate-web.git
    $ cd crate-web
    $ git submodule init
    $ git submodule update

The dev environment requires Python 2.7 to be installed.

    $ python2.7 bootstrap.py
    $ bin/buildout -N

Select an environment:

    $ bin/py src/web/env.py local > crate/config.json

or simpler:

    $ bin/env local

To start the development server:

    $ bin/serve

By default Cactus serves the site on port `8000`.
You can specify a specific port with the `--port` argument:

    $ bin/serve --port 8888

### Convert Wordpress content to Markdown

You'll need to run buildout with a dev configuration:

    $ bin/buildout -Nvc buildout-dev.cfg

To convert the WP dump (.xml) to Markdown files we use
[wp2md](https://github.com/dreikanter/wp2md).

First, export WordPress data to XML file (Tools -> Export -> All content),
then run:

    $ bin/wp2md -d out data/crate.wordpress.yyyy-mm-dd.xml

Move the posts into the blog folder
and rename from .md to .html

    $ mv out/posts/* crate/pages/blog/
    $ cd crate/pages/blog/
    $ for fn in *.md; do mv $fn ${fn//.md/.html}; done
    $ for fn in *.html; do mv $fn "${fn//#[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-/}"; done

## Manage

All pages are located in `./crate/pages` and respective subfolders.

Blog posts are located in `./crate/pages/blog`.


## Deployment

### Deploy Staging

Simply run the [deploy_web-staging](https://jenkins.crate.io/job/deploy_web-staging/)
job on Jenkins.

Site will be served without caching on <https://staging.crate.io>.

### Deploying to Amazon

To deploy to S3 run

    $ cd crate-web/crate
    $ ../bin/cactus deploy

The first time you run this command it will ask for
 - The bucket: crate-web
 - Your AWS access key: https://console.aws.amazon.com/iam/home?#users
 - Your AWS access key password: https://console.aws.amazon.com/iam/home?#users

### Deploying to Google Cloud Storage

*requirments*
- Install google-api-python-client
- Install httplib2
- Modify upstream/cactus/deployment/gcs/engine:41
    - Old:  "service = apiclient.discovery.build('storage', 'v1beta2', http=http_client)"
    - New: "service = apiclient.discovery.build('storage', 'v1', http=http_client)"


Modify the config.json to include:

    $ "gcs-bucket-name": "crateweb",
    $ "gcs-bucket-website": "Unavailable for GCS",
    $ "provider": "google"

Now you can deploy with:

    $ cd crate-web/crate
    $ ../bin/cactus deploy

The first time you run this command Google will verify the account and you have to copy and paste a code from your browser into your terminal.
