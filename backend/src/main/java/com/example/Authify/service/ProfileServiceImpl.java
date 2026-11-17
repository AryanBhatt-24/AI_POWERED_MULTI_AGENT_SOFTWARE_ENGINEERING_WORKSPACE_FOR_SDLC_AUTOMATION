package com.example.Authify.service;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.example.Authify.entity.UserEntity;
import com.example.Authify.io.ProfileRequest;
import com.example.Authify.io.ProfileResponse;
import com.example.Authify.repository.UserRepository;

import lombok.RequiredArgsConstructor;


@Service
@RequiredArgsConstructor
public class ProfileServiceImpl implements ProfileService{

    @Autowired
    private final UserRepository userRepository;


    private final PasswordEncoder passwordEncoder;

    private final EmailService emailService;


    @Override
    public ProfileResponse createProfile(ProfileRequest request) {
        if(!userRepository.existsByEmail(request.getEmail())){
             UserEntity newProfile = convertToUserEntity(request);
             newProfile = userRepository.save(newProfile);
            return convertToProfileResponse(newProfile);
        }
      
       throw new  ResponseStatusException(HttpStatus.CONFLICT , "Email Already Exists");

    }


    private ProfileResponse convertToProfileResponse(UserEntity newProfile) {
       return ProfileResponse.builder()
       .name(newProfile.getName())
       .email(newProfile.getEmail())
       .userId(newProfile.getUserId())
       .isAccountVerified(newProfile.getIsAccountVerified())
       .build();
    }


    private UserEntity convertToUserEntity(ProfileRequest request) {
       return  UserEntity.builder()
        .email(request.getEmail())
        .userId(UUID.randomUUID().toString())
        .name(request.getName())
        .password(passwordEncoder.encode(request.getPassword()))
        .isAccountVerified(false)
        .resetOtpExpireAt(0L)
        .verifyOtp(null)
        .verifyOtpExpirAt(0L)
        .resetOtp(null)
        .build();
    }


    @Override
    public ProfileResponse getProfile(String email) {
      UserEntity existingUser =   userRepository.findByEmail(email).orElseThrow(()-> new UsernameNotFoundException("USer not found " + email));

      return convertToProfileResponse(existingUser);
    }


    @Override
    public void sendResetOtp(String email) {
        UserEntity existingEntity = userRepository.findByEmail(email)
        .orElseThrow(()-> new UsernameNotFoundException("User not found " + email));
        String otp = String.valueOf(ThreadLocalRandom.current().nextInt(100000 ,1000000));

        long expiryTime = System.currentTimeMillis() + (15 *60 * 1000);


        existingEntity.setResetOtp(otp);
        existingEntity.setResetOtpExpireAt(expiryTime);

        userRepository.save(existingEntity);

        try {
            
                emailService.sendResetOtpEmail(existingEntity.getEmail(), otp);


        } catch (Exception e) {

            throw new RuntimeException("Unable to Send email");
        }

    }


    @Override
    public void resetPassword(String email, String otp, String newPassword) {
        UserEntity existingUser = userRepository.findByEmail(email)
        .orElseThrow(() -> new UsernameNotFoundException("User Not Found" + email));

        if(existingUser.getResetOtp() == null || !existingUser.getResetOtp().equals(otp)){
            throw new RuntimeException("Invalid Otp ");
        }

        if(existingUser.getResetOtpExpireAt() < System.currentTimeMillis()){
            throw new RuntimeException("OTP Expired");
        }


        existingUser.setPassword(passwordEncoder.encode(newPassword));
        existingUser.setResetOtp(otp);
        existingUser.setResetOtpExpireAt(0L);

        userRepository.save(existingUser);
    }


    @Override
    public void sendOtp(String email) {

        UserEntity existingUser = userRepository.findByEmail(email)
        .orElseThrow(()-> new UsernameNotFoundException("User not Found" + email));


        if(existingUser.getIsAccountVerified() != null && existingUser.getIsAccountVerified()){
            return;
        }


         String otp = String.valueOf(ThreadLocalRandom.current().nextInt(100000 ,1000000));

        long expiryTime = System.currentTimeMillis() + (24 * 60 * 60 * 1000);

        existingUser.setVerifyOtp(otp);
        existingUser.setVerifyOtpExpirAt(expiryTime);

        userRepository.save(existingUser);

        try {
            emailService.sendOtpEmail(existingUser.getEmail(), otp);
        } catch (Exception e) {

            throw new RuntimeException("Unable to send Email");
        }
    }


    @Override
    public void verifyOtp(String email, String otp) {
        UserEntity existingUser = userRepository.findByEmail(email)
        .orElseThrow(()-> new UsernameNotFoundException("User not Found" + email));

        if(existingUser.getVerifyOtp() == null || !existingUser.getVerifyOtp().equals(otp))
        {
            throw new RuntimeException("Invalid Otp");
        }

        if(existingUser.getVerifyOtpExpirAt() < System.currentTimeMillis()){
            throw new RuntimeException("Otp Expired");
        }

        existingUser.setIsAccountVerified(true);
        existingUser.setVerifyOtp(null);
        existingUser.setVerifyOtpExpirAt(0L);

        userRepository.save(existingUser);
    }


    
}
