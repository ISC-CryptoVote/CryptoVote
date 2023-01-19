package ml.cryptovote.auth_service.model.dao;

import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@RequiredArgsConstructor
@RedisHash("Nonce")
public class RedisNonce {
    @Id
    private String nic;

    private String nonce;
}
