package ml.cryptovote.auth_service.config;

import ml.cryptovote.auth_service.service.JWTService;
import ml.cryptovote.auth_service.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;

import java.util.List;

@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(
        prePostEnabled = true,
        securedEnabled = true,
        jsr250Enabled = true
)
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired
    private JWTService jwtService;
    @Autowired
    private UserService userService;
    @Autowired
    private JwtAuthenticationEntryPoint jwtAuthenticationEntryPoint;
    @Value("${ALLOWED_ORIGIN}")
    private List<String> allowedOrigins;

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                .cors()
                .and()
                .httpBasic().disable()
                .csrf().disable()
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                .authorizeRequests()
                .antMatchers(
                        "/api/passenger/login",
                        "/api/passenger/signup",
                        "/api/driver/login",
                        "/api/admin/**",
                        "/api/voter/**",
                        "/api/auth/**",
                        "/v3/api-docs/**",
                        "/api/swagger-ui.html",
                        "/swagger-ui.html",
                        "/api/swagger-ui/*",
                        "/ws/**",
                        "/app/**",
                        "/user/**"
                ).permitAll()
                .anyRequest().authenticated()
                .and()
                .apply(new JwtConfigurer(jwtService, userService))
                .and()
                .exceptionHandling()
                .authenticationEntryPoint(jwtAuthenticationEntryPoint);
    }
}
