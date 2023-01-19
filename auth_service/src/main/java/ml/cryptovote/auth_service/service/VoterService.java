package ml.cryptovote.auth_service.service;

import ml.cryptovote.auth_service.exception.EntityNotFoundException;
import ml.cryptovote.auth_service.exception.InvalidOperationException;
import ml.cryptovote.auth_service.helper.PasswordGenerator;
import ml.cryptovote.auth_service.model.dao.RedisNonce;
import ml.cryptovote.auth_service.model.dao.Voter;
import ml.cryptovote.auth_service.model.dto.VoterNonceResDTO;
import ml.cryptovote.auth_service.repository.RedisNonceRepository;
import ml.cryptovote.auth_service.repository.VoterRepository;
import org.bouncycastle.util.io.pem.PemReader;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.NoSuchPaddingException;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.Optional;

@Service
public class VoterService {

    @Autowired
    private VoterRepository voterRepository;

    @Autowired
    private RedisNonceRepository redisNonceRepository;

    private static Logger LOGGER = LoggerFactory.getLogger(UserService.class);

    public VoterNonceResDTO generateNonce(String nic) {
        Optional<Voter> optVoter = voterRepository.findByNic(nic);
        if(optVoter.isEmpty()) {
            throw new EntityNotFoundException("Invalid NIC");
        }
        String nonce = PasswordGenerator.generateCommonLangPassword();
        RedisNonce redisNonce = new RedisNonce(nic, nonce);
        redisNonceRepository.save(redisNonce);
        VoterNonceResDTO nonceReq = new VoterNonceResDTO(nic, nonce);
        return nonceReq;
    }

    public Voter verifyPubKey(String nic, String pubKey, String encNonce) {
        Optional<Voter> optVoter = voterRepository.findByNic(nic);
        if(optVoter.isEmpty()) {
            throw new EntityNotFoundException("Invalid NIC");
        }
        Voter voter = optVoter.get();
        Optional<RedisNonce> optNonce = redisNonceRepository.findById(nic);
        if(optNonce.isEmpty()) {
            throw new EntityNotFoundException("Nonce is expired");
        }
        RedisNonce nonce = optNonce.get();
        try {

            byte[] encNonceBytes = Base64.getDecoder().decode(encNonce);
            PublicKey publicKey = loadPublicKey(pubKey);
            Cipher decryptCipher = Cipher.getInstance("RSA");
            decryptCipher.init(Cipher.DECRYPT_MODE, publicKey);
            byte[] decryptedNonceBytes = decryptCipher.doFinal(encNonceBytes);
            String decryptedNonce = new String(decryptedNonceBytes, StandardCharsets.UTF_8);
            if(!nonce.getNonce().equals(decryptedNonce)) {
                throw new InvalidOperationException("Invalid encryption");
            }
            voter.setPubKey(pubKey);
            return voterRepository.save(voter);
        } catch (NoSuchAlgorithmException e) {
            LOGGER.error(e.getMessage());
            throw new RuntimeException(e);
        } catch (NoSuchPaddingException e) {
            LOGGER.error(e.getMessage());
            throw new RuntimeException(e);
        } catch (BadPaddingException e) {
            throw new InvalidOperationException("Decryption error");
        } catch (Exception e) {
            LOGGER.error(e.getMessage());
            throw new InvalidOperationException("Invalid public key");
        }
    }

    private PublicKey loadPublicKey(String publicKey) throws Exception {
        byte[] keyBytes = new PemReader(new StringReader(publicKey)).readPemObject().getContent();
        X509EncodedKeySpec spec = new X509EncodedKeySpec(keyBytes);
        KeyFactory kf = KeyFactory.getInstance("RSA");
        return kf.generatePublic(spec);
    }
}
