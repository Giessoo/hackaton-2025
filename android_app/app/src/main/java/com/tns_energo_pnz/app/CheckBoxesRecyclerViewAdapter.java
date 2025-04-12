package com.tns_energo_pnz.app;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class CheckBoxesRecyclerViewAdapter extends RecyclerView.Adapter<CheckBoxesRecyclerViewAdapter.ViewHolder> {
    private final LayoutInflater inflater;
    private List<String> textForCheckBoxes;

    public CheckBoxesRecyclerViewAdapter(Context context, List<String> textForCheckBoxes){
        this.inflater = LayoutInflater.from(context);
        this.textForCheckBoxes = textForCheckBoxes;
    }

    public void setTextForCheckBoxes(List<String> textForCheckBoxes){
        this.textForCheckBoxes = textForCheckBoxes;
    }

    @NonNull
    @Override
    public CheckBoxesRecyclerViewAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = inflater.inflate(R.layout.checkbox_item, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public int getItemCount() {
        return textForCheckBoxes.size();
    }

    @Override
    public void onBindViewHolder(@NonNull CheckBoxesRecyclerViewAdapter.ViewHolder holder, int position) {
        String textForCheckBox = textForCheckBoxes.get(position);
        holder.checkBox.setText(textForCheckBox);
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        CheckBox checkBox;
        ViewHolder(@NonNull View itemView) {
            super(itemView);
            checkBox = itemView.findViewById(R.id.checkBox);
        }
    }
}
