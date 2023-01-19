package ml.cryptovote.auth_service.service;

import ml.cryptovote.auth_service.exception.EntityNotFoundException;
import ml.cryptovote.auth_service.helper.PasswordGenerator;
import ml.cryptovote.auth_service.model.dao.Voter;
import ml.cryptovote.auth_service.model.dto.VoterNonceResDTO;
import ml.cryptovote.auth_service.repository.RedisNonceRepository;
import ml.cryptovote.auth_service.repository.VoterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class VoterService {

    @Autowired
    private VoterRepository voterRepository;

    @Autowired
    private RedisNonceRepository redisNonceRepository;

    public VoterNonceResDTO generateNonce(String nic) {
        Optional<Voter> optVoter = voterRepository.findByNic(nic);
        if(optVoter.isEmpty()) {
            throw new EntityNotFoundException("Invalid NIC");
        }
        String nonce = PasswordGenerator.generateCommonLangPassword();
        VoterNonceResDTO nonceReq = new VoterNonceResDTO(nic, nonce);
        return nonceReq;
    }
}
