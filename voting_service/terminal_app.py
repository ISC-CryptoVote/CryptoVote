import click
import requests
import aes
import jwt

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


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
@click.argument('token')
def vote(token):
    
    # request signed ballot
    url = 'http://localhost:8000/request-ballot'
    response = requests.get(url, headers={"Token": token})
    # validate signed ballot
    if verify_ballot(response.json()['ballot'], response.json()['signature'], response.json()['public-key'].encode()):
        print('\nCandidate List\n')
        for i in range(len(candidates)):
            print(str(i) + ' - ' + candidates[i])
        v = int(input('\nEnter the vote: '))

        v_reponse_list = ['0'] * len(candidates)
        v_reponse_list[v] = '1'
        
        v_reponse = ''.join(v_reponse_list)

        # decode the JWT token
        decoded_token = jwt.decode(token, secret_key, algorithms='HS256')
        nic = decoded_token['id']

        # get otp from the system
        url = 'http://localhost:8000/request-otp'
        otp = requests.get(url, headers={"Token": token}).json()['otp']

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
            url = 'http://localhost:8000/submit-ballot'
            response = requests.post(url, headers={"Token": token}, json=payload)
            click.echo("Successfully Voted")
            return
        click.echo("Cancelled Vote")
    else:
        click.echo('Invalid Ballot')
        return


    click.echo(response.json())

if __name__ == '__main__':
    cli()