package ml.cryptovote.auth_service.model.dto;

import lombok.Data;

@Data
public class VoterVerifiedResDTO {
    private String id;

    private String nic;

    private String name;

    private String phone;

    private String macHash;

    private String address;

    private String gnDivision;

    private String pubKey;

    private String token;

    private String refreshToken;

}
