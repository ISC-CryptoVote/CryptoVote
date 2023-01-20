import click
import requests
import aes

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# voting system service
voting_system_host = 'localhost'
voting_system_port = '8000'

# user secret key
user_secret_key = '-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDF4hI9s0Mem349YzSu3r+ZvuQlx7Zmr2LNWXaeeR+m8xbnX9cq\nIeeFCRdxBfXNzoYgexbnG2hW+1JFbg4OQiFpoLi9KJEoyRYZR8dgzrUUFgm0DjpH\nreiuu/Cr0GvkzBscV0LwBHCoUUJlGLWW6vMQmwGHBRV8/tsRtQVy0yB4ZQIDAQAB\nAoGACxhGUoxK/pvUQ6fcy9M0Ze/khdPBP9ekkAPsmS0MX8Vwas+eVj/pZbWhSVZ+\ntifWsFqGabXJL1tO/RKTGiyOB+9aeh2wtmBuCBDvYf85hAl4mXzm43ID7za0OCJf\n76V8tZjdO2zIgKtnwoJ30liwNorbjq5jc8plj0C43jmuz98CQQDbzGe/MIfTY3gw\nqJUe8lzmsLBRCxmUCksk5XBngjgAiFNgF8jMug7fMy6Z9FBk/5thfhyJFIeCbCl8\nwakRHAu7AkEA5nmgDPkYbsobrQR3IqT7vZFzGvfEzXMm5fvhmXeo3T6eW4oFz2Nz\ny7GnInRxcFlwEG+yYw2FkqIjdDTzw9N6XwJAdmEby2Q280oSdJqHXhiIopKtE6kX\nyJzWpfOQ257NzLOfvBRzSJg45EuroK1uE0d7h0Gl2sqcxUi9+3xOM3HYewJAeX/C\nrTQf+j/XqTVCbOQWxg/IY34cpMZAylsnyhS307KwHse7WmIuaEKGPnauWrD7j96i\nZu947B1HnXpQy3pP9wJBAKqPivxEDI2fThsIUvwATvOHnsqJW/ubp95BmW2cYvOE\nW431LEDoCvKgshiD8p2XADrgVlJfSNsVf95T62ljzPk=\n-----END RSA PRIVATE KEY-----'

# secret key for decoding jwt
secret_key = "5bd44771b6531c12c8354aec3e27a8eeeba049cc0423c9208532eb96491c3335"
candidates = ['John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe'] # candidates list

@click.group()
def cli():
    pass

def verify_ballot(ballot, signature, public_key_pem):
    public_key = RSA.import_key(public_key_pem)
    hashed_ballot = SHA256.new(ballot.encode())
    try:
        pkcs1_15.new(public_key).verify(hashed_ballot, bytes.fromhex(signature))
        return True
    except (ValueError, TypeError):
        return False


@cli.command()
@click.argument('nic')
def vote(nic):
    
    # sign user nic with user secret key
    private_key = RSA.import_key(user_secret_key.encode())
    hashed_data = SHA256.new(nic.encode())
    nic_signature = pkcs1_15.new(private_key).sign(hashed_data)

    # request signed ballot
    url = f'http://{voting_system_host}:{voting_system_port}/request-ballot'
    response = requests.get(url, headers={"id": nic, "sign": nic_signature.hex()})

    # validate signed ballot
    if verify_ballot(response.json()['ballot'], response.json()['signature'], response.json()['public-key'].encode()):
        print('\nCandidate List\n')
        for i in range(len(candidates)):
            print(str(i) + ' - ' + candidates[i])
        v = int(input('\nEnter the vote: '))

        v_reponse_list = ['0'] * len(candidates)
        v_reponse_list[v] = '1'
        
        v_reponse = ''.join(v_reponse_list)

        # get otp from the system
        url = f'http://{voting_system_host}:{voting_system_port}/request-otp'
        otp = requests.get(url, headers={"id": nic, "sign": nic_signature.hex()}).json()['otp']

        # generate AES key
        key = aes.get_key(nic, otp)
        v_reponse_enc, nonce = aes.encrypt(key, v_reponse.encode())
        cmac_text = aes.cmac(key, v_reponse_enc)

        # submit reponse
        s = int(input('\nSubmit [1/0]: '))
        if s:
            payload = {
                "ciphertext": v_reponse_enc,
                "nonce": nonce,
                "cmac": cmac_text
            }
            url = f'http://{voting_system_host}:{voting_system_port}/submit-ballot'
            response = requests.post(url, headers={"id": nic, "sign": nic_signature.hex()}, json=payload)
            if response.status_code == 200:
                click.echo("Successfully Voted")
            return
        click.echo("Cancelled Vote")
    else:
        click.echo('Invalid Ballot')
        return


    click.echo(response.json())

if __name__ == '__main__':
    cli()