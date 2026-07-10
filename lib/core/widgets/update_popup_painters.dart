import 'dart:math' as math;
import 'dart:ui' as ui;
import 'package:flutter/material.dart';

class StarData {
  final double x, y, size, opacity, phase;
  const StarData({
    required this.x, required this.y,
    required this.size, required this.opacity, required this.phase,
  });
}

class StarsPainter extends CustomPainter {
  final List<StarData> stars;
  final double t;
  const StarsPainter(this.stars, this.t);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint();
    for (final s in stars) {
      final twinkle = (math.sin((t * 2.5 + s.phase) * 2 * math.pi) + 1) / 2;
      paint.color = Colors.white.withValues(alpha: s.opacity * (0.3 + twinkle * 0.7));
      canvas.drawCircle(Offset(s.x * size.width, s.y * size.height), s.size, paint);
    }
  }

  @override
  bool shouldRepaint(StarsPainter old) => old.t != t;
}

class RaysPainter extends CustomPainter {
  final Color color;
  final double centerDy;
  const RaysPainter({required this.color, this.centerDy = 0.0});

  // (demi-angle rad, longueur px, alpha local) — 12 cônes à 30° d'intervalle
  static const List<(double, double, double)> _defs = [
    (0.11, 82, 0.90), // 0°
    (0.07, 50, 0.38), // 30°
    (0.10, 72, 0.70), // 60°
    (0.06, 44, 0.28), // 90°
    (0.10, 66, 0.62), // 120°
    (0.07, 48, 0.36), // 150°
    (0.11, 82, 0.90), // 180°
    (0.07, 50, 0.38), // 210°
    (0.10, 72, 0.70), // 240°
    (0.06, 44, 0.28), // 270°
    (0.10, 66, 0.62), // 300°
    (0.07, 48, 0.36), // 330°
  ];

  static const _innerR = 44.0; // bord extérieur du globe

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2 + centerDy);
    for (int i = 0; i < _defs.length; i++) {
      final angle = i * math.pi * 2 / _defs.length;
      final (halfAngle, length, localAlpha) = _defs[i];
      _drawRay(canvas, center, angle, halfAngle, length, localAlpha);
    }
  }

  void _drawRay(Canvas canvas, Offset c, double angle, double halfAngle, double length, double localAlpha) {
    final innerPt = Offset(c.dx + math.cos(angle) * _innerR, c.dy + math.sin(angle) * _innerR);
    final outerPt = Offset(c.dx + math.cos(angle) * length,  c.dy + math.sin(angle) * length);
    final leftIn  = Offset(c.dx + math.cos(angle - halfAngle) * _innerR, c.dy + math.sin(angle - halfAngle) * _innerR);
    final rightIn = Offset(c.dx + math.cos(angle + halfAngle) * _innerR, c.dy + math.sin(angle + halfAngle) * _innerR);

    final path = Path()
      ..moveTo(leftIn.dx, leftIn.dy)
      ..lineTo(outerPt.dx, outerPt.dy)
      ..lineTo(rightIn.dx, rightIn.dy)
      ..close();

    final bright = color.withValues(alpha: color.a * localAlpha);
    canvas.drawPath(
      path,
      Paint()..shader = ui.Gradient.linear(innerPt, outerPt, [bright, bright.withValues(alpha: 0)]),
    );
  }

  @override
  bool shouldRepaint(RaysPainter old) => old.color != color || old.centerDy != centerDy;
}
