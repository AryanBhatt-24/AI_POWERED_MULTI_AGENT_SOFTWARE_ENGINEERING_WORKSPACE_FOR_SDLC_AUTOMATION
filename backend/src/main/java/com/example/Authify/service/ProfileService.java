package com.example.Authify.service;

import com.example.Authify.io.ProfileRequest;
import com.example.Authify.io.ProfileResponse;

public interface  ProfileService {
      public ProfileResponse createProfile(ProfileRequest request);

      public ProfileResponse getProfile(String email);

      void sendResetOtp(String email);

      void resetPassword(String email , String otp , String newPassword);

      void sendOtp(String email);

      void verifyOtp(String email , String otp);

     
}
