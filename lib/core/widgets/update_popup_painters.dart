import 'dart:math' as math;
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
  const RaysPainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final paint = Paint()..strokeCap = StrokeCap.round;
    const rays = 8;
    for (int i = 0; i < rays; i++) {
      final angle = (i / rays) * 2 * math.pi;
      final long = i % 2 == 0;
      paint
        ..strokeWidth = long ? 2.0 : 1.5
        ..color = color.withValues(alpha: long ? 1.0 : 0.55);
      canvas.drawLine(
        Offset(center.dx + 46 * math.cos(angle), center.dy + 46 * math.sin(angle)),
        Offset(center.dx + (long ? 64 : 57) * math.cos(angle),
               center.dy + (long ? 64 : 57) * math.sin(angle)),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(RaysPainter old) => old.color != color;
}
