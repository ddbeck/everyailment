"""Tweet every ICD-10-CM code."""

# test index 4744

import json
import os
import sys
import textwrap
import time

import click
import twython

DEFAULT_CODES_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'data/ailments.json')


def make_tweets(index, codes):
    """Generate tweets from the next code."""
    next_code = codes['codes'][index + 1]
    tweet = '{code} {desc}'.format(**next_code)

    if len(tweet) < 141:
        return [tweet]
    else:
        wrapped = textwrap.wrap(tweet, 100)
        return ['{}… (1/2)'.format(wrapped[0]),
                '…{} (2/2)'.format(wrapped[1])]


def increment_index(indexfile):
    """Increment the index file."""
    indexfile.seek(0)
    index = json.load(indexfile)['index']
    indexfile.seek(0)
    json.dump({'index': index + 1}, indexfile)
    indexfile.truncate()
    indexfile.seek(0)


def oauth_dance(ctx, param, value):
    """Set up OAuth."""
    if not value or ctx.resilient_parsing:
        return

    # set up
    try:
        auth_info = ctx.params['auth_info']
    except KeyError:
        click.echo("Error: --keyfile option is required to request access")
        ctx.exit(1)

    pre_auth_twitter = twython.Twython(auth_info['consumer_key'],
                                       auth_info['consumer_secret'])
    twitter_auth = pre_auth_twitter.get_authentication_tokens()

    # prompt user to go to web and get verifier code
    click.echo("Open: {}".format(twitter_auth['auth_url']))
    verifier = click.prompt("Please enter the code provided by Twitter")

    post_auth_twitter = twython.Twython(auth_info['consumer_key'],
                                        auth_info['consumer_secret'],
                                        twitter_auth['oauth_token'],
                                        twitter_auth['oauth_token_secret'])
    access_info = post_auth_twitter.get_authorized_tokens(verifier)

    click.echo("")
    click.echo("Access key: {}".format(access_info['oauth_token']))
    click.echo("Access secret: {}".format(access_info['oauth_token_secret']))

    new_keyfile_data = dict(auth_info)
    new_keyfile_data['access_key'] = access_info['oauth_token']
    new_keyfile_data['access_secret'] = access_info['oauth_token_secret']

    click.echo("Save this JSON object to your keyfile:")
    click.echo("")
    click.echo(json.dumps(new_keyfile_data))

    ctx.exit()


def load_json(ctx, param, value):
    if value is not None:
        try:
            obj = json.load(value)
        except:
            click.echo('{value} is not a valid JSON file!'.format(value))
            raise
        return obj
    else:
        return value


@click.command(help=__doc__)
@click.argument('indexfile',
                'index_info',
                type=click.File('r+'),
                envvar='EVERYAILMENT_INDEX_FILE',
                required=True)
@click.option('--keyfile',
              'auth_info',
              type=click.File('r'),
              envvar='EVERYAILMENT_KEYFILE',
              required=True,
              callback=load_json,
              help='JSON file with Twitter keys and secrets.')
@click.option('--request-access',
              default=False,
              is_flag=True,
              callback=oauth_dance,
              expose_value=False,
              help='Request access key and secret.')
@click.option('--post/--no-post',
              default=False)
def cli(indexfile, auth_info, post):
    twitter = twython.Twython(auth_info['consumer_key'],
                              auth_info['consumer_secret'],
                              auth_info['access_key'],
                              auth_info['access_secret'])

    index = json.load(indexfile)['index']
    with open(DEFAULT_CODES_FILE) as fp:
        codes = json.load(fp)

    tweets = make_tweets(index, codes)
    prev_status = None
    try:
        for tweet in tweets:
            if post:
                result = twitter.update_status(
                    status=tweet,
                    in_reply_to_status_id=prev_status)
                prev_status = result['id_str']
            else:
                click.echo(tweet)
            time.sleep(2)
        if post:
            increment_index(indexfile)
    except:
        print("Attempted to tweet: {}".format(tweets), file=sys.stderr)
        raise


if __name__ == '__main__':
    cli()
