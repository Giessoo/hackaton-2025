package com.tns_energo_pnz.app.views;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.List;

public class SquareLoaderView extends View {
    private static final int SQUARE_SIZE = 20; // размер квадрата в dp
    private static final int SQUARE_MARGIN = 30; // расстояние между квадратами в dp
    private static final int ANIMATION_DURATION = 675; // длительность анимации
    private static final int DELAY_BETWEEN_SQUARES = 75; // задержка между анимациями

    private Paint squarePaint;
    private final List<Square> squares = new ArrayList<>();
    private long startTime;
    private boolean isAnimating = false;

    public SquareLoaderView(Context context) {
        super(context);
        init();
    }

    public SquareLoaderView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    private void init() {
        squarePaint = new Paint();
        squarePaint.setColor(0xFFDDDDDD);
        squarePaint.setStyle(Paint.Style.FILL);

        for (int i = 0; i < 9; i++) {
            squares.add(new Square());
        }
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);

        float centerX = w / 2f;
        float centerY = h / 2f;
        float squareSizePx = dpToPx(SQUARE_SIZE);
        float marginPx = dpToPx(SQUARE_MARGIN);

        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                int index = row * 3 + col;
                squares.get(index).x = centerX - marginPx + (col * marginPx);
                squares.get(index).y = centerY - marginPx + (row * marginPx);
                squares.get(index).size = squareSizePx;
                squares.get(index).delay = index * DELAY_BETWEEN_SQUARES;
            }
        }
    }

    @Override
    protected void onDraw(@NonNull Canvas canvas) {
        super.onDraw(canvas);

        if (!isAnimating) {
            startTime = System.currentTimeMillis();
            isAnimating = true;
        }

        long currentTime = System.currentTimeMillis() - startTime;

        for (Square square : squares) {
            long elapsed = currentTime - square.delay;

            if (elapsed >= 0) {
                float progress = (elapsed % ANIMATION_DURATION) / (float) ANIMATION_DURATION;
                square.alpha = (int) (255 * (progress < 0.5f ? progress * 2 : (1 - progress) * 2));
                squarePaint.setAlpha(square.alpha);
                canvas.drawRect(
                        square.x - square.size / 2,
                        square.y - square.size / 2,
                        square.x + square.size / 2,
                        square.y + square.size / 2,
                        squarePaint
                );
            }
        }

        invalidate();
    }

    private float dpToPx(float dp) {
        return dp * getResources().getDisplayMetrics().density;
    }

    private static class Square {
        float x, y, size;
        int alpha = 0;
        long delay;
    }
}
