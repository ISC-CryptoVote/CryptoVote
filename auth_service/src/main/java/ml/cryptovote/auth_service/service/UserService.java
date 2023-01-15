package ml.cryptovote.auth_service.service;

import com.twilio.exception.ApiException;
import ml.cryptovote.auth_service.enums.Role;
import ml.cryptovote.auth_service.exception.EntityNotFoundException;
import ml.cryptovote.auth_service.exception.InvalidOperationException;
import ml.cryptovote.auth_service.helper.CustomHash;
import ml.cryptovote.auth_service.helper.Otp;
import ml.cryptovote.auth_service.helper.OtpGenerator;
import ml.cryptovote.auth_service.model.dao.RedisUserLogin;
import ml.cryptovote.auth_service.model.dao.User;
import ml.cryptovote.auth_service.model.dao.Voter;
import ml.cryptovote.auth_service.model.dto.VoterVerifiedResDTO;
import ml.cryptovote.auth_service.repository.UserRepository;
import ml.cryptovote.auth_service.repository.RedisUserLoginRepository;
import ml.cryptovote.auth_service.repository.VoterRepository;
import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.security.InvalidKeyException;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class UserService implements UserDetailsService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private VoterRepository voterRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private OtpGenerator otpGenerator;

    @Autowired
    private SMSSender smsSender;

    @Autowired
    private RedisUserLoginRepository redisUserLoginRepository;

    @Autowired
    private ModelMapper modelMapper;

    @Autowired
    private JWTService jwtService;

    @Value("${REFRESH_TOKEN_VALIDITY}")
    private long REFRESH_TOKEN_VALIDITY;

    private static Logger LOGGER = LoggerFactory.getLogger(UserService.class);

    @Override
    public UserDetails loadUserByUsername(String nic) throws UsernameNotFoundException {
        Optional<User> userOptional = userRepository.findByNicAndSuspend(nic, false);
        if(userOptional.isPresent())
            return userOptional.get();
        else
            throw new EntityNotFoundException("User not found");
    }

    public Authentication getAuthentication(String phone) {
        UserDetails userDetails = this.loadUserByUsername(phone);
        return new UsernamePasswordAuthenticationToken(userDetails, "", userDetails.getAuthorities());
    }

    public User createUser(String nic, String phone, String password, List<Role> roles, boolean enable) {
        User user = new User(
                nic,
                phone,
                passwordEncoder.encode(password),
                roles,
                Instant.now().getEpochSecond() + REFRESH_TOKEN_VALIDITY,
                enable,
                false);
        return userRepository.save(user);
    }

    private void redisSaveService(String phone, Role role, String otpHash, long exp) {
        redisUserLoginRepository.save(new RedisUserLogin(phone, role, otpHash, exp));
    }

    private boolean redisVerifyOtp(String phone, Role role, String otp) {
        Optional<RedisUserLogin> userLoginOptional = redisUserLoginRepository.findById(phone);
        if(userLoginOptional.isEmpty())
            throw new EntityNotFoundException("Can't find the user record");
        RedisUserLogin userReg = userLoginOptional.get();
        if(userReg.getRole() != role) {
            throw new InvalidOperationException("Invalid operation");
        }
        if(userReg.getExp() < Instant.now().getEpochSecond())
            throw new InvalidOperationException("OTP expired");
        CustomHash hash = new CustomHash(otp);
        redisUserLoginRepository.deleteById(phone);
        return hash.verifyHash(userReg.getOtpHash());
    }

    public String sendOTP(String phone, Role role) throws InvalidKeyException {
        Otp otp = otpGenerator.generateOTP();
        // CustomHash otpHash = new CustomHash(otp.getOtp());
        CustomHash otpHash = new CustomHash("123456");
        // this.redisSaveService(phone, role, otpHash.getTxtHash(), otp.getExp());
        this.redisSaveService(phone, role, otpHash.getTxtHash(), otp.getExp());
        try {
            // smsSender.sendSms(phone, otp.getOtp());
            smsSender.sendSms(phone, "123456");
        } catch (ApiException e) {
            // do nothing
        }
        // LOGGER.info(otp.getOtp());
        LOGGER.info("123456");
        return "OTP is sent";
    }

    public VoterVerifiedResDTO voterVerification(String phone, String otp) {
        User user;
        Voter voter;
        if(!this.redisVerifyOtp(phone, Role.VOTER, otp))
            throw new InvalidOperationException("Invalid OTP");
        String refreshToken = UUID.randomUUID().toString();

        user = (User)this.loadUserByUsername(phone);
        Optional<Voter> passengerOptional = voterRepository.findByPhone(phone);
        if(passengerOptional.isEmpty())
            throw new InvalidOperationException("Try another phone number"); // must change later
        voter = passengerOptional.get();
        user.setPassword(passwordEncoder.encode(refreshToken));
        userRepository.save(user);

        VoterVerifiedResDTO response = modelMapper.map(voter, VoterVerifiedResDTO.class);
        response.setToken(jwtService.createToken(phone, Arrays.asList(Role.VOTER)));
        response.setRefreshToken(refreshToken);
        return response;
    }

}
