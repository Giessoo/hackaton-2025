package com.tns_energo_pnz.app.activities;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import android.util.Log;
import com.tns_energo_pnz.app.controllers.UserController;
import com.tns_energo_pnz.app.models.User;
import java.util.List;

import com.tns_energo_pnz.app.R;
import com.tns_energo_pnz.app.fragments.PinCodeDialogFragment;

public class InspectorActivity extends BaseActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        initButtonsListeners();
    }

    private void initButtonsListeners(){
        Button inspector_button1 = findViewById(R.id.inspector_button1);
        Button inspector_button2 = findViewById(R.id.inspector_button2);
        Button confirm_button = findViewById(R.id.confirm_button);
        confirm_button.setOnClickListener(this::sendNextActivity);
        inspector_button1.setOnClickListener(this::callPinCodeDialog);
        inspector_button2.setOnClickListener(this::callPinCodeDialog);
    }

    private void sendNextActivity(View view){
        Intent intent = new Intent(this, FillingActivity.class);
        startActivity(intent);
    }

    private void callPinCodeDialog(View view){
        PinCodeDialogFragment pinDialog = new PinCodeDialogFragment();
        pinDialog.setOnPinEnteredListener(pin -> {
            if (pin.equals("1234")) {
                Toast.makeText(InspectorActivity.this, "PIN верный", Toast.LENGTH_SHORT).show();

                // Вызов UserController для получения пользователей
                UserController.fetchUsers(new UserController.UserResponse() {
                    @Override
                    public void onSuccess(List<User> users) {
                        // Вывод в лог
                        for (User user : users) {
                            Log.d("USER_DATA", "User: " + user.toString());
                        }
                        Toast.makeText(InspectorActivity.this,
                                "Получено пользователей: " + users.size(),
                                Toast.LENGTH_SHORT).show();
                    }

                    @Override
                    public void onError(String message) {
                        Log.e("API_ERROR", message);
                        Toast.makeText(InspectorActivity.this,
                                "Ошибка получения данных: " + message,
                                Toast.LENGTH_SHORT).show();
                    }
                });

            } else {
                Toast.makeText(InspectorActivity.this, "Неверный PIN", Toast.LENGTH_SHORT).show();
            }
        });
        pinDialog.show(getSupportFragmentManager(), "PinCodeDialog");
    }

    @Override
    protected int getLayout() {
        return R.layout.activity_inspector;
    }
}
