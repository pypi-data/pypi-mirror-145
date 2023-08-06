from embed.client import Client


if __name__ == '__main__':
    client_id = "CWRY-htZMzbGaEzTYJmQPISK7bHNuVmHecgSLPShRuzdU"
    client_secret = "CWRY-SECRET-bfc7581q2klRJe8FiFGsVDmB1w32BIQXFILVMLj9iCH" \
                    "szMBVJSDoOMGF7WhEeyolAxRSCsU8vBzdKbf4hsLBOVuC7sEx7Qc2eE" \
                    "yJhl7wBacO9ElyqEShzGSFykNxWenp"
    base_url = "http://127.0.0.1:8000"

    embed_client = Client(client_id, client_secret, base_url)
    resp = embed_client.assets.list_assets()
    pass
