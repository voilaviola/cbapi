import sys
import struct
import socket
import pprint
import optparse 

# in the github repo, cbapi is not in the example directory
sys.path.append('../src/cbapi')

import cbapi 

def build_cli_parser():
    parser = optparse.OptionParser(usage="%prog [options]", description="Get and set Bit9 Platform Server Configuration")

    # for each supported output type, add an option
    #
    parser.add_option("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_option("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_option("-n", "--no-ssl-verify", action="store_false", default=True, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    parser.add_option("-u", "--server-url", action="store", default=None, dest="server_url",
                      help="Specify the URL of the configured Bit9 Platform Server")
    parser.add_option("-s", "--ssl-cert-verify", action="store", default=None, dest="ssl_cert_verify",
                      help="Specify if the SSL certificate of the Bit9 Platform Server should be verified; should be 'True' or 'False'")
    parser.add_option("-w", "--watchlist-enable", action="store", default=None, dest="watchlist_enable",
                      help="Enable export of CB Watchlists to Bit9 Platform Server; should be 'True' or 'False'")
    parser.add_option("-t", "--authtoken", action="store", default=None, dest="auth_token",
                      help="Bit9 Platform Server Auth Token used by CB server to send watchlist hits")
    return parser

def truncate(string, length):
    if len(string) + 2 > length:
        return string[:length] + "..."
    return string

def s2b(s):
    """
    naive string-to-boolean converter helper
    """
    if s.lower() in ["true", "1", "yes", "enabled", "on"]:
        return True
    return False

def main(argv):
    parser = build_cli_parser()
    opts, args = parser.parse_args(argv)
    if not opts.url or not opts.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    # build a cbapi object
    #
    cb = cbapi.CbApi(opts.url, token=opts.token, ssl_verify=opts.ssl_verify)

    # if none of the four "set" parameters are provided,
    # query for the existing Bit9 Platform Server configuration  
    #
    if None == opts.server_url and\
       None == opts.ssl_cert_verify and\
       None == opts.watchlist_enable and\
       None == opts.auth_token:
        config = cb.get_platform_server_config()
        pprint.pprint(config)
        sys.exit(0)

    # here because one or more of the Bit9 Platform Server configuration options is to be set
    # start with an empty dictionary of parameters
    #
    config = {}

    # apply the server url if so specified
    #
    if opts.server_url is not None:
        config["server_url"] = opts.server_url

    # apply the auth token if so specified
    #
    if opts.auth_token is not None:
        config["auth_token"] = opts.auth_token

    # apply the "watchlist enable" flag if so specified
    #
    if opts.watchlist_enable:
        config["watchlist_export"] = s2b(opts.watchlist_enable)

    # apply the "ssl cert verify" flag if so specified
    #
    if opts.ssl_cert_verify:
       config["ssl_certificate_verify"] = s2b(opts.ssl_cert_verify)

    # apply the configuration
    #
    cb.set_platform_server_config(config)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
