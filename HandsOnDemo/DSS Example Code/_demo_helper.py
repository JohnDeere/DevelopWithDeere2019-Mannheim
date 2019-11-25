# Copyright (c) 2019 Deere & Company
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.


from _common_setup import *

#############################################################################
# HTTPS Request Header constants

DEFAULT_GET_REQUEST_HEADERS = {
    'Accept': 'application/vnd.deere.axiom.v3+json',
}

DEFAULT_GET_IMAGE_HEADERS = {
    'Accept': 'application/vnd.deere.axiom.v3.image+json',
    'Content-Type': 'application/vnd.deere.axiom.v3+json'
}


#############################################################################

class DemoHelper:
    #############################################################################
    def __init__(self):
        # Setup the OAuth session
        self.oauth_session = OAuth1Session(CLIENT_KEY, client_secret=CLIENT_SECRET,
                                           resource_owner_key=OAUTH_TOKEN,
                                           resource_owner_secret=OAUTH_TOKEN_SECRET)
        self.link_dictionary = dict()
        self.logger = logging.getLogger()

    def setup(self):
        # Setup the logger
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
        self.logger.setLevel(logging.INFO)

        # For the purpose of this demo, avoid going through a proxy to avoid authentication requirements
        if 'https_proxy' in os.environ:
            os.environ.pop('https_proxy')

    #############################################################################
    # Get content from URL link
    def get_from_url_link(self, url):
        http_response = self.process_http_oauth_get_request(url, 'Getting content for link provided')
        return http_response.json()

    #############################################################################
    def get_from_url_link_with_image(self, url):
        http_response = self.process_http_oauth_get_request_with_image(url, 'Getting content with image for link '
                                                                            'provided')
        return http_response.json()

    #############################################################################
    # HTTPS GET Request Helper
    def process_http_oauth_get_request(self, url, custom_text, expected_status=200, exit_on_failure=True):
        return self.process_http_request(
            self.oauth_session.get(url, headers=DEFAULT_GET_REQUEST_HEADERS),
            custom_text,
            expected_status,
            exit_on_failure)

    #############################################################################
    def process_http_oauth_get_request_with_image(self, url, custom_text, expected_status=200, exit_on_failure=True):
        return self.process_http_request(
            self.oauth_session.get(url, headers=DEFAULT_GET_IMAGE_HEADERS),
            custom_text,
            expected_status,
            exit_on_failure)

    #############################################################################
    # Generic HTTPS Request Helper
    def process_http_request(self, http_response, custom_text, expected_status, exit_on_failure=True):
        result_string = "{}:{} - {} - {} - {}".format(
            vars(http_response.request)['method'],
            vars(http_response.request)['url'],
            str(http_response.status_code),
            http_response.reason,
            custom_text)

        if expected_status == http_response.status_code:
            log_message = "{} - SUCCESS - {}"
            self.logger.info(log_message)
        else:
            log_message = "{} - ERROR   - {}"
            self.logger.info(log_message)
            if exit_on_failure:
                exit(log_message)

        return http_response

    #############################################################################
