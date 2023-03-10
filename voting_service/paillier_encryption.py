from phe import paillier
from operator import add
import pickle
import codecs

def encrypt_vote_array(publickey, votes):
    # Receives an array of size number of candidates.
    # eg - [0,1,0,0,0] (voter voted for the 2nd candidate)
    # votes - voted array
    # returns an encrypted array of votes

    encryptedArr = [publickey.encrypt(x) for x in votes]
    return encryptedArr

def decrypt_voted_array(privatekey, encryptedArr):
    # encryptedArr - encrypted array of votes
    # returns - deciphered votes (eg - [10,11,9,7,3] if there are 30 voters)

    decryptedArr = [privatekey.decrypt(x) for x in encryptedArr]
    return decryptedArr


# for now later save and read from db
public_key, private_key = paillier.generate_paillier_keypair()
keyring = paillier.PaillierPrivateKeyring()
keyring.add(private_key)

if __name__ == "__main__":

    """ 
    votes_from_cand_1 = [0,1,0,0,0]
    votes_from_cand_2 = [0,1,0,0,0]
    votes_from_cand_3 = [0,0,1,0,0]
    votes_from_cand_4 = [0,0,0,0,1]
    votes_from_cand_5 = [1,0,0,0,0]

    zipped_lst = zip(votes_from_cand_1,votes_from_cand_2,votes_from_cand_3,votes_from_cand_4,votes_from_cand_5)
    print("Correct : " + str([sum(item) for item in zipped_lst]))

    encrypt_1 = encrypt_vote_array(votes_from_cand_1)
    encrypt_2 = encrypt_vote_array(votes_from_cand_2)
    encrypt_3 = encrypt_vote_array(votes_from_cand_3)
    encrypt_4 = encrypt_vote_array(votes_from_cand_4)
    encrypt_5 = encrypt_vote_array(votes_from_cand_5)
    zipped_lst_enc = zip(encrypt_1,encrypt_2,encrypt_3,encrypt_4,encrypt_5)
    encrypted_counted_votes = [sum(item) for item in zipped_lst_enc]
    decrpted_counted_votes  = decrypt_voted_array(encrypted_counted_votes)
    print("Counting votes : "+ str(decrpted_counted_votes))
    """
    a = 23
    print(a)
    print("public key : "+str(public_key.n))
    bytes_key = pickle.dumps(public_key)
    str_bytes = codecs.encode(bytes_key,"base64").decode()
    #print(isinstance(str_bytes, str))
    # print(str_bytes)
    pub_obj = pickle.loads(codecs.decode(str_bytes.encode(),"base64"))
    print("public key : "+str(pub_obj.n))
    print(public_key)
    en_a = public_key.encrypt(a)
    print(isinstance(en_a, str))
    print()
