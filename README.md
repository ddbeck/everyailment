# Every Ailment

Every Ailment is a bot that's tweeting each and every code of the FY2016 release of the [International Classification of Diseases, Tenth Revision, Clinical Modification](http://www.cdc.gov/nchs/icd/icd10cm.htm) (ICD-10-CM). There are approximately 43,000 codes known to Every Ailment; tweeting twice an hour, it will take about two and half years to complete its task.

## Accolades

Every Ailment [was named the eleventh best bot of 2015](http://qz.com/572763/the-best-twitter-bots-of-2015/) by Quartz.


## Installation

Every Ailment requires Python 3.5. To install Every Ailment:

1. Run `pip install https://github.com/ddbeck/everyailment`.

2. Create [a Twitter API app](https://apps.twitter.com/) and put your API keys in a JSON file, like this:

    ```
    {
        "consumer_key": "consumer (api) key goes here",
        "consumer_secret": "consumer (api) secret goes here",
        "access_key": "",
        "access_secret": ""
    }
    ```

3. Run `everyailment --keyfile <path_to_keyfile> --request-access`, where `<path_to_keyfile>` is the path to the file you created in the previous step, and follow the instructions shown.

4. Create an index file containing this JSON object: `{"index": -1}`.


## Usage

To tweet with Every Ailment, run `everyailment --post --keyfile <path_to_keyfile> <index_file_path>` (optionally, you can see what the next tweet is without actually posting to Twitter by omitting the `--post` option).


## About the ICD-10-CM

The ICD codes, created by the World Health Organization (WHO), are used around the world to categorize diseases, injuries, and other medical conditions. In the United States, the codes also used for medical billing, so the Centers for Disease Control (CDC) publishes its own version of the codes, commonly known as the ICD-10-CM. These codes, alone or in combination with other codes, are meant to capture every possible condition that a patient might present before a medical worker.


## Author and Acknowledgements

Every Ailment was made by [Daniel Beck](http://twitter.com/ddbeck). Every Ailment is inspired by [@everyword](https://twitter.com/everyword) by Allison Parrish. And shout out to everyone working in the medical profession because y'all deal with some weird stuff.


## License and Copyright

You are free to use, copy, modify, and distribute this software under the terms of an MIT license. See the `LICENSE` file for details.

The status of the list of codes is a bit murkier, however. [According to the WHO (PDF)](http://www.who.int/about/licensing/Internettext_FAQ.pdf):

> The governments of certain countries have developed clinical modifications however, WHO is not responsible for these modifications. The authorities concerned should be contacted to obtain a license for the use of the modifications

Unfortunately, the ICD-10-CM provided by the CDC (`ailmentsGenerator/data/tabular.xml`), does not have explicit licensing information, but other publications of the United States government are in the public domain, so I assume that you and I are free to use the list of codes without restriction.
