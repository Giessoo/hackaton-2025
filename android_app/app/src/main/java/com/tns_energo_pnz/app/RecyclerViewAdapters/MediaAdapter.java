package com.tns_energo_pnz.app.RecyclerViewAdapters;

import android.content.Context;
import android.net.Uri;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.tns_energo_pnz.app.R;

import java.util.List;

public class MediaAdapter extends RecyclerView.Adapter<MediaAdapter.ViewHolder> {

    private final LayoutInflater inflater;
    private List<Uri> imageUris;
    private RecyclerView recyclerView;

    public MediaAdapter(Context context, List<Uri> imageUris) {
        this.inflater = LayoutInflater.from(context);
        this.imageUris = imageUris;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = inflater.inflate(R.layout.item_image, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onAttachedToRecyclerView(@NonNull RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
        this.recyclerView = recyclerView;
    }

    public void setImageUris(List<Uri> imageUris){
        this.imageUris = imageUris;
        this.notifyDataSetChanged();
        if (this.getItemCount() == 0) {
            recyclerView.setVisibility(View.GONE);
        } else {
            recyclerView.setVisibility(View.VISIBLE);
        }
    }

    public List<Uri> getImageUris(){
        return imageUris;
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        if(imageUris.isEmpty()) return;
        try {
            Uri imageUri = imageUris.get(position);
            holder.imageView.setImageURI(imageUri);
            holder.deleteButton.setOnClickListener(view -> {
                imageUris.remove(position);
                ((MediaAdapter) recyclerView.getAdapter()).setImageUris(imageUris);
            });
        }catch (Exception e){
            Log.e("ImageAdapter: ", e.getMessage());
        }
    }

    @Override
    public int getItemCount() {
        return imageUris.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        ImageView imageView;
        ImageButton deleteButton;
        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            imageView = itemView.findViewById(R.id.imageView);
            deleteButton = itemView.findViewById(R.id.cancel_image);
        }
    }

}
