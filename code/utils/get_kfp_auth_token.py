import argparse
import adal
import sys


def main():
    parser = argparse.ArgumentParser("KFP host Auth")

    parser.add_argument(
        "--tenant",
        type=str,
        required=False,
        help="Tenant"
    )

    parser.add_argument(
        "--service_principal",
        type=str,
        required=False,
        help="Service Principal"
    )

    parser.add_argument(
        "--sp_secret",
        type=str,
        required=False,
        help="Service Principal Secret"
    )

    args = parser.parse_args()
    authorityHostUrl = "https://login.microsoftonline.com"
    GRAPH_RESOURCE = '00000002-0000-0000-c000-000000000000'

    authority_url = authorityHostUrl + '/' + str(args.tenant)

    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(GRAPH_RESOURCE, args.service_principal, args.sp_secret)  # noqa: E501
    return token['accessToken']


if __name__ == '__main__':
    sys.exit(main())
