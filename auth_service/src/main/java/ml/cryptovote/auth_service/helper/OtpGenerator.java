package ml.cryptovote.auth_service.helper;

import com.eatthepath.otp.TimeBasedOneTimePasswordGenerator;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.KeyGenerator;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;

@Component
public class OtpGenerator {
    private final TimeBasedOneTimePasswordGenerator totp;
    private final KeyGenerator keyGenerator;
    private final Key key;
    @Value("${OTP_VALIDITY}")
    private long otpValidity;
    @Getter
    private long exp;

    public OtpGenerator() throws NoSuchAlgorithmException {
        this.totp = new TimeBasedOneTimePasswordGenerator();
        this.keyGenerator = KeyGenerator.getInstance(totp.getAlgorithm());
        this.keyGenerator.init(160);
        this.key = keyGenerator.generateKey();
    }

    public Otp generateOTP() throws InvalidKeyException {
        final Instant now = Instant.now();
        return new Otp(totp.generateOneTimePasswordString(key, now), now.getEpochSecond() + otpValidity);
    }
}
