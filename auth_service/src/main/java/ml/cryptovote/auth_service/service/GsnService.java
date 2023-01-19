package ml.cryptovote.auth_service.service;


import ml.cryptovote.auth_service.enums.Status;
import ml.cryptovote.auth_service.exception.InvalidOperationException;
import ml.cryptovote.auth_service.model.dao.Voter;
import ml.cryptovote.auth_service.model.dto.VoterVerifiedResDTO;
import ml.cryptovote.auth_service.repository.VoterRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class GsnService {
    @Autowired
    private VoterRepository voterRepository;

    @Autowired
    private ModelMapper modelMapper;

    public VoterVerifiedResDTO changeStatus(String  nic, Status status) {
        Optional<Voter> optVoter = voterRepository.findByNic(nic);
        if(optVoter.isEmpty()) {
            throw new InvalidOperationException("NIC is invaild");
        }
        Voter voter = optVoter.get();
        voter.setStatus(status);
        Voter updatedVoter = voterRepository.save(voter);
        return modelMapper.map(updatedVoter,  VoterVerifiedResDTO.class);
    }

    public List<VoterVerifiedResDTO> getPendingVoters() {
        List<Voter> pendingList = voterRepository.findByStatus(Status.PENDING);
        List<VoterVerifiedResDTO>  res = pendingList.stream().map(this::convertToVerifiedDTO).collect(Collectors.toList());
        return res;
    }

    private VoterVerifiedResDTO convertToVerifiedDTO(Voter voter) {
        return modelMapper.map(voter, VoterVerifiedResDTO.class);
    }

}
