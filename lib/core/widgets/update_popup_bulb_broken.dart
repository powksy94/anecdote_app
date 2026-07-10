import 'package:flutter/material.dart';
import 'update_popup_bulb_base.dart';
import 'update_popup_bulb_globe.dart';

/// Dessine l'ampoule après l'explosion :
/// col + culot + bord de verre dentelé + fils cassés.
void drawBrokenBulb(Canvas canvas, Offset gc, double gr) {
  drawBulbBase(canvas, gc, gr);
  drawBulbNeck(canvas, gc, gr);
  drawBulbFilament(canvas, gc, broken: true, flicker: 0, light: 0);
  drawBulbJaggedEdge(canvas, gc, gr);
}

/// Dessine le bord de verre cassé (zigzag irrégulier au sommet du col).
void drawBulbJaggedEdge(Canvas canvas, Offset gc, double gr) {
  final gx = gc.dx;
  final y0 = gc.dy + gr - 7;

  canvas.drawPath(
    Path()
      ..moveTo(gx - 18, y0 + 3)
      ..lineTo(gx - 13, y0 - 5)
      ..lineTo(gx - 8,  y0 + 6)
      ..lineTo(gx - 2,  y0 - 1)
      ..lineTo(gx + 4,  y0 + 7)
      ..lineTo(gx + 10, y0 - 3)
      ..lineTo(gx + 15, y0 + 4)
      ..lineTo(gx + 18, y0 + 2),
    Paint()
      ..color = const Color(0xFFBCD8EE).withValues(alpha: 0.82)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.6
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round,
  );
}
