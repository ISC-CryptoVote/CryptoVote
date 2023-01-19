package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import ml.cryptovote.auth_service.enums.Status;

@Data
@NoArgsConstructor
public class VoterRegistrationResDTO {
    private String id;

    private String nic;

    private String name;

    private String phone;

    private String macHash;

    private String address;

    private String gnDivision;

    private Status status;
}
