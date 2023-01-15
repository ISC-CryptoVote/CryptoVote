package ml.cryptovote.auth_service.repository;

import ml.cryptovote.auth_service.model.dao.RedisUserLogin;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RedisUserLoginRepository extends CrudRepository<RedisUserLogin, String> {
}
