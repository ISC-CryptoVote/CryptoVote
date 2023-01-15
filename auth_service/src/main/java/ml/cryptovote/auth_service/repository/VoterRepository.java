package ml.cryptovote.auth_service.repository;

import ml.cryptovote.auth_service.model.dao.Voter;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface VoterRepository extends MongoRepository<Voter, String> {
    public Optional<Voter> findByPhone(String phone);
    public Boolean existsByPhone(String phone);
}
