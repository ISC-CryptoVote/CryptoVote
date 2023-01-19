package ml.cryptovote.auth_service.repository;

import ml.cryptovote.auth_service.enums.Status;
import ml.cryptovote.auth_service.model.dao.Voter;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface VoterRepository extends MongoRepository<Voter, String> {
    public Optional<Voter> findByPhone(String phone);
    public Optional<Voter> findByNic(String nic);
    public Boolean existsByPhone(String phone);
    public List<Voter> findByStatus(Status status);
}
