package com.tns_energo_pnz.app.fragments;

import android.app.Dialog;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.text.InputType;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.DialogFragment;

import com.tns_energo_pnz.app.R;

public class PinCodeDialogFragment extends DialogFragment {
    private OnPinEnteredListener listener;
    private EditText pinInput;

    public interface OnPinEnteredListener {
        void onPinEntered(String pin);
    }

    public void setOnPinEnteredListener(OnPinEnteredListener listener) {
        this.listener = listener;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.dialog_pin_code, container, false);

        pinInput = view.findViewById(R.id.pin_input);
        Button btnConfirm = view.findViewById(R.id.btn_confirm);

        pinInput.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_VARIATION_PASSWORD);

        btnConfirm.setOnClickListener(v -> {
            String pin = pinInput.getText().toString();
            if (pin.length() == 4) {
                if (listener != null) {
                    listener.onPinEntered(pin);
                }
                dismiss();
            } else {
                Toast.makeText(getContext(), "Введите 4-значный PIN-код", Toast.LENGTH_SHORT).show();
            }
        });

        return view;
    }

    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        Dialog dialog = super.onCreateDialog(savedInstanceState);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
            dialog.getWindow().requestFeature(Window.FEATURE_NO_TITLE);
        }
        return dialog;
    }
}
