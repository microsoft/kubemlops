import adal
import argparse


def get_access_token(tenant, clientId, client_secret):
    authorityHostUrl = "https://login.microsoftonline.com"
    GRAPH_RESOURCE = '00000002-0000-0000-c000-000000000000'

    authority_url = authorityHostUrl + '/' + tenant

    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(GRAPH_RESOURCE, clientId, client_secret)  # noqa: E501
    return token['accessToken']


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--tenant",
        type=str,
        required=True,
        help="Tenant"
    )

    parser.add_argument(
        "--service_principal",
        type=str,
        required=True,
        help="Service Principal"
    )

    parser.add_argument(
        "--sp_secret",
        type=str,
        required=True,
        help="Service Principal Secret"
    )

    args = parser.parse_args()

    token = get_access_token(args.tenant, args.service_principal, args.sp_secret)  # noqa: E501, E261
    return token


if __name__ == '__main__':
    exit(main())
