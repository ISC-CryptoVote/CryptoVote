package ml.cryptovote.auth_service.model.dao;

import lombok.Data;
import ml.cryptovote.auth_service.enums.Role;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.time.Instant;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Document
@Data
public class User implements UserDetails {
    @Id
    private String id;

    @Indexed(unique = true)
    private String nic;

    @Indexed(unique = true)
    private String phone;

    private String password;

    private List<Role> roles;

    private Collection<? extends GrantedAuthority> authorities;

    private long exp;

    private Boolean enabled;

    private Boolean suspend;

    public User(String nic, String phone, String password, List<Role> roles, long exp, Boolean enabled, Boolean suspend) {
        this.nic = nic;
        this.phone = phone;
        this.password = password;
        this.roles = roles;
        this.exp = exp;
        this.enabled = enabled;
        this.suspend = suspend;
        this.authorities = roles.stream().map(role -> new SimpleGrantedAuthority(role.name())).collect(Collectors.toList());
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return phone;
    }

    @Override
    public boolean isAccountNonExpired() {
        return enabled;
    }

    @Override
    public boolean isAccountNonLocked() {
        return enabled;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        if(password == null || password =="")
            return false;
        if(enabled && (roles.contains(Role.VOTER)  || roles.contains(Role.GSN)))
            return exp > Instant.now().getEpochSecond();
        return enabled;
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }
}
