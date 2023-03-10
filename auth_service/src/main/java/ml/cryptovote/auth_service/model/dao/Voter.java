package ml.cryptovote.auth_service.model.dao;

import lombok.Data;
import ml.cryptovote.auth_service.enums.Status;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Document
@Data
public class Voter {
    @Id
    private String id;

    @Indexed(unique = true)
    private String nic;

    private String name;

    private String phone;

    private String macHash;

    private String address;

    private String gnDivision;

    private String pubKey;

    private Status status;

    public Voter(String nic, String name, String phone, String macHash, String address, String gnDivision, String pubKey, Status status) {
        this.nic = nic;
        this.name = name;
        this.phone = phone;
        this.macHash = macHash;
        this.address = address;
        this.gnDivision = gnDivision;
        this.pubKey = pubKey;
        this.status = status;
    }
}
