package ml.cryptovote.auth_service.model.dao;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@RequiredArgsConstructor
@AllArgsConstructor
@RedisHash("Nonce")
public class RedisNonce {
    @Id
    private String nic;

    private String nonce;
}
