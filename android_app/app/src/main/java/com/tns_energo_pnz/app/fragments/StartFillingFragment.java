package com.tns_energo_pnz.app.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.tns_energo_pnz.app.R;
import com.tns_energo_pnz.app.activities.BaseActivity;


public class StartFillingFragment extends BaseFragment {
    private final String[] types_work = {"Контроль введенных ограничений", "Введение ограничения ээ/ Возобновление питания"};
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_start_filling, container, false);
        Button button = view.findViewById(R.id.confirm);
        Spinner type_work = view.findViewById(R.id.type_work);
        ArrayAdapter<String> spinner_adapter = new ArrayAdapter<>(this.getContext(), android.R.layout.simple_spinner_item, types_work);

        button.setOnClickListener(v -> ((BaseActivity)getActivity()).switchFragment(new FillingCheckBoxesFragment()));
        return view;
    }
}
