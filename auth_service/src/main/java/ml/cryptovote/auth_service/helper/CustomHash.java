package ml.cryptovote.auth_service.helper;

import com.google.common.hash.Hashing;
import lombok.Getter;

import java.nio.charset.StandardCharsets;
import java.util.UUID;

public class CustomHash {
    @Getter
    private final String txt;
    @Getter
    private final String txtHash;

    public CustomHash() {
        this(UUID.randomUUID().toString());
    }

    public CustomHash(String txt) {
        this.txt = txt;
        this.txtHash = Hashing
                .sha256()
                .hashString(this.txt, StandardCharsets.UTF_8)
                .toString();
    }

    public boolean verifyHash(String hash) {
        return this.txtHash.equals(hash);
    }
}
