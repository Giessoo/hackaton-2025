package com.tns_energo_pnz.app.activities;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

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
        inspector_button1.setOnClickListener(this::callPinCodeDialog);
        inspector_button2.setOnClickListener(this::callPinCodeDialog);
    }

    private void callPinCodeDialog(View view){
        PinCodeDialogFragment pinDialog = new PinCodeDialogFragment();
        pinDialog.setOnPinEnteredListener(pin -> {
            if (pin.equals("1234")) {
                Toast.makeText(InspectorActivity.this, "PIN верный", Toast.LENGTH_SHORT).show();
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
