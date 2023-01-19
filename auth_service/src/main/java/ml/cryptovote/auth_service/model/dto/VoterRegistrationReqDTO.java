package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

@Data
@AllArgsConstructor
public class VoterRegistrationReqDTO {
    @NotBlank
    @Pattern(regexp="(\\d{10})")
    private String nic;
    @NotBlank
    private String name;
    @NotBlank
    @Pattern(regexp="(\\+94\\d{9})")
    private String phone;
    @NotBlank
    private String macHash;
    @NotBlank
    private String address;
    @NotBlank
    private String gnDivision;

}
