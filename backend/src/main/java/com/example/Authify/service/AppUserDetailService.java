package com.example.Authify.service;

import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.example.Authify.entity.UserEntity;
import com.example.Authify.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AppUserDetailService implements UserDetailsService{

    @Autowired
    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
       
    UserEntity existingUser  =  userRepository.findByEmail(email)
      .orElseThrow(()-> new UsernameNotFoundException("Email not found for the email " + email));

      return new User(existingUser.getEmail() , existingUser.getPassword() , new ArrayList<>());
    }
    
}
