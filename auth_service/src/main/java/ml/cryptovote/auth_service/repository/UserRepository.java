package ml.cryptovote.auth_service.repository;

import ml.cryptovote.auth_service.enums.Role;
import ml.cryptovote.auth_service.model.dao.User;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;
import java.util.Optional;

public interface UserRepository extends MongoRepository<User, String> {
    public Optional<User> findByPhone(String phone);
    public Optional<User> findByPhoneAndSuspend(String phone, Boolean suspend);
    public Optional<User> findByNicAndSuspend(String phone, Boolean suspend);
    public List<User> findByRolesIn(List<Role> role);
}
