package ml.cryptovote.auth_service.model.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class GsnLoginResDTO {
    private String id;

    private String username;

    private String gnDivision;

    private String token;
}
