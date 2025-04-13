package com.tns_energo_pnz.app.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.tns_energo_pnz.app.R;
import com.tns_energo_pnz.app.activities.BaseActivity;


public class StartFillingFragment extends BaseFragment {
    private int currentPositionTypeWorkSpinner = 0;
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_start_filling, container, false);
        Button button = view.findViewById(R.id.confirm);
        String[] types_work = {
            "Контроль введенных ограничений",
            "Введение ограничения ээ",
            "Возобновление питания"
        };
        initSpinner(view, types_work);
        button.setOnClickListener(v -> ((BaseActivity)getActivity()).switchFragment(
                FillingCheckBoxesFragment.newInstance(
                        currentPositionTypeWorkSpinner,
                        ((EditText)view.findViewById(R.id.address_edit_text)).getText().toString()
                )
        ));
        return view;
    }

    private void initSpinner(View view, String[] data){
        Spinner type_work = view.findViewById(R.id.type_work);
        ArrayAdapter<String> spinner_adapter = new ArrayAdapter<>(this.getContext(), android.R.layout.simple_spinner_item, data);
        spinner_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        type_work.setAdapter(spinner_adapter);
        AdapterView.OnItemSelectedListener itemSelectedListener = new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                currentPositionTypeWorkSpinner = position;
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        };
        type_work.setOnItemSelectedListener(itemSelectedListener);
    }
}
