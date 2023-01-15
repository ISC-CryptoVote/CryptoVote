package ml.cryptovote.auth_service.model.dao;

import lombok.Data;
import lombok.RequiredArgsConstructor;
import ml.cryptovote.auth_service.enums.Role;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@RequiredArgsConstructor
@RedisHash("UserLogin")
public class RedisUserLogin {
    @Id
    private String phone;
    private Role role;
    private String otpHash;
    private long exp;

    public RedisUserLogin(String phone, Role role, String otp, long exp) {
        this.phone = phone;
        this.role = role;
        this.otpHash = otp;
        this.exp = exp;
    }
}
