package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

@Data
@AllArgsConstructor
public class VoterNonceVerifyDTO {
    @NotBlank
    @Pattern(regexp = "(\\d{10})")
    private String nic;
    @NotBlank
    private String pubKey;
    @NotBlank
    private String encNonce;

}
