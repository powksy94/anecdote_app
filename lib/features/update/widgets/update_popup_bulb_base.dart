import 'package:flutter/material.dart';

/// Dessine le col (trapèze courbé entre globe et culot) et le culot Edison fileté.
void drawBulbNeck(Canvas canvas, Offset gc, double gr) {
  final gx = gc.dx;
  final gy = gc.dy;
  final y0 = gy + gr - 8;   // début (légèrement dans le globe)
  final y1 = gy + gr + 19;  // fin (haut du culot)

  final neckPath = Path()
    ..moveTo(gx - 18, y0)
    ..quadraticBezierTo(gx - 16, y0 + 11, gx - 13, y1)
    ..lineTo(gx + 13, y1)
    ..quadraticBezierTo(gx + 16, y0 + 11, gx + 18, y0)
    ..close();

  canvas.drawPath(
    neckPath,
    Paint()
      ..shader = LinearGradient(
        begin: Alignment.centerLeft,
        end: Alignment.centerRight,
        colors: const [
          Color(0xFF585868),
          Color(0xFFB0B0C0),
          Color(0xFF484858),
        ],
        stops: const [0.0, 0.5, 1.0],
      ).createShader(Rect.fromLTRB(gx - 18, y0, gx + 18, y1)),
  );
}

/// Dessine le culot Edison (corps fileté + contact bas).
void drawBulbBase(Canvas canvas, Offset gc, double gr) {
  final gx = gc.dx;
  final baseTop = gc.dy + gr + 19;
  const baseH = 24.0;
  const hw    = 13.0;

  final baseRect = Rect.fromLTRB(gx - hw, baseTop, gx + hw, baseTop + baseH);

  // Corps métallique (dégradé latéral simulant le cylindre)
  canvas.drawRRect(
    RRect.fromRectAndCorners(
      baseRect,
      bottomLeft:  const Radius.circular(3),
      bottomRight: const Radius.circular(3),
    ),
    Paint()
      ..shader = LinearGradient(
        begin: Alignment.centerLeft,
        end: Alignment.centerRight,
        colors: const [
          Color(0xFF3C3C4A),
          Color(0xFF787886),
          Color(0xFF3C3C4A),
        ],
      ).createShader(baseRect),
  );

  // Stries du filetage Edison
  final striePaint = Paint()
    ..color = Colors.black.withValues(alpha: 0.30)
    ..strokeWidth = 0.7;
  for (double dy = 4; dy < baseH - 3; dy += 4.5) {
    canvas.drawLine(
      Offset(gx - hw + 1, baseTop + dy),
      Offset(gx + hw - 1, baseTop + dy),
      striePaint,
    );
  }

  // Contact bas (dome métallique)
  final tipC = Offset(gx, baseTop + baseH + 3);
  canvas.drawCircle(
    tipC, 4.5,
    Paint()
      ..shader = RadialGradient(
        colors: const [Color(0xFFB8B8C0), Color(0xFF606068)],
      ).createShader(Rect.fromCircle(center: tipC, radius: 4.5)),
  );
}
