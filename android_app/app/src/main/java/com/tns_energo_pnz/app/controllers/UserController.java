package com.tns_energo_pnz.app.controllers;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import java.util.List;

import com.tns_energo_pnz.app.models.User;

public class UserController {
    public interface UserResponse {
        void onSuccess(List<User> users);
        void onError(String message);
    }

    public static void fetchUsers(UserResponse callback) {
        ApiClient.getService().getUsers().enqueue(new Callback<List<User>>() {
            @Override
            public void onResponse(Call<List<User>> call, Response<List<User>> response) {
                if (response.isSuccessful()) {
                    callback.onSuccess(response.body());
                } else {
                    callback.onError("Server error: " + response.code());
                }
            }

            @Override
            public void onFailure(Call<List<User>> call, Throwable t) {
                callback.onError("Network error: " + t.getMessage());
            }
        });
    }
}